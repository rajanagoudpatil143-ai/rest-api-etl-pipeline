import logging
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
DEFAULT_OUTPUT = "output.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


class ETLError(Exception):
    """Custom exception for ETL pipeline errors."""


def fetch_data(url=API_URL, timeout=10):
    """Extract JSON data from a REST API."""
    logger.info("Extracting data from API: %s", url)

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout as exc:
        logger.error("API request timed out.")
        raise ETLError("API request timed out.") from exc
    except requests.exceptions.RequestException as exc:
        logger.error("API request failed: %s", exc)
        raise ETLError(f"API request failed: {exc}") from exc
    except ValueError as exc:
        logger.error("API returned invalid JSON.")
        raise ETLError("API returned invalid JSON.") from exc

    if not isinstance(data, list):
        logger.error("Unexpected API response format.")
        raise ETLError("Expected API response to be a list.")

    logger.info("Extracted %d records.", len(data))
    return data


def transform_data(data):
    """Clean and transform API data into a DataFrame."""
    logger.info("Transforming data.")

    if not isinstance(data, list):
        raise ETLError("Input data must be a list.")

    if not data:
        logger.warning("No records available for transformation.")
        return pd.DataFrame(columns=["id", "name", "username", "email"])

    df = pd.DataFrame(data)

    required_columns = ["id", "name", "username", "email"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logger.error("Missing required columns: %s", missing_columns)
        raise ETLError(f"Missing required columns: {missing_columns}")

    df = df[required_columns].copy()

    for column in ["name", "username", "email"]:
        df[column] = df[column].fillna("").astype(str).str.strip()

    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df = df.dropna(subset=["id"])
    df["id"] = df["id"].astype(int)

    df = df.drop_duplicates(subset=["id"])
    df = df.reset_index(drop=True)

    logger.info("Transformation completed: %d clean records.", len(df))
    return df


def validate_data(df):
    """Validate the transformed DataFrame."""
    logger.info("Validating transformed data.")

    required_columns = ["id", "name", "username", "email"]

    if not isinstance(df, pd.DataFrame):
        raise ETLError("Validation input must be a Pandas DataFrame.")

    if list(df.columns) != required_columns:
        raise ETLError("DataFrame does not contain the expected columns.")

    if df["id"].isna().any():
        raise ETLError("ID column contains missing values.")

    if df["id"].duplicated().any():
        raise ETLError("Duplicate IDs found.")

    if (df["email"] == "").any():
        logger.warning("Some records have missing email values.")

    logger.info("Data validation passed.")
    return True


def save_to_csv(df, filename=DEFAULT_OUTPUT):
    """Load transformed data into a CSV file."""
    logger.info("Loading data into CSV: %s", filename)

    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    logger.info("CSV file created successfully: %s", output_path)
    return output_path


def run_pipeline(output_file=DEFAULT_OUTPUT):
    """Run the complete Extract -> Transform -> Validate -> Load pipeline."""
    logger.info("========== ETL PIPELINE STARTED ==========")

    try:
        data = fetch_data()
        df = transform_data(data)
        validate_data(df)
        save_to_csv(df, output_file)

        logger.info("========== ETL PIPELINE COMPLETED ==========")
        return df

    except ETLError:
        logger.exception("ETL pipeline failed.")
        raise


if __name__ == "__main__":
    run_pipeline()
