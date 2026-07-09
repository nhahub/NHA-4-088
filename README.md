<p align="center">
  <!-- SCREENSHOT: project logo -->
  <!-- Recommended: a square PNG, ~400x400px, placed at 08 Screenshots/logo.png -->
  <img src="./08 Screenshots/steadyfin_logo.jpeg" alt="STEADYFin logo" width="300">
</p>

<h1 align="center">STEADYFin</h1>
<p align="center"><b>Cash Flow Intelligence Pipeline for a Coffee Shop Business</b></p>
<p align="center">Data Engineering Capstone Project — Databricks · Power BI · Flask</p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue">
  <img src="https://img.shields.io/badge/Databricks-FF3621?logo=databricks&logoColor=white">
  <img src="https://img.shields.io/badge/PowerBI-F2C811?logo=powerbi&logoColor=black">
  <img src="https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/Delta_Lake-00ADD8">
</p>
---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Repository Structure](#repository-structure)
- [Tech Stack](#tech-stack)
- [Datasets](#datasets)
- [Screenshots](#screenshots)
- [Setup Guide](#setup-guide)
  - [1. Databricks Pipeline (Bronze → Silver → Gold)](#1-databricks-pipeline-bronze--silver--gold)
  - [2. AI Suggestions Layer](#2-ai-suggestions-layer)
  - [3. Power BI Dashboard](#3-power-bi-dashboard)
  - [4. STEADYFin Website](#4-steadyfin-website)
- [Key Design Decisions](#key-design-decisions)
- [Demo Link](#demo-link)
- [Team](#team)

---

## Overview

STEADYFin is an end-to-end cash flow intelligence system built for a coffee
shop business. It ingests raw financial and point-of-sale data, transforms it
through a medallion architecture (Bronze → Silver → Gold), detects cash-flow
shortages automatically, generates AI-written recommendations for the
business owner, and presents everything through both a Power BI dashboard
and a custom web application.

**What it answers for the business owner:**
- Is this month financially healthy, and why or why not?
- How many months could the business survive on its current cash reserve?
- Which quarter makes the most money?
- Where is money actually going (payroll, supplies, marketing, utilities)?
- What should I actually do about it — in plain English, not just a chart?

---

<!-- SCREENSHOT: architecture / medallion diagram -->
<!-- Place the diagram exported from "07 Project Diagrams" here, e.g.:
<img src=".07 Project Diagrams/project_pipeline.jpeg" alt="Medallion architecture diagram" width="800">
-->
## Architecture

The following diagram illustrates the complete STEADYFin data pipeline,
starting from raw financial datasets through the Medallion Architecture,
ending with both the Power BI dashboard and the Flask web application.

<img src="./07 Project Diagrams/project-pipeline.jpeg" alt="STEADYFin Architecture" width="900">

## Repository Structure

| Folder | Contents |
|---|---|
| `01 Data Source` | Raw source CSVs (financial accounts, credit card, payroll, POS sales) |
| `02 Medallion Architecture` | Databricks notebooks: Bronze, Silver, Gold, and Gold Views layers |
| `03 AI Suggestions` | Notebook that generates structured cash-flow recommendations (Gemini) |
| `04 Power BI Dashboards` | The `.pbix` Power BI report file |
| `05 STEADYFin web-app/steadyfin` | Flask web application source code |
| `07 Project Diagrams` | Architecture and schema diagrams |
| `08 Screenshots` | Screenshots referenced throughout this README |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data platform | Databricks (Delta Lake, PySpark, Spark SQL) |
| Storage format | Delta Lake, medallion architecture |
| AI layer | Google Gemini |
| BI / Visualization | Power BI |
| Web application | Python, Flask, Gunicorn |
| Hosting | Databricks Apps |

---

## Datasets

| Source | Rows | Content |
|---|---|---|
| `checking_account_main` | 877 | Daily cash: sales revenue, COGS, operating expenses, balance |
| `checking_account_secondary` | 48 | Payroll account transfers |
| `coffee_sales_2years` | 517,365 | Individual POS transactions (product, qty, price, time) |
| `credit_card_account` | 133 | Business credit card, 5 vendors |
| `gusto_payroll` | 92 | Employee + contractor payroll by role |

Date range: January 2022 – December 2023.

---

## Screenshots

<!-- SCREENSHOT SECTION - fill in each block below with an actual image from 08 Screenshots -->

### Databricks Pipeline
<!-- e.g. workspace view of the 4 notebooks, a successful run, the Gold tables in the catalog -->
<img src="./08 Screenshots/databricks_arch.png" alt="Databricks pipeline notebooks" width="800">

### Power BI Dashboard
<!-- one screenshot per report page: Executive Overview, Expense Deep-Dive, Sales & Products, AI Recommendations -->
The Power BI dashboard provides a complete overview of the business's financial
performance by combining operational, sales, payroll, and cash flow data from
the Gold Layer. It enables business owners to monitor financial health,
identify spending patterns, evaluate sales performance, and detect potential
cash flow risks through interactive visualizations.

The dashboard consists of five main report pages:
### Executive Overview

<img src="./08 Screenshots/Executive_overview.png" alt="Power BI Executive Overview page" width="800">

*High-level KPIs, revenue, expenses, and cash flow summary. This page provides an overall view of the business's financial performance, including total revenue, expenses, net cash flow, account balance, and key operational metrics.*

---

### Sales Analysis

<img src="./08 Screenshots/sales.png" alt="Power BI Sales Analysis page" width="800">

*Analyzes sales performance through revenue trends, product categories, order volume, average order value, and hourly sales patterns to help identify customer purchasing behavior and top-performing products.*

---

### Business Health Monitor

<img src="./08 Screenshots/bussniess_health_monitor.png" alt="Power BI Business Health Monitor page" width="800">

*Monitors the overall financial health of the business by tracking cash flow status, shortage detection, healthy versus risky months, profitability indicators, and early warning signals.*

---

### Payroll & Expenses

<img src="./08 Screenshots/payroll.png" alt="Power BI Payroll & Expenses page" width="800">

*Provides a detailed breakdown of payroll, operating expenses, marketing, utilities, supplies, and credit card spending, helping identify the largest cost drivers within the business.*

---

### Financial Insights

<img src="./08 Screenshots/financial_insights.png" alt="Power BI Financial Insights page" width="800">

*Offers a detailed financial transaction analysis, allowing users to explore income and expenses by account, category, month, and year to better understand overall cash movement.*

### STEADYFin Website
While the Power BI dashboard focuses on business intelligence and interactive reporting, the STEADYFin web application offers a user-friendly platform that combines financial dashboards with AI-generated insights. It enables business owners to easily explore their financial status, monitor cash flow, and receive actionable recommendations through a responsive web interface.
### Dashboard

<img src="./08 Screenshots/web_dashboard.png" alt="STEADYFin Dashboard" width="800">

*The homepage presents the most important business KPIs, including revenue, expenses, net cash flow, current balance, and financial health indicators, allowing users to quickly assess the overall performance of their business.*

---

### AI Insights

<img src="./08 Screenshots/ai_insights.png" alt="STEADYFin AI Insights" width="800">

*Displays AI-generated financial recommendations based on the detected cash flow status. The suggestions help business owners understand potential risks and provide actionable recommendations to improve financial stability.*

---

### Quarterly Analysis

<img src="./08 Screenshots/web_quarterly.png" alt="STEADYFin Quarterly Analysis" width="800">

*Provides a quarterly breakdown of business performance, allowing users to compare revenue, expenses, and cash flow trends across different quarters and identify seasonal patterns.*

---

## Setup Guide

### 1. Databricks Pipeline (Bronze → Silver → Gold)

**Prerequisites:** a Databricks workspace with Unity Catalog enabled and a
running SQL Warehouse.

1. Clone this repository:
   ```bash
   git clone https://github.com/nhahub/NHA-4-088.git
   ```
2. In your Databricks workspace, import each notebook from
   `02 Medallion Architecture` (**Workspace → Import → File**).
3. Run the notebooks **in this exact order** (each one depends on the Delta
   tables created by the previous one):
   1. `01 Bronze_Layer` — ingests the 5 raw CSVs from `01 Data Source`
      (upload them to a Unity Catalog Volume first, and update the file path
      in the notebook to match).
   2. `02 Silver_Layer` — cleans types, standardizes dates, deduplicates.
   3. `03 Gold_Layer` — builds the star schema (dimensions + fact tables) and
      runs shortage detection.
   4. `04 Gold_Layer_Views` — creates the SQL views used by both Power BI and
      the website.
4. Confirm it worked:
   ```sql
   SELECT * FROM cash_flow_project.cash_flow_gold.vw_business_kpi_summary;
   ```

### 2. AI Suggestions Layer

1. Import the notebook from `03 AI Suggestions` into Databricks.
2. Set your Gemini API key inside the notebook (see the notebook's own setup
   note for exactly where).
3. Run it — this reads flagged months from `vw_shortage_detection` and
   writes structured recommendations to
   `cash_flow_project.cash_flow_gold.ai_suggestions`, which both the website
   and (optionally) Power BI can read from.

### 3. Power BI Dashboard

1. Open the `.pbix` file from `04 Power BI Dashboards` in **Power BI
   Desktop**.
2. Get your Databricks SQL Warehouse **Server hostname** and **HTTP Path**
   (**SQL Warehouses → your warehouse → Connection details**).
3. **Home → Transform data → Data source settings** (or reconnect via
   **Get data → Databricks**) and enter your own hostname/HTTP path plus a
   Personal Access Token.
4. Refresh the data (**Home → Refresh**).

### 4. STEADYFin Website

**Prerequisites:** Python 3.11+, a Databricks Personal Access Token with the
**BI Tools** scope.

1. Navigate to the app folder:
   ```bash
   cd "05 STEADYFin web-app/steadyfin"
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in this folder:
   ```
   DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxxxxxx
   DATABRICKS_TOKEN=your-databricks-token
   POWERBI_EMBED_URL=https://app.powerbi.com/view?r=your-embed-id
   ```
4. Run it locally:
   ```bash
   python app.py
   ```
   Open **http://localhost:8000**.
5. **To deploy inside Databricks as a Databricks App** instead of running it
   locally:
   ```bash
   databricks sync . /Workspace/Users/<your-email>/databricks_apps/steadyfin
   databricks apps deploy steadyfin --source-code-path /Workspace/Users/<your-email>/databricks_apps/steadyfin
   ```
   (Requires the Databricks CLI installed and authenticated —
   `databricks auth login --host <your-workspace-url>`.)

---

## Key Design Decisions

- **Galaxy schema, not a single mega-table.** 4 fact tables
  (`fact_transactions`, `fact_monthly_summary`, `fact_sales`,
  `fact_payroll`), each at its own grain, sharing conformed dimensions. See
  `02 Medallion Architecture/03 Gold_Layer` for the full reasoning.
- **Signed amounts for cash flow math.** Debits are stored as negative
  numbers so net cash flow is a plain `SUM()`, matching standard accounting
  ledger convention.
- **Shortage detection with a startup grace period.** The first 3 months of
  the business's history are classified `STARTUP_PERIOD` rather than
  `WARNING`/`INCOME_DROP`, since a 3-month-old business naturally has a low
  cash balance and no reliable rolling baseline yet. `CRITICAL` (actual
  negative cash flow) still fires unconditionally regardless of history
  length.
- **AI suggestions are precomputed, not called live.** The website reads
  from a Delta table populated by the `03 AI Suggestions` notebook, rather
  than calling an AI API on every page load — faster, cheaper, and the
  recommendations stay consistent between the website and Power BI.

---
## Demo Link
A full demonstration of the project is available below:

🎥**https://drive.google.com/file/d/1AQx2FK0vY3UZXyu_qSd9vG9U2KChZSXf/view?usp=sharing**
## Team

<!-- Add team member names and roles here -->
1.Basmala Samir <br/>
2.Evronia Romany <br/>
3.Malak Ibrahim <br/>
4.Asmaa Ashraf 
