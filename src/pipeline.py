"""
=============================================================================
PIPELINE BIG DATA : PRÉDICTION DU CHURN CLIENTS TÉLÉCOM
=============================================================================
Auteur : Ahmed Channoufi
Projet : telecom-churn-bigdata-pipeline

Ce script représente le moteur de traitement Big Data (ETL + Machine Learning) :
1. Configuration de l'environnement (Java, OpenJDK, PySpark)
2. Ingestion des données volumineuses de test (fevrier_2026.csv)
3. Traitement et sélection des 46 features temporelles
4. Inférence du modèle Machine Learning (XGBoost pré-entraîné)
5. Persistance optimisée au format Parquet (Data Lake)
=============================================================================
"""

import os
import sys
import time
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Configuration des Chemins et Environnement
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "data" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuration automatique du JDK si présent
JDK_PATH = r"C:\Program Files\Android\openjdk\jdk-21.0.8"
if os.path.exists(JDK_PATH) and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = JDK_PATH
    os.environ["PATH"] = f"{JDK_PATH}\\bin;" + os.environ.get("PATH", "")

# Chemins des artefacts
MODEL_CONFIG_PATH = MODELS_DIR / "model_config.json"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
XGB_MODEL_PATH = MODELS_DIR / "xgb_model.pkl"
INPUT_DATA_PATH = DATA_DIR / "fevrier_2026.csv"
OUTPUT_PARQUET_PATH = OUTPUT_DIR / "predictions_fevrier_2026.parquet"
OUTPUT_SUMMARY_PATH = OUTPUT_DIR / "churn_summary.json"


def load_artifacts():
    """Charge la configuration du modèle, le scaler et le modèle XGBoost."""
    print("[1/5] Chargement des artefacts de Machine Learning...")
    if not MODEL_CONFIG_PATH.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {MODEL_CONFIG_PATH}")
    
    with open(MODEL_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    features = config.get("features", [])
    threshold = float(config.get("optimal_threshold", 0.5))
    
    print(f"      • Modèle configuré pour {len(features)} features")
    print(f"      • Seuil de décision optimal : {threshold}")
    
    scaler = joblib.load(SCALER_PATH)
    model = joblib.load(XGB_MODEL_PATH)
    print("      • Scaler et Modèle XGBoost chargés avec succès.")
    
    return features, threshold, scaler, model


def run_pipeline():
    start_total_time = time.time()
    print("=" * 70)
    print("      DÉMARRAGE DU PIPELINE BIG DATA : TÉLÉCOM CHURN PREDICTION")
    print("=" * 70)
    
    # 1. Chargement des modèles
    features, threshold, scaler, model = load_artifacts()
    
    # 2. Ingestion des données de test
    print(f"\n[2/5] Ingestion des données massives de test : {INPUT_DATA_PATH.name}...")
    start_read = time.time()
    
    if not INPUT_DATA_PATH.exists():
        raise FileNotFoundError(f"Données de test introuvables : {INPUT_DATA_PATH}")
    
    df = pd.read_csv(INPUT_DATA_PATH)
    read_time = time.time() - start_read
    
    nb_clients = len(df)
    taille_mo = INPUT_DATA_PATH.stat().st_size / (1024 * 1024)
    print(f"      • {nb_clients:,} clients chargés ({taille_mo:.2f} MB) en {read_time:.2f} secondes.")
    
    # 3. Préparation des Features
    print("\n[3/5] Extraction et alignement des 46 variables comportementales...")
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        print(f"      [ATTENTION] {len(missing_features)} variables manquantes remplies par 0.")
        for f in missing_features:
            df[f] = 0.0

    X = df[features].copy()
    X = X.fillna(0.0)

    # 4. Inférence Distribuée / Scaled Inference
    print(f"\n[4/5] Exécution de la prédiction du Churn pour {nb_clients:,} clients...")
    start_pred = time.time()
    
    # Normalisation
    X_scaled = scaler.transform(X)
    
    # Prédiction des probabilités
    probabilities = model.predict_proba(X_scaled)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    
    pred_time = time.time() - start_pred
    print(f"      • Inférence terminée en {pred_time:.2f} secondes.")
    print(f"      • Cadence de traitement : {nb_clients / pred_time:,.0f} clients/seconde.")
    
    # Enrichissement du DataFrame résultat
    results_df = pd.DataFrame({
        "CODE_CONTRAT": df["CODE_CONTRAT"] if "CODE_CONTRAT" in df.columns else np.arange(nb_clients),
        "PROBABILITE_CHURN": np.round(probabilities, 4),
        "PREDICTION_CHURN": predictions,
        "NIVEAU_RISQUE": pd.cut(
            probabilities,
            bins=[-0.01, 0.35, 0.65, 1.0],
            labels=["Faible", "Moyen", "Élevé"]
        )
    })
    
    # Conserver quelques métriques clés pour le dashboard
    for col in ["ANC_M", "STATUT", "appels_sortants_m0", "internet_m0", "montant_recharge_m0"]:
        if col in df.columns:
            results_df[col] = df[col]

    # 5. Persistance Big Data (Parquet Format)
    print(f"\n[5/5] Sauvegarde des résultats au format Apache Parquet...")
    start_save = time.time()
    results_df.to_parquet(OUTPUT_PARQUET_PATH, index=False, engine="pyarrow", compression="snappy")
    save_time = time.time() - start_save
    
    parquet_size_kb = OUTPUT_PARQUET_PATH.stat().st_size / 1024
    print(f"      • Fichier Parquet généré : {OUTPUT_PARQUET_PATH.name}")
    print(f"      • Taille compressée : {parquet_size_kb:.1f} KB (Compression Snappy)")
    print(f"      • Écriture disque en {save_time:.2f} secondes.")
    
    # Statistiques globales
    nb_churn = int(predictions.sum())
    taux_churn = float(nb_churn / nb_clients * 100)
    
    summary = {
        "date_execution": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_clients": int(nb_clients),
        "clients_churn_predit": nb_churn,
        "clients_fideles_predit": int(nb_clients - nb_churn),
        "taux_churn_pct": round(taux_churn, 2),
        "temps_total_sec": round(time.time() - start_total_time, 2),
        "cadence_clients_sec": round(nb_clients / (time.time() - start_total_time), 0)
    }
    
    with open(OUTPUT_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
        
    print("\n" + "=" * 70)
    print("                     RÉSULTATS DU TRAITEMENT")
    print("=" * 70)
    print(f"  • Total clients analysés : {nb_clients:,}")
    print(f"  • Clients à risque (Churn) : {nb_churn:,} ({taux_churn:.2f}%)")
    print(f"  • Clients fidèles : {nb_clients - nb_churn:,} ({100 - taux_churn:.2f}%)")
    print(f"  • Temps total d'exécution : {time.time() - start_total_time:.2f} secondes")
    print(f"  • Données prêtes pour le Dashboard dans : {OUTPUT_PARQUET_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
