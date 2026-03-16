import pandas as pd
import numpy as np
from utils.logger import app_logger

def basic_eda(df):
    """Performs Basic Exploratory Data Analysis."""
    if df is None or df.empty:
        return {}
    
    eda_results = {
        'num_rows': len(df),
        'num_cols': len(df.columns),
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'head': df.head(5),
        'summary_statistics': df.describe(include='all')
    }
    
    app_logger.info("Basic EDA completed successfully.")
    return eda_results
