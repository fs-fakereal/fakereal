#!/bin/sh

if [ -d ".venv" ]; then
    python -m venv .venv

    source .venv/bin/activate
    if [ "$?" = "0" ]; then
        pip install -r requirements.txt
        deactivate
    fi
    printf "Finished setting up!\nRun 'source .venv/bin/activate' to use the local python.\n"
fi
