from unittest.mock import patch, Mock
import requests
from season_etl import extract

@patch("season_etl.requests.get")
def test_extract(mock_get):

    mock_response = Mock()

    mock_response.ok = True

    mock_response.json.return_value = [
        {
            "name": {
                "common": "Phillipines",
                "official": "Anguilla",
                "nativeName": {
                    "eng": {
                        "official": "Anguilla",
                        "common": "Anguilla"
                    }
                }
            }
        },
    ]

    mock_get.return_value = mock_response

    result = extract("test_extract.json")

    assert result[0]["name"]["common"] == "Phillipines"

    mock_get.assert_called_once_with(
        url="https://restcountries.com/v3.1/all?fields=name,flags",
        params={"fields": ["name", "flags"]},
        timeout=10
    )


@patch("season_etl.requests.get")
def test_extract_failed(mock_get):

    mock_response = Mock()

    mock_response.ok = False
    mock_response.status_code = 404

    mock_get.return_value = mock_response

    result = extract("test.json")

    assert result is None


@patch("season_etl.requests.get")
def text_test_timeout(mock_get):

    mock_get.side_effect = requests.exceptions.Timeout

    result = extract("test.json")

    assert result is None