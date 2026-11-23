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
2. **Contrainte Critique de Vélocité (Time-to-Action < 48h) :** Si la prédiction et l'écriture prennent des heures (format CSV séquentiel), le client a **déjà acheté une carte SIM concurrente**. Le pipeline Big Data (Apache Parquet) s'exécute en **moins de 0.1s**, permettant de déclencher immédiatement une **offre de rétention proactive**.
3. **Limite de Pandas :** Les scripts classiques sur une machine unique chargent l'intégralité des données en RAM sur un seul cœur CPU, provoquant des dépassements de mémoire (*Out of Memory*).
4. **Optimisation Parquet :** Passage d'un fichier CSV brut à un fichier Parquet compressé Snappy (gain de stockage de **78%** et lecture colonnaire instantanée).

---

## 🎯 Stratégie Métier : Offres de Rétention Proactives & Campagne Massive

Dès que le modèle identifie les clients à risque (6 001 clients), le pipeline et le tableau de bord permettent de déclencher une **Campagne de Rétention Massive** d'un seul coup (au lieu d'un traitement unitaire) :
* **👑 Pack Fidélité VIP (2 077 clients) :** Clients fidèles (> 3 ans) à forte valeur (Remise 25% + Appels illimités week-end).
* **💰 Bonus Recharge (1 995 clients) :** Clients sensibles au solde (+100% de bonus immédiat).
* **⚡ Forfait Duo Famille (1 211 clients) :** Clients voix (Appels gratuits vers numéros favoris).
* **🎁 Pass Data Boost (718 clients) :** Consommateurs Internet (10 Go offerts immédiatement).

**Impact prévisionnel de la campagne :**
* Taux d'acceptation moyen estimé : **~60%**
* Clients sauvés de la résiliation : **~3 600 clients conservés**
* Taux de Churn global résiduel : chute de **17.65% à 7.1%**
* Chiffre d'affaires annuel sécurisé : **~1,080,000 DT** (sur base d'un ARPU moyen de 25 DT/mois)

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
│       ├── predictions_fevrier_2026.csv      # Résultats format CSV classique
│       └── benchmark.json                    # Métriques comparatives d'exécution
│
├── models/
│   ├── xgb_model.pkl                 # Modèle XGBoost pré-entraîné
│   ├── scaler.pkl                    # StandardScaler pré-entraîné
│   └── model_config.json             # Schéma des 46 features et seuil (0.5)
│
├── src/
│   ├── pipeline.py                   # Script Big Data ETL + Inférence ML + Rétention
│   ├── pipeline_csv.py               # Version démo CSV (lente)
│   ├── pipeline_parquet.py           # Version Big Data optimisée Parquet
│   └── dashboard.py                  # Dashboard interactif Streamlit & Simulateur What-If
│
├── run_pipeline.bat                  # Exécution du traitement complet
├── run_pipeline_csv.bat              # Test de la lenteur sur CSV (~2 minutes)
├── run_pipeline_parquet.bat          # Test de la rapidité Parquet (< 0.05 seconde)
├── run_dashboard.bat                 # Lancement de l'interface en 1 clic
├── Presentation_Big_Data_Telecom_Churn_v2.pptx # Slides de présentation (16:9)
├── Plan_Projet_Big_Data.pdf          # Fiche technique d'architecture
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


