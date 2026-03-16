import os
import pandas as pd
from config import settings
from database.db_connection import execute_query
from utils.logger import app_logger
from utils.file_manager import get_file_size_mb

def handle_upload(uploaded_file):
    """Saves the user uploaded file to the raw data directory."""
    if uploaded_file is None:
        return None
    
    file_path = os.path.join(settings.RAW_DATA_DIR, uploaded_file.name)
    
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        app_logger.info(f"File uploaded successfully to {file_path}")
        return file_path
    
    except Exception as e:
        app_logger.error(f"Failed to save uploaded file: {e}")
        return None

def register_dataset_in_db(filepath, original_name, source="upload", row_count=0, col_count=0):
    """Logs the dataset metadata in SQLite db."""
    file_size = get_file_size_mb(filepath)
    query = '''
    INSERT INTO dataset_metadata (filename, source, row_count, col_count, file_size_mb)
    VALUES (?, ?, ?, ?, ?)
    '''
    dataset_id = execute_query(query, (original_name, source, row_count, col_count, file_size), commit=True)
    return dataset_id
