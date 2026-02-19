# Bruin (data platform)

> Follow the Hands on Tutorial: https://github.com/bruin-data/bruin/tree/main/templates/zoomcamp

### Install Bruin

```bash
# Download and Install
curl -LsSf https://getbruin.com/install/cli | sh

# Refresh the terminal
source ~/.bashrc

# Check the version
bruin --version

```

### Basics of bruin project

---

The required parts of a Bruin project are:
- `.bruin.yml` in the root directory
- `pipeline.yml` in the `pipeline/` directory (or in the root directory if you keep everything flat)
- `assets/` folder next to `pipeline.yml` containing your Python, SQL, and YAML asset files

---


```text
my-first-pipeline/
├── .bruin.yml              # Environment and connection configuration
├── pipeline.yml            # Pipeline name, schedule, default connections
└── assets/
    ├── players.asset.yml   # Ingestr asset (data ingestion)
    ├── player_stats.sql    # SQL asset with quality checks
    └── my_python_asset.py  # Python asset
```

### Bruin commands

```bash
# Validate the pipeline (catches errors before running)
bruin validate .

# Run the entire pipeline
bruin run .

# Run a single asset
bruin run assets/my_python_asset.py

# Run an asset with its downstream dependencies
bruin run assets/players.asset.yml --downstream

# Show the lineage for a specific asset
bruin lineage assets/players.asset.yml

# Query the resulting table
bruin query --connection duckdb-default --query "SELECT * FROM dataset.player_stats"
```