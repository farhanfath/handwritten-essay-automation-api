import json
from jiwer import wer, cer

# Fungsi untuk load JSON dari file
def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

ocr_data_path = "data/ocr-data/ocr_results.json"
ground_truth_path = "data/ocr-data/ground_truth.json"

ocr_data = load_json_file(ocr_data_path)
ground_truth = load_json_file(ground_truth_path)

# Hitung WER dan CER per entry
for ocr, gt in zip(ocr_data, ground_truth):
    nama_wer = wer(gt['nama'], ocr['nama'])
    for o_j, g_j in zip(ocr['jawaban_essay'], gt['jawaban_essay']):
        soal_wer = wer(g_j['soal'], o_j['soal'])
        soal_cer = cer(g_j['soal'], o_j['soal'])
        jawab_wer = wer(g_j['jawaban'], o_j['jawaban'])
        jawab_cer = cer(g_j['jawaban'], o_j['jawaban'])
        
        print(f"Nama     : {ocr['nama']}")
        print(f"Nama WER: {nama_wer:.2%}")
        print(f"Soal WER : {soal_wer:.2%}")
        print(f"Soal CER : {soal_cer:.2%}")
        print(f"Jawab WER: {jawab_wer:.2%}")
        print(f"Jawab CER: {jawab_cer:.2%}")
        print()
