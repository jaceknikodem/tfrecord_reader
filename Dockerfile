FROM gcr.io/tensorflow/tensorflow
MAINTAINER Jacek Nikodem <jacek.nikodem@gmail.com>

# Install git, and pip.
RUN apt-get update && apt-get install -y git-core software-properties-common python-software-properties python-pip

# Install Java.
RUN apt-get install -y debconf-utils && \
    add-apt-repository -y ppa:webupd8team/java  && \
    apt-get update  && \
    echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections  && \
    apt-get install -y oracle-java8-installer

# Install Bazel.
RUN echo "deb http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list && \
    curl https://storage.googleapis.com/bazel-apt/doc/apt-key.pub.gpg | sudo apt-key add -
RUN apt-get update && sudo apt-get install -y bazel && sudo apt-get upgrade -y bazel

ENV CODE_BASE=/code

COPY . /src
WORKDIR /src

# Install Python libraries.
RUN pip install -r requirements.txt

# Modify git pre-commit hooks.
RUN pre-commit install

CMD /bin/bash