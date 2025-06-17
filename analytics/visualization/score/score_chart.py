import json
import matplotlib.pyplot as plt
import numpy as np

# Load JSON
def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Hitung MAE dan siapkan data
def compute_mae_data(predicted, ground_truth):
    errors = []
    for pred, true in zip(predicted, ground_truth):
        errors.append(abs(pred['skor_akhir'] - true['skor_akhir']))
    mae = sum(errors) / len(errors) if errors else 0
    return mae, errors

# Load data
ai = load_json("../../data/score-data/score_ai_results.json")
kj = load_json("../../data/score-data/score_kj_results.json")
gt = load_json("../../data/score-data/score_ground_truth.json")

# Nama-nama
labels = [item['nama'] for item in gt]
gt_scores = [item['skor_akhir'] for item in gt]
ai_scores = [item['skor_akhir'] for item in ai]
kj_scores = [item['skor_akhir'] for item in kj]

# Hitung MAE
mae_ai, error_ai = compute_mae_data(ai, gt)
mae_kj, error_kj = compute_mae_data(kj, gt)

# 1. Bar chart per siswa
x = np.arange(len(labels))  # label index
width = 0.25

plt.figure(figsize=(12, 6))
plt.bar(x - width, gt_scores, width, label='Ground Truth', color='gray')
plt.bar(x, ai_scores, width, label='AI Prediction', color='blue')
plt.bar(x + width, kj_scores, width, label='KJ Prediction', color='green')

plt.ylabel('Skor Akhir')
plt.title('Perbandingan Skor Akhir per Siswa')
plt.xticks(x, labels, rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.grid(axis='y')
plt.savefig("perbandingan_skor.png")  # Simpan chart ke file
plt.close()  # Tutup figure

# MAE chart
plt.figure(figsize=(6, 4))
plt.bar(['AI', 'KJ'], [mae_ai, mae_kj], color=['blue', 'green'])
plt.ylabel('MAE')
plt.title('Mean Absolute Error (MAE) vs Ground Truth')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("mae_chart.png")  # Simpan chart ke file
plt.close()
