import pandas as pd
import os
from utils.logger import app_logger

def load_data(filepath):
    """Loads a CSV or Excel file into a Pandas DataFrame."""
    try:
        _, ext = os.path.splitext(filepath)
        if ext.lower() == '.csv':
            df = pd.read_csv(filepath)
            return df
        elif ext.lower() in ['.xls', '.xlsx']:
            df = pd.read_excel(filepath)
            return df
        else:
            app_logger.error(f"Unsupported file format: {ext}")
            return None
    except Exception as e:
        app_logger.error(f"Error loading data from {filepath}: {e}")
        return None

def save_data(df, filepath):
    """Saves a Pandas DataFrame to a CSV or Excel file."""
    try:
        _, ext = os.path.splitext(filepath)
        if ext.lower() == '.csv':
            df.to_csv(filepath, index=False)
            return True
        elif ext.lower() in ['.xls', '.xlsx']:
            df.to_excel(filepath, index=False)
            return True
        else:
            app_logger.error(f"Unsupported file format for saving: {ext}")
            return False
    except Exception as e:
        app_logger.error(f"Error saving data to {filepath}: {e}")
        return False
