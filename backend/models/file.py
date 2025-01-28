import json

import model
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

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
async def _file_upload(files: list[UploadFile] = File(...),
                 # uid: list[str] = Form(...),
                 # userUid: str = Form(...),
                 # url: str = Form(...),
                 ):
    if not files:
        return JSONResponse(content={"error": "No files selected"}, status_code=400)

    fileRatings = []
    for file in files:
        result = model.parse_check(model.check_media(file.filename))
        fileRatings.append(result)

    return JSONResponse(content={
        "message": "Files uploaded and scanned", "result": fileRatings,
        # "uid": uid,
        # "userUid": userUid,
        # "url": url
        })

