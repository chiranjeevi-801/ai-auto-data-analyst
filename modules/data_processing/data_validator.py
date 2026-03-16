import pandas as pd
from utils.logger import app_logger

def validate_dataset(df):
    """Validates the structure and basic integrity of the dataset."""
    if df is None or df.empty:
        return False, "Dataset is empty or None."
    
    issues = []
    
    # Check for empty columns
    empty_cols = [col for col in df.columns if df[col].isnull().all()]
    if empty_cols:
        issues.append(f"Contains entirely empty columns: {', '.join(empty_cols)}")
        
    # Check for single-value columns (zero variance)
    single_val_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if single_val_cols:
        issues.append(f"Contains columns with only a single unique value: {', '.join(single_val_cols)}")
        
    is_valid = len(issues) == 0
    message = "Dataset passed basic validation." if is_valid else " | ".join(issues)
    
    if not is_valid:
        app_logger.warning(f"Validation issues found: {message}")
        
    return is_valid, message
