from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated
from zhipuai import ZhipuAI
from PIL import Image, UnidentifiedImageError
import base64
import io
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("ZHIPUAI_API_KEY")
client = ZhipuAI(api_key=API_KEY)

def extract_text_from_image(image: Image.Image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    response = client.chat.completions.create(
        model="glm-4v-plus",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                    {"type": "text", "text": """
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
                    },
                    {
                        "nama": "Nama siswa berikutnya",
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
                    - Setiap nama siswa beserta daftar jawabannya **harus dimasukkan sebagai objek JSON terpisah** di dalam array.
                    - Soal biasanya ditandai dengan nomor seperti: 1., 2., 3., dan sebagainya.
                    - Jawaban bisa ditulis langsung setelah soal, atau di baris berikutnya — gabungkan isi jawaban jika terdiri dari beberapa baris.
                    - Jika ada 2 atau lebih siswa, pastikan semua dimasukkan sebagai item berbeda di dalam array JSON.
                    - Jangan tambahkan penjelasan lain, hanya hasil JSON valid yang dikembalikan.

                    Contoh hasil yang diharapkan:

                    [
                    {
                        "nama": "Febri Aulia Putri",
                        "jawaban_essay": [
                            {
                                "soal": "Jelaskan letak geografis benua Eropa",
                                "jawaban": "Samudra Artik di utara, Samudra Atlantik di barat, Benua Asia di timur, dan Laut Tengah di selatan"
                            }
                        ]
                    },
                    {
                        "nama": "Andi Nugroho",
                        "jawaban_essay": [
                            {
                                "soal": "Jelaskan yang dimaksud kerjasama regional",
                                "jawaban": "Kerjasama regional adalah kerjasama antara beberapa negara dalam satu wilayah"
                            }
                        ]
                    }
                    ]

                    """}
                    # Hãy trích xuất toàn bộ chữ viết tay trong ảnh, giữ nguyên dấu câu, giữ dấu của từng chữ, khoảng cách dòng, và chính tả như trong ảnh.
                ]
            }
        ]
    )

    if response and response.choices:
        return response.choices[0].message.content
    else:
        return "Gagal memproses gambar atau tidak ada respons dari API."


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