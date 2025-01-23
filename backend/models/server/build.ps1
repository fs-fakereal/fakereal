
if (Test-Path ".venv") {
    python -m venv .venv

    .\.venv\Scripts\Activate.ps1

    if ($?) {
        pip install -r requirements

        deactivate
    }

    Write-Host "Finished setting up!"
    Write-Host "Run '. .venv\Scripts\Activate.ps1' to use the local Python."
}
