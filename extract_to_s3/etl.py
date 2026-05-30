import os
import pandas as pd
import logging
import boto3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# create a logs & state folders
os.makedirs("logs", exist_ok=True)
os.makedirs("state", exist_ok=True)

# logging log book
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



s3 = boto3.client('s3',
                region_name = os.environ["region_name"],
                aws_access_key_id = os.environ["aws_access_key_id"],
                aws_secret_access_key = os.environ["aws_secret_access_key"]
    
)

response = s3.list_buckets()

for bucket in response['Buckets']:
    print(bucket['Name'])

RAW_BUCKET = 'healthcare-processed-data'
PROCESSED_BUCKET = 'bucket-healthcare-raw-data'

RAW_FILE = "data/raw/healthcare_dataset.csv"
PROCESSED_FILE = 'healthcare_clean_data.csv'

STATE_FILE = 'state/last_processed.txt'


def get_last_processed():

    if os.path.exists(STATE_FILE):

        with open(STATE_FILE, 'r') as file:
            return file.read().strip()

    return "2000-01-01"

def save_last_processed(date):

    with open(STATE_FILE, "w") as file:
        file.write(str(date))



# Extract
def extract_file():

    logging.info("CSV files loaded successfully.")

    df = pd.read_csv(RAW_FILE)

    df.columns = df.columns.str.strip()

    print(df.columns)

    return df



# Transformations
def transform_file(df, last_processed_date):

    logging.info("Transforming healthcare data.")

        # RENAME A COLUMNS NAMES
    df.rename(columns={
        "NAME": "name",
        "Age": "age",
        "Gender": "gender",
        "Blood Type": "blood_type",
        "Medical Condition": "medical_condition",
        "Date of Admission": "admission_date",
        "Doctor": "doctor",
        "Hospital": "hospital",
        "Insurance Provider": "insurance_provider",
        "Billing Amount": "billing_amount",
        "Room Number": "room_number",
        "Admission Type": "admission_type",
        "Discharge Date": "discharge_date",
        "Medication": "medication",
        "Test Results": "test_results"
    }, inplace = True)




        # Convert date
    df["admission_date"] = pd.to_datetime(
        df["admission_date"],
        errors="coerce"
    )

    last_processed_date = pd.to_datetime(last_processed_date)

    # Incremental load
    df = df[
        df["admission_date"] > last_processed_date
    ].copy()


    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Fill nulls
    df.fillna({
        "Name": "Unknown",
        "Gender": "Unknown"
    }, inplace=True)

    # Standardize text
    df["name"] = df["Name"].str.strip().str.title()


    df["hospital"] = (
        df["hospital"]
        .str.strip()
        .str.replace("-", " ", regex=False)
    )

    df["insurance_provider"] = (
            df["insurance_provider"]
            .str.strip()
            .str.replace(
                "UnitedHealthcare",
                "United Healthcare",
                regex=False
            )
        )

    # Numeric billing amount
    df["billing_amount"] = pd.to_numeric(
        df["billing_amount"],
        errors="coerce"
    ).round(2)

    # ETL timestamp
    df["etl_processed_date"] = datetime.now()

    return df


def load_file(df):

    logging.info("Loading Transformed Data.")

    # Save processed CSV locally
    df.to_csv(PROCESSED_FILE, index=False)

    # Upload RAW file
    s3.upload_file(
        RAW_FILE,
        RAW_BUCKET,
        f"raw/{os.path.basename(RAW_FILE)}"
    )


    # Upload PROCESSED file
    s3.upload_file(
        PROCESSED_FILE,
        PROCESSED_BUCKET,
        f"processed/{PROCESSED_FILE}"
    )

    logging.info("Upload Successfull.")



# MAIN ETL PIPELINE
def run_etl():

    try:

        logging.info("Healthcare ETL Job Started.")

        last_processed_date = get_last_processed()

        df = extract_file()

        transformed_df = transform_file(
            df,
            last_processed_date
        )

        if transformed_df.empty:

            logging.info("No new Healthcare Record Found.")
            return
        
        load_file(transformed_df)

        latest_date = transformed_df[
            "admission_date"
        ].max()
        
        save_last_processed(latest_date)

        logging.info(
            "Healthcare ETL Complete Successfully."
            )

    except FileNotFoundError as e:

        logging.error(f"File missing: {e}")

    except pd.errors.EmptyDataError:

        logging.error("CSV file is empty")

    except Exception as e:

        logging.error(f"Unexpected error: {e}")


if __name__=="__main__":
    run_etl()