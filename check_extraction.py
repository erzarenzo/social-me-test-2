import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from fastapi_app.workflow_api import WORKFLOWS
    
    workflow_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not workflow_id:
        print("No workflow ID provided")
        sys.exit(1)
    
    if workflow_id not in WORKFLOWS:
        print(f"Workflow ID {workflow_id} not found")
        sys.exit(1)
    
    workflow = WORKFLOWS[workflow_id]
    
    print(f"Workflow ID: {workflow_id}")
    print(f"Topic: {workflow.get('topic', 'Not set')}")
    
    if "key_data_sources" in workflow:
        key_data = workflow["key_data_sources"]
        print(f"Total word count: {key_data.get('total_word_count', 0)}")
        print(f"Successful extractions: {key_data.get('successful_extractions', 0)}")
        print(f"Failed extractions: {key_data.get('failed_extractions', 0)}")
        
        for i, source in enumerate(key_data.get("processed_sources", [])):
            print(f"\nSource {i+1}: {source.get('url', 'Unknown')}")
            print(f"Word count: {source.get('word_count', 0)}")
    else:
        print("No key_data_sources found in workflow")
        
        # Check if data is stored in another format
        if "data_sources" in workflow and isinstance(workflow["data_sources"], dict):
            print("Data sources found in dictionary format")
            print(workflow["data_sources"])
        
        source_keys = [k for k in workflow.keys() if "source" in k.lower()]
        if source_keys:
            print(f"Found source-related keys: {source_keys}")
except Exception as e:
    print(f"Error checking extraction: {str(e)}")
    import traceback
    traceback.print_exc()
