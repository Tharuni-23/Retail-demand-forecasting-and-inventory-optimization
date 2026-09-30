# ☁️ Google BigQuery — Complete Setup & Data Loading Process

Google BigQuery was used as the cloud data warehouse for the Retail Demand Forecasting & Inventory Optimization project.

The purpose of using BigQuery was to store the processed M5 retail data in a centralized cloud warehouse and make it available for the dbt transformation pipeline.

---

## 1. Create Google Cloud Project

First, a Google Cloud project was created for the retail demand forecasting project.

```text
Project Name: Retail Demand Forecasting
```
Create BigQuery Dataset:

Google Cloud Project
        │
        ▼
    m5_retail
        │
        ├── raw_calendar
        ├── sales_validation_long
        └── raw_sell_prices

Preparing the Datasets:
DATA/
└── RAW/
    ├── calendar.csv
    ├── sales_train_validation.csv
    ├── sales_train_evaluation.csv
    ├── sample_submission.csv
    └── sell_prices.csv


--> Now Preprocess the data and save the data

--> Now validate the every dataset.. and Load into the Google BigQuery 
        m5_retail
          │
          ├── raw_calendar
          │      └── 1,969 rows
          │
          ├── sales_validation_long
          │      └── 58,327,370 rows
          │
          └── raw_sell_prices
                 └── 6,841,121 rows

--> Connect dbt to BigQuery
    dbt
     │
     ▼
    Google BigQuery
     │
     ▼
    m5_retail





### The complete process we actually followed

**First:** Create Google Cloud Project  
↓  
**Next:** Create `m5_retail` BigQuery dataset  
↓  
**Next:** Prepare the M5 CSV data using Python  
↓  
**Next:** Convert huge sales data from **wide → long** format  
↓  
**Next:** Perform sales/calendar/pricing quality checks  
↓  
**Next:** Save processed data as Parquet  
↓  
**Next:** Load the processed data into BigQuery  
↓  
**Next:** We got the **free-storage quota error** while trying to reload the huge sales table  
↓  
**Next:** Changed the loading approach so the script checks whether the table already exists  
↓  
**Next:** Verified all 3 BigQuery tables and row counts  
↓  
**Next:** Connected **dbt → BigQuery**  
↓  
**Finally:** `dbt debug` passed → ready for the Week 2 transformation pipeline.
