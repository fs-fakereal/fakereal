import model
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
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
    return {"Hello": "World"}

@app.post('/upload')
async def _file_upload(files: list[UploadFile] = File(...),
                 uid: str = Form(...),
                 userUid: str = Form(...),
                 url: str = Form(...),
                 ):
    if not file:
        return JSONResponse(content={"error": "No files selected"}, status_code=400)

    fileRatings = []
    for file in files:
        result = model.parse_check(model.check_media(file.filename))
        fileRatings.append(result)

    return JSONResponse(content={
        "message": "Files uploaded and scanned", "result": fileRatings,
        "uid": uid,
        "userUid": userUid,
        "url": url
        })

