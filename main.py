from typing import Annotated
from fastapi import FastAPI, File

app = FastAPI()

@app.get("/")
def sample_root():
    return {"Hello": "World"}

@app.post("/imgToText")
async def image_ocr(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}