import operator
from typing import Annotated, List, Dict, Optional, Any, TypedDict

# define the schema for a single compliance result
# Error Report generation
class ComplianceIssue(TypedDict):
    category : str      # eg: FTC disclosure
    description : str   # specific detail of violation
    severity : str      # CRITICAL | WARNING
    timestamp : Optional[str]

# define the global graph state
# this defines the state that gets passed around in the agentic workflow
class VideoAuditState(TypedDict):
    '''
    defines the data schema for langgraph execution content
    Main container : holds all the info about the audit right from the initial url that the user gives to the final report
    '''
    # input parameters 
    video_url : str
    video_id : str

    # ingestion and extraction data
    local_file_path : Optional[str]
    video_metadata: Dict[str, Any] # {"duration":15, "resolution": 1080p}
    transcript : Optional[str] # fully extracted speech to text
    ocr_text : List[str]  # list of all the text visually available on the screen   

    # analysis output
    # stores the list of all the violations found by AI/ Agentic system
    compliance_results : Annotated[List[ComplianceIssue], operator.add]

    #final deliverables
    final_status : str # PASS | FAIL
    final_report : str # markdown report

    #system observability
    # errors: API timeout, system level errors
    errors : Annotated[List[str], operator.add]


 
