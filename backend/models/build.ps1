
if (Test-Path ".venv") {
    python -m venv .venv

    . .\.venv\Scripts\Activate.ps1

    if ($?) {
        pip install psycopg2 sqlachemy flask flask_cors
        deactivate
    }

    Write-Host "Finished setting up!"
    Write-Host "Run '. .venv\Scripts\Activate.ps1' to use the local Python setup."
}
