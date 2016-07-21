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

* Run all the tests `run_tests`.

## TODO list a.k.a. feature requests

* <s>Loading a proto definition dynamically</s>.
* <s>Scan the whole project and keep a global DB of protos</s>.
* Reloading the proto DB.
* Tab-completion.
* <s>Selecting sub-fields</s>.
* Value filtering.
* <s>Add limit</s>.
* Add <s>key</s> and size options.
* Add options to write data back to a file (<s>text format</s>, proto).
* Colorful output.
* <s>Globbing support</s>.
* <s>Support for archives</s>.
