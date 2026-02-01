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
