# 🎬 Multimodal Compliance Auditor with LangGraph

An automated AI pipeline that audits video content against regulatory standards using a RAG architecture, orchestrated by LangGraph. The system ingests video, extracts transcripts and OCR data, retrieves relevant compliance rules semantically, and uses GPT-4o to deterministically detect violations — delivering structured JSON compliance reports with full end-to-end observability.

---

## 📌 Overview

Traditional video compliance review is manual, time-consuming, and error-prone. This project automates that process entirely. Given a video, the pipeline extracts its spoken and visual content, matches it against a library of regulatory documents, and flags any violations with precision — all without human intervention.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Orchestration | LangGraph |
| LLM | Azure OpenAI (GPT-4o) |
| Video Ingestion | Azure Video Indexer |
| Rule Retrieval | Azure AI Search + OpenAI Embeddings |
| Tracing | LangSmith |
| Monitoring | Azure Application Insights |
| API Server | FastAPI |
| Containerization | Docker |
| Output | Structured JSON Reports |

---

## ⚙️ How It Works

**Step 1 — Video Ingestion**
Azure Video Indexer processes the input video and extracts multimodal content including spoken transcripts and on-screen text (OCR). This raw content is passed into the LangGraph pipeline as the initial state.

**Step 2 — Compliance Rule Retrieval (RAG)**
The extracted content is embedded using Azure OpenAI Embeddings and used to query Azure AI Search. Relevant compliance rules are retrieved from the indexed regulatory documents (`data/`) and injected into the LLM context.

**Step 3 — Violation Detection**
Azure OpenAI (GPT-4o) acts as the core reasoning engine. It synthesizes the video content and retrieved compliance rules to deterministically identify regulatory violations, producing structured findings.

**Step 4 — Report Generation**
The pipeline outputs a structured JSON compliance report containing detected violations, the relevant rule references, confidence scores, and remediation suggestions.

**Step 5 — Observability**
LangSmith traces every LLM call and node execution within the LangGraph workflow. Azure Application Insights captures production-grade telemetry, logging, and real-time performance metrics.

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.10+
- Azure account with access to: OpenAI, Video Indexer, AI Search, Application Insights
- LangSmith account
- Docker (optional)

### 1. Clone the Repository
```bash
git clone https://github.com/shwetagupta042/multimodal-compliance-auditor-langgraph
cd multimodal-compliance-auditor-langgraph
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_KEY=your_search_admin_key
AZURE_SEARCH_INDEX=compliance-rules

# Azure Video Indexer
AZURE_VIDEO_INDEXER_ACCOUNT_ID=your_account_id
AZURE_VIDEO_INDEXER_LOCATION=your_region
AZURE_VIDEO_INDEXER_KEY=your_api_key

# LangSmith
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=compliance-auditor

# Azure Application Insights
APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string
```

### 5. Index Compliance Documents
Run this once to embed and index the compliance PDFs into Azure AI Search:
```bash
python scripts/index_documents.py
```

### 6. Run the Pipeline
```bash
python main.py
```

### 7. Run via Docker
```bash
docker build -t compliance-auditor .
docker run --env-file .env compliance-auditor
```

---

## 📊 Sample Output

```json
{
  "video_id": "sample_video_001",
  "compliance_status": "NON_COMPLIANT",
  "violations": [
    {
      "timestamp": "00:01:23",
      "violation_type": "Missing Disclosure",
      "description": "Sponsored content detected without FTC-required disclosure",
      "rule_reference": "FTC Influencer Guide — Section 4.2",
      "severity": "HIGH"
    }
  ],
  "total_violations": 1,
  "audit_timestamp": "2025-05-04T10:30:00Z"
}
```

---

## 🔑 Key Concepts Demonstrated

- Orchestrating multi-step LLM workflows with LangGraph state machines
- Building production RAG pipelines with Azure AI Search and OpenAI Embeddings
- Multimodal content ingestion using Azure Video Indexer (transcripts + OCR)
- Deterministic violation detection with structured LLM outputs
- Full-stack observability using LangSmith tracing and Azure Application Insights telemetry
- Containerized deployment with Docker

---

---

## 🙏 Acknowledgements

This project was built by following the hands-on project tutorial by
**Krish Naik Academy**. Full walkthrough available on YouTube:
[Watch Tutorial](https://www.youtube.com/watch?v=I3CWFDgqvq8)

---

## 📄 License

MIT License — feel free to use, modify, and distribute.