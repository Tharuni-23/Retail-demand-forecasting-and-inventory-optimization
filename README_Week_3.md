# Week 3 --- Demand Forecasting & Model Evaluation

## Overview

Week 3 focuses on building and evaluating demand forecasting models for
the **Retail Demand Forecasting & Inventory Optimization** project using
the **M5 retail sales dataset**.

Two forecasting approaches were implemented and compared:

-   **Prophet** --- time-series forecasting baseline
-   **LightGBM** --- gradient-boosting machine-learning model using
    calendar, price, lag, rolling, and event-based features

The objective was to forecast demand for a selected product-store
combination and determine which model provides better forecasting
performance.

------------------------------------------------------------------------

## Dataset

The project uses the M5 dataset containing Walmart retail sales
information.

### Selected Series

-   **Product:** `FOODS_3_090`
-   **Store:** `CA_3`
-   **Historical observations:** 1,913 days
-   **Forecast/Test Horizon:** 30 days

The following raw datasets were used:

-   `sales_train_validation.csv`
-   `calendar.csv`
-   `sell_prices.csv`

------------------------------------------------------------------------

# 1. Time Series Forecasting with Prophet

## Data Preparation

The selected product-store series was extracted from the sales dataset
and converted from the original wide format into a time-series format
containing:

-   `date`
-   `sales`

The data was then prepared in Prophet's required format:

-   `ds` → date
-   `y` → actual demand

## Train-Test Split

A time-based split was used:

-   Training period: 1,883 days
-   Testing period: 30 days

The final 30 historical observations were kept as unseen test data.

## Prophet Configuration

The Prophet model was configured with:

-   Yearly seasonality: enabled
-   Weekly seasonality: enabled
-   Daily seasonality: disabled
-   Multiplicative seasonality

## Evaluation Metrics

The Prophet model was evaluated using:

-   **MAE (Mean Absolute Error)**
-   **RMSE (Root Mean Squared Error)**
-   **WMAPE (Weighted Mean Absolute Percentage Error)**

### Prophet Results

  Metric     Result
  -------- --------
  MAE         47.06
  RMSE        56.87
  WMAPE      40.11%

------------------------------------------------------------------------

# 2. LightGBM Demand Forecasting

LightGBM was implemented as a machine-learning approach for demand
forecasting.

Unlike Prophet, LightGBM uses engineered features to learn relationships
between historical demand, calendar information, price, events, and
previous sales values.

## Feature Engineering

The following features were created:

### Calendar Features

-   `day_of_week`
-   `day_of_month`
-   `week_of_year`
-   `month`
-   `quarter`
-   `year`

### Price Features

-   `sell_price`
-   `price_change`

### Event Features

-   `is_event_1`
-   `is_event_2`

### Lag Features

-   `lag_1`
-   `lag_7`
-   `lag_14`
-   `lag_28`

### Rolling Features

-   `rolling_mean_7`
-   `rolling_mean_14`
-   `rolling_mean_28`

Lag and rolling features were created using previous observations to
avoid using future demand information.

## Model Configuration

The LightGBM regressor was configured with:

``` python
LGBMRegressor(
    objective="regression",
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,
    max_depth=-1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
```

## Train-Test Split

The final 30 observations were reserved for testing, while the preceding
observations were used for training.

## LightGBM Results

  Metric     Result
  -------- --------
  MAE         24.30
  RMSE        32.89
  WMAPE      20.71%

------------------------------------------------------------------------

# 3. Model Comparison

The two models were evaluated on the same 30-day test period.

  Model                  MAE        RMSE        WMAPE
  -------------- ----------- ----------- ------------
  Prophet              47.06       56.87       40.11%
  **LightGBM**     **24.30**   **32.89**   **20.71%**

## Result

**LightGBM performed significantly better than the Prophet baseline for
the selected product-store series.**

Compared with Prophet:

-   MAE improved by approximately **48.4%**
-   RMSE improved by approximately **42.2%**
-   WMAPE improved by approximately **48.4%**

This indicates that incorporating historical demand patterns, lag
features, rolling averages, price information, calendar variables, and
event indicators provided a substantial improvement over the baseline
time-series model.

------------------------------------------------------------------------

# 4. Visualizations

The following visualizations were created during Week 3:

### Actual vs Prophet Forecast

Shows the actual demand against Prophet's predictions for the 30-day
test period.

### Actual vs LightGBM Prediction

Shows the actual demand against LightGBM predictions.

### Prophet vs LightGBM Comparison

A combined visualization was created to compare:

-   Actual demand
-   Prophet forecast
-   LightGBM forecast

This provides a direct visual comparison of forecasting performance.

### LightGBM Feature Importance

Feature importance was analyzed to identify which engineered variables
contributed most to the model's predictions.

------------------------------------------------------------------------

# 5. Output Files

The forecasting results were saved under:

``` text
DATA/PROCESSED/
```

Important output files include:

``` text
prophet_forecast_FOODS_3_090_CA_3.csv
lightgbm_forecast_FOODS_3_090_CA_3.csv
model_comparison.csv
```

### Prophet Forecast Output

Contains:

-   `item_id`
-   `store_id`
-   `ds`
-   `y`
-   `yhat`
-   `yhat_lower`
-   `yhat_upper`

### LightGBM Forecast Output

Contains:

-   `item_id`
-   `store_id`
-   `date`
-   `actual`
-   `predicted`

### Model Comparison Output

Contains:

-   Model
-   MAE
-   RMSE
-   WMAPE

------------------------------------------------------------------------

# 6. Notebook

The main Week 3 notebooks are:

``` text
Notebooks/
├── 02_time_series_forecasting.ipynb
└── 03_lightgbm_forecasting.ipynb
```

### `02_time_series_forecasting.ipynb`

Contains:

-   Time-series preparation
-   Product-store series analysis
-   Prophet forecasting
-   30-day evaluation
-   Prophet visualization

### `03_lightgbm_forecasting.ipynb`

Contains:

-   Product-store extraction
-   Calendar and price integration
-   Feature engineering
-   Lag and rolling features
-   LightGBM training
-   Evaluation
-   Model comparison
-   Feature importance
-   Forecast output generation

------------------------------------------------------------------------

# 7. Key Findings

1.  Prophet provides a useful baseline for retail demand forecasting.
2.  LightGBM achieved substantially lower forecasting errors.
3.  Historical demand features such as lag and rolling features are
    highly useful for demand prediction.
4.  Price and calendar information can provide additional predictive
    signals.
5.  LightGBM is the preferred model for the current forecasting pipeline
    based on the evaluated test period.

------------------------------------------------------------------------
