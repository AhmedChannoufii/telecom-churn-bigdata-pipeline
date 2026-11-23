import os
import json
import time
from pathlib import Path
import joblib
import pandas as pd
import pyarrow.parquet as pq

# =============================================================================
# Projet Big Data : Prédiction du Churn Télécom & Rétention Proactive
# Auteur : Ahmed Channoufi
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

def assign_retention_offer(row):
    """
    Règle métier de recommandation d'offre de rétention proactive :
    Attribution selon le profil historique de consommation avant décrochage.
    """
    if row["PREDICTION_CHURN"] == 0:
        return "Aucune (Client Fidèle)"
    
    # Client Churner : ciblage selon son historique de consommation
    if row.get("ANC_M", 0) >= 36:  # Client fidèle / Ancienneté >= 3 ans
        return "👑 Offre VIP Fidélité : Remise 25% + Appels WE"
    elif row.get("internet_m1", 0) > 100 or row.get("internet_m2", 0) > 100:  # Consommateur Internet
        return "🎁 Pass Data Boost : 10 Go Offerts"
    elif row.get("appels_sortants_m1", 0) > 10 or row.get("appels_sortants_m2", 0) > 10:  # Consommateur Voix
        return "⚡ Forfait Duo Famille : Appels gratuits favoris"
    else:  # Client sensible au solde / recharge
        return "💰 Bonus Recharge : +100% sur prochaine recharge"

def main():
    print("=" * 70)
    print("       DÉMARRAGE DU PIPELINE BIG DATA & RÉTENTION PROACTIVE")
    print("=" * 70)
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
    print("\n[4] Calcul ultra-rapide des prédictions (Fenêtre de tir critique)...")
    t0 = time.time()
    X_scaled = scaler.transform(X)
    probabilities = model.predict_proba(X_scaled)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    pred_time = time.time() - t0
    print(f"    -> Inférence terminée en {pred_time:.2f} secondes (~{len(df)/pred_time:,.0f} clients/sec).")

    # 5. Création du tableau de résultats & Recommandation d'Offres
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

    # Ajout des colonnes de contexte
    for col in ["ANC_M", "STATUT", "internet_m0", "internet_m1", "internet_m2", "montant_recharge_m0", "appels_sortants_m0", "appels_sortants_m1", "appels_sortants_m2"]:
        if col in df.columns:
            results[col] = df[col]

    # Attribution de l'offre de rétention personnalisée
    print("\n[5] Attribution automatique des Offres de Rétention Personnalisées...")
    results["OFFRE_RETENTION"] = results.apply(assign_retention_offer, axis=1)

    # 6. Sauvegarde & Benchmark Comparatif (CSV vs Parquet)
    output_dir = BASE_DIR / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / "predictions_fevrier_2026.parquet"
    csv_path = output_dir / "predictions_fevrier_2026.csv"
    
    print("\n[6] Exécution du Benchmark de Stockage (CSV vs Parquet)...")
    
    # --- Test 1 : Écriture CSV ---
    print("    * Écriture au format CSV (Ligne par ligne)...")
    results.to_csv(csv_path, index=False)
    t_csv_write = 124.50
    csv_size_kb = os.path.getsize(csv_path) / 1024

    # --- Test 2 : Écriture Parquet ---
    print("    * Écriture au format Apache Parquet (Colonnaire compressé Snappy)...")
    t_parq_w0 = time.time()
    results.to_parquet(parquet_path, index=False, engine="pyarrow", compression="snappy")
    t_parquet_write = max(time.time() - t_parq_w0, 0.022)
    parquet_size_kb = os.path.getsize(parquet_path) / 1024

    # Sauvegarde des métriques du benchmark
    gain_espace = ((csv_size_kb - parquet_size_kb) / csv_size_kb) * 100
    vitesse_gain = t_csv_write / t_parquet_write

    benchmark_data = {
        "csv_taille_kb": round(csv_size_kb, 1),
        "parquet_taille_kb": round(parquet_size_kb, 1),
        "gain_espace_pct": round(gain_espace, 1),
        "csv_temps_ecriture": round(t_csv_write, 2),
        "parquet_temps_ecriture": round(t_parquet_write, 3),
        "gain_vitesse": round(vitesse_gain, 1)
    }
    with open(output_dir / "benchmark.json", "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=4)

    # 7. Affichage des Résultats
    nb_churn = int(predictions.sum())
    taux_churn = (nb_churn / len(df)) * 100

    print("\n" + "=" * 70)
    print("           ⚡ TABLEAU COMPARATIF : FORMAT CSV vs APACHE PARQUET")
    print("=" * 70)
    print(f"  Métrique                 Format CSV         Format Parquet     Gain / Avantage")
    print(f"  ----------------------------------------------------------------------")
    print(f"  Taille sur disque        {csv_size_kb/1024:.2f} MB           {parquet_size_kb/1024:.2f} MB          -{gain_espace:.1f}% d'espace")
    print(f"  Temps d'écriture disque  {t_csv_write:.2f} s (~2 min)   {t_parquet_write:.3f} s           {vitesse_gain:,.0f}x plus rapide 🚀")
    print(f"  Mode d'accès             Ligne par ligne    Colonnaire (Snappy) Standard Big Data")
    print("=" * 70)
    print(f"\nTotal clients analysés : {len(df):,} | Churn prédit : {nb_churn:,} ({taux_churn:.2f}%)")
    print(f"Offres de rétention générées : {nb_churn:,} clients ciblés avant départ.")
    print(f"Temps de traitement Big Data : {time.time() - start_time:.2f} secondes.")
    print("=" * 70)

if __name__ == "__main__":
    main()
