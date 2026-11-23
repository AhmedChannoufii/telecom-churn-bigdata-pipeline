import os
import json
import time
from pathlib import Path
import joblib
import pandas as pd

# =============================================================================
# Projet Big Data : Prédiction du Churn Télécom
# Auteur : Ahmed Channoufi
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    print("=== Démarrage du Pipeline Big Data Télécom ===")
    start_time = time.time()

    # 1. Chargement des données de test
    data_path = BASE_DIR / "data" / "fevrier_2026.csv"
    print(f"\n[1] Chargement des données depuis : {data_path.name} ...")
    if not data_path.exists():
        print(f"[ERREUR] Fichier introuvable : {data_path}")
        return

    df = pd.read_csv(data_path)
    print(f"    -> {len(df):,} lignes chargées avec succès.")

    # 2. Chargement de la configuration et des modèles ML
    print("\n[2] Chargement du modèle XGBoost et du Scaler...")
    config_path = BASE_DIR / "models" / "model_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    features = config["features"]
    threshold = config.get("optimal_threshold", 0.5)

    scaler = joblib.load(BASE_DIR / "models" / "scaler.pkl")
    model = joblib.load(BASE_DIR / "models" / "xgb_model.pkl")
    print(f"    -> Modèle chargé avec {len(features)} features (Seuil: {threshold})")

    # 3. Préparation des variables (Features)
    print("\n[3] Alignement des features...")
    X = df[features].fillna(0)

    # 4. Inférence (Prédiction du Churn)
    print("\n[4] Calcul des prédictions de Churn...")
    t0 = time.time()
    X_scaled = scaler.transform(X)
    probabilities = model.predict_proba(X_scaled)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    print(f"    -> Inférence terminée en {time.time() - t0:.2f} secondes.")

    # 5. Création du tableau de résultats
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

    # Ajout de quelques colonnes pour l'analyse
    for col in ["ANC_M", "STATUT", "internet_m0", "montant_recharge_m0", "appels_sortants_m0"]:
        if col in df.columns:
            results[col] = df[col]

    # 6. Sauvegarde au format Parquet (Big Data Storage)
    output_dir = BASE_DIR / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / "predictions_fevrier_2026.parquet"
    
    print(f"\n[5] Sauvegarde des résultats en format Parquet...")
    results.to_parquet(parquet_path, index=False, engine="pyarrow", compression="snappy")
    
    file_size_kb = os.path.getsize(parquet_path) / 1024
    print(f"    -> Fichier généré : {parquet_path.name} ({file_size_kb:.1f} KB)")

    # 7. Résumé
    nb_churn = int(predictions.sum())
    taux_churn = (nb_churn / len(df)) * 100
    print("\n=== Résumé de l'Exécution ===")
    print(f"Total clients : {len(df):,}")
    print(f"Clients Churn prédits : {nb_churn:,} ({taux_churn:.2f}%)")
    print(f"Clients Fidèles : {len(df) - nb_churn:,} ({100 - taux_churn:.2f}%)")
    print(f"Temps total : {time.time() - start_time:.2f} secondes")
    print("================================")

if __name__ == "__main__":
    main()
