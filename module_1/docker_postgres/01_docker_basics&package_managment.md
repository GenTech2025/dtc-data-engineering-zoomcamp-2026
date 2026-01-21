# Docker Commands and Test ingestion python script

## Docker commands

```bash
docker --version

docker run hello-world

docker run -it ubuntu

docker ps -a

docker rm `docker ps -aq`

docker run -it --rm ubuntu

docker run -it --rm python:3.9.16
# add -slim to get a smaller version

docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.9.16-slim

##### VOLUMES ##########

mkdir test
cd test
touch file1.txt file2.txt file3.txt
echo "Hello from host" > file1.txt
cd ..
```

```python
# Simple script to list all the files in the current directory

from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"Files in {current_dir}:")

for filepath in current_dir.iterdir():
    if filepath.name == current_file:
        continue

    print(f"  - {filepath.name}")

    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"    Content: {content}")


```

```bash
# Map the directory to the container
docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \
    --entrypoint=bash \
    python:3.9.16-slim

# Run the command below inside the container and we will get the files returned from the host machine

cd /app/test
ls -la
cat file1.txt
python list_files.py
```

## Test ingestion python script and package management using ***uv*** package manager

```python

# pipeline.py
import sys
import pandas as pd

print("arguments", sys.argv)

day = int(sys.argv[1])
print(f"Running pipeline for day {day}")

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")

```
<br\>

Since we need **pandas** but dont want to install it globally on our system we will use **uv** package manager which is a new and fast Python package and project manager that is written in Rust

```bash
pip install uv

uv init --python=3.13 #initializes a python project with pyproject.toml and .python-version fle


uv run which python  # Python in the virtual environment
uv run python -V

which python        # System Python
python -V

##### Adding python libraries through uv ###########

uv add pandas pyarrow


# Now execute the pipeline.py script using uv python

uv run python pipeline.py 10 # 10 is the argument provided to the script since it expects one.
```








