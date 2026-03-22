import pandas as pd
import numpy as np

df = pd.read_csv("train.csv")

def Train_transform_data(df):
    # Identify data quality issue
    def data_quality_check(df):
        return {
            "total_records": len(df),
            "duplicate_rows": df.duplicated().sum(),
            "missing_values": df.isnull().sum().to_dict(),
            "invalid_ages": df[(df["Age"] < 0) | (df["Age"] > 120)].shape[0]
        }

    quality_report = data_quality_check(df)

    # remove duplicates
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates(subset=["ID", "Gender", "Graduated"], keep="first")

    # Strandardize text formating
    df_clean["Ever_Married"] = df_clean["Ever_Married"].str.strip().str.title()
    df_clean["Gender"] = df_clean["Gender"].str.strip().str.lower()
    df_clean["Profession"] = df_clean["Profession"].str.strip().str.lower()

    # Handle missing values
    df_clean["Profession"] = df_clean["Profession"].fillna("Not Provided")
    df_clean["Ever_Married"] = df_clean["Ever_Married"].fillna("Unknown")
    df_clean["Work_Experience"] = df_clean["Work_Experience"].fillna(0.0)
    df_clean["Family_Size"] = df_clean["Family_Size"].fillna(0.0)

    # Filter invalid records
    initial = len(df_clean)
    df_clean = df_clean[(df_clean["Age"] >= 0) & (df_clean["Age"] <= 120)]
    df_clean = df_clean[df_clean["Graduated"].notna()]

    invalid_removed = initial - len(df_clean)
    print(f"Invalid records removed {invalid_removed}")

    # add data quality flags
    df_clean["data_quality_flag"] = np.where(
        (df_clean["Profession"] == "Not Provided") | (df_clean["Ever_Married"] == "Unknown"),
        "Incomplete",
        "Complete"
    )
    
    return df_clean, quality_report

def load_train_data(df_clean, quality_report):
    print("\n=== DATA CLEANING SUMMARY ===")
    print(f"Original records: {quality_report['total_records']}")
    print(f"Duplicates removed: {quality_report['duplicate_rows']}")
    print(f"Invalid ages removed: {quality_report['invalid_ages']}")
    print(f"Missing values before cleaning: {quality_report['missing_values']}")
    print(f"\nData Quality Distribution:\n{df_clean['data_quality_flag'].value_counts()}")
    
    df_clean.to_csv("Clean_Train_customer.csv", index=False)
    print("\nCleaned data exported to 'Clean_Train_customer.csv'")

def main():
    cleaned_df, quality_report = Train_transform_data(df)
    load_train_data(cleaned_df, quality_report)
    

if __name__=="__main__":
    main()