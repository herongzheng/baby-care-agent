import os
from dotenv import load_dotenv

def configure_environment():
    # Load environment variables from .env file
    load_dotenv(dotenv_path="/app/.env")
    if 'GOOGLE_API_KEY' in os.environ:
        print("environment and variables are loaded...")