import sys
import os
import json

# Get workflow ID from command line
workflow_id = sys.argv[1] if len(sys.argv) > 1 else None
if not workflow_id:
    print("ERROR: Workflow ID required")
    sys.exit(1)

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the workflows data
    from fastapi_app.workflow_api import WORKFLOWS
    
    if workflow_id not in WORKFLOWS:
        print(f"ERROR: Workflow ID {workflow_id} not found")
        print(f"Available workflow IDs: {list(WORKFLOWS.keys())}")
        sys.exit(1)
    
    workflow = WORKFLOWS[workflow_id]
    
    # Basic workflow info
    print(f"\n=== WORKFLOW {workflow_id} ===")
    print(f"Topic: {workflow.get('topic', 'Not set')}")
    print(f"Data sources: {workflow.get('data_sources', [])}")
    
    # Check data sources handling
    print("\n=== DATA SOURCES HANDLING ===")
    
    # Check for direct data_sources (should be set from topic endpoint)
    if "data_sources" in workflow:
        print(f"Data sources set: {len(workflow['data_sources'])}")
        for i, url in enumerate(workflow['data_sources']):
            print(f"  Source {i+1}: {url}")
    else:
        print("No data_sources found in workflow")
    
    # Check for key_data_sources (should be set by QuantumUniversalCrawler)
    if "key_data_sources" in workflow:
        key_data = workflow["key_data_sources"]
        print("\n=== KEY DATA SOURCES (EXTRACTED) ===")
        print(f"Total word count: {key_data.get('total_word_count', 0)}")
        print(f"Successful extractions: {key_data.get('successful_extractions', 0)}")
        print(f"Failed extractions: {key_data.get('failed_extractions', 0)}")
        
        # Print details for each processed source
        if "processed_sources" in key_data:
            for i, source in enumerate(key_data["processed_sources"]):
                print(f"\nSource {i+1}: {source.get('url', 'Unknown')}")
                print(f"  Word count: {source.get('word_count', 0)}")
                if "metadata" in source:
                    print(f"  Extraction method: {source['metadata'].get('extraction_method', 'Unknown')}")
                    print(f"  Confidence: {source['metadata'].get('confidence', 0)}")
                
                # Print short preview of content
                content = source.get('content', '')
                if content:
                    print(f"  Content preview: {content[:100]}...")
                else:
                    print("  No content extracted")
        else:
            print("No processed_sources found in key_data_sources")
    else:
        print("\nNo key_data_sources found in workflow")
    
    # Check alternative locations based on memory
    print("\n=== CHECKING ALTERNATIVE SOURCE LOCATIONS ===")
    
    # Check top-level data_sources
    if "content" in workflow.get("data_sources", []):
        print("Found content directly in data_sources")
    
    # Check for processed_sources as separate key
    if "processed_sources" in workflow:
        print(f"Found processed_sources as separate key with {len(workflow['processed_sources'])} items")
    
    # Check for extracted_content
    if "extracted_content" in workflow:
        print("Found extracted_content key")
        
    # Check for source_content
    if "source_content" in workflow:
        print("Found source_content key")
    
    # Check for any keys with 'source' in the name
    source_keys = [k for k in workflow.keys() if 'source' in k.lower()]
    if source_keys:
        print(f"Found source-related keys: {source_keys}")
    
    # Check article generation
    print("\n=== ARTICLE GENERATION ===")
    if "article" in workflow:
        article = workflow["article"]
        print(f"Article title: {article.get('title', 'Not set')}")
        content = article.get('content', '')
        print(f"Article content length: {len(content)} characters, ~{len(content.split())} words")
    else:
        print("No article found")
    
    # Check alternative article storage
    if "generated_content" in workflow:
        print("Found generated_content key")
        generated_content = workflow["generated_content"]
        print(f"Generated content length: {len(generated_content)} characters")
    
    # Save the workflow data for inspection
    with open(f'workflow_{workflow_id}_detailed.json', 'w') as f:
        # Create a serializable copy
        serializable_workflow = {}
        for k, v in workflow.items():
            if k == "_lock":
                continue
            try:
                # Test if it's JSON serializable
                json.dumps(v)
                serializable_workflow[k] = v
            except:
                serializable_workflow[k] = str(v)
        
        json.dump(serializable_workflow, f, indent=2)
    
    print(f"\nDetailed workflow data saved to workflow_{workflow_id}_detailed.json")
    
except Exception as e:
    print(f"ERROR checking workflow: {str(e)}")
    import traceback
    traceback.print_exc()
