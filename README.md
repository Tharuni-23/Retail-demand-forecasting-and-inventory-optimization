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

```

## Week 4: Interactive Dashboard & Inventory Optimization

### Objective
Develop an interactive web dashboard to visualize retail demand forecasts, compare machine learning models, and estimate inventory requirements using the M5 retail sales dataset.

### Tools & Technologies
- **Python** — Data processing and inventory calculations
- **Streamlit** — Interactive dashboard development
- **Pandas** — Data loading and manipulation
- **Prophet** — Time-series forecasting baseline
- **LightGBM** — Machine learning-based demand forecasting
- **Git & GitHub** — Version control and collaboration

### Dashboard Modules

**1. Retail Demand Dashboard**
- Displays total demand and average daily demand for the evaluation period.
- Identifies the best-performing model using WMAPE.
- Presents recent forecast results and model metrics.

**2. Demand Forecasting**
- Visualizes actual demand against Prophet and LightGBM predictions.
- Provides an interactive time-series chart for the selected product and store.
- Displays forecast evaluation data for the 30-day test period.

**3. Model Comparison**
- Compares Prophet and LightGBM using MAE, RMSE, and WMAPE.
- Displays model performance metrics and comparison charts.
- LightGBM achieved lower error values than Prophet on the evaluated test period.

**4. Inventory Optimization**
- Estimates safety stock and reorder points.
- Calculates recommended stock for a 30-day planning horizon.
- Allows users to adjust supplier lead time, current inventory, and target service level.
- Displays inventory status and additional stock requirements.

**5. What-if Analysis**
- Allows users to adjust assumed demand changes, supplier lead time, and price changes.
- Recalculates inventory requirements under different scenarios.
- Displays the price change as a scenario index; price elasticity is not yet modeled.

### Model Evaluation Results

| Model | MAE | RMSE | WMAPE |
|---|---:|---:|---:|
| Prophet | 47.06 | 56.87 | 40.11% |
| LightGBM | 24.30 | 32.89 | 20.71% |

*Evaluation metrics are based on the same 30-day historical holdout period for product FOODS_3_090 at store CA_3. They measure test-period performance, not future forecast accuracy.*

### Application Execution

Run the following command from the project root after activating the virtual environment:

```bash
streamlit run app.py
```

The dashboard will normally open at `http://localhost:8501`.

### Week 4 Outcome
Implemented an interactive Streamlit dashboard integrating demand visualization, model comparison, and baseline inventory-planning calculations.

### Next Steps
- Validate inventory estimates using the full historical demand series.
- Extend forecasting to additional products and stores.
- Integrate the processed data and analytical models into a broader inventory decision-support workflow.
- Improve deployment and application documentation.
