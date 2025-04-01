import os
import openai
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure your key is in the .env file

def diagnose_with_openai(log_file):
    """Use OpenAI's API to analyze logs and provide suggestions."""
    with open(log_file, 'r') as file:
        logs = file.read()

    # Send logs to OpenAI for analysis
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can replace with "gpt-4" if you have access
            prompt=f"Analyze the following logs and suggest potential issues or fixes:\n{logs}",
            max_tokens=500
        )
        logger.info(f"OpenAI Diagnosis: {response.choices[0].text.strip()}")
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        return "❌ Error with OpenAI API. Please check your connection or API key."

def run_diagnostics():
    """Run diagnostic checks and use OpenAI for deep analysis."""
    log_file = 'flask.log'  # Change this to your log file if necessary
    diagnosis = diagnose_with_openai(log_file)
    
    # Print the results of the diagnosis
    print(f"\nOpenAI Diagnostics:\n{diagnosis}")
    
if __name__ == "__main__":
    run_diagnostics()
