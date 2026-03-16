# AI Auto Data Analyst

> **A modular, AI-powered automated data analytics platform built with Python and Streamlit.**
> Upload a dataset and get instant EDA, visualizations, AI insights, a natural-language chatbot, and a professional report — all in one place.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **Data Ingestion** | Upload CSV/Excel, import from URL, or search & download Kaggle datasets |
| 🧹 **Auto Cleaning** | Remove duplicates, impute missing values, standardize column names |
| ✅ **Validation** | Schema checks, empty-column and zero-variance detection |
| 📤 **Export** | Download cleaned data as CSV, Excel, or SQL dump |
| 🔬 **EDA** | Summary stats, missing-value heatmap, per-column statistics |
| 🔗 **Correlation** | Pearson/Spearman/Kendall matrix + top correlated pairs |
| 📈 **Auto Charts** | Intelligent Plotly chart selection based on column data types |
| 🤖 **AI Insights** | Rule-based insight engine (skewness, outliers, high cardinality…) |
| 💬 **Ask the Data** | Natural-language chatbot (rule-based + optional PandasAI/OpenAI) |
| 📄 **Report** | One-click professional HTML storytelling report |
| 🔍 **Recommendations** | Curated Kaggle dataset suggestions based on your data |
| 🗄️ **SQLite Storage** | Datasets and metadata persisted locally |
| 📊 **KPIs** | Auto-generated key metrics for every dataset |

---

## 🗂️ Project Structure

```
ai-auto-data-analyst/
├── app.py                          # Main Streamlit entry point
├── requirements.txt
├── .env                            # API keys (not committed)
│
├── config/
│   ├── settings.py                 # Paths and app constants
│   └── api_keys.py                 # Key retrieval helpers
│
├── data/                           # Auto-created at runtime
│   ├── raw/       cleaned/   processed/   reports/   exports/
│
├── modules/
│   ├── data_ingestion/             # file_uploader, url_importer, kaggle_importer, dataset_search
│   ├── data_processing/            # data_cleaner, data_validator, data_converter, data_profiler
│   ├── analysis/                   # eda_analyzer, statistical_analysis, correlation_analysis
│   ├── visualization/              # chart_generator, auto_visualization, kpi_generator
│   ├── dashboard/                  # layout_manager, dashboard_builder
│   ├── ai_modules/                 # dataset_summary, insight_generator,
│   │                               #   natural_language_query, story_report_generator
│   └── recommendation/             # dataset_recommender
│
├── database/
│   ├── db_connection.py
│   ├── data_storage.py
│   └── schema_manager.py
│
├── utils/
│   ├── logger.py
│   ├── helper_functions.py
│   └── file_manager.py
│
└── tests/
    ├── test_ingestion.py
    ├── test_cleaning.py
    └── test_analysis.py
```

---

## 🚀 Quick Start

### 1. Clone / open the project

```bash
cd "c:\Users\chira\OneDrive\Desktop\Data Analysis with py\ai-auto-data-analyst"
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Edit `.env` and fill in your keys:

```env
OPENAI_API_KEY=sk-...
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_kaggle_api_key
```

> **Note:** The chatbot and CSV charts work without any API key. OpenAI and Kaggle keys are only needed for the advanced AI chat and Kaggle dataset search features.

### 5. Run the app

```bash
streamlit run app.py
```

The platform will open at **http://localhost:8501** in your browser.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📊 Data Pipeline

```
User Input
    │
    ▼
Data Ingestion (Upload / URL / Kaggle)
    │
    ▼
Data Validation (schema, null checks)
    │
    ▼
Data Cleaning (duplicates, imputation, renaming)
    │
    ▼
Cleaned Dataset saved → data/cleaned/
    │
    ▼
EDA + Statistics + Correlation
    │
    ▼
Auto Chart Generation (Plotly)
    │
    ▼
AI Summary + Insights + NL Chatbot
    │
    ▼
Storytelling HTML Report
```

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| UI / Dashboard | Streamlit |
| Data Processing | Pandas, NumPy, SciPy |
| Visualization | Plotly |
| AI / NLP | OpenAI, LangChain, PandasAI |
| Data Profiling | ydata-profiling |
| Database | SQLite (built-in) |
| Export | XlsxWriter, ReportLab |

---

## 📄 License

MIT — free to use and modify.
