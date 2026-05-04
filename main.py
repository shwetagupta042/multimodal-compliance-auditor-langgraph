import os
import uuid
import json
import logging
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

from backend.src.graph.workflow import app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("brand-guardian-runner")

print("CLIENT_ID:", os.getenv("AZURE_CLIENT_ID"))
print("TENANT_ID:", os.getenv("AZURE_TENANT_ID"))
print("SECRET:", os.getenv("AZURE_CLIENT_SECRET"))

def run_cli_simulation():

    '''
    Simulates a Video Compliance Audit Request

    This function orchesrates the entire audit process:
    - creates a unique session ID
    - prepares the video URL and metadata
    - Runs it through the AI workflow
    - Displays the compliance results
    '''

    # first generate session id
    session_id = str(uuid.uuid4)
    logger.info(f"Starting Audit session : {session_id}")

    # next define initial state
    initial_input = {
        "video_url": "https://youtu.be/dT7S75eYhcQ",
        "video_id": f"vid_{session_id[:8]}",
        "compliance_results": [],
        "errors": []
    }

    print("---- Initializing workflow -----")
    print(f"Input payload : {json.dumps(initial_input, indent=2)}")

    try:
        final_state = app.invoke(initial_input)   # app.invoke() triggers the LangGraph workflow
        print("\n----- workflow execution is complete ------")

        print("\n Compliance aufit report")
        print(f"Video ID : {final_state.get('video_id')}")
        print(f"Status: {final_state}.get('final_status')")
        print("\n [Violations Detected]")
        results = final_state.get('compliance_results',[])

        if results:
            for issue in results:
                print(f"- [{issue.get('severity')}][{issue.get('category')}] : [{issue.get('description')}]")
        else:
            print("No violations detected....")
        print("\n [FINAL SUMMARY]")
        print(f"{final_state}.get('final_report')")

    except Exception as e:
        logger.error(f"The workflow execution has failed : {str(e)}")
        raise e
    
if __name__ == "__main__":
    run_cli_simulation()

