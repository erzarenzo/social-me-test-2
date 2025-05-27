import threading
import time
from complete_workflow_test import find_free_port, run_flask_server, app as workflow_app
from flask_workflow_api_verify import FlaskWorkflowAPIVerifier

def main():
    # Find a free port
    port = find_free_port()
    print(f"Using port {port}")
    
    # Start Flask server in a separate thread
    server_thread = threading.Thread(
        target=run_flask_server, 
        args=(workflow_app, port), 
        daemon=True
    )
    server_thread.start()
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Run API verification
    verifier = FlaskWorkflowAPIVerifier(base_url=f"http://localhost:{port}")
    result = verifier.verify_workflow()
    
    print("Verification Result:", "PASSED" if result else "FAILED")

if __name__ == "__main__":
    main()
