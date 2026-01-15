# Choose what to build the image from
FROM python:3.13.11-slim

# Install all libraries used in the pipeline
RUN pip install pandas pyarrow

# Create our working directory and navigate to it inside the container
WORKDIR /code

# Copy the pipeline to th current working directory
COPY pipeline.py .

ENTRYPOINT ["python","pipeline.py"]

# BASH: docker run -it --rm test:pandas 12, 12 is the parameter for pipeline.py since the entry point is pipeline.py