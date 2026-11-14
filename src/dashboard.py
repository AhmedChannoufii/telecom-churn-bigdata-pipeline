import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Churn Télécom",
    page_icon="📶",
    layout="wide"
)

# Titre principal
st.title("📶 Dashboard de Prédiction du Churn Télécom")
st.write("Projet Big Data — Analyse et Rétention des clients (Tunisie Telecom)")

# 1. Chargement des données Parquet
@st.cache_data
def load_data():
    file_path = "data/output/predictions_fevrier_2026.parquet"
    return pd.read_parquet(file_path)

try:
    df = load_data()
except Exception as e:
    st.error("Erreur : veuillez d'abord exécuter le pipeline (run_pipeline.bat)")
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

col1.metric("Total Clients", f"{total_clients:,}")
col2.metric("Clients en Risque de Churn", f"{nb_churn:,}")
col3.metric("Taux de Churn Global", f"{taux_churn:.1f} %")
col4.metric("Clients Risque Élevé (> 65%)", f"{nb_risque_eleve:,}")

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

# 5. Tableau des Clients Filtrés
st.subheader("Liste des Clients à Risque")
search = st.text_input("Rechercher par Code Contrat :", "")

if search:
    df_filtre = df_filtre[df_filtre["CODE_CONTRAT"].astype(str).str.contains(search)]

# Affichage des colonnes importantes
cols = ["CODE_CONTRAT", "PROBABILITE_CHURN", "NIVEAU_RISQUE", "PREDICTION_CHURN"]
for c in ["ANC_M", "montant_recharge_m0", "internet_m0"]:
    if c in df_filtre.columns:
        cols.append(c)

st.dataframe(df_filtre[cols].sort_values(by="PROBABILITE_CHURN", ascending=False).head(200), use_container_width=True)

# 6. Bouton de Téléchargement CSV
csv_data = df_filtre[cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="Télécharger la liste filtrée (CSV)",
    data=csv_data,
    file_name="clients_churn_prioritaires.csv",
    mime="text/csv"
)
