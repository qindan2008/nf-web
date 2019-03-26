FROM ubuntu:18.04

# Let's start with some basic stuff.
RUN apt-get update && apt-get install -y \
    curl \
    python3-pip

# Install Docker from Docker Inc. repositories.
RUN curl -fsSL get.docker.com | sh

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy over source code
COPY tests ./tests
COPY run.sh ./

CMD ls
