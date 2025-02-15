
if (!$(Test-Path ".venv")) {
    mkdir .\data

    python -m venv .venv

    . .\.venv\Scripts\Activate.ps1

    if ($?) {
        #pip install sqlalchemy psycopg2 flask flask_cors requests pillow
        pip install -r .\requirements.txt
        deactivate
    }

    Write-Host "Finished setting up!"
    #Write-Host "Run '. .venv\Scripts\Activate.ps1' to use the local Python setup."
}


Write-Host "EXPERIMENTAL: Starting Debug Server!"
. .\.venv\Scripts\Activate.ps1
python -m flask --app .\file-flask.py --debug run

deactivate
