import os
import requests
from config import settings
from utils.logger import app_logger

def download_from_url(url, output_filename):
    """Downloads a dataset from a direct URL and saves it to the raw data folder."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        file_path = os.path.join(settings.RAW_DATA_DIR, output_filename)
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        app_logger.info(f"Downloaded dataset from URL successfully to {file_path}")
        return file_path
    except Exception as e:
        app_logger.error(f"Failed to download dataset from URL: {e}")
        return None
