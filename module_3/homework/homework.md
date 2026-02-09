# Solution to Questions from Module 3 Homework

1) What is count of records for the 2024 Yellow Taxi Data?

```sql
-- First create an external table
CREATE OR REPLACE EXTERNAL TABLE `starlit-effect-484216-a1.zoomcamp202625.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://data-nytaxi-dtc-de2026/yellow_tripdata_2024-*.parquet']
);
 -- Note: gs://data-nytaxi-dtc-de2026/yellow_tripdata_2024-01.parquet is a gsutils link

 -- Count the total number of rows for Jan 2024 to June 2024 data
 SELECT COUNT(*)
 FROM 'starlit-effect-484216-a1.zoomcamp202625.external_yellow_tripdata';
```
> 20,332,093

2) Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```sql
-- First create a materialized table
CREATE OR REPLACE TABLE starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_non_partitioned AS
SELECT * FROM starlit-effect-484216-a1.zoomcamp202625.external_yellow_tripdata;

-- Execute the query on both the tables

-- For External Table (0 MB)
SELECT COUNT(DISTINCT(PULocationID))
FROM starlit-effect-484216-a1.zoomcamp202625.external_yellow_tripdata;

-- For Materialized Table (155.12 MB)
SELECT COUNT(DISTINCT(PULocationID))
FROM starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_non_partitioned;
```

> External Table: 0MB and Materialized Table: 155.12MB

3) Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

```sql

-- Retrieve PULocationID from the Materialized Table
SELECT PULocationID
FROM starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_non_partitioned;

-- Retrieve PULocationID and DOLocationID
SELECT PULocationID, DOLocationID
FROM starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_non_partitioned;

```

> BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

4) How many records have a fare_amount of 0?

```sql

SELECT COUNT(*)
FROM starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_non_partitioned
WHERE fare_amount==0;

```

> 8333

5) What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

```sql
-- Create a table with partition and clustering
CREATE OR REPLACE TABLE starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM starlit-effect-484216-a1.zoomcamp202625.external_yellow_tripdata;

```

> Partition by tpep_dropoff_datetime and Cluster on VendorID

6) Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

```sql
-- Non Partitioned Materialized Table (310.24MB)
SELECT DISTINCT(VendorID)
FROM starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_non_partitioned
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned and Clustered Materialized Table (26.84MB)
SELECT DISTINCT(VendorID)
FROM starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```

> 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

7) Where is the data stored in the External Table you created?

> GCP Bucket

8) It is best practice in Big Query to always cluster your data:

> False

9)  Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why? (Optional)

```sql
SELECT COUNT(*)
FROM starlit-effect-484216-a1.zoomcamp202625.materialized_yellow_tripdata_partitioned_clustered;
```

> BigQuery estimates that the query above will process 0B when ran. The reason behind this is that the number of rows in a table is already stored as metadata and without any filtering conditions BigQuery can just access that value from the metadata.