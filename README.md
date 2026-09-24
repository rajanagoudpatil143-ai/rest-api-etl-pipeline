# REST API ETL Pipeline

A Python mini project demonstrating a complete **ETL (Extract, Transform, Validate, Load)** pipeline with automated unit testing.

## Project Objective

The pipeline extracts user data from a REST API, transforms and validates it with Pandas, and loads the final dataset into a CSV file.

The project also includes automated tests using pytest for normal and failure scenarios.

## Architecture

```text
             REST API
                 |
                 v
        +----------------+
        |    EXTRACT     |
        |    requests    |
        +----------------+
                 |
                 v
            JSON Data
                 |
                 v
        +----------------+
        |   TRANSFORM    |
        |     Pandas     |
        +----------------+
                 |
                 v
        +----------------+
        |    VALIDATE    |
        | Data Validation|
        +----------------+
                 |
                 v
        +----------------+
        |      LOAD      |
        |      CSV       |
        +----------------+
                 |
                 v
             output.csv

             pytest
                |
                v
      Automated Unit Testing
```

## Features

- REST API data extraction
- API timeout handling
- API connection/error handling
- JSON response validation
- Pandas data transformation
- Missing-column detection
- Duplicate-record removal
- Data validation
- CSV loading
- Structured logging
- Automated pytest unit tests
- Failure-case testing

## Technologies

- Python 3
- Requests
- Pandas
- pytest
- REST API
- CSV

## API

The project uses the JSONPlaceholder Users API:

`https://jsonplaceholder.typicode.com/users`

## Project Structure

```text
rest-api-etl-pipeline/
│
├── etl_pipeline.py
├── test_etl_pipeline.py
├── requirements.txt
├── README.md
├── sample_output.csv
├── .gitignore
└── output.csv              # generated locally, ignored by Git
```

## Setup

Create a virtual environment:

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the ETL Pipeline

```bash
python etl_pipeline.py
```

Expected output:

```text
ETL PIPELINE STARTED
Extracting data from API...
Extracted 10 records.
Transforming data.
Transformation completed: 10 clean records.
Validating transformed data.
Data validation passed.
Loading data into CSV...
CSV file created successfully.
ETL PIPELINE COMPLETED
```

## Run Tests

```bash
pytest -v
```

The test suite covers:

- Successful API extraction
- API connection failure
- API timeout
- Data transformation
- Duplicate removal
- Empty input
- Missing columns
- Data validation
- Duplicate ID validation
- CSV creation

## ETL Process

### 1. Extract

`requests` sends an HTTP GET request to the REST API.

### 2. Transform

Pandas converts the JSON response into a DataFrame and:

- selects required fields
- removes unnecessary fields
- cleans whitespace
- converts IDs to numeric values
- removes invalid IDs
- removes duplicate records

### 3. Validate

The transformed data is checked for:

- expected columns
- missing IDs
- duplicate IDs

### 4. Load

The validated DataFrame is saved as `output.csv`.

## Error Handling

The pipeline handles:

- API timeout
- connection errors
- HTTP errors
- invalid JSON
- invalid response formats
- missing required columns
- duplicate records
- invalid IDs

A custom `ETLError` exception is used for ETL-specific failures.

## Future Enhancements

- Database loading using MySQL/PostgreSQL
- Scheduling with Apache Airflow
- Docker containerization
- Cloud deployment
- Data quality reporting
- Streamlit monitoring dashboard
