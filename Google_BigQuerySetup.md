# ☁️ Google BigQuery — Complete Setup & Data Loading Process

Google BigQuery was used as the cloud data warehouse for the **Retail Demand Forecasting & Inventory Optimization** project.

The purpose of using BigQuery was to store the processed M5 retail data in a centralized cloud warehouse and make it available for the dbt transformation pipeline.

---

## 1. Google Cloud Project Setup

First, a Google Cloud project was created for the retail demand forecasting project.

**Project Name:** `Retail Demand Forecasting`

**Project ID:** `swift-casing-509808-a7`

---

## 2. Create BigQuery Dataset

A BigQuery dataset was created inside the Google Cloud project.

**Dataset:** `m5_retail`

**Location:** `US`

The dataset acts as the main container for the M5 retail tables.

### BigQuery Structure

```text
Google Cloud Project
│
└── m5_retail
    │
    ├── raw_calendar
    ├── sales_validation_long
    └── raw_sell_prices
```

---

## 3. M5 Dataset Preparation

The M5 Forecasting Dataset was organized inside the project.

### Raw Dataset Structure

```text
DATA/
│
└── RAW/
    ├── calendar.csv
    ├── sales_train_validation.csv
    ├── sales_train_evaluation.csv
    ├── sample_submission.csv
    └── sell_prices.csv
```

The raw datasets were first processed using Python before loading them into BigQuery.

---

## 4. Data Preprocessing

Python was used to prepare the raw M5 data.

The main preprocessing tasks were:

- Cleaning calendar data
- Checking sales data
- Checking pricing data
- Converting sales data from wide format to long format
- Enriching sales data with calendar information
- Saving processed datasets in Parquet format

---

## 5. Wide-to-Long Sales Transformation

The original sales dataset was in wide format.

### Original Format

```text
id       item_id    store_id    d_1    d_2    d_3    d_4
item_1   FOODS_1    CA_1        3      5      0      2
```

The sales data was converted into long format.

### Long Format

```text
id       item_id    store_id    d      sales
item_1   FOODS_1    CA_1        d_1    3
item_1   FOODS_1    CA_1        d_2    5
item_1   FOODS_1    CA_1        d_3    0
item_1   FOODS_1    CA_1        d_4    2
```

This structure makes the sales data easier to query, aggregate, and transform using BigQuery and dbt.

---

## 6. Processed Data

The processed datasets were stored in Parquet format.

```text
DATA/
│
├── RAW/
│
└── PROCESSED/
    ├── sales_validation_long.parquet
    ├── sales_validation_enriched.parquet
    ├── sales_validation_final.parquet
    └── sell_prices.parquet
```

The main datasets used for BigQuery loading were:

- `calendar.csv`
- `sales_validation_long.parquet`
- `sell_prices.parquet`

---

## 7. Data Quality Validation

Before loading the data into BigQuery, data quality checks were performed.

### Sales Data Checks

| Check | Result |
|---|---:|
| Sales rows | 30,490 |
| Daily sales columns | 1,913 |
| Total daily observations | 58,327,370 |
| Duplicate product rows | 0 |
| Missing sales values | 0 |
| Negative sales values | 0 |
| Minimum sales | 0 |
| Maximum sales | 763 |

### Zero Sales Analysis

| Metric | Result |
|---|---:|
| Zero-sales observations | 39,777,094 |
| Zero-sales percentage | 68.2% |

---

## 8. Calendar Data Validation

The calendar dataset was checked for:

- Missing values
- Duplicate records
- Date formatting
- Day identifiers
- Week identifiers
- Event information
- SNAP information

The cleaned calendar data was then prepared for BigQuery.

---

## 9. Pricing Data Validation

The `sell_prices` dataset was validated before loading.

| Check | Result |
|---|---:|
| Total rows | 6,841,121 |
| Null `store_id` | 0 |
| Null `item_id` | 0 |
| Null `wm_yr_wk` | 0 |
| Null `sell_price` | 0 |
| Negative prices | 0 |
| Zero prices | 0 |
| Minimum price | 0.01 |
| Maximum price | 107.32 |
| Duplicate price keys | 0 |

The following combination was also verified to be unique:

```text
(store_id, item_id, wm_yr_wk)
```

---

## 10. Load Data into BigQuery

After preprocessing and validation, the processed datasets were loaded into the `m5_retail` BigQuery dataset.

### Final BigQuery Tables

| Table | Rows | Purpose |
|---|---:|---|
| `raw_calendar` | 1,969 | Calendar and event information |
| `sales_validation_long` | 58,327,370 | Long-format daily sales data |
| `raw_sell_prices` | 6,841,121 | Store, item and weekly pricing data |

### BigQuery Structure

```text
m5_retail
│
├── raw_calendar
│   └── 1,969 rows
│
├── sales_validation_long
│   └── 58,327,370 rows
│
└── raw_sell_prices
    └── 6,841,121 rows
```

---

