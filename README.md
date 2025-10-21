
-----

# Data Preprocessing Pipeline for Multi-Purpose Applications
## Note : This repo only stores the data loader, transformer and extraction file. Use official mage.ai for docker installation.

## 1\. Overview

This project provides a modular and robust data preprocessing pipeline built with **Python** and orchestrated using **Mage.ai**. It is designed to be easily adapted for various data sources and downstream applications, such as machine learning, business intelligence, or data warehousing.

The core workflow is broken into three distinct stages:

1.  **Load:** Ingest data from various sources.
2.  **Transform:** Clean, process, and engineer features.
3.  **Export:** Save the processed data to a target destination.

-----

## 2\. Technology Stack

  * **Orchestration:** [Mage.ai](https://www.mage.ai/)
  * **Core Language:** Python 3.9+
  * **Key Libraries:**
      * **Pandas:** For core data manipulation and structures.
      * **Scikit-learn:** For scaling, encoding, and feature transformation.
      * *(Add others as needed, e.g., `psycopg2` for-PostgreSQL, `boto3` for-AWS S3, `sqlalchemy`)*

-----

## 3\. Project Structure

The project's logic is organized into three main Python files, each corresponding to a block type in Mage.

```
/your-mage-project
├── pipelines
│   └── /your_pipeline_name
│       ├── data_loader.py
│       ├── transformer.py
│       ├── data_exporter.py
│       └── metadata.yaml     (Defines the pipeline DAG)
├── io_config.yaml            (Environment-specific configurations)
├── requirements.txt          (Project dependencies)
└── README.md                 (This documentation)
```

-----

## 4\. Core Components (Mage Blocks)

This section details the purpose and function of each core file.

### 4.1. `data_loader.py` 📥

This file contains all data ingestion logic. It uses the `@data_loader` decorator in Mage. Its primary responsibility is to fetch data from one or more sources and return it as a Pandas DataFrame.

**Key Functions (Examples):**

  * `load_from_csv(...)`: Loads data from a local or remote CSV file.
  * `load_from_postgres(...)`: Connects to a PostgreSQL database, executes a query, and fetches the results.
  * `load_from_api(...)`: Fetches data from a REST API endpoint and parses the JSON response.

**Mage Decorator:**

```python
@data_loader
def load_data(*args, **kwargs):
    # Your loading logic here
    # Example:
    # db_config = kwargs['config']['POSTGRES_DB']
    # df = load_from_postgres(db_config)
    # return df
```

**Output:** A raw Pandas DataFrame.

-----

### 4.2. `transformer.py` ✨

This is the main "workhorse" of the pipeline. It contains all data cleaning, validation, and feature engineering logic using the `@transformer` decorator. It takes the raw DataFrame(s) from the loader, performs a series of transformations, and returns a clean, analysis-ready DataFrame.

**Key Functions (Examples):**

  * `handle_missing_values(...)`: Imputes or drops nulls using strategies like mean, median, or a constant.
  * `encode_categorical_features(...)`: Applies One-Hot Encoding or Label Encoding to categorical columns.
  * `normalize_numerical_features(...)`: Scales numerical data using `MinMaxScaler` or `StandardScaler`.
  * `create_new_features(...)`: Performs feature engineering (e.g., extracting day-of-week from a date, combining text fields).
  * `cast_data_types(...)`: Ensures all columns have the correct data type (e.g., `int`, `float`, `datetime`).

**Mage Decorator:**

```python
@transformer
def transform_data(df, *args, **kwargs):
    # Your transformation logic here
    # Example:
    # df = handle_missing_values(df, strategy='median')
    # df = encode_categorical_features(df, columns=['category'])
    # df = normalize_numerical_features(df, columns=['price'])
    # return df
```

**Input:** A raw Pandas DataFrame.
**Output:** A cleaned, transformed Pandas DataFrame.

-----

### 4.3. `data_exporter.py` 📤

This file handles loading the final, processed DataFrame to its destination. It uses the `@data_exporter` decorator.

**Key Functions (Examples):**

  * `export_to_parquet(...)`: Saves the DataFrame to a Parquet file, locally or in cloud storage (e.g., S3, GCS).
  * `load_to_bigquery(...)`: Loads the DataFrame into a Google BigQuery table.
  * `write_to_production_db(...)`: Inserts or updates records in a production SQL database.

**Mage Decorator:**

```python
@data_exporter
def export_data(df, *args, **kwargs):
    # Your exporting logic here
    # Example:
    # target_bucket = kwargs['config']['S3_BUCKET_NAME']
    # export_to_parquet(df, bucket=target_bucket, key='processed/data.parquet')
```

**Input:** A transformed Pandas DataFrame.

-----

## 5\. Setup and Installation

1.  **Clone the Repository:**

    ```bash
    git clone [YOUR_REPOSITORY_URL]
    cd [YOUR_PROJECT_NAME]
    ```

2.  **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    You must have a `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

    *(**Note:** A typical `requirements.txt` for this project might include `mage-ai`, `pandas`, `scikit-learn`, `psycopg2-binary`, `google-cloud-bigquery`, etc.)*

4.  **Configure Environment:**
    Mage uses `io_config.yaml` to manage environment variables (like database credentials, API keys) for different environments (e.g., `dev`, `prod`).

      * Copy the `io_config.yaml.example` (if you have one) to `io_config.yaml`.
      * Fill in your `dev` profile with the necessary credentials. **Do not commit sensitive keys to Git.**

5.  **Start Mage.ai:**

    ```bash
    mage start [your_project_name]
    ```

    This will start the Mage UI, typically at `http://localhost:6789`.

-----

## 6\. How to Run the Pipeline

1.  **Open the Mage UI:** Navigate to `http://localhost:6789` in your browser.
2.  **Open Your Pipeline:** Find your pipeline (e.g., `your_pipeline_name`) in the dashboard.
3.  **Define the DAG:** If you haven't already, connect your blocks in the visual editor or `metadata.yaml` file. The flow should be:
    `data_loader.py` → `transformer.py` → `data_exporter.py`
4.  **Run the Pipeline:**
      * Click the **"Run"** button in the UI.
      * Select your execution environment (e.g., `dev`).
      * You can trigger a full run or run individual blocks.
5.  **Schedule (Optional):** Use the "Triggers" tab in the Mage UI to set up a schedule (e.g., run daily at midnight).

-----

## 7\. Customization and Extension

This pipeline is designed for modularity. To adapt it for a new purpose:

  * **To Change Data Source:** Modify the function(s) in `data_loader.py` to point to your new source (e.g., change the SQL query, API endpoint, or file path).
  * **To Change Preprocessing Logic:** This is the most common change. Add, remove, or modify the transformation functions within `transformer.py` to suit your new dataset's needs.
  * **To Change Destination:** Modify the function(s) in `data_exporter.py` to save the data to your desired location (e.g., a different S3 bucket, a Redshift warehouse, or a local CSV).
  * **To Add Steps:** You can add new `.py` files with `@transformer` blocks and insert them into the pipeline flow within the Mage UI or `metadata.yaml`.
