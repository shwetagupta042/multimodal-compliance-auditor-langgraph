import os
import glob
import logging
from dotenv import load_dotenv
load_dotenv(override=True)

# document loaders and splitters
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

logging.basicConfig(
    level=logging.info,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("indexer")

def index_docs():
    '''
    Reads the pdf
    chunks them
    uploads them to Azure AI Search
    '''

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, "../../backend/data")

    logger.info("="*60)
    logger.info("Environment configuration check")
    logger.info(f"AZURE_OPENAI_ENDPOINT : {os.getenv('AZURE_OPENAI_ENDPOINT')}") 
    logger.info(f"AZURE_OPENAI_API_VERSION : {os.getenv('AZURE_OPENAI_API_VERSION')}") 
    logger.info(f"Embedding Deployment : {os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT','text-embedding-3-small')}") 
    logger.info(f"AZURE_SEARCH_ENDPOINT : {os.getenv('AZURE_SEARCH_ENDPOINT')}") 
    logger.info(f"AZURE_SEARCH_INDEX_NAME : {os.getenv('AZURE_SEARCH_INDEX_NAME')}") 
    logger.info("="*60)

    # validate the req env variabes
    req_vars = [
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_API_KEY',
        'AZURE_SEARCH_ENDPOINT',
        'AZURE_SEARCH_API_KEY',
        'AZURE_SEARCH_INDEX_NAME'
    ]

    missing_vars = [var for var in req_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing req env variables: {missing_vars}")
        logger.error("Please check your .env file and ensure all the variables are set")
        return 
    
    # initialize the embedding model --> text into numbers/vector
    try:
        logger.info(f"Initializing Azure OpenAI Embeddings....")
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT','text-embedding-3-small'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION','2024-02-01')
        )
        logger.info("Embeddings model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize embeddings : {e}")
        logger.error("Please verify your Azure OpenAI deployment name and endpoint")
        return
    
    # initialize the Azure search
    try:
        logger.info(f"Initializing Azure AI Search Vector Store....")
        embeddings = AzureOpenAIEmbeddings(
            azure_search_endpoint=os.getenv('AZURE_SEARCH_ENDPOINT'),
            azure_search_key=os.getenv('AZURE_SEARCH_API_KEY'),
            index_name=os.getenv('AZURE_SEARCH_INDEX_NAME'),
            embedding_function=embeddings.embed_query, 
        )
        logger.info(f"Azure vector store initialized for index : {index_name}")
    except Exception as e:
        logger.error(f"Failed to initialize Azure Search : {e}")
        logger.error("Please verify your Azure Search Endpoint, API key and Index name")
        return

    # Find PDF files
    pdf_files = glob.glob(os.path.join(data_folder,"*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDFs found in the data folder. Please add files")
    logger.info(f"Found {len(pdf_files)} PDFs to process: {[os.path.basename(f) for f in pdf_files]}")

    all_splits = []

    # process each pdf
    for pdf_path in pdf_files:
        try:
            logger.info(f"Loading: {os.path.basename(pdf_path)}...")
            loader = PyPDFLoader(pdf_path)
            raw_docs = loader.load()

            #chunking strategy
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 200
            )

            splits = text_splitter.split_documents(raw_docs)
            for split in splits:
                split.metadata["source"] = os.path.basename(pdf_path)
            
            all_splits.extend(splits)
            logger.info(f"Splitted into {len(splits)} chunks")

        except Exception as e:
            logger.error(f"Failed to process {pdf_path}: {e}")
             
        # Upload to Azure
        if all_splits:
            logger.info(f"Upload {len(all_splits)} chunks to Azure AI Search Index '{index_name}'")
            try:
                # Azure search accepts batches automatically via this method
                vector_store.add_documents(documents = all_splits)
                logger.info("="*60)
                logger.info("Indexing complete! Knowledge base is ready...")
                logger.info(f"Total chunks indexed: {len(all_splits)}")
                logger.info("="*60)
            except Exception as e:
                logger.error(f"Failed to upload the docs to Azure Search : {e}")
                logger.error("Please check the Azure Search configuration and try again")
        else:
            logger.warning("No documents were processed")
    

if __name__ == "__main__":
    index_docs()