## 11. BigQuery Extraction and Loading Script

A reusable Python extraction and loading script was created:

```text
Scripts/
└── load_m5_to_bigquery.py
```

The script automates the data loading process.

### Script Workflow

```text
Processed Data
      │
      ▼
Python Loading Script
      │
      ▼
Connect to BigQuery
      │
      ▼
Check if Table Exists
      │
      ├── YES ──► Skip Loading
      │
      └── NO ───► Load Data
                    │
                    ▼
              Verify Table
                    │
                    ▼
               Print Row Count
```

---

## 12. BigQuery Loading Configuration

The loading script was configured with the Google Cloud project and BigQuery dataset.

| Configuration | Value |
|---|---|
| Project | `swift-casing-509808-a7` |
| Dataset | `m5_retail` |
| Location | `US` |

### Target Tables

- `raw_calendar`
- `sales_validation_long`
- `raw_sell_prices`

---

## 13. Error Encountered — BigQuery Storage Quota

During the initial loading process, an error occurred while working with the large sales table.

```text
403 Quota exceeded:
Your project exceeded quota for free storage for projects
```

The issue occurred while attempting to reload or replace the large `sales_validation_long` table.

The table contains:

```text
58,327,370 rows
```

---

## 14. Solution to the Storage Error

Instead of repeatedly recreating or replacing existing tables, the loading script was modified to check whether the table already exists.

### Loading Logic

```text
Run Loading Script
        │
        ▼
Check if Table Exists
        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
 Skip      Load
Loading    Data
   │         │
   └────┬────┘
        ▼
   Continue
```

This prevents unnecessary reloading of already-existing tables.

---

## 15. Final Script Output

After modifying the loading logic, the script successfully detected the existing tables.

```text
Already exists: swift-casing-509808-a7.m5_retail.raw_calendar
Rows: 1,969
Skipping load.
------------------------------------------------------------

Already exists: swift-casing-509808-a7.m5_retail.raw_sell_prices
Rows: 6,841,121
Skipping load.
------------------------------------------------------------

Already exists: swift-casing-509808-a7.m5_retail.sales_validation_long
Rows: 58,327,370
Skipping load.
------------------------------------------------------------

M5 BigQuery extraction/load completed successfully.
```

The script can therefore be executed repeatedly without unnecessarily reloading existing tables.

---

## 16. Verify BigQuery Tables

The final BigQuery dataset was verified successfully.

```text
Google Cloud Project
│
└── m5_retail
    │
    ├── raw_calendar
    │   └── 1,969 rows
    │
    ├── sales_validation_long
    │   └── 58,327,370 rows
    │
    └── raw_sell_prices
        └── 6,841,121 rows
```

---

## 17. Connect dbt to BigQuery

After BigQuery was successfully configured, dbt was connected to the BigQuery warehouse.

```text
dbt
 │
 ▼
Google BigQuery
 │
 ▼
m5_retail
```

Google Cloud OAuth authentication was configured for the dbt connection.

The connection was verified using:

```bash
dbt debug
```

### Result

```text
Connection test: [OK connection ok]

All checks passed!
```

---

## 18. Complete BigQuery Data Flow

The complete process followed during Week 1 was:

```text
M5 Forecasting Dataset
        │
        ▼
Google Cloud Project
        │
        ▼
BigQuery Dataset
m5_retail
        │
        ▼
Python Data Preprocessing
        │
        ▼
Wide → Long Transformation
        │
        ▼
Data Quality Checks
        │
        ▼
Processed Parquet Data
        │
        ▼
BigQuery Data Loading
        │
        ▼
Storage Quota Issue
        │
        ▼
Table Existence Check
        │
        ▼
BigQuery Tables Verified
        │
        ▼
dbt Connection
        │
        ▼
dbt Transformation Pipeline
```

---

## 19. Final BigQuery Architecture

```text
                    M5 DATASET
                        │
                        ▼
               Python Preprocessing
                        │
                        ▼
                Data Quality Checks
                        │
                        ▼
              ┌───────────────────┐
              │   GOOGLE BIGQUERY  │
              │                    │
              │     m5_retail      │
              │                    │
              │  raw_calendar      │
              │  sales_validation  │
              │  raw_sell_prices   │
              └─────────┬─────────┘
                        │
                        ▼
                       dbt
                        │
                        ▼
                Data Transformation
                        │
                        ▼
               Forecasting-Ready Data
```


## 🔄 Overall Process

```text
M5 Forecasting Dataset
        ↓
Google Cloud Project
        ↓
BigQuery Dataset
        ↓
Python Preprocessing
        ↓
Wide → Long Transformation
        ↓
Data Quality Validation
        ↓
Save Processed Data
        ↓
Load into BigQuery
        ↓
Handle Storage Quota Issue
        ↓
Check Existing Tables
        ↓
Verify BigQuery Tables
        ↓
Connect dbt
        ↓
Ready for dbt Transformation
```
