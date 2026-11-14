import os
import json
import time
import joblib
import pandas as pd

# =============================================================================
# Projet Big Data : Prédiction du Churn Télécom
# Auteur : Ahmed Channoufi
# =============================================================================

def main():
    print("=== Démarrage du Pipeline Big Data Télécom ===")
    start_time = time.time()

    # 1. Chargement des données de test
    data_path = "data/fevrier_2026.csv"
    print(f"\n[1] Chargement des données depuis : {data_path} ...")
    df = pd.read_csv(data_path)
    print(f"    -> {len(df):,} lignes chargées avec succès.")

    # 2. Chargement de la configuration et des modèles ML
    print("\n[2] Chargement du modèle XGBoost et du Scaler...")
    with open("models/model_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    features = config["features"]
    threshold = config.get("optimal_threshold", 0.5)

    scaler = joblib.load("models/scaler.pkl")
    model = joblib.load("models/xgb_model.pkl")
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
    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)
    parquet_path = os.path.join(output_dir, "predictions_fevrier_2026.parquet")
    
    print(f"\n[5] Sauvegarde des résultats en format Parquet...")
    results.to_parquet(parquet_path, index=False, engine="pyarrow", compression="snappy")
    
    file_size_kb = os.path.getsize(parquet_path) / 1024
    print(f"    -> Fichier généré : {parquet_path} ({file_size_kb:.1f} KB)")

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
