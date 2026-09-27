# 📊 Retail Demand Forecasting & Inventory Optimization

## Zaalima Development Pvt. Ltd. — Data Analytics Project 2

An end-to-end retail analytics and demand forecasting project designed to help retail and supply-chain teams understand historical sales patterns, forecast future product demand, and support inventory optimization decisions.

The project uses the **M5 Forecasting Dataset** containing Walmart historical sales data and follows a structured pipeline using **Python, Google BigQuery, dbt, and time-series forecasting models**.

---

# 🎯 Project Objective

The objective of this project is to build an automated analytics and forecasting pipeline that can:

- Process historical retail sales data
- Perform data quality checks
- Store data in a cloud data warehouse
- Transform raw data into analytical datasets
- Aggregate daily sales into weekly and monthly views
- Build clean data marts for analysis
- Forecast future product demand
- Support inventory restocking decisions
- Provide interactive dashboards and reporting

---

# 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Data Warehouse | Google BigQuery |
| Data Transformation | dbt |
| Data Processing | Pandas, PyArrow |
| Forecasting | Prophet, LightGBM |
| Visualization | Streamlit / Tableau |
| Version Control | Git & GitHub |
| Dataset | M5 Forecasting Dataset |

---

# 📦 Dataset

The project uses the **M5 Forecasting Dataset**, which contains historical Walmart retail sales information.

### Main Dataset Files

```text
sales_train_validation.csv
sales_train_evaluation.csv
calendar.csv
sell_prices.csv
sample_submission.csv

```
# 🏗️ Project Architecture

The project follows an end-to-end data pipeline from raw M5 retail data to demand forecasting and inventory optimization.

```text
M5 Forecasting Dataset
        │
        ▼
   Raw M5 Data
        │
        ▼
Python Data Preprocessing
        │
        ├──────────────────────┐
        ▼                      ▼
Data Quality Checks      Data Formatting
        │                      │
        └──────────┬───────────┘
                   ▼
          Google BigQuery
             m5_retail
                   │
                   ▼
             dbt Sources
                   │
                   ▼
          dbt Staging Models
        ┌──────────┼──────────┐
        ▼          ▼          ▼
 stg_calendar  stg_sales  stg_sell_prices
        │          │          │
        └──────────┼──────────┘
                   ▼
              daily_sales
                   │
             ┌─────┴─────┐
             ▼           ▼
       weekly_sales  monthly_sales
             │
             ▼
      retail_demand_mart
             │
             ▼
     Time-Series Forecasting
        ┌────┴────┐
        ▼         ▼
     Prophet   LightGBM
        │         │
        └────┬────┘
             ▼
      Demand Forecasts
             │
             ▼
   Inventory Optimization
             │
             ▼
    Dashboard & Reporting
