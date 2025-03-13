
# fakereal

## Setup

### To set up the python virtual environment:
Navigate to the root directory containing the project and run the following:
```sh
git clone https://github.com/fs-fakereal/fakereal
cd ./fakereal

# ensure python version is 3.12.* (required by tensorflow)
pyenv install 3.12
pyenv local 3.12

python -m venv .venv

# linux
source ./.venv/bin/activate

# windows
. ./.venv/bin/activate.ps1

# install all the python package dependencies
pip install -r requirements.txt

# if on a terminal, run this to turn off virtual environment.
deactivate
```
Make sure to place the provided .flaskenv file in the root directory.

### To run the site
Navigate to the root directory and activate your virtual environment, then run this command:
```sh
flask run
```
The project will now be running on localhost.
