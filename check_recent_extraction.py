import os
import sys
import json

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the workflows data
    from fastapi_app.workflow_api import WORKFLOWS
    
    # Get the most recent workflow
    if not WORKFLOWS:
        print("No workflows found")
        sys.exit(1)
    
    # Sort workflows by ID (if they're timestamp-based, this should work)
    workflow_ids = sorted(WORKFLOWS.keys())
    latest_workflow_id = workflow_ids[-1]
    workflow = WORKFLOWS[latest_workflow_id]
    
    print(f"Most Recent Workflow ID: {latest_workflow_id}")
    print(f"Topic: {workflow.get('topic', 'Not set')}")
    
    # Check for extracted content
    if "key_data_sources" in workflow:
        key_data = workflow["key_data_sources"]
        print(f"\n=== EXTRACTION RESULTS ===")
        print(f"Total word count: {key_data.get('total_word_count', 0)}")
        print(f"Successful extractions: {key_data.get('successful_extractions', 0)}")
        print(f"Failed extractions: {key_data.get('failed_extractions', 0)}")
        
        # Show details for each source
        for i, source in enumerate(key_data.get('processed_sources', [])):
            print(f"\nSource {i+1}: {source.get('url', 'Unknown')}")
            print(f"Word count: {source.get('word_count', 0)}")
            print(f"Extraction method: {source.get('metadata', {}).get('extraction_method', 'Unknown')}")
            
        # Compare to memory goal
        total_words = key_data.get('total_word_count', 0)
        if total_words >= 18000:
            print("\nEXCEEDED GOAL: Extracted more than 18,000 words (memory target)")
        elif total_words >= 12000:
            print("\nMET GOAL: Extracted more than 12,000 words (minimum target)")
        else:
            print(f"\nBELOW GOAL: Extracted {total_words} words (target was 12,000+)")
    else:
        print("\nNo extracted content found in this workflow")
        
        # Check if any data sources were set
        if "data_sources" in workflow:
            print(f"Data sources were set: {workflow['data_sources']}")
        else:
            print("No data sources were set")
    
except Exception as e:
    print(f"Error checking workflow: {str(e)}")
    import traceback
    traceback.print_exc()
