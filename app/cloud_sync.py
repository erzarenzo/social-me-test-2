from google.cloud import logging
import logging

# Set up Cloud Logging Client
client = logging.Client()

def log_to_cloud(message):
    logger = client.logger("diagnostic-log")
    logger.log_text(message)
    print(f"Logged to cloud: {message}")

if __name__ == "__main__":
    log_to_cloud("System diagnostic completed.")
