
from pathlib import Path
from google.cloud import bigquery

PROJECT_ID = "swift-casing-509808-a7"
DATASET_ID = "m5_retail"

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "DATA" / "PROCESSED"

client = bigquery.Client(project=PROJECT_ID)

forecast_files = {
    "prophet_forecasts": (
        DATA_DIR / "prophet_forecast_FOODS_3_090_CA_3.csv"
    ),
    "lightgbm_forecasts": (
        DATA_DIR / "lightgbm_forecast_FOODS_3_090_CA_3.csv"
    ),
}

for table_name, file_path in forecast_files.items():
    if not file_path.exists():
        raise FileNotFoundError(f"Missing forecast CSV: {file_path}")

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with file_path.open("rb") as file:
        job = client.load_table_from_file(
            file,
            table_id,
            job_config=job_config,
        )

    job.result()
    table = client.get_table(table_id)

    print(f"Loaded {table_id}: {table.num_rows:,} rows")

print("Forecast tables loaded successfully.")
