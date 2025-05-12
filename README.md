
# fakereal

## Requirements
- Python <=3.12

## Setup

### Clone the repo:
```sh
git clone https://github.com/fs-fakereal/fakereal
cd ./fakereal
```

### Setup the virtual environment:
```sh
python -m venv .venv

# linux
source ./.venv/bin/activate

# windows
. ./.venv/bin/activate.ps1

# install all the python package dependencies
pip install -r requirements.txt
```

A .flaskenv is required to be accessible in the root directory to run the server.

Either use the provided .flaskenv, or provide the required environment variables for
(A template has been provided for convenience within the root directory):
- PostgresSQL
- News API
- GenAI API


### To run the site
Navigate to the root directory and activate your virtual environment, then run this command:
```sh
flask run
```
The project will now be running on http://localhost:5000.
