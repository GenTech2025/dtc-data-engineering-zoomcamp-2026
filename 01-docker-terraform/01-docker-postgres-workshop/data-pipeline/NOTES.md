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


### Transforming and Inserting Data into Postgres SQL database

First download the taxi csv dataset from DTC and then transform it and create a sql connection to our postgres database using *sqlalchemy* library. Once connection is extablished we will insert the contents of the csv file into our database in chunks (so that we dont overload our memory). <br/>
    Once we have finished exploring our data in the jupyter notebook we will convert it into script using the following bash command.

```bash
#!/bin/bash
uv run jupyter nbconvert --to=script notebook.ipynb
```

Once the script has been created, we can improve the script by parametizing it for different months and year for the taxi trip data and use *click* python library to create cli parameters that can be passed while executing the script from the command line.

### Create a dockerized data container

* One docker container running the postgres database
* Another docker container which will actually run the ingestion script
* Put both the containers under the same docker network by setting up a docker network
* A third docker container will run **PgAdmin** to manage our postgres database
* Use **Docker Compose** to run all these containers with ease, all containers in a docker compose file run on the same network.

```bash
# Navigate to the docker-compose yaml file and execute the command below
docker-compose up
```


