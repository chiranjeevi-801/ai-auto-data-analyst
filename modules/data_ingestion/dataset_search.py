"""
dataset_search.py

Thin orchestration wrapper that delegates to kaggle_importer
for the actual Kaggle API calls.  Kept as a separate module so
future search engines (e.g. HuggingFace datasets, data.gov) can
be added without touching the rest of the codebase.
"""

from modules.data_ingestion.kaggle_importer import search_kaggle_datasets
from utils.logger import app_logger


def search_datasets(query: str, source: str = "kaggle", max_results: int = 10):
    """
    Search for public datasets matching *query*.

    Parameters
    ----------
    query       : free-text search string
    source      : currently only 'kaggle' is supported
    max_results : maximum number of results to return

    Returns
    -------
    list[dict]  : each dict has keys 'ref', 'title', 'size', 'votes'
    """
    if source == "kaggle":
        app_logger.info(f"Searching Kaggle for: '{query}'")
        return search_kaggle_datasets(query, max_results=max_results)
    else:
        app_logger.warning(f"Unsupported dataset source: {source}")
        return []
