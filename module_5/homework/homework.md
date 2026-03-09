# Solution to Questions from Module 5 Homework

1) In a Bruin project, what are the required files/directories?

> **pipeline.yaml and assets/ only**

2) Which incremental strategy processes a specific interval period by deleting and inserting data for that time period?

> **time_interval**

3) Pipeline VariablesYou have a variable defined in pipeline.yml:variables: taxi_types: type: array items: type: string default: ["yellow", "green"]How do you override this when running the pipeline to only process yellow taxis? 

> **bruin run ./pipeline/pipeline.yml --var 'taxi_types=["yellow"]'**

4) You've modified the ingestion/trips.py asset and want to run it plus all downstream assets. Which command should you use?

> **bruin run --select ingestion.trips+**

5) You want to ensure the pickup_datetime column in your trips table never has NULL values. Which quality check should you add to your asset definition?

> **name: not_null**

6) After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

> **bruin lineage**

7) First-Time RunYou're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

> **--full-refresh**