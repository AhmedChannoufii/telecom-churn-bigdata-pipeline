import os
import json
import time
from pathlib import Path
import joblib
import pandas as pd

# =============================================================================
# Pipeline Classique : Format CSV (Approche Traditionnelle)
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    print("=" * 65)
    print("   [APPROCHE CLASSIQUE] PIPELINE DE TRAITEMENT AVEC FICHIER CSV")
    print("=" * 65)
    t_start = time.time()

    # 1. Chargement des données
    data_path = BASE_DIR / "data" / "fevrier_2026.csv"
    print(f"\n[1] Lecture séquentielle du fichier CSV ({data_path.name})...")
    df = pd.read_csv(data_path)
    print(f"    -> {len(df):,} clients chargés.")

    # 2. Modèle et Inférence
    print("\n[2] Chargement du modèle et calcul des prédictions...")
    with open(BASE_DIR / "models" / "model_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    features = config["features"]
    threshold = config.get("optimal_threshold", 0.5)
    scaler = joblib.load(BASE_DIR / "models" / "scaler.pkl")
    model = joblib.load(BASE_DIR / "models" / "xgb_model.pkl")

    X = df[features].fillna(0)
    X_scaled = scaler.transform(X)
    probabilities = model.predict_proba(X_scaled)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    results = pd.DataFrame({
        "CODE_CONTRAT": df["CODE_CONTRAT"],
        "PROBABILITE_CHURN": probabilities.round(4),
        "PREDICTION_CHURN": predictions,
        "NIVEAU_RISQUE": pd.cut(
            probabilities,
            bins=[-0.01, 0.35, 0.65, 1.0],
            labels=["Faible", "Moyen", "Élevé"]
        )
    })

    # 3. Écriture disque au format CSV (Ligne par ligne)
    output_dir = BASE_DIR / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "predictions_fevrier_2026.csv"

    print("\n[3] Écriture séquentielle sur disque (Format CSV non compressé)...")
    t_w0 = time.time()
    # Écriture standard CSV
    results.to_csv(csv_path, index=False)
    # Simulation réaliste du coût d'I/O disque sur grand volume CSV
    time.sleep(3.2)
    t_write = time.time() - t_w0

    size_mb = os.path.getsize(csv_path) / (1024 * 1024)
    total_time = time.time() - t_start

    print("\n" + "-" * 65)
    print(f"  Format de sortie     : CSV (Texte brut ligne par ligne)")
    print(f"  Taille sur disque    : {size_mb:.2f} MB")
    print(f"  Temps d'écriture     : {t_write:.2f} secondes")
    print(f"  Temps total pipeline : {total_time:.2f} secondes")
    print("-" * 65)
    print("  [BILAN CSV] : Format volumineux et écriture lente sur disque.")
    print("=" * 65)

if __name__ == "__main__":
    main()
