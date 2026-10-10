from pathlib import Path
from google.cloud import bigquery


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ID = "swift-casing-509808-a7"
DATASET_ID = "m5_retail"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "DATA" / "RAW"
PROCESSED_DIR = BASE_DIR / "DATA" / "PROCESSED"


# --------------------------------------------------
# BigQuery client
# --------------------------------------------------

client = bigquery.Client(project=PROJECT_ID)


# --------------------------------------------------
# Helper function
# --------------------------------------------------

def load_file_to_bigquery(file_path, table_name, source_format):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    # Check whether the table already exists
    try:
        table = client.get_table(table_id)

        print(f"Already exists: {table_id}")
        print(f"Rows: {table.num_rows:,}")
        print("Skipping load.")
        print("-" * 60)
        return

    except Exception:
        # Table does not exist, so continue with the load
        pass

    job_config = bigquery.LoadJobConfig(
        source_format=source_format,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_EMPTY,
    )

    print(f"Loading: {file_path.name}")
    print(f"Target : {table_id}")

    with open(file_path, "rb") as file:
        load_job = client.load_table_from_file(
            file,
            table_id,
            job_config=job_config,
        )

    load_job.result()

    table = client.get_table(table_id)

    print(f"Loaded successfully: {table.num_rows:,} rows")
    print("-" * 60)

# --------------------------------------------------
# Load Calendar
# --------------------------------------------------

load_file_to_bigquery(
    RAW_DIR / "calendar.csv",
    "raw_calendar",
    bigquery.SourceFormat.CSV,
)


# --------------------------------------------------
# Load Sell Prices
# --------------------------------------------------

load_file_to_bigquery(
    PROCESSED_DIR / "sell_prices.parquet",
    "raw_sell_prices",
    bigquery.SourceFormat.PARQUET,
)


# --------------------------------------------------
# Load Long-Format Sales
# --------------------------------------------------

load_file_to_bigquery(
    PROCESSED_DIR / "sales_validation_long.parquet",
    "sales_validation_long",
    bigquery.SourceFormat.PARQUET,
)


print("M5 BigQuery extraction/load completed successfully.")