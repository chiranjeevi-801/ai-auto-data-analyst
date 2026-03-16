import pandas as pd
import numpy as np
from utils.logger import app_logger


def generate_kpis(df):
    """
    Automatically computes KPI-style numeric summaries from the dataset.
    Returns a list of dicts with 'label', 'value', and optional 'delta'.
    """
    kpis = []
    if df is None or df.empty:
        return kpis

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    kpis.append({"label": "Total Rows", "value": f"{len(df):,}", "icon": "📁"})
    kpis.append({"label": "Total Columns", "value": f"{len(df.columns):,}", "icon": "📊"})

    missing = int(df.isnull().sum().sum())
    kpis.append({"label": "Missing Values", "value": f"{missing:,}", "icon": "⚠️"})

    dup = int(df.duplicated().sum())
    kpis.append({"label": "Duplicate Rows", "value": f"{dup:,}", "icon": "🔁"})

    # Numeric KPIs (first 3 numeric columns only to keep dashboard clean)
    for col in num_cols[:3]:
        kpis.append({
            "label": f"Avg {col}",
            "value": f"{df[col].mean():,.2f}",
            "icon": "📈"
        })
        kpis.append({
            "label": f"Max {col}",
            "value": f"{df[col].max():,.2f}",
            "icon": "🔝"
        })

    app_logger.info("KPIs generated successfully.")
    return kpis
