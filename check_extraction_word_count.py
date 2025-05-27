"""
Check the word count of extracted content in workflows
"""
import sys
import os
import json

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the workflows data
    from fastapi_app.workflow_api import WORKFLOWS
    
    print(f"Total workflows: {len(WORKFLOWS)}")
    
    # Check each workflow for extraction data
    for workflow_id, workflow in WORKFLOWS.items():
        print(f"\nWorkflow ID: {workflow_id}")
        print(f"Topic: {workflow.get('topic', 'Not set')}")
        
        # Check for extracted content
        if "key_data_sources" in workflow:
            key_data = workflow["key_data_sources"]
            print(f"Total word count: {key_data.get('total_word_count', 0)}")
            print(f"Successful extractions: {key_data.get('successful_extractions', 0)}")
            print(f"Failed extractions: {key_data.get('failed_extractions', 0)}")
            
            # Show individual source word counts
            for i, source in enumerate(key_data.get('processed_sources', [])):
                print(f"Source {i+1}: {source.get('url', 'Unknown')} - {source.get('word_count', 0)} words")
        else:
            print("No extracted content found")
            
        # Check if any data sources were set
        if "data_sources" in workflow:
            print(f"Data sources: {len(workflow['data_sources'])}")
        else:
            print("No data sources set")
            
except Exception as e:
    print(f"Error checking workflows: {str(e)}")
    import traceback
    traceback.print_exc()
