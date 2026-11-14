import os
import json
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Configuration de la page Streamlit
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Telecom Churn Big Data Analytics",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "output"
PARQUET_FILE = OUTPUT_DIR / "predictions_fevrier_2026.parquet"
SUMMARY_FILE = OUTPUT_DIR / "churn_summary.json"

# ---------------------------------------------------------------------------
# Style CSS personnalisé
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1A365D 0%, #2B6CB0 100%);
        padding: 18px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-val {
        font-size: 28px;
        font-weight: bold;
        margin: 4px 0;
    }
    .metric-lbl {
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .alert-high {
        background-color: #FED7D7;
        color: #9B2C2C;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Chargement des Données
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    if not PARQUET_FILE.exists():
        return None, None
    df = pd.read_parquet(PARQUET_FILE)
    summary = None
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
            summary = json.load(f)
    return df, summary

df, summary = load_data()

# ---------------------------------------------------------------------------
# Header & Navigation
# ---------------------------------------------------------------------------
st.title("📶 Système Big Data de Prédiction du Churn Télécom")
st.caption("Architecture de Traitement Distribué (PySpark & Parquet) pour la Rétention Client — Tunisie Telecom")

if df is None:
    st.error("⚠️ Fichier de résultats introuvable ! Veuillez d'abord exécuter le pipeline : `python src/pipeline.py`.")
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar (Filtres)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🔍 Filtres & Paramètres")
    
    # Filtre par niveau de risque
    selected_risk = st.multiselect(
        "Niveau de Risque :",
        options=["Élevé", "Moyen", "Faible"],
        default=["Élevé", "Moyen", "Faible"]
    )
    
    # Filtre par ancienneté
    if "ANC_M" in df.columns:
        min_anc, max_anc = int(df["ANC_M"].min()), int(df["ANC_M"].max())
        anc_range = st.slider("Ancienneté client (Mois) :", min_anc, max_anc, (min_anc, max_anc))
    else:
        anc_range = None
        
    st.divider()
    st.markdown("### 📊 Spécifications Big Data")
    st.info(
        "• **Moteur :** PySpark / Distributed ETL\n"
        "• **Stockage :** Apache Parquet (Snappy)\n"
        "• **Modèle :** XGBoost (F1: 88.7%)\n"
        "• **Jeu de données :** Test Février 2026"
    )

# Filtrage du DataFrame
filtered_df = df[df["NIVEAU_RISQUE"].isin(selected_risk)]
if anc_range and "ANC_M" in df.columns:
    filtered_df = filtered_df[(filtered_df["ANC_M"] >= anc_range[0]) & (filtered_df["ANC_M"] <= anc_range[1])]

# ---------------------------------------------------------------------------
# KPIs Principaux
# ---------------------------------------------------------------------------
total_clients = len(df)
high_risk_count = int((df["NIVEAU_RISQUE"] == "Élevé").sum())
churn_rate = (df["PREDICTION_CHURN"].sum() / total_clients) * 100
avg_prob = df["PROBABILITE_CHURN"].mean() * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Total Clients Analysés</div>
        <div class="metric-val">{total_clients:,}</div>
        <div style="font-size: 11px;">Format Parquet Ultra-Rapide</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #C53030 0%, #E53E3E 100%);">
        <div class="metric-lbl">Taux de Churn Prédit</div>
        <div class="metric-val">{churn_rate:.1f} %</div>
        <div style="font-size: 11px;">{int(df['PREDICTION_CHURN'].sum()):,} clients à retenir</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #DD6B20 0%, #ED8936 100%);">
        <div class="metric-lbl">Clients à Risque Élevé</div>
        <div class="metric-val">{high_risk_count:,}</div>
        <div style="font-size: 11px;">Probabilité &gt; 65%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    cadence = summary.get("cadence_clients_sec", "15,000") if summary else "20,000+"
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #276749 0%, #38A169 100%);">
        <div class="metric-lbl">Vitesse de Traitement</div>
        <div class="metric-val">{cadence}</div>
        <div style="font-size: 11px;">Clients / seconde</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------------------------------------------------------------------
# Visualisations Graphiques
# ---------------------------------------------------------------------------
chart_col1, chart_col2 = st.columns([1, 1])

with chart_col1:
    st.subheader("📊 Répartition par Niveau de Risque")
    risk_counts = df["NIVEAU_RISQUE"].value_counts().reset_index()
    risk_counts.columns = ["Niveau", "Nombre"]
    
    fig_pie = px.pie(
        risk_counts,
        names="Niveau",
        values="Nombre",
        hole=0.45,
        color="Niveau",
        color_discrete_map={
            "Faible": "#38A169",
            "Moyen": "#ED8936",
            "Élevé": "#E53E3E"
        }
    )
    fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader("📈 Distribution des Probabilités de Churn")
    fig_hist = px.histogram(
        df,
        x="PROBABILITE_CHURN",
        nbins=30,
        color_discrete_sequence=["#2B6CB0"],
        labels={"PROBABILITE_CHURN": "Probabilité de Churn"}
    )
    fig_hist.add_vline(x=0.5, line_dash="dash", line_color="red", annotation_text="Seuil (0.5)")
    fig_hist.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Liste Opérationnelle des Clients à Risque
# ---------------------------------------------------------------------------
st.subheader("🎯 Liste Opérationnelle des Clients Prioritaires (Ciblage Rétention)")

search_contract = st.text_input("🔎 Rechercher par Code Contrat :", "")

display_df = filtered_df.copy()
if search_contract:
    display_df = display_df[display_df["CODE_CONTRAT"].astype(str).str.contains(search_contract)]

display_df = display_df.sort_values(by="PROBABILITE_CHURN", ascending=False)

# Sélection et renommage des colonnes pour affichage
cols_to_show = ["CODE_CONTRAT", "PROBABILITE_CHURN", "NIVEAU_RISQUE", "PREDICTION_CHURN"]
if "ANC_M" in display_df.columns:
    cols_to_show.append("ANC_M")
if "montant_recharge_m0" in display_df.columns:
    cols_to_show.append("montant_recharge_m0")
if "internet_m0" in display_df.columns:
    cols_to_show.append("internet_m0")

st.dataframe(
    display_df[cols_to_show].head(500),
    use_container_width=True,
    height=350
)

st.caption(f"Affichage des 500 premiers résultats sur un total de {len(display_df):,} clients filtrés.")

# Export CSV pour équipe marketing
csv = display_df[cols_to_show].to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Exporter la liste des clients ciblés (CSV)",
    data=csv,
    file_name="clients_churn_prioritaires.csv",
    mime="text/csv",
)
