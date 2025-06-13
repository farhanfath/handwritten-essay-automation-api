import json

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_mae_percentage(predicted_list, ground_truth_list):
    errors_percent = []
    for pred, true in zip(predicted_list, ground_truth_list):
        true_score = true['skor_akhir']
        pred_score = pred['skor_akhir']
        if true_score == 0:
            continue  # skip if ground truth is 0 to avoid division by zero
        error_pct = abs(pred_score - true_score) / true_score * 100
        errors_percent.append(error_pct)
    mae_pct = sum(errors_percent) / len(errors_percent) if errors_percent else 0
    accuracy_pct = 100 - mae_pct
    return mae_pct, accuracy_pct

# Load data
# ai = load_json("data/score-data/score_ai_results.json")
kj = load_json("data/score-data/score_kj_results.json")
gt = load_json("data/score-data/score_ground_truth.json")

# Hitung MAE% dan akurasi
# mae_pct_ai, acc_ai = calculate_mae_percentage(ai, gt)
mae_pct_kj, acc_kj = calculate_mae_percentage(kj, gt)

# print(f"AI vs GT → MAE%: {mae_pct_ai:.2f}%, Accuracy: {acc_ai:.2f}%")
print(f"KJ vs GT → MAE%: {mae_pct_kj:.2f}%, Accuracy: {acc_kj:.2f}%")
