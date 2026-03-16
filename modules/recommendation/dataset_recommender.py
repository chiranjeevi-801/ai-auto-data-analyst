import pandas as pd
import numpy as np
from utils.logger import app_logger


# Curated list of well-known public datasets for recommendation
_PUBLIC_DATASETS = [
    {"name": "Titanic Survival Dataset", "source": "Kaggle", "ref": "heptapod/titanic",
     "description": "Classic classification dataset about Titanic passenger survival.", "size": "Small"},
    {"name": "House Prices Dataset", "source": "Kaggle", "ref": "harlfoxem/housesalesprediction",
     "description": "Predict house sale prices from features like location and size.", "size": "Small"},
    {"name": "Iris Flower Dataset", "source": "Kaggle", "ref": "uciml/iris",
     "description": "Famous multi-class classification dataset for flower species.", "size": "Tiny"},
    {"name": "COVID-19 Global Data", "source": "Kaggle", "ref": "josephassaker/world-covid-19-dataset",
     "description": "Global COVID-19 statistics and trends over time.", "size": "Medium"},
    {"name": "World Population", "source": "Kaggle", "ref": "rsrishav/world-population",
     "description": "Country-level population data across years.", "size": "Small"},
    {"name": "Netflix Movies & TV Shows", "source": "Kaggle", "ref": "shivamb/netflix-shows",
     "description": "Explore Netflix catalogue with genres, ratings, and release years.", "size": "Small"},
    {"name": "Amazon Top 50 Bestselling Books", "source": "Kaggle", "ref": "sootersaalu/amazon-top-50-bestselling-books-2009-2019",
     "description": "Amazon bestsellers data with user ratings and genres.", "size": "Tiny"},
    {"name": "Global Superstore", "source": "Kaggle", "ref": "juhi1994/superstore",
     "description": "Sales data from a global retail superstore — great for BI dashboards.", "size": "Medium"},
    {"name": "Spotify Tracks Dataset", "source": "Kaggle", "ref": "maharshipandya/-spotify-tracks-dataset",
     "description": "Audio features and popularity stats for Spotify tracks.", "size": "Medium"},
    {"name": "Airline Passenger Satisfaction", "source": "Kaggle", "ref": "teejmahal20/airline-passenger-satisfaction",
     "description": "Survey data about airline passenger satisfaction.", "size": "Medium"},
]


def recommend_datasets(df=None, keyword=None, top_n=6):
    """
    Returns curated dataset recommendations.
    - If a keyword is provided, filters by name/description.
    - If a dataframe is given, tries to match based on column patterns
      (e.g. lat/lon → geo datasets, date columns → time-series datasets).
    """
    candidates = _PUBLIC_DATASETS.copy()

    # Keyword filter
    if keyword:
        kw = keyword.lower()
        candidates = [d for d in candidates
                      if kw in d['name'].lower() or kw in d['description'].lower()]

    # Dataset-aware recommendations (heuristic)
    if df is not None and not df.empty:
        col_lower = [c.lower() for c in df.columns]
        boosts = []
        rest = []
        for d in candidates:
            boosted = False
            if any(k in col_lower for k in ['date', 'year', 'month', 'time', 'timestamp']):
                if any(k in d['description'].lower() for k in ['time', 'trend', 'year', 'covid']):
                    boosts.append(d)
                    boosted = True
            if any(k in col_lower for k in ['price', 'sale', 'revenue', 'profit', 'cost']):
                if any(k in d['description'].lower() for k in ['price', 'sales', 'retail', 'store', 'book']):
                    boosts.append(d)
                    boosted = True
            if not boosted:
                rest.append(d)
        candidates = boosts + rest

    app_logger.info(f"Returning {min(top_n, len(candidates))} dataset recommendations.")
    return candidates[:top_n]
