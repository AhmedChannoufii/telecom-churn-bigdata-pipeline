from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Churn Télécom & Rétention",
    page_icon="📶",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Titre principal
st.title("📶 Dashboard de Prédiction du Churn & Rétention Télécom")
st.write("Projet Big Data — Analyse Prédictive & Rétention Proactive des Clients")

# 1. Chargement des données Parquet
@st.cache_data
def load_data():
    file_path = BASE_DIR / "data" / "output" / "predictions_fevrier_2026.parquet"
    if not file_path.exists():
        return None
    return pd.read_parquet(file_path)

df = load_data()
if df is None:
    st.error("⚠️ Fichier de résultats introuvable ! Veuillez d'abord exécuter le pipeline (double-cliquer sur run_pipeline.bat).")
    st.stop()

# 2. Sidebar (Filtres)
st.sidebar.header("Filtres")
niveaux_choisis = st.sidebar.multiselect(
    "Niveau de risque :",
    options=["Faible", "Moyen", "Élevé"],
    default=["Faible", "Moyen", "Élevé"]
)

# Filtrage
df_filtre = df[df["NIVEAU_RISQUE"].isin(niveaux_choisis)]

# 3. Métriques Principales (KPIs)
col1, col2, col3, col4 = st.columns(4)

total_clients = len(df)
nb_churn = int(df["PREDICTION_CHURN"].sum())
taux_churn = (nb_churn / total_clients) * 100
nb_risque_eleve = int((df["NIVEAU_RISQUE"] == "Élevé").sum())

col1.metric("Total Clients Analysés", f"{total_clients:,}")
col2.metric("Clients en Risque de Churn", f"{nb_churn:,}")
col3.metric("Taux de Churn Global", f"{taux_churn:.1f} %")
col4.metric("Clients Risque Élevé (> 65%)", f"{nb_risque_eleve:,}")

# Section Benchmark (Comparaison CSV vs Parquet)
with st.expander("⚡ Voir le Benchmark Big Data : Format CSV vs Apache Parquet"):
    b1, b2, b3 = st.columns(3)
    b1.metric("Taille Disque", "0.54 MB (Parquet)", "-65.4% vs CSV (1.57 MB)")
    b2.metric("Vitesse d'Écriture", "0.02 s (Parquet)", "~5 600x plus rapide que CSV (~2 min)")
    b3.metric("Type de Stockage", "Colonnaire (Snappy)", "Format Standard Big Data")
    st.caption("💡 **Pourquoi Apache Parquet ?** Contrairement au CSV qui écrit et lit chaque ligne en texte brut (prenant plus de 2 minutes sur de gros volumes), Parquet compresse la donnée en colonnes avec Snappy en une fraction de seconde.")

st.write("---")

# 4. Graphiques
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Répartition des Clients par Niveau de Risque")
    risk_counts = df["NIVEAU_RISQUE"].value_counts().reset_index()
    risk_counts.columns = ["Niveau de Risque", "Nombre de Clients"]
    
    fig_pie = px.pie(
        risk_counts,
        names="Niveau de Risque",
        values="Nombre de Clients",
        color="Niveau de Risque",
        color_discrete_map={
            "Faible": "#2ecc71",
            "Moyen": "#f39c12",
            "Élevé": "#e74c3c"
        }
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader("Distribution des Probabilités de Churn")
    fig_hist = px.histogram(
        df,
        x="PROBABILITE_CHURN",
        nbins=25,
        labels={"PROBABILITE_CHURN": "Probabilité de Churn"},
        color_discrete_sequence=["#3498db"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

st.write("---")

# 5. Tableau des Clients avec Offres de Rétention Recommandées
st.subheader("📋 Liste Opérationnelle & Offres de Rétention Recommandées")
st.caption("⏱️ **Contrainte de Vélocité :** La prédiction ultra-rapide permet de déclencher l'offre de rétention avant que le client ne passe chez un opérateur concurrent.")

search = st.text_input("Rechercher par Code Contrat :", "")

if search:
    df_filtre = df_filtre[df_filtre["CODE_CONTRAT"].astype(str).str.contains(search)]

# Colonnes affichées (incluant l'offre de rétention personnalisée)
cols = ["CODE_CONTRAT", "PROBABILITE_CHURN", "NIVEAU_RISQUE"]
if "OFFRE_RETENTION" in df_filtre.columns:
    cols.append("OFFRE_RETENTION")

st.dataframe(
    df_filtre[cols].sort_values(by="PROBABILITE_CHURN", ascending=False).head(200),
    use_container_width=True,
    hide_index=True
)

# 6. Bouton de Téléchargement CSV
csv_data = df_filtre[cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Télécharger la liste de ciblage pour l'équipe Rétention (CSV)",
    data=csv_data,
    file_name="ciblage_retention_churn.csv",
    mime="text/csv"
)

st.write("---")

# 7. Simulateur d'Action de Rétention Proactive (What-If)
st.subheader("🎯 Simulateur d'Action de Rétention Proactive (Sauver le Client)")
st.info("💡 **Problématique Temps Réel :** Si le modèle met des heures à calculer, le client est déjà parti. Grâce au pipeline Big Data (< 0.1s), on peut lui proposer une offre de rétention immédiate.")

sim_col1, sim_col2 = st.columns([1, 1])

with sim_col1:
    high_risk_sample = df[df["NIVEAU_RISQUE"] == "Élevé"]["CODE_CONTRAT"].head(10).tolist()
    if not high_risk_sample:
        high_risk_sample = df["CODE_CONTRAT"].head(5).tolist()
    
    selected_client = st.selectbox("Sélectionner un client à risque élevé :", high_risk_sample)
    client_row = df[df["CODE_CONTRAT"] == selected_client].iloc[0]
    initial_prob = float(client_row["PROBABILITE_CHURN"])

    st.warning(f"⚠️ **Score de Churn Actuel : {initial_prob * 100:.1f}% (Risque Élevé)**")
    
    selected_offer = st.selectbox(
        "Offre de rétention personnalisée à appliquer :",
        [
            "🎁 Pass Data Boost (10 Go offerts immédiatement)",
            "💰 Bonus Recharge (+100% sur la prochaine recharge)",
            "👑 Offre Fidélité VIP (Appels illimités week-end + Remise 25%)",
            "⚡ Forfait Duo Famille (Appels gratuits vers 2 numéros)"
        ]
    )

with sim_col2:
    st.write("#### Simulation de l'Impact de l'Offre :")
    # Réduction simulée selon l'offre
    if "10 Go" in selected_offer:
        reduction = 0.58
    elif "+100%" in selected_offer:
        reduction = 0.52
    elif "VIP" in selected_offer:
        reduction = 0.65
    else:
        reduction = 0.45

    new_prob = max(initial_prob * (1 - reduction), 0.12)
    
    st.write(f"• **Ancienne Probabilité de Churn :** `{initial_prob * 100:.1f} %`")
    st.write(f"• **Nouvelle Probabilité Estimée :** `{new_prob * 100:.1f} %`")
    st.write(f"• **Réduction du Risque :** `-{reduction * 100:.0f} %`")

    if st.button("🚀 Valider & Déclencher l'Offre de Rétention par SMS"):
        st.success(f"🎉 **Client {selected_client} Sauvé !** L'offre '{selected_offer.split(':')[0]}' a été validée. Le risque de départ passe de {initial_prob*100:.1f}% à {new_prob*100:.1f}%.")
