## Create and manage a python virtual enviroment

```bash
pip install uv

# navigate to the directory where the python script is

uv init --python 3.13

uv run python -V

uv add pandas pyarrow

# uv is very fast comapred to conda
```

### Running Python script inside a docker container

> First create the **docker file** that will be used to create the **docker container** inside which we will run our *pipeline.py* script.

```Dockerfile
# Choose what to build the image from
FROM python:3.13.11-slim

# Install all libraries used in the pipeline
RUN pip install pandas pyarrow

# Create our working directory and navigate to it inside the container
WORKDIR /code

# Copy the pipeline to the current working directory
COPY pipeline.py ./

ENTRYPOINT ["python","pipeline.py"]
```
> Now create the docker container using the bash command below

```bash
# Build the container image from the dockerfile
docker build -t test:pandas ./ # explanation of the command later

# Run the container image
docker run -it --entrypoint=bash --rm test:pandas # explanation of the command later
```