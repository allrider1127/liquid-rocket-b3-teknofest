# THIS LINE IS MANDATORY
FROM python:3.10-slim

# Install system dependencies for NASA CEA and RocketCEA
RUN apt-get update && apt-get install -y \
    gfortran \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install the engineering stack
RUN pip install --no-cache-dir \
    rocketcea \
    numpy \
    scipy \
    matplotlib \
    pandas \
    rocketprops

# Set the working directory
WORKDIR /app

# Copy EVERYTHING from your local project folder to the container
COPY . .

# By default, open a bash shell
CMD ["/bin/bash"]
