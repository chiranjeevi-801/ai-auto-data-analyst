from database.db_connection import execute_query
from utils.logger import app_logger


SCHEMA = {
    "dataset_metadata": """
        CREATE TABLE IF NOT EXISTS dataset_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            source TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            row_count INTEGER,
            col_count INTEGER,
            file_size_mb REAL
        )
    """,
    "analysis_log": """
        CREATE TABLE IF NOT EXISTS analysis_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER,
            analysis_type TEXT,
            performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            result_summary TEXT
        )
    """,
    "query_log": """
        CREATE TABLE IF NOT EXISTS query_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
}


def create_all_tables():
    """Creates all tables defined in the SCHEMA dict."""
    for table_name, ddl in SCHEMA.items():
        execute_query(ddl, commit=True)
        app_logger.info(f"Table ensured: {table_name}")


def drop_table(table_name):
    """Drops a table by name (use with caution)."""
    execute_query(f"DROP TABLE IF EXISTS {table_name}", commit=True)
    app_logger.warning(f"Table dropped: {table_name}")


def list_tables():
    """Returns a list of all user-created table names in the database."""
    rows = execute_query(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    return [r[0] for r in rows] if rows else []
