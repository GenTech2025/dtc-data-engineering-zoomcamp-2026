import duckdb
import requests
from pathlib import Path

# Base URL for NYC TLC data
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

def download_and_convert_files(taxi_type, years):
    """
    Downloads CSV.gz files for the given taxi type and years,
    converts them to Parquet, and stores in data/{taxi_type}/
    """
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for year in years:
        for month in range(1, 13):
            # Skip months that don't exist (e.g., FHV 2020)
            if taxi_type == "fhv" and year > 2019:
                continue

            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename
            if parquet_filepath.exists():
                print(f"Skipping {parquet_filename} (already exists)")
                continue

            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            url = f"{BASE_URL}/{taxi_type}/{csv_gz_filename}"
            print(f"Downloading {url} ...")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(csv_gz_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Converting {csv_gz_filename} to Parquet...")
            con = duckdb.connect()
            con.execute(f"""
                COPY (
                    SELECT * FROM read_csv_auto('{csv_gz_filepath}')
                )
                TO '{parquet_filepath}' (FORMAT PARQUET)
            """)
            con.close()

            # Remove CSV.gz file to save space
            csv_gz_filepath.unlink()
            print(f"Completed {parquet_filename}")

def update_gitignore():
    """
    Ensures 'data/' directory is ignored in git
    """
    gitignore_path = Path(".gitignore")
    content = gitignore_path.read_text() if gitignore_path.exists() else ""

    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')

if __name__ == "__main__":
    # Step 1: Update .gitignore
    update_gitignore()

    # Step 2: Download & convert data
    for taxi_type in ["yellow", "green", "fhv"]:
        years = [2019, 2020] if taxi_type in ["yellow", "green"] else [2019]
        download_and_convert_files(taxi_type, years)

    # Step 3: Load Parquet into DuckDB
    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in ["yellow", "green", "fhv"]:
        print(f"Loading {taxi_type} Parquet files into DuckDB...")
        con.execute(f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        """)

    con.close()
    print("All data loaded into taxi_rides_ny.duckdb (prod schema).")
