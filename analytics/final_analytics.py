import json
from jiwer import wer, cer

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

ocr_data_path = "data/ocr-data/ocr_results.json"
ground_truth_path = "data/ocr-data/ground_truth.json"

ocr_data = load_json_file(ocr_data_path)
ground_truth = load_json_file(ground_truth_path)

# =============== Per Entry Evaluation ================
print("=== Per Entry Evaluation ===")
for ocr, gt in zip(ocr_data, ground_truth):
    ocr_texts = []
    gt_texts = []

    for o_j, g_j in zip(ocr['jawaban_essay'], gt['jawaban_essay']):
        ocr_texts.append(o_j['soal'])
        ocr_texts.append(o_j['jawaban'])
        gt_texts.append(g_j['soal'])
        gt_texts.append(g_j['jawaban'])

    joined_ocr = " ".join(ocr_texts)
    joined_gt = " ".join(gt_texts)

    entry_wer = wer(joined_gt, joined_ocr)
    entry_cer = cer(joined_gt, joined_ocr)

    print(f"Nama            : {ocr['nama']}")
    print(f"WER             : {entry_wer:.2%}")
    print(f"CER             : {entry_cer:.2%}")
    print(f"WER Accuracy    : {(1 - entry_wer) * 100:.2f}%")
    print(f"CER Accuracy    : {(1 - entry_cer) * 100:.2f}%")
    print("-" * 50)

# =============== Overall Evaluation ================
def extract_all_text(data):
    texts = []
    for entry in data:
        for item in entry["jawaban_essay"]:
            texts.append(item["soal"])
            texts.append(item["jawaban"])
    return " ".join(texts)

ocr_text = extract_all_text(ocr_data)
gt_text = extract_all_text(ground_truth)

overall_wer = wer(gt_text, ocr_text)
overall_cer = cer(gt_text, ocr_text)
overall_wer_accuracy = (1 - overall_wer) * 100
overall_cer_accuracy = (1 - overall_cer) * 100

print("\n=== Overall Evaluation ===")
print(f"Total WER Score           : {overall_wer:.2%}")
print(f"Total CER Score           : {overall_cer:.2%}")
print(f"Total OCR WER Accuracy    : {overall_wer_accuracy:.2f}%")
print(f"Total OCR CER Accuracy    : {overall_cer_accuracy:.2f}%")
