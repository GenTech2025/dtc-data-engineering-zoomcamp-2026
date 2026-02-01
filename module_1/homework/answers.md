# Contain Answers to the Homework Questions from Module 1

> Q1: What's the version of pip in the python:3.13 image?

```bash
# Spin up the python docker container
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.13

# Once inside the container
pip --version
```

> Q2: Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

**db:5432**


> Use the ingestion script to ingest data into our PostgresSQL database

```python
# Ingests the dataset from homework one to the postgres database


# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for large files')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize):
    """Ingest Green Taxi Parquet + Taxi Zone Lookup CSV into PostgreSQL"""

    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    # ------------------------------------------------------------------
    # 1️⃣ Green taxi data (Parquet)
    # ------------------------------------------------------------------
    green_url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        "green_tripdata_2025-11.parquet"
    )

    print("Ingesting green taxi parquet data...")

    df_green = pd.read_parquet(green_url)

    df_green.to_sql(
        name="green_taxi_data",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("✅ Green taxi data ingested")

    # ------------------------------------------------------------------
    # 2️⃣ Taxi zone lookup (CSV)
    # ------------------------------------------------------------------
    zone_url = (
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/"
        "download/misc/taxi_zone_lookup.csv"
    )

    print("Ingesting taxi zone lookup data...")

    df_zones = pd.read_csv(zone_url)

    df_zones.to_sql(
        name="taxi_zone_lookup",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("✅ Taxi zone lookup ingested")


if __name__ == "__main__":
    run()
```

> Q3: For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

```sql

SELECT COUNT(*) AS short_trips
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;

-- 8007
```

> Q4: Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_date,
       MAX(trip_distance) AS longest_trip_distance
FROM green_taxi_data
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY longest_trip_distance DESC
LIMIT 1;

-- 2025-11-14
```

> Q5: Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

```sql

SELECT taxi_zone_lookup."Zone",
       SUM(green_taxi_data."total_amount") AS total_revenue
FROM green_taxi_data
JOIN taxi_zone_lookup
  ON green_taxi_data."PULocationID" = taxi_zone_lookup."LocationID"
WHERE green_taxi_data."lpep_pickup_datetime" >= '2025-11-18'
  AND green_taxi_data."lpep_pickup_datetime" < '2025-11-19'
GROUP BY taxi_zone_lookup."Zone"
ORDER BY total_revenue DESC
LIMIT 1;

-- East Harlem North
-- Note that not using quotes on the column names didnt work (most likely an issue while transforming the data in python and ingesting it to the main )

```

> Q6: For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

```sql

-- Find the location ID of East Harlem North

SELECT * FROM taxi_zone_lookup WHERE "Zone"='East Harlem North'; -- 74

-- Determine the Drop Off location ID

SELECT "tip_amount", "DOLocationID"
FROM green_taxi_data
WHERE "PULocationID"=74
ORDER BY 1 DESC
LIMIT 1; -- 263

-- Look up the drop off location in taxi zone lookup
SELECT "Zone" FROM taxi_zone_lookup WHERE "LocationID"=263; -- Yorkville West

```

> Q7: Which of the following sequences describes the Terraform workflow for: 1) Downloading plugins and setting up backend, 2) Generating and executing changes, 3) Removing all resources?

**terraform init, terraform apply -auto-approve, terraform destroy**