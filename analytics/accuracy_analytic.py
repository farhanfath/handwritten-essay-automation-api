import json
from jiwer import wer, cer

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

ocr_data_path = "data/ocr-data/ocr_results.json"
ground_truth_path = "data/ocr-data/ground_truth.json"

ocr_data = load_json_file(ocr_data_path)
ground_truth = load_json_file(ground_truth_path)

def extract_all_text(data):
    texts = []
    for entry in data:
        for item in entry["jawaban_essay"]:
            texts.append(item["soal"])
            texts.append(item["jawaban"])
    return " ".join(texts)

ocr_text = extract_all_text(ocr_data)
gt_text = extract_all_text(ground_truth)

print(f"WER SCORE: {wer(gt_text, ocr_text):.2%}")
print(f"CER SCORE: {cer(gt_text, ocr_text):.2%}")

wer_score = wer(gt_text, ocr_text)
cer_score = cer(gt_text, ocr_text)

wer_accuracy = (1 - wer_score) * 100
cer_accuracy = (1 - cer_score) * 100

print(f"OCR Accuracy based on WER : {wer_accuracy:.2f}%")
print(f"OCR Accuracy based on CER : {cer_accuracy:.2f}%")
