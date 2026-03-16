import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_api_key():
    return os.environ.get("OPENAI_API_KEY")

def get_kaggle_credentials():
    return {
        "username": os.environ.get("KAGGLE_USERNAME"),
        "key": os.environ.get("KAGGLE_KEY")
    }
