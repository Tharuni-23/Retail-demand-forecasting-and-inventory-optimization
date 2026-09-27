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

```

# 🏗️ Week 2 — Data Transformation with dbt

Week 2 focuses on transforming the raw M5 retail data stored in Google BigQuery into clean, structured analytical datasets using dbt.

## Week 2 Architecture

```text
Google BigQuery
    │
    ▼
m5_retail Dataset
    │
    ├──────────────────┬──────────────────┐
    ▼                  ▼                  ▼
raw_calendar    sales_validation_long   raw_sell_prices
    │                  │                  │
    └──────────────────┼──────────────────┘
                       ▼
                  dbt Sources
                       │
                       ▼
                Staging Models
             ┌─────────┼─────────┐
             ▼         ▼         ▼
      stg_calendar  stg_sales  stg_sell_prices
             │         │         │
             └─────────┼─────────┘
                       ▼
                  daily_sales
                       │
                ┌──────┴──────┐
                ▼             ▼
          weekly_sales   monthly_sales
                │
                ▼
        retail_demand_mart
                │
                ▼
        Data Quality Tests
                │
                ▼
        Forecasting-Ready Data
```
## 📌 Week 2 Components

| Component | Technology / Tool | Purpose |
|---|---|---|
| **Data Warehouse** | Google BigQuery | Store and provide access to the M5 retail data |
| **Data Transformation** | dbt | Transform raw data into clean, structured datasets |
| **dbt Configuration** | dbt Core + BigQuery Adapter | Connect dbt with the BigQuery warehouse |
| **Data Sources** | dbt Sources | Define and manage the raw BigQuery tables |
| **Staging Models** | dbt SQL | Prepare raw calendar, sales, and pricing data |
| **Daily Sales Model** | `daily_sales` | Combine sales data with calendar information |
| **Weekly Aggregation** | `weekly_sales` | Aggregate daily sales into weekly demand metrics |
| **Monthly Aggregation** | `monthly_sales` | Aggregate daily sales into monthly demand metrics |
| **Data Mart** | `retail_demand_mart` | Create a clean forecasting-ready weekly dataset |
| **Data Quality Testing** | dbt Tests | Validate important fields such as IDs, dates, and sales values |
| **Documentation** | dbt Docs | Document models, dependencies, and data lineage |
