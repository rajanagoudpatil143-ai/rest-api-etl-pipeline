# REST API ETL Pipeline

A beginner-friendly Python mini project that demonstrates an **ETL (Extract, Transform, Load)** pipeline.

## Project Overview

The project:

1. Fetches user data from a REST API.
2. Transforms and cleans the data using Pandas.
3. Saves the transformed data to a CSV file.
4. Uses pytest unit tests to validate the ETL functions.

## Architecture

```text
REST API
   |
   v
Extract - requests
   |
   v
JSON Data
   |
   v
Transform - Pandas
   |
   v
Clean DataFrame
   |
   v
Load - CSV
   |
   v
output.csv

pytest -> validates ETL functions
```

## Technologies

- Python 3
- Requests
- Pandas
- pytest
- REST API
- CSV

## API Used

JSONPlaceholder Users API:

`https://jsonplaceholder.typicode.com/users`

## Setup

Create and activate a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the ETL Pipeline

```bash
python etl_pipeline.py
```

The pipeline creates:

```text
output.csv
```

## Run Tests

```bash
pytest -v
```

Expected result:

```text
4 passed
```

## ETL Stages

### Extract
`requests` retrieves JSON data from the REST API.

### Transform
Pandas converts the JSON data into a DataFrame and cleans the selected fields.

### Load
The transformed DataFrame is saved as a CSV file.

### Test
pytest verifies API handling, transformation, empty-data handling, and CSV output.

## Future Improvements

- Add logging
- Add API retry handling
- Add data validation
- Support multiple APIs
- Add a scheduled ETL job
- Add a dashboard using Streamlit
