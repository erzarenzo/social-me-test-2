# Frontend Integration Guide for SocialMe Content Generation Workflow

## Prerequisites
- Python 3.8+
- Flask
- Requests library
- Postman (optional, for API testing)

## Backend Setup
1. Clone the repository
2. Create a virtual environment
```bash
python3 -m venv myenv
source myenv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set environment variables
Create a `.env` file with:
```
DEBUG=true
PORT=8004
SECRET_KEY=your_secret_key_here
```

## Running the Backend
```bash
python complete_workflow_test.py
```

## Frontend Integration Strategies

### 1. Sequential Workflow
```python
def content_generation_workflow():
    # 1. Start workflow
    workflow_start_response = requests.post(f"{BASE_URL}/api/workflow/start")
    workflow_id = workflow_start_response.json()['workflow_id']

    # 2. Submit topic
    requests.post(f"{BASE_URL}/api/workflow/{workflow_id}/topic", json={
        "primary_topic": "AI in Healthcare",
        "secondary_topics": ["Machine Learning"]
    })

    # Continue with subsequent steps...
```

### 2. Error Handling
```python
def handle_workflow_step(step_function):
    try:
        response = step_function()
        if response.status_code != 200:
            # Log error, show user-friendly message
            print(f"Step failed: {response.json().get('message', 'Unknown error')}")
            return False
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False
```

## Frontend Components Needed
1. Workflow Initialization Screen
2. Topic Input Component
3. Data Source Selection
4. Tone Analysis Configuration
5. Article Preview and Editing
6. Final Article Generation

## Recommended Frontend Flow
1. Call `/start` to initialize workflow
2. Progressively collect user inputs
3. Call each endpoint sequentially
4. Provide visual feedback for each step
5. Allow user to modify or regenerate content

## Testing
- Use provided Postman collection
- Implement unit tests for each workflow step
- Simulate various input scenarios

## Performance Considerations
- Implement loading states
- Handle potential timeouts
- Provide clear error messages
- Consider caching workflow state
