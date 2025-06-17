import json
from jiwer import wer, cer
import matplotlib.pyplot as plt

# Load JSON file
def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# File paths
ocr_data_path = "../../data/ocr-data/ocr_results.json"
ground_truth_path = "../../data/ocr-data/ground_truth.json"

# Load data
ocr_data = load_json_file(ocr_data_path)
ground_truth = load_json_file(ground_truth_path)

# Per-entry evaluation data storage
names = []
wer_list = []
cer_list = []
wer_acc_list = []
cer_acc_list = []

# =============== Per Entry Evaluation ================
print("=== Per Entry Evaluation ===")
for ocr, gt in zip(ocr_data, ground_truth):
    ocr_texts = [ocr['nama']]
    gt_texts = [gt['nama']]

    for o_j, g_j in zip(ocr['jawaban_essay'], gt['jawaban_essay']):
        ocr_texts.extend([o_j['soal'], o_j['jawaban']])
        gt_texts.extend([g_j['soal'], g_j['jawaban']])

    joined_ocr = " ".join(ocr_texts)
    joined_gt = " ".join(gt_texts)

    entry_wer = wer(joined_gt, joined_ocr)
    entry_cer = cer(joined_gt, joined_ocr)

    names.append(gt['nama'])
    wer_list.append(entry_wer * 100)
    cer_list.append(entry_cer * 100)
    wer_acc_list.append((1 - entry_wer) * 100)
    cer_acc_list.append((1 - entry_cer) * 100)

    print(f"Nama            : ocr: {ocr['nama']} | real: {gt['nama']}")
    print(f"WER             : {entry_wer:.2%}")
    print(f"CER             : {entry_cer:.2%}")
    print(f"WER Accuracy    : {(1 - entry_wer) * 100:.2f}%")
    print(f"CER Accuracy    : {(1 - entry_cer) * 100:.2f}%")
    print("-" * 50)

# =============== Overall Evaluation ================
def extract_all_text(data):
    texts = []
    for entry in data:
        texts.append(entry["nama"])
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

# =============== Chart Visualization ================

# 1. Bar chart per peserta (WER & CER)
x = range(len(names))
plt.figure(figsize=(12, 6))
plt.bar(x, wer_list, width=0.4, label="WER (%)", color="orange")
plt.bar([i + 0.4 for i in x], cer_list, width=0.4, label="CER (%)", color="purple")
plt.xticks([i + 0.2 for i in x], names, rotation=45, ha="right")
plt.ylabel("Error Rate (%)")
plt.title("OCR WER & CER per Peserta")
plt.legend()
plt.tight_layout()
plt.savefig("chart_per_peserta.png")
plt.close()

# 2. Ringkasan Overall WER & CER
plt.figure(figsize=(6, 4))
plt.bar(["WER", "CER"], [overall_wer * 100, overall_cer * 100], color=["orange", "purple"])
plt.ylabel("Error Rate (%)")
plt.title("Overall WER & CER")
plt.tight_layout()
plt.savefig("chart_overall_wer_cer.png")
plt.close()
