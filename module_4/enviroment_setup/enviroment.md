# Installing dbt-Core using pip

### Create a python virtual enviorment

```bash
# Reference: https://docs.getdbt.com/faqs/Core/install-pip-best-practices.md#using-virtual-environments

# Create the python virtual enviroment
python3 -m venv env_name
source env_name /bin/activate
which python

# Install dbt-core and dbt-duckdb
python -m pip install dbt-core dbt-duckdb
```