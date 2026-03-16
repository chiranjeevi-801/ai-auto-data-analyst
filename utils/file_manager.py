import os
import shutil
from utils.logger import app_logger
from config import settings

def clear_directory(directory_path):
    """Deletes all files in a specific directory."""
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                app_logger.error(f"Failed to delete {file_path}. Reason: {e}")

def initialize_working_directories():
    """Ensures all expected directories exist."""
    dirs_to_check = [
        settings.RAW_DATA_DIR,
        settings.CLEANED_DATA_DIR,
        settings.PROCESSED_DATA_DIR,
        settings.REPORTS_DIR,
        settings.EXPORTS_DIR
    ]
    for directory in dirs_to_check:
        if not os.path.exists(directory):
            os.makedirs(directory)
            app_logger.info(f"Created directory: {directory}")

def get_file_size_mb(filepath):
    """Returns the size of the file in MB."""
    if os.path.exists(filepath):
        size_bytes = os.path.getsize(filepath)
        return round(size_bytes / (1024 * 1024), 2)
    return 0.0
