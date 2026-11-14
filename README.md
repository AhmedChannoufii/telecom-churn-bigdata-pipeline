# 📶 Telecom Churn Big Data Pipeline

> **Pipeline Big Data & Architecture de Prédiction du Churn Télécom utilisant Apache Parquet, PySpark & XGBoost.**

Ce projet transpose les travaux de modélisation Machine Learning du PFE vers une **solution Big Data opérationnelle**, capable de traiter des volumes massifs de consommation réseau (appels, internet, recharges) et de prédire le risque de résiliation (Churn) pour des dizaines de milliers de clients en quelques secondes.

---

## 🏗️ Architecture du Pipeline

```mermaid
flowchart LR
    A["Données de Test Télécom\n(fevrier_2026.csv - 34,000 clients)"] --> B["Moteur Big Data ETL\n(Ingestion & Normalisation 46 Features)"]
    B --> C["Inférence Machine Learning\n(Modèle XGBoost Pré-entraîné)"]
    C --> D["Data Lake (Format Parquet)\nCompression Snappy (558 KB)"]
    D --> E["Tableau de Bord Streamlit\n(Visualisation & Alertes Rétention)"]
```

---

## ⚡ Pourquoi ce projet relève du Big Data ?

Dans un opérateur de télécommunications réel :
1. **Volume Massif :** Les CDRs (Call Detail Records), sessions data 4G/5G et transactions de recharges se comptent en **millions d'événements par heure**.
2. **Limite de Pandas :** Les scripts classiques sur une machine unique chargent l'intégralité des données en RAM sur un seul cœur CPU, provoquant des dépassements de mémoire (*Out of Memory*).
3. **Optimisation Parquet :** Passage d'un fichier CSV brut de **16.4 MB** à un fichier Parquet compressé de **558 KB** (gain de stockage de **96.6%** et lecture colonnaire instantanée).

---

## 📊 Métriques & Résultats du Traitement

Lors de l'exécution sur le jeu de test **Février 2026** :

| Indicateur | Valeur Obtenue |
| :--- | :--- |
| **Volume de clients analysés** | **34,000 clients** |
| **Temps d'ingestion des données** | **0.07 seconde** |
| **Cadence de prédiction ML** | **~480,000 clients / seconde** |
| **Taille brute CSV** | **16.41 MB** |
| **Taille compressée Parquet (Snappy)** | **558.0 KB (-96.6%)** |
| **Taux de Churn prédit** | **17.65% (6,001 clients à risque)** |
| **Clients fidèles prédits** | **82.35% (27,999 clients)** |

---

## 📁 Arborescence du Projet

```text
telecom-churn-bigdata-pipeline/
│
├── data/
│   ├── fevrier_2026.csv              # Jeu de données de test (34,000 clients)
│   ├── cible_churn_F.csv             # Référentiel client
│   └── output/
│       ├── predictions_fevrier_2026.parquet  # Résultats compressés Big Data
│       └── churn_summary.json                # Métriques d'exécution du pipeline
│
├── models/
│   ├── xgb_model.pkl                 # Modèle XGBoost pré-entraîné
│   ├── scaler.pkl                    # StandardScaler pré-entraîné
│   └── model_config.json             # Schéma des 46 features et seuil (0.5)
│
├── src/
│   ├── pipeline.py                   # Script Big Data ETL + Inférence ML
│   └── dashboard.py                  # Dashboard interactif Streamlit
│
├── run_pipeline.bat                  # Exécution du traitement en 1 clic
├── run_dashboard.bat                 # Lancement de l'interface en 1 clic
├── requirements.txt                  # Dépendances Python
└── README.md                         # Documentation complète
```

---

## 🚀 Guide d'Exécution Rapide

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Lancer le Pipeline Big Data
Pour traiter les données de test et générer les prédictions au format Parquet :
* **Double-cliquer sur :** `run_pipeline.bat`  
* Ou en ligne de commande :
  ```bash
  python src/pipeline.py
  ```

### 3. Lancer le Tableau de Bord
Pour explorer les résultats dans le navigateur web :
* **Double-cliquer sur :** `run_dashboard.bat`  
* Ou en ligne de commande :
  ```bash
  streamlit run src/dashboard.py
  ```


