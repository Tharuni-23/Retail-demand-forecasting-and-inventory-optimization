# 🏗️ Week 1 — Data Architecture & ETL

Week 1 focuses on setting up the data warehouse, loading the M5 dataset, preprocessing the data, and performing data quality checks.

## Week 1 Architecture

```text
M5 Forecasting Dataset
        │
        ▼
     Raw CSV Files
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
             Processed Data
                   │
                   ▼
            Google BigQuery
               m5_retail
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
raw_calendar  sales_validation_long  raw_sell_prices
        │          │          │
        └──────────┼──────────┘
                   ▼
          Data Ready for
        dbt Transformation
