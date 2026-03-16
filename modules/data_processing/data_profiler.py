import pandas as pd
from ydata_profiling import ProfileReport
import os
from config import settings
from utils.logger import app_logger

def generate_profile_report(df, dataset_name="dataset"):
    """Generates an HTML profile report using ydata-profiling."""
    if df is None or df.empty:
        app_logger.warning("Empty dataframe provided for profiling.")
        return None
        
    try:
        report_path = os.path.join(settings.REPORTS_DIR, f"{dataset_name}_profiling_report.html")
        profile = ProfileReport(df, title=f"{dataset_name.capitalize()} Profiling Report", explorative=True)
        profile.to_file(report_path)
        app_logger.info(f"Data profiling report generated at {report_path}")
        return report_path
    except Exception as e:
        app_logger.error(f"Failed to generate profile report for {dataset_name}: {e}")
        return None
