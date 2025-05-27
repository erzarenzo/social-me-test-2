import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the workflows data
    from fastapi_app.workflow_api import WORKFLOWS
    
    # Check all workflows
    print("Checking all workflows for extracted content:")
    
    for workflow_id, workflow in WORKFLOWS.items():
        if "key_data_sources" in workflow:
            key_data = workflow["key_data_sources"]
            total_words = key_data.get('total_word_count', 0)
            
            print(f"Workflow {workflow_id}:")
            print(f"  Topic: {workflow.get('topic', 'Not set')}")
            print(f"  Total words extracted: {total_words}")
            
            # Show individual sources
            for i, source in enumerate(key_data.get('processed_sources', [])):
                url = source.get('url', 'Unknown')
                words = source.get('word_count', 0)
                print(f"  Source {i+1}: {url} - {words} words")
            
            print("")
        
except Exception as e:
    print(f"Error: {str(e)}")
