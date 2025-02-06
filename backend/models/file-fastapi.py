import hashlib
import json
from typing import Optional

import model
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
DEBUG = True

# NOTE(liam): specify site(s) that can connect here.
origins = [
        "http://localhost:8080",
        "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recent_results = {}

@app.get("/")
def read_hello():
    return {"message": "Hello World!"}

@app.post('/upload')
async def _file_upload(file: UploadFile = File(...),
                       force_scan: Optional[str] = Form('false')):
    try:
        contents = file.file.read()
        hash = hashlib.sha256(contents).hexdigest()

        if hash in recent_results.keys() and \
                force_scan.lower() == 'false':
            # TODO(liam): also force scan if timestamp shows last scan
            # as being more than 24 hours.
            if DEBUG:
                print("INFO: HASH FOUND. RESTORING PREVIOUS RESULT.")
            result = recent_results[hash]
        else:
            if DEBUG:
                print("INFO: SENDING IMAGE TO MODEL.")

            result = model.parse_check(model.check_media(file.filename))
            recent_results[hash] = result

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    finally:
        if DEBUG:
            print("INFO: FINISHED PROCESSING. RETURNING TO CLIENT.")
        file.file.close()

    return JSONResponse(content={
        "hash": hash,
        "result": result,
        }, status_code=200)

