import pandas as pd
import os
from datetime import datetime
from config import settings
from modules.ai_modules.dataset_summary import generate_dataset_summary
from modules.ai_modules.insight_generator import generate_insights
from utils.logger import app_logger


def generate_html_report(df, dataset_name="dataset"):
    """
    Generates a professional HTML storytelling report from the dataset.
    Saves to the reports directory and returns the file path.
    """
    if df is None or df.empty:
        return None

    summary_md = generate_dataset_summary(df, dataset_name)
    insights = generate_insights(df)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_filename = f"{dataset_name}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_path = os.path.join(settings.REPORTS_DIR, report_filename)

    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Build HTML
    insights_html = "".join(f"<li>{ins}</li>" for ins in insights)
    stats_html = df.describe(include='all').to_html(classes="stats-table", border=0)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{dataset_name.capitalize()} Analysis Report</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: #0f1117;
      color: #e0e0e0;
      line-height: 1.7;
      padding: 0;
    }}
    header {{
      background: linear-gradient(135deg, #1a1f2e 0%, #252c3b 100%);
      padding: 48px 64px;
      border-bottom: 1px solid #2d3650;
    }}
    header h1 {{
      font-size: 2.4rem;
      font-weight: 700;
      background: linear-gradient(90deg, #6366f1, #06b6d4);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 8px;
    }}
    header p {{ color: #9ca3af; font-size: 0.95rem; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 48px 32px; }}
    .card {{
      background: #1a1f2e;
      border: 1px solid #2d3650;
      border-radius: 12px;
      padding: 32px;
      margin-bottom: 32px;
    }}
    .card h2 {{ font-size: 1.3rem; font-weight: 600; margin-bottom: 20px;
                color: #6366f1; border-bottom: 1px solid #2d3650; padding-bottom: 12px; }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }}
    .kpi-card {{
      background: #252c3b;
      border: 1px solid #2d3650;
      border-radius: 10px;
      padding: 20px;
      text-align: center;
    }}
    .kpi-card .kpi-value {{ font-size: 1.8rem; font-weight: 700; color: #6366f1; }}
    .kpi-card .kpi-label {{ font-size: 0.8rem; color: #9ca3af; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }}
    ul.insights {{ list-style: none; padding: 0; }}
    ul.insights li {{ padding: 12px 16px; margin-bottom: 10px;
                       background: #252c3b; border-left: 4px solid #6366f1;
                       border-radius: 0 8px 8px 0; font-size: 0.93rem; }}
    .stats-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
    .stats-table th, .stats-table td {{
      padding: 10px 14px; text-align: left;
      border-bottom: 1px solid #2d3650;
    }}
    .stats-table th {{ background: #252c3b; color: #6366f1; font-weight: 600; }}
    .stats-table tr:hover {{ background: #20263a; }}
    footer {{ text-align: center; padding: 32px; color: #4b5563; font-size: 0.82rem;
              border-top: 1px solid #2d3650; }}
  </style>
</head>
<body>

<header>
  <h1>📊 {dataset_name.capitalize()} — Data Analysis Report</h1>
  <p>Generated on {timestamp} · AI Auto Data Analyst Platform</p>
</header>

<div class="container">

  <!-- KPI cards -->
  <div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-value">{len(df):,}</div><div class="kpi-label">Total Rows</div></div>
    <div class="kpi-card"><div class="kpi-value">{len(df.columns)}</div><div class="kpi-label">Columns</div></div>
    <div class="kpi-card"><div class="kpi-value">{df.isnull().sum().sum():,}</div><div class="kpi-label">Missing Values</div></div>
    <div class="kpi-card"><div class="kpi-value">{df.duplicated().sum():,}</div><div class="kpi-label">Duplicates</div></div>
    <div class="kpi-card"><div class="kpi-value">{len(num_cols)}</div><div class="kpi-label">Numeric Cols</div></div>
    <div class="kpi-card"><div class="kpi-value">{len(cat_cols)}</div><div class="kpi-label">Categorical Cols</div></div>
  </div>

  <!-- Dataset Summary -->
  <div class="card">
    <h2>📋 Dataset Overview</h2>
    <p><strong>Columns:</strong> {', '.join(f'<code>{c}</code>' for c in df.columns)}</p>
    <br/>
    <p><strong>Numeric Columns:</strong> {', '.join(f'<code>{c}</code>' for c in num_cols) or 'None'}</p>
    <p><strong>Categorical Columns:</strong> {', '.join(f'<code>{c}</code>' for c in cat_cols) or 'None'}</p>
  </div>

  <!-- AI Insights -->
  <div class="card">
    <h2>🤖 AI-Generated Insights</h2>
    <ul class="insights">
      {insights_html}
    </ul>
  </div>

  <!-- Descriptive Statistics -->
  <div class="card">
    <h2>📊 Descriptive Statistics</h2>
    {stats_html}
  </div>

</div>

<footer>
  Powered by <strong>AI Auto Data Analyst</strong> · Report generated at {timestamp}
</footer>
</body>
</html>"""

    try:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        app_logger.info(f"Storytelling HTML report saved to {report_path}")
        return report_path
    except Exception as e:
        app_logger.error(f"Failed to save HTML report: {e}")
        return None


def read_report(report_path):
    """Reads and returns the HTML report content."""
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        app_logger.error(f"Failed to read report at {report_path}: {e}")
        return None
