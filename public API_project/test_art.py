import pandas as pd
from art import fetch_data, data_transform

def test_fetch_data():
    data = fetch_data()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "artworks" in data[0]

def test_transform_data():
    df = fetch_data()
    result = data_transform(df)

    assert "links" in result.columns
    assert "id" in result.columns
    df.duplicated(subset="api_model").sum() == 0