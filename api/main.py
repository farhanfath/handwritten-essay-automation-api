from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated
from PIL import Image, UnidentifiedImageError
import base64
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def extract_text_from_image(image: Image.Image):
    # Convert PIL image to byte stream
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()

    prompt = """
    Ekstrak semua tulisan tangan dalam gambar, lalu ubah ke format JSON seperti berikut:

    [
    {
        "nama": "Nama siswa",
        "jawaban_essay": [
            {
                "soal": "Isi soal lengkap",
                "jawaban": "Isi jawaban lengkap"
            }
        ]
    }
    ]

    Petunjuk penting:
    - Nama siswa biasanya ditulis dengan awalan seperti: **"Nama: ..."** atau **"Nama siswa: ..."**.
    - Soal biasanya ditandai dengan nomor seperti: 1., 2., 3., dan sebagainya.
    - Jangan tambahkan penjelasan lain, hanya hasil JSON valid yang dikembalikan.
    """

    try:
        response = model.generate_content([
            prompt,
            Image.open(io.BytesIO(image_bytes))
        ])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/imgToText")
async def image_ocr(file: Annotated[UploadFile, File()]):
    try:
        contents = await file.read()

        # Validasi apakah file adalah gambar
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            return JSONResponse(status_code=400, content={"error": "File yang diunggah bukan gambar yang valid."})

        extracted_text = extract_text_from_image(image)
        return JSONResponse(content={"text": extracted_text})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
