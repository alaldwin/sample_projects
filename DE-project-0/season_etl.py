import requests
import pandas as pd
import json
import os
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

os.makedirs("data/raw", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/main.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

quirystring = {
    "fields": ["name","flags"]
}

url = "https://restcountries.com/v3.1/all?fields=name,flags"



def extract(filename = "data/raw/countrie.json"):

    logging.info("Request Is Successful.")

    try:

        response = requests.get(
                url=url,
                params=quirystring, 
                timeout=10
            )
        
        logging.error("Request Timeout.")

        if response.ok:

            data = response.json()

            print(json.dumps(data, indent=4))
            print(f"Total records: {len(data)}")

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
                print("save a json file")

            print("Request Is Successful.")

            return data
        
        else:
            print(f"Request Failed: {response.status_code}")

    except requests.exceptions.Timeout as e:
        print(f"Time is Failed: {e}")

    except requests.exceptions.RequestException as e:
        print(f"requests is Failed: {e}")
    


def transform(data):

    logging.info("Transformation Is Successful.")

    raw = []

    for i in data:

        native = (
            i.get("name", {})
            .get("nativeName", {})
        )

        # get first native language safely
        native_data = {}

        if native:
            first_key = list(native.keys())[0]
            native_data = native[first_key]

        row = {
            "image": i.get("flags", {}).get("png"),
            "svg": i.get("flags", {}).get("svg"),
            "alt": i.get("flags", {}).get("alt"),

            "common": i.get("name", {}).get("common"),
            "official": i.get("name", {}).get("official"),

            "native_official": native_data.get("official"),
            "native_common": native_data.get("common")
        }

        raw.append(row)

    df = pd.DataFrame(raw)

    print(df.info())
    print(df.head(20))

    shape = df.shape
    print(f"Total row and columns {shape}")

    return df



def load(df):

    logging.info("Load The Dataset In To Database Is Successful.")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(DATABASE_URL)

    logging.error("connection in data base is successful.")

    if not df.empty:

        df.to_sql(
            "countries",
            con=engine,
            if_exists="replace",
            index=False
        )

        print("Data saved to PostgreSQL.")

    else:
        print("Insert data failed.")

    engine.dispose()

    print("Data save to PostgreSQL.")


def main():

    logging.info("Extract - Transform - Load (ETL) Is Successful.")

    data = extract()

    df = transform(data)

    load(df)

if __name__=="__main__":
    main()