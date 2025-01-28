import json

import model
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

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

@app.get("/")
def read_hello():
    return {"message": "Hello World!"}

@app.post('/upload')
async def _file_upload(file: UploadFile = File(...),
                 uid: list[str] = Form(...),
                 # userUid: str = Form(...),
                 # url: str = Form(...),
                 ):
    if not file:
        return JSONResponse(content={"error": "No files selected"}, status_code=400)

    result = model.parse_check(model.check_media(file.filename))

    return JSONResponse(content={
        "result": result,
        "uid": uid,
        # "userUid": userUid,
        # "url": url
        }, status_code=200)

