import pandas as pd
import pytest

from etl_pipeline import fetch_data, transform_data, save_to_csv


def test_fetch_data(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return [{"id": 1, "name": "Rajan", "email": "rajan@example.com"}]

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("etl_pipeline.requests.get", mock_get)

    data = fetch_data("https://example.com/api")

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_transform_data():
    data = [
        {
            "id": 1,
            "name": "  Rajan  ",
            "username": " rajan01 ",
            "email": " rajan@example.com ",
        }
    ]

    df = transform_data(data)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "name", "username", "email"]
    assert df.loc[0, "name"] == "Rajan"
    assert df.loc[0, "email"] == "rajan@example.com"


def test_transform_empty_data():
    df = transform_data([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty


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
