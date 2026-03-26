import pandas as pd
from sqlalchemy import create_engine

# EXTRACT
def extract():
    return pd.read_csv(r"C:\Users\aldwin\OneDrive\Desktop\part 1\sleep_health\Sleep_health_and_lifestyle_dataset.csv")

# TRANSFORM
def transform(df):
    # Data cleaning
    # Remove a duplicates
    df = df.drop_duplicates()
    # Handling missing value
    df = df.fillna("Unknown")
    # drop
    df = df.dropna(subset=["Person ID"])

    # Data standardization
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Fix wrong formats
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["sleep_duration"] = pd.to_numeric(df["sleep_duration"], errors="coerce")

    # Feature Engineering (NEW column)
    df["age_group"] = df["age"].apply(
        lambda x: "Adult" if x > 18 else "Minor"
    )

    return df 

# LOAD
def load(df):
    engine = create_engine(
    "postgresql+psycopg2://postgres:aldwino0012@localhost:5432/sleep_report"
)

    df.to_sql("sleep_report", con=engine, if_exists="append", index=False)

    return df

# MAIN PIPELINE
def main():
    df = extract()
    transformation = transform(df)
    load(transformation)

    print("Successfully Complete ETL!!")


if __name__=="__main__":
    main()