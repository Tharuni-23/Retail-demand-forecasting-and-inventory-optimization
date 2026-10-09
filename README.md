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
## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Google Cloud Platform | Cloud project and BigQuery environment |
| Google BigQuery | Cloud data warehouse |
| Python | Data preprocessing and ETL |
| Pandas | Data manipulation and validation |
| PyArrow | Parquet processing |
| Google Cloud BigQuery Client | Programmatic data loading |
| dbt | Data transformation and modeling |
| Google Cloud OAuth | Authentication |


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


# 📈 Week 3 --- Demand Forecasting & Model Evaluation

Week 3 focuses on building demand forecasting models using the M5 retail
dataset, evaluating their performance, comparing forecasting approaches,
and identifying the most important demand-driving features.

## Week 3 Architecture

``` text
                    M5 Retail Sales Dataset
                              │
                              ▼
                    Product-Store Selection
                     FOODS_3_090 — CA_3
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
       Time Series Preparation       Feature Engineering
                │                           │
                ▼                           ├── Calendar Features
             Prophet                      ├── Price Features
                │                         ├── Event Features
                ▼                         ├── Lag Features
        30-Day Forecast                  └── Rolling Features
                │                           │
                │                           ▼
                │                      LightGBM Model
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    30-Day Test Evaluation
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ MAE / RMSE / WMAPE     │
                 └─────────────────────────┘
                              │
                              ▼
                    Model Comparison
                 Prophet vs LightGBM
                              │
                              ▼
                    Feature Importance
                              │
                              ▼
                  Forecast Results Saved
```

## 🧠 Forecasting Models
  | Model / Purpose |
  |---|---|
  | **Prophet** |                             | Time-series forecasting baseline using trend and seasonality |

  |**LightGBM**|                          | Machine-learning demand forecasting using engineered features |  
  -----------------------------------------------------------------------

## 🛠️ Tools & Technologies

| Tool / Technology | Purpose |
|---|---|
| **Python** | Forecasting and model development |
| **Pandas** | Data preparation and manipulation |
| **NumPy** | Numerical calculations |
| **Prophet** | Time-series forecasting baseline |
| **LightGBM** | Gradient-boosting demand forecasting |
| **Scikit-learn** | Model evaluation metrics |
| **Matplotlib** | Forecast visualization |
| **Jupyter Notebook** | Experimentation and model development |
| **M5 Dataset** | Retail demand forecasting data |



# 🚀 Week 4 — Dashboard & Inventory Optimization

Week 4 focuses on transforming the forecasting results from Week 3 into an interactive **Streamlit dashboard** and implementing **inventory optimization and what-if analysis**.

---

## 🏗️ Week 4 Architecture

```text
                    FROM WEEK 3 
                         │
                         ▼
              ┌──────────────────────┐
              │  Forecast Results    │
              │                      │
              │  Prophet Forecast    │
              │  LightGBM Forecast   │
              │  Model Comparison    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    STREAMLIT APP     │
              │       app.py         │
              └──────────┬───────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌────────────┐ ┌─────────────┐ ┌──────────────┐
   │    KPI     │ │  Forecast   │ │    Model     │
   │ Dashboard  │ │ Visualization│ │  Comparison │
   └────────────┘ └─────────────┘ └──────────────┘
          │              │              │
          └──────────────┼──────────────┘
                         ▼
              ┌──────────────────────┐
              │ Inventory Optimization│
              └──────────┬───────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌────────────┐ ┌─────────────┐ ┌──────────────┐
   │   Safety   │ │   Reorder   │ │    Stock     │
   │   Stock    │ │    Point    │ │ Requirement  │
   └────────────┘ └─────────────┘ └──────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    What-If Analysis  │
              │                      │
              │  Demand Change       │
              │  Price Change        │
              │  Lead Time Change    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Business Insights   │
              │ & Recommendations    │
              └──────────────────────┘
