import os
import urllib.request
import json
import base64

BASE_DIR = r"c:\Big_data_project"
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

REPO_RAW_BASE = "https://raw.githubusercontent.com/AhmedChannoufii/Customer-Churn-Prediction/master"

FILES_TO_DOWNLOAD = [
    # Models
    ("models/model_config.json", os.path.join(MODELS_DIR, "model_config.json")),
    ("models/scaler.pkl", os.path.join(MODELS_DIR, "scaler.pkl")),
    ("models/xgb_model.pkl", os.path.join(MODELS_DIR, "xgb_model.pkl")),
    # Test Data (Fevrier 2026 dataset - evaluation/test data)
    ("data/processed/fevrier_2026.csv", os.path.join(DATA_DIR, "fevrier_2026.csv")),
    ("data/processed/cible_churn_F.csv", os.path.join(DATA_DIR, "cible_churn_F.csv")),
]

for repo_path, local_path in FILES_TO_DOWNLOAD:
    url = f"{REPO_RAW_BASE}/{repo_path}"
    print(f"Downloading {repo_path} -> {local_path} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp, open(local_path, "wb") as f:
            f.write(resp.read())
        size_kb = os.path.getsize(local_path) / 1024
        print(f"  OK ({size_kb:.1f} KB)")
    except Exception as e:
        print(f"  ERROR: {e}")

print("Download completed!")
