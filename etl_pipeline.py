import requests
import pandas as pd

API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_data(url=API_URL):
    """Fetch JSON data from a REST API."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def transform_data(data):
    """Transform API data into a clean DataFrame."""
    df = pd.DataFrame(data)

    if df.empty:
        return df

    # Keep only the columns needed for the ETL output.
    columns = ["id", "name", "username", "email"]
    df = df[[column for column in columns if column in df.columns]].copy()

    # Standardize text fields.
    for column in ["name", "username", "email"]:
        if column in df.columns:
            df[column] = df[column].fillna("").astype(str).str.strip()

    return df


def save_to_csv(df, filename="output.csv"):
    """Save the transformed DataFrame to a CSV file."""
    df.to_csv(filename, index=False)
    return filename


def run_pipeline(output_file="output.csv"):
    """Run the complete Extract -> Transform -> Load pipeline."""
    print("ETL Pipeline Started")

    print("Fetching data from API...")
    data = fetch_data()
    print(f"Data fetched successfully: {len(data)} records")

    print("Transforming data...")
    df = transform_data(data)
    print("Transformation completed.")

    print("Saving data...")
    save_to_csv(df, output_file)
    print(f"{output_file} created successfully.")

    print("ETL Pipeline Completed")
    return df


if __name__ == "__main__":
    run_pipeline()
