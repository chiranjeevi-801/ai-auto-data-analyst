import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# App paths & constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
CLEANED_DATA_DIR = os.path.join(DATA_DIR, "cleaned")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
EXPORTS_DIR = os.path.join(DATA_DIR, "exports")
DB_PATH = os.path.join(BASE_DIR, os.environ.get("DB_PATH", "database/app_database.db"))

APP_TITLE = "AI Auto Data Analyst"
APP_SUBTITLE = "Your intelligent, automated end-to-end data analytics platform"
