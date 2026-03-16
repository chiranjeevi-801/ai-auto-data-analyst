import pandas as pd
import numpy as np
from scipy import stats
from utils.logger import app_logger

def compute_statistics(df, num_column):
    """Computes basic statistics for a numerical column."""
    if num_column not in df.columns or not pd.api.types.is_numeric_dtype(df[num_column]):
        return {"error": "Invalid numerical column"}
    
    series = df[num_column].dropna()
    stats_result = {
        'mean': series.mean(),
        'median': series.median(),
        'mode': series.mode().iloc[0] if not series.mode().empty else None,
        'std_dev': series.std(),
        'variance': series.var(),
        'min': series.min(),
        'max': series.max(),
        'skewness': series.skew(),
        'kurtosis': series.kurtosis()
    }
    
    app_logger.info(f"Statistics computed for column {num_column}")
    return stats_result
