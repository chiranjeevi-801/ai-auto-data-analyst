import os
import kaggle
from config import settings
from utils.logger import app_logger

def authenticate_kaggle():
    """Sets up Kaggle authentication using environment variables."""
    # Kaggle library automatically checks for KAGGLE_USERNAME and KAGGLE_KEY in env manually.
    try:
        kaggle.api.authenticate()
        return True
    except Exception as e:
        app_logger.error(f"Kaggle authentication failed: {e}")
        return False

def search_kaggle_datasets(query, max_results=10):
    """Searches for Kaggle datasets matching a query."""
    if not authenticate_kaggle():
        return []
    
    try:
        datasets = kaggle.api.dataset_list(search=query, sort_by='votes', max_size=1000000)
        results = [{"ref": str(d.ref), "title": str(d.title), "size": str(d.size), "votes": int(d.votes)} 
                   for d in datasets[:max_results]]
        return results
    except Exception as e:
        app_logger.error(f"Failed to search Kaggle datasets: {e}")
        return []

def download_kaggle_dataset(dataset_ref):
    """Downloads a dataset from Kaggle to the raw data dir."""
    if not authenticate_kaggle():
        return None
        
    try:
        app_logger.info(f"Downloading Kaggle dataset: {dataset_ref} to {settings.RAW_DATA_DIR}")
        kaggle.api.dataset_download_files(dataset_ref, path=settings.RAW_DATA_DIR, unzip=True)
        return settings.RAW_DATA_DIR # Note: The exact filename requires inspecting the dir, handled in UI
    except Exception as e:
        app_logger.error(f"Failed to download Kaggle dataset {dataset_ref}: {e}")
        return None
