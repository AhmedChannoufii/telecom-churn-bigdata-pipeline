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

# 7. Campagne de Rétention Massive (Envoi Groupé pour TOUS les Clients Churn)
st.subheader("🎯 Campagne de Rétention Massive (Ciblage Groupé des 6 001 Clients Churn)")
st.caption("⏱️ **Vélocité Big Data & Time-to-Action (< 48h) :** Traitement en lot (Batch) pour envoyer l'offre de rétention à TOUS les clients en risque de départ avant qu'ils n'achètent une SIM concurrente.")

# Récupération de tous les clients en Churn
df_churners = df[df["PREDICTION_CHURN"] == 1].copy()
nb_churners_total = len(df_churners)

camp_col1, camp_col2 = st.columns([1, 1])

with camp_col1:
    st.write("#### 1. Configuration de la Campagne Globale :")
    st.write(f"👥 **Cible sélectionnée :** `{nb_churners_total:,} clients Churners` (100% des clients à risque)")
    
    selected_mass_offer = st.selectbox(
        "Sélectionner l'offre de rétention à envoyer à TOUS les churners :",
        [
            "🤖 Ciblage Hybride Personnalisé (Attribution selon profil Big Data)",
            "🎁 Pass Data Boost (10 Go offerts immédiatement)",
            "💰 Bonus Recharge (+100% sur la prochaine recharge)",
            "👑 Offre Fidélité VIP (Appels illimités week-end + Remise 25%)",
            "⚡ Forfait Duo Famille (Appels gratuits vers 2 numéros favoris)"
        ]
    )
    
    # Message SMS simulé
    if "Pass Data" in selected_mass_offer:
        sms_preview = "Cher client, pour vous remercier de votre fidélité, votre opérateur vous offre 10 Go Internet gratuits valables immédiatement !"
        taux_sauvetage = 0.58
    elif "Bonus Recharge" in selected_mass_offer:
        sms_preview = "Offre Spéciale : Rechargez dès aujourd'hui et profitez de +100% de bonus immédiat sur toutes vos recharges pendant 30 jours !"
        taux_sauvetage = 0.52
    elif "VIP" in selected_mass_offer:
        sms_preview = "Statut VIP : Vos appels sont désormais illimités tous les week-ends + bénéficiez de 25% de remise sur votre facture !"
        taux_sauvetage = 0.65
    elif "Duo Famille" in selected_mass_offer:
        sms_preview = "Offre Famille : Choisissez 2 numéros favoris et appelez-les gratuitement et en illimité dès aujourd'hui !"
        taux_sauvetage = 0.48
    else:  # Hybride
        sms_preview = "Offre Proactive Ultra-Ciblée : Chaque client reçoit par SMS l'offre adaptée à son historique (Data, Recharge, VIP ou Voix)."
        taux_sauvetage = 0.60

    st.text_area("Aperçu du SMS envoyé en masse aux 6 001 clients :", sms_preview, height=85)

with camp_col2:
    st.write("#### 2. Impact Estimé de la Campagne Massive :")
    
    clients_sauves = int(nb_churners_total * taux_sauvetage)
    taux_churn_post = ((nb_churners_total - clients_sauves) / total_clients) * 100
    ca_sauve = clients_sauves * 25 * 12  # ARPU 25 DT/mois sur 1 an
    
    mc1, mc2 = st.columns(2)
    mc1.metric("Clients Sauvés Estimés", f"{clients_sauves:,}", f"{taux_sauvetage*100:.0f}% d'acceptation")
    mc2.metric("Nouveau Taux de Churn", f"{taux_churn_post:.1f} %", f"-{(taux_churn - taux_churn_post):.1f}% de baisse", delta_color="inverse")
    
    st.write(f"• **Chiffre d'Affaires Annuel Sauvé :** `{ca_sauve:,.0f} DT` (ARPU moyen de 25 DT/mois)")
    st.write(f"• **Délai d'exécution Big Data :** `< 0.1 seconde` (Passage à l'action immédiat)")

# Bouton d'action massif
st.write("")
if st.button("🚀 DÉCLENCHER L'ENVOI SMS MASSIF À TOUS LES 6 001 CLIENTS CHURNERS", use_container_width=True, type="primary"):
    st.success(
        f"🎉 **CAMPAGNE MASSIVE DÉCLENCHÉE AVEC SUCCÈS !**\n\n"
        f"✅ **6 001 SMS** de rétention ont été générés et transmis à la passerelle opérateur.\n\n"
        f"📊 **Résultat Prévisionnel :** **{clients_sauves:,} clients** sauvés de la résiliation "
        f"(le taux de Churn chute de **{taux_churn:.1f}%** à **{taux_churn_post:.1f}%**).\n\n"
        f"💰 **Impact Financier :** **{ca_sauve:,.0f} DT** de revenus préservés grâce à la vélocité Big Data."
    )
    
    # Export du fichier de campagne massif
    df_campagne = df_churners[["CODE_CONTRAT", "PROBABILITE_CHURN", "OFFRE_RETENTION"]].copy()
    if "Hybride" not in selected_mass_offer:
        df_campagne["OFFRE_RETENTION_APPLIQUEE"] = selected_mass_offer
    else:
        df_campagne["OFFRE_RETENTION_APPLIQUEE"] = df_campagne["OFFRE_RETENTION"]
        
    csv_campagne = df_campagne.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger le fichier d'envoi SMS Campagne Massive (6 001 lignes CSV)",
        data=csv_campagne,
        file_name="campagne_massive_retention_6001_clients.csv",
        mime="text/csv"
    )
