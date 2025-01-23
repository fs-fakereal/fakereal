#!/bin/sh

model_file=model.py
server_file=file.py

if [ "$1" = "run" ]; then
    source .venv/bin/activate
    if [ "$2" = "$model_file" ]; then
        python $2 $3
    else
        python $2
    fi
    deactivate
    printf "Finished running $1.\n"
    exit
fi

if [ "$1" = "serve" ]; then
    source .venv/bin/activate
    python -m fastapi run $server_file
    deactivate
    printf "Finished running $1.\n"
    exit
fi

if [ "$1" = "install" ]; then
    source .venv/bin/activate
    pip install $2
    deactivate
    printf "Finished installing '$2' package.\n"
    exit
fi


if [[ ( "$1" = "setup" ) && ( ! -d ".venv" ) ]]; then
    python -m venv .venv

    source .venv/bin/activate
    if [ "$?" = "0" ]; then
        pip install -r requirements.txt
        deactivate
    fi
    printf "Finished setting up!\nRun 'source .venv/bin/activate' to use the local python.\n"
fi
