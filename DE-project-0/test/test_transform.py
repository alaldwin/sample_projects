from season_etl import transform
import pandas as pd


def test_transform_success():

    # fake API data
    sample_data = [
        {
            "flags": {
                "png": "ph.png",
                "svg": "ph.svg",
                "alt": "Philippines Flag"
            },

            "name": {
                "common": "Philippines",
                "official": "Republic of the Philippines",

                "nativeName": {
                    "fil": {
                        "official": "Republika ng Pilipinas",
                        "common": "Pilipinas"
                    }
                }
            }
        }
    ]

    # run function
    df = transform(sample_data)

    # check dataframe type
    assert isinstance(df, pd.DataFrame)

    # check values
    assert df.loc[0, "common"] == "Philippines"

    assert df.loc[0, "official"] == "Republic of the Philippines"

    assert df.loc[0, "native_common"] == "Pilipinas"

    assert df.loc[0, "native_official"] == "Republika ng Pilipinas"

    assert df.loc[0, "image"] == "ph.png"


def test_transform_missing_native_name():

    sample_data = [
        {
            "flags": {
                "png": "jp.png"
            },

            "name": {
                "common": "Japan",
                "official": "Japan"
            }
        }
    ]

    df = transform(sample_data)

    assert df.loc[0, "common"] == "Japan"

    # should safely return None
    assert df.loc[0, "native_common"] is None


def test_transform_empty_data():

    df = transform([])

    assert df.empty