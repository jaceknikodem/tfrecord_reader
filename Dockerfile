FROM grpc/python:0.11
MAINTAINER Jacek Nikodem <jacek.nikodem@gmail.com>

# Install git, and pip.
RUN apt-get update && \
    apt-get install -y git-core software-properties-common python-software-properties python-pip && \
    pip install --upgrade pip

ENV CODE_BASE=/code

COPY . /src
WORKDIR /src

# Install Python libraries.
RUN pip install -r requirements.txt

# Modify git pre-commit hooks.
RUN pre-commit install

CMD /bin/bash
