# climate-data-plotly Container
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Update OS package list and install git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# Copy the Python pip requirements file
COPY requirements/requirements.txt requirements/requirements.txt

# Upgrade pip and install requirements from the requirements file
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements/requirements.txt && \
    rm -rf requirements

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

COPY /app /app

# List exposure of port 8088 for Flask
EXPOSE 8088/TCP

# Start the bash prompt
CMD ["/bin/bash"]
