from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated
from PIL import Image, UnidentifiedImageError
import base64
import io
import os
import json
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
    PENTING: Sebelum melakukan ekstraksi, periksa apakah gambar ini berisi lembar jawaban essay siswa yang valid.

    Kriteria gambar yang VALID:
    - Terdapat tulisan tangan siswa
    - Ada nama siswa (biasanya ditulis dengan awalan "Nama:" atau "Nama siswa:")
    - Ada soal essay (biasanya ditandai nomor 1., 2., 3., dll)
    - Ada jawaban essay yang ditulis tangan

    Jika gambar TIDAK VALID (bukan lembar jawaban essay), kembalikan JSON berikut:
    {
        "status": "invalid",
        "message": "Gambar yang diunggah bukan lembar jawaban essay yang valid"
    }

    Jika gambar VALID, ekstrak semua tulisan tangan dan ubah ke format JSON berikut:
    {
        "status": "success",
        "data": [
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
    }

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

def validate_gemini_response(response_text: str):
    """Validasi response dari Gemini"""
    try:
        # Coba parse sebagai JSON
        parsed_response = json.loads(response_text)
        
        # Cek apakah response menunjukkan gambar tidak valid
        if parsed_response.get("status") == "invalid":
            return False, parsed_response.get("message", "Gambar tidak valid")
        
        # Cek apakah ada data yang valid
        if parsed_response.get("status") == "success" and parsed_response.get("data"):
            return True, parsed_response
        
        return False, "Response tidak dalam format yang diharapkan"
    
    except json.JSONDecodeError:
        # Jika tidak bisa di-parse sebagai JSON, coba cek apakah ada indikasi error
        if "tidak valid" in response_text.lower() or "bukan lembar jawaban" in response_text.lower():
            return False, "Gambar yang diunggah bukan lembar jawaban essay yang valid"
        
        # Jika response text biasa, kembalikan sebagai legacy format
        return True, {"status": "success", "text": response_text}

@app.post("/imgToText")
async def image_ocr(file: Annotated[UploadFile, File()]):
    try:
        contents = await file.read()

        # Validasi apakah file adalah gambar
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            return JSONResponse(status_code=400, content={
                "error": "File yang diunggah bukan gambar yang valid.",
                "status": "invalid_file"
            })

        # Validasi ukuran file (optional)
        if len(contents) > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse(status_code=400, content={
                "error": "Ukuran file terlalu besar. Maksimal 10MB.",
                "status": "file_too_large"
            })

        extracted_text = extract_text_from_image(image)
        
        # Validasi response dari Gemini
        is_valid, result = validate_gemini_response(extracted_text)
        
        if not is_valid:
            return JSONResponse(status_code=400, content={
                "error": result,
                "status": "invalid_content"
            })

        return JSONResponse(content={
            "status": "success",
            "result": result
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": f"Terjadi kesalahan server: {str(e)}",
            "status": "server_error"
        })