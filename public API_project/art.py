import requests
import pandas as pd
import json
from datetime import datetime

url = "https://api.artic.edu/api/v1/artworks"

def fetch_data():
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_raw_json(data, filename="art_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def save_raw_csv(data, filename="art_data.csv"):
    if isinstance(data, dict):
        data = data.get("articles", data.get("data", data))
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return df

def data_transform(df):
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates(subset=["api_model", "api_link"], keep="first")
    df_clean = df_clean[["id", "api_model", "api_link", "updated_at", "suggest_autocomplete_boosted"]].fillna("unkown")
    df_clean = df_clean.rename(columns={
        "api_model": "models",
        "api_link": "links",
        "updated_at": "update_time",
        "timestamp": "datetime",
        "suggest_autocomplete_boosted": "auto_boosted"
    })

    return df_clean

def main():
    data = fetch_data()

    save_raw_json(data)
    df = save_raw_csv(data)
    transformation = data_transform(df)

    transformation.to_csv("Final_output.csv", index=False)

    print("Successfully!")

if __name__=="__main__":
    main()