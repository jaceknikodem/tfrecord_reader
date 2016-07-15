HISTCONTROL=ignoreboth

shopt -s histappend
shopt -s cmdhist

HISTSIZE=100000
HISTFILESIZE=500000

export PYTHONPATH='.'

run_tests () {
    python -m unittest discover -s $1 -p '*_test.py'
}

generate_grpc () {
    python -m grpc.tools.protoc --proto_path=. --python_out=. --grpc_python_out=. *.proto
}

alias tfreader="python /code/src/prototype_main.py"
