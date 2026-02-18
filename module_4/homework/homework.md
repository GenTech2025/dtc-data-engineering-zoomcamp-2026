# Solution to questions from Module 4 (Analytics Engineering)

1) Given a dbt project with the following structure:

```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

If you run `dbt run --select int_trips_unioned`, what models will be built?

> **int_trips_unioned.sql** only since this model is being explicitly selected in the dbt run command without any preceding or following '+' sign.

2) You've configured a generic test like this in your `schema.yml`:

```yaml
columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
```

Your model `fct_trips` has been running successfully for months. A new value `6` now appears in the source data.

What happens when you run `dbt test --select fct_trips`?

> **dbt will fail the test, returning a non-zero exit code**

3) After running your dbt project, query the fct_monthly_zone_revenue model. What is the count of records in the fct_monthly_zone_revenue model?

```sql

SELECT COUNT(*) FROM taxi_rides_ny.prod.fct_monthly_zone_revenue;

```
> **12,184**


4) Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020. Which zone had the highest revenue?

```sql
SELECT pickup_zone, SUM(revenue_monthly_total_amount) as total_revenue
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM revenue_month) = 2020
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 1;
```

> **East Harlem North**

5) Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?

```sql
SELECT SUM(total_monthly_trips)
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND EXTRACT (MONTH FROM revenue_month) = 10
  AND EXTRACT(YEAR FROM revenue_month) = 2019;
```

> **384634**

6) Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019. Load the FHV trip data for 2019 into your data warehouse
Create a staging model stg_fhv_tripdata with these requirements:
- Filter out records where dispatching_base_num IS NULL
- Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)

What is the count of records in stg_fhv_tripdata?

```sql
SELECT count(*)
FROM taxi_rides_ny.prod.stg_fhv_tripdata
WHERE dispatching_base_num IS NOT NULL;
```

> **43244639**