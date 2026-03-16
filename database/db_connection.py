import sqlite3
import pandas as pd
from config import settings
from utils.logger import app_logger

def get_db_connection():
    """Returns a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
        return conn
    except Exception as e:
        app_logger.error(f"Database connection error: {e}")
        return None

def execute_query(query, params=(), commit=False):
    """Executes a SQL query on the SQLite DB."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return cursor.lastrowid
        else:
            return cursor.fetchall()
    except Exception as e:
        app_logger.error(f"Error executing query [{query}]: {e}")
        return None
    finally:
        conn.close()

def init_db():
    """Initializes basic database schema if it doesn't exist."""
    init_query = '''
    CREATE TABLE IF NOT EXISTS dataset_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        source TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        row_count INTEGER,
        col_count INTEGER,
        file_size_mb REAL
    )
    '''
    execute_query(init_query, commit=True)
    app_logger.info("Database initialized successfully.")
