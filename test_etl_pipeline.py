import pandas as pd
import pytest
import requests

from etl_pipeline import ETLError, fetch_data, save_to_csv, transform_data, validate_data


def test_fetch_data(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return [{"id": 1, "name": "Rajan", "username": "rajan01", "email": "rajan@example.com"}]

    monkeypatch.setattr("etl_pipeline.requests.get", lambda *args, **kwargs: MockResponse())

    data = fetch_data("https://example.com/api")

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_fetch_data_api_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Connection failed")

    monkeypatch.setattr("etl_pipeline.requests.get", mock_get)

    with pytest.raises(ETLError, match="API request failed"):
        fetch_data("https://example.com/api")


def test_fetch_data_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr("etl_pipeline.requests.get", mock_get)

    with pytest.raises(ETLError, match="timed out"):
        fetch_data("https://example.com/api")


def test_transform_data():
    data = [
        {
            "id": 1,
            "name": "  Rajan  ",
            "username": " rajan01 ",
            "email": " rajan@example.com ",
            "extra": "remove",
        }
    ]

    df = transform_data(data)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "name", "username", "email"]
    assert df.loc[0, "name"] == "Rajan"
    assert df.loc[0, "email"] == "rajan@example.com"


def test_transform_removes_duplicates():
    data = [
        {"id": 1, "name": "Rajan", "username": "r1", "email": "r1@example.com"},
        {"id": 1, "name": "Rajan", "username": "r1", "email": "r1@example.com"},
    ]

    df = transform_data(data)

    assert len(df) == 1


def test_transform_empty_data():
    df = transform_data([])

    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert list(df.columns) == ["id", "name", "username", "email"]


def test_transform_missing_column():
    data = [{"id": 1, "name": "Rajan", "username": "r1"}]

    with pytest.raises(ETLError, match="Missing required columns"):
        transform_data(data)


def test_validate_data():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Rajan", "Test"],
            "username": ["r1", "test"],
            "email": ["r1@example.com", "test@example.com"],
        }
    )

    assert validate_data(df) is True


def test_validate_duplicate_ids():
    df = pd.DataFrame(
        {
            "id": [1, 1],
            "name": ["Rajan", "Rajan"],
            "username": ["r1", "r1"],
            "email": ["r1@example.com", "r1@example.com"],
        }
    )

    with pytest.raises(ETLError, match="Duplicate IDs"):
        validate_data(df)


def test_save_to_csv(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Rajan"],
            "username": ["rajan01"],
            "email": ["rajan@example.com"],
        }
    )

    output_file = tmp_path / "test_output.csv"
    result = save_to_csv(df, output_file)

    assert result == output_file
    assert output_file.exists()

    saved_df = pd.read_csv(output_file)

    assert len(saved_df) == 1
    assert saved_df.loc[0, "name"] == "Rajan"
