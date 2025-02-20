#!/bin/sh

if [ ! -d ".venv" ]; then
    mkdir -p data

    python -m venv .venv

    source .venv/bin/activate
    if [ "$?" = "0" ]; then
        pip install -r requirements.txt
        deactivate
    fi
    printf "Finished setting up!\n"
fi

echo "EXPERIMENTAL: Starting Debug Server!"
source .venv/bin/activate
python -m flask --app ./file-flask.py --debug run

deactivate
