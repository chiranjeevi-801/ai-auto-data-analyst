import pandas as pd
from database.db_connection import get_db_connection, execute_query
from utils.logger import app_logger

def save_dataframe_to_db(df, table_name, if_exists='replace'):
    """Saves a pandas DataFrame to an SQLite table."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        app_logger.info(f"Successfully saved dataframe to table: {table_name}")
        return True
    except Exception as e:
        app_logger.error(f"Error saving to database table {table_name}: {e}")
        return False
    finally:
        conn.close()

def load_dataframe_from_db(query):
    """Loads data from the SQLite DB into a pandas DataFrame."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        app_logger.error(f"Error reading from database with query [{query}]: {e}")
        return None
    finally:
        conn.close()
