"""
STEADYFin - Flask web app for the Cash Flow Intelligence capstone project.

What this file does, top to bottom:
1. Loads config (Databricks SQL warehouse creds, Power BI embed URL)
2. Opens a connection to the Databricks SQL warehouse on each request that needs data
3. Defines routes: home dashboard, AI suggestions page, CSV export, health check
4. Reads AI recommendations from cash_flow_gold.ai_suggestions - a table already
   populated by the 05_AI_Suggestions Databricks notebook (Gemini). This app
   does not call an AI API itself; it only displays what that notebook produced.
"""

import os
import csv
import io
import json
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()  # picks up a local .env file if present; no-op in Databricks Apps

from flask import Flask, render_template, request, Response, jsonify
from databricks import sql as databricks_sql

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Config - all read from environment variables so no secrets live in the code.
# In Databricks Apps, set these in app.yaml (env section) or as app secrets.
# Locally, set these in a .env file and load with `python-dotenv` (see README).
# ---------------------------------------------------------------------------
DATABRICKS_SERVER_HOSTNAME = os.environ.get("DATABRICKS_SERVER_HOSTNAME", "")
DATABRICKS_HTTP_PATH = os.environ.get("DATABRICKS_HTTP_PATH", "")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
POWERBI_EMBED_URL = os.environ.get("POWERBI_EMBED_URL", "")


def get_connection():
    """One place that opens a Databricks SQL connection - reused by every query
    below instead of repeating the same 4 lines everywhere."""
    return databricks_sql.connect(
        server_hostname=DATABRICKS_SERVER_HOSTNAME,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
    )


def run_query(query, params=None):
    """Runs a SQL query against the Gold views and returns rows as a list of dicts."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or [])
            columns = [c[0] for c in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return rows


# ---------------------------------------------------------------------------
# Data access helpers - one function per Gold view we actually use on a page
# ---------------------------------------------------------------------------

def get_latest_kpi_summary():
    """Most recent month's row from vw_business_kpi_summary, for the homepage cards."""
    rows = run_query("""
        SELECT * FROM cash_flow_project.cash_flow_gold.vw_business_kpi_summary
        ORDER BY month_key DESC LIMIT 1
    """)
    return rows[0] if rows else None


def get_kpi_trend(limit=12):
    """Last N months of KPI data, for the small trend sparkline on the homepage."""
    return run_query(f"""
        SELECT month_key, revenue, expenses, net_cash_flow
        FROM cash_flow_project.cash_flow_gold.vw_business_kpi_summary
        ORDER BY month_key DESC LIMIT {int(limit)}
    """)[::-1]


def get_shortage_rows(limit=24):
    """All months from vw_shortage_detection, for the AI Suggestions page."""
    return run_query(f"""
        SELECT * FROM cash_flow_project.cash_flow_gold.vw_shortage_detection
        ORDER BY month_key DESC LIMIT {int(limit)}
    """)


def get_quarterly_performance():
    return run_query("""
        SELECT * FROM cash_flow_project.cash_flow_gold.vw_quarterly_performance
        ORDER BY calendar_year, quarter
    """)


# ---------------------------------------------------------------------------
# AI Suggestions - reads the structured recommendations already generated and
# saved by 05_AI_Suggestions.py (Gemini) into cash_flow_gold.ai_suggestions.
# The website never calls an AI API itself - it just displays what that
# notebook already produced.
# ---------------------------------------------------------------------------

def get_ai_suggestions(limit=24):
    """All rows from the ai_suggestions table, most recent month first.
    recommendations_json is parsed here so templates get a plain Python list."""
    rows = run_query(f"""
        SELECT * FROM cash_flow_project.cash_flow_gold.ai_suggestions
        ORDER BY month_key DESC LIMIT {int(limit)}
    """)
    for row in rows:
        try:
            row["recommendations"] = json.loads(row.get("recommendations_json") or "[]")
        except (TypeError, ValueError):
            row["recommendations"] = []
    return rows


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Homepage: KPI cards, trend sparkline, and the embedded Power BI report."""
    try:
        kpi = get_latest_kpi_summary()
        trend = get_kpi_trend()
    except Exception as exc:
        app.logger.error(f"Data load failed: {exc}")
        kpi, trend = None, []
    return render_template(
        "index.html",
        kpi=kpi,
        trend=trend,
        powerbi_url=POWERBI_EMBED_URL,
        year=datetime.now().year,
    )


@app.route("/ai-suggestions")
def ai_suggestions():
    """AI Recommendations page: shows every month's structured recommendation
    (issue, root cause, priority, business impact, and the numbered suggestion
    list) exactly as generated by the 05_AI_Suggestions notebook."""
    try:
        suggestions = get_ai_suggestions()
        latest = suggestions[0] if suggestions else None
    except Exception as exc:
        app.logger.error(f"Data load failed: {exc}")
        suggestions, latest = [], None
    return render_template(
        "ai_suggestions.html",
        suggestions=suggestions,
        latest=latest,
        year=datetime.now().year,
    )


@app.route("/quarterly")
def quarterly():
    """Extra page: quarterly performance ranking, answers 'best quarter' directly."""
    try:
        rows = get_quarterly_performance()
    except Exception as exc:
        app.logger.error(f"Data load failed: {exc}")
        rows = []
    return render_template("quarterly.html", rows=rows, year=datetime.now().year)


@app.route("/export/monthly-summary.csv")
def export_csv():
    """Lets the owner download the KPI summary as a spreadsheet-friendly CSV."""
    rows = run_query("""
        SELECT * FROM cash_flow_project.cash_flow_gold.vw_business_kpi_summary
        ORDER BY month_key
    """)
    buffer = io.StringIO()
    if rows:
        writer = csv.DictWriter(buffer, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=steadyfin_monthly_summary.csv"},
    )


@app.route("/health")
def health():
    """Simple endpoint Databricks Apps (or you) can hit to confirm the app is alive."""
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})


if __name__ == "__main__":
    # Local dev only - Databricks Apps runs this via Gunicorn per app.yaml, not this block.
    app.run(host="0.0.0.0", port=8000, debug=True)
