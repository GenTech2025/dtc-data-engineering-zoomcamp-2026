# Setup Local Enviroment for Module 4

1) Create a conda enviroment and use **uv** or **pip** to keep dependencies isolated

```bash
# Create and activate the conda enviroment
conda create -n de-zoomcamp-dbt python=3.11 -y
conda activate de-zoomcamp-dbt

# Initialize the directory with uv\
cd module_4/taxi_rides_ny
uv init

# Add python dependencies through uv
uv add dbt-duckdb requests # Will not be going with uv as the package manager as every dbt command needs to be prefixed by 'uv run'

# Add python dependencies using pip
pip install dbt-duckdb requests

# Install the CLI version of DuckDB using conda
conda install duckdb -y

# Check if tools installed sucessfully
dbt --version
duckdb --version
```

2) Start setting up **dbt Core**

```bash
# Create where the dbt profile will be stored
mkdir -p ~/.dbt

# Create the profile.yml file to setup dbt with DuckDB
nano ~/.dbt/profiles.yml
```

> The profile.yml file defines which database/datawarehouse dbt is connected to, in our case it we will connect to our persistent DuckDB database.

```yaml
# projects.yml
taxi_rides_ny:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: dev
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '4GB'
        preserve_insertion_order: false

    prod:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: prod
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '4GB'
        preserve_insertion_order: false
```

> Now navigate to our data directory where we will initialize **dbt**

```bash

cd module_4/taxi_rides_ny

dbt init

```

> Logs for dbt project initialization

```txt
(de-zoomcamp-dbt) > dbt init
13:02:37  Running with dbt=1.11.4
13:02:37  Creating dbt configuration folder at /home/roy/.dbt
Enter a name for your project (letters, digits, underscore): taxi_rides_ny
13:02:47  
Your new dbt project "taxi_rides_ny" was created!

For more information on how to configure the profiles.yml file,
please consult the dbt documentation here:

  https://docs.getdbt.com/docs/configure-your-profile

One more thing:

Need help? Don't hesitate to reach out to us via GitHub issues or on Slack:

  https://community.getdbt.com/

Happy modeling!

13:02:47  Setting up your profile.
Which database would you like to use?
[1] duckdb

(Don't see the one you want? https://docs.getdbt.com/docs/available-adapters)

Enter a number: 1
13:03:21  Profile taxi_rides_ny written to /home/roy/.dbt/profiles.yml using target's sample configuration. Once updated, you'll be able to start developing with dbt.
```
