# TensorFlow Record Reader

The project provides a binary that can read and display TF records.


## Development environment

* Get [PyCharm](https://www.jetbrains.com/pycharm/download/) and [Docker](https://docs.docker.com/engine/installation/)

* Go to the project root and start a Docker image
```
sudo docker build -t tfreader .
docker run -v ${PWD}:/code -w /code -i -t tfreader
source .bashrc
```
