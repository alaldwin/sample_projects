import pandas as pd
from customer import Train_transform_data

def sample_df():
    return pd.DataFrame({
        "ID": [1,2,2],
        "Gender": ["Male", "Female", "Female"],
        "Graduated": ["Yes","No","No"],
        "Ever_Married": ["Yes", None, "No"],
        "Profession": ["Engineer", None, "Doctor"],
        "Work_Experience": [5, None, 2],
        "Family_Size": [3, None, 4],
        "Age": [25, -5, 130]
    })

def test_transform_data():
    df = sample_df()
    cleaned = Train_transform_data(df)

    # check duplicates remove
    assert cleaned.duplicated(subset=["ID", "Gender", "Graduated"]).sum() == 0 

    # Check no negative or too large age
    assert cleaned["Age"].between(0, 120).all()

    # check missing values filled
    assert cleaned["Profession"].isnull().sum() == 0
    assert cleaned["Ever_Married"].isnull().sum() == 0

    # check data_quality_flag exists in a file
    assert "data_quality_flag" in cleaned.columns