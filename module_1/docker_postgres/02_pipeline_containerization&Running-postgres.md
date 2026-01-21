# Dockerizing the Ingestion Pipeline and Running PostgreSQL on a Container

## Dockerizing the Pipeline

```dockerfile
# base Docker image that we will build on
FROM python:3.13.11-slim

# set up our image by installing prerequisites; pandas in this case
RUN pip install pandas pyarrow

# set up the working directory inside the container
WORKDIR /app
# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["python", "pipeline.py"]
```

Once we have our *Dockerfile* we will create a docker image of that file and run the image.

```bash

docker build -t test:pandas .

docker run -it test:pandas 10 # 10 is the argument being passed to pipeline.py as the entry point of the image is pipeline.py

```

> 10 is the argument being passed to pipeline.py as the entry point of the image is pipeline.py

**Using *uv* as the package manager rather than *pip*.**

```dockerfile

# Start with slim Python 3.13 image
FROM python:3.13.10-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["python", "pipeline.py"]

```

## Running PostgresSQL on a Docker Container

```bash

mkdir ny_taxi_postgres_data

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

```
> -e sets environment variables (user, password, database name)
-v ny_taxi_postgres_data:/var/lib/postgresql creates a named volume
Docker manages this volume automatically
Data persists even after container is removed
Volume is stored in Docker's internal storage
-p 5432:5432 maps port 5432 from container to host
postgres:18 uses PostgreSQL version 18 (latest as of Dec 2025)

```bash

mkdir ny_taxi_postgres_data

# Using a bind mount rather than name mount (-v parameter)

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

```

**Named Volume vs Bind Mount**
Named volume (name:/path): Managed by Docker, easier
Bind mount (/host/path:/container/path): Direct mapping to host filesystem, more control

### Connecting to the Postgres database using *pgcli*

```bash

uv add --dev pgcli # --dev flag marks this as a development dependency (not needed in production). It will be added to the [dependency-groups] section of pyproject.toml instead of the main dependencies section.

# Connect to the database
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

```




