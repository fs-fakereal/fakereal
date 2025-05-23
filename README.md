
# FakeReal
FakeReal is an **extension/addon** and **web service** for the public to detect and inform themselves 
about deep fakes.

Deep fakes are a relatively new concept and have been growing every day. Deep fakes
generate fake videos, photos, and audios. This development makes it possible for individuals to
not only develop fake materials of a person, but to impersonate a person. Other deep fake
identifiers software caters to companies or are paid to use. This makes it difficult for people who
do not have the funds or the general public to detect deep fakes, as well as learning about deep
fakes. 

FakeReal wants to make it easier and more accessible for the public to use deep fake
identification as well as gather more insight on what deep fake is. We will use a website to host
our identification application and gather information about deep fakes.

## Requirements
- Python <=3.12
- News API key
- GenAI API key
- PostgresSQL Database

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
the following (note: a template has been provided for convenience within the root directory):
- PostgresSQL
- News API
- GenAI API


### To run the site:
Navigate to the root directory and activate your virtual environment, then run this command:
```sh
flask run
```
The project will now be running on http://localhost:5000.

### To run Browser extension:
Go to google and in the top right click the three dots. Then go to extensions and click manage extensions. 

Once in extension screen click load unpack and in the FakeReal files locate:

Chrome-Extension-BoilerPlate

Select the folder and now the FakeReal extension will be in your extension list

You can then open a new web window and click the extension icon and tab the FakeReal extension to view and run.
