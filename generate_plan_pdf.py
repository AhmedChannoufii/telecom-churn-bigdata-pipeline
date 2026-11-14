import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(18 * mm, 285 * mm, "PROJET BIG DATA : PIPELINE STREAMING CHURN TÉLÉCOM")
            self.setFont("Helvetica", 8)
            self.drawRightString(192 * mm, 285 * mm, "Plan d'Exécution & Spécifications")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.6)
            self.line(18 * mm, 282 * mm, 192 * mm, 282 * mm)
            
        # Running Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
        self.setFont("Helvetica", 8)
        self.drawString(18 * mm, 10 * mm, "Projet Universitaire Big Data - Ahmed Channoufi")
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(192 * mm, 10 * mm, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#1A365D")   # Deep navy
    secondary = colors.HexColor("#2B6CB0") # Vibrant blue
    accent = colors.HexColor("#DD6B20")    # Amber / Coral
    text_dark = colors.HexColor("#2D3748") # Charcoal
    bg_light = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=primary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=secondary,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=text_dark,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#2C5282")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=primary
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("PLAN D'EXÉCUTION & SPÉCIFICATIONS TECHNIQUES", title_style))
    story.append(Paragraph("Projet Big Data : Pipeline Streaming & Batch pour la Prédiction du Churn Télécom", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=secondary, spaceBefore=0, spaceAfter=8))

    # Meta Info Card
    meta_data = [
        [
            Paragraph("<b>Étudiant / Auteur :</b> Ahmed Channoufi", body_style),
            Paragraph("<b>Dépôt GitHub :</b> telecom-churn-bigdata-pipeline", body_style)
        ],
        [
            Paragraph("<b>Modèle Machine Learning :</b> XGBoost (F1: 88.7%, Recall: 92.4%)", body_style),
            Paragraph("<b>Technologies :</b> Apache Spark, Kafka, MongoDB, Docker", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[87*mm, 87*mm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Section 1: Contexte & Justification
    story.append(Paragraph("1. Contexte du Projet & Justification Big Data", h1_style))
    story.append(Paragraph(
        "Dans le secteur des télécommunications (ex: Tunisie Telecom, Orange, Ooredoo), la résiliation de contrat (<b>Churn</b>) représente un enjeu stratégique. Les événements générés au quotidien (CDRs - <i>Call Detail Records</i>, sessions data internet, recharges et transactions USSD) se chiffrent en <b>millions de transactions par heure</b>. Les méthodes classiques sur machine unique (Pandas / Scikit-learn) saturent rapidement face à ce volume massif.",
        body_style
    ))
    story.append(Paragraph(
        "Ce projet transpose le modèle ML développé lors du PFE vers une <b>architecture distribuée Big Data de bout en bout</b>, combinant ingestion streaming, calcul haute performance et restitution temps réel.",
        body_style
    ))

    # Callout Box: 3 V du Big Data
    callout_data = [[
        Paragraph("<b>Application concrète des 3 V du Big Data :</b><br/>"
                  "• <b>Volume :</b> Fusion et agrégation de 6 sources massives (appels sortants/entrants, data, recharges, forfaits, contrats).<br/>"
                  "• <b>Vélocité :</b> Ingestion et traitement continu d'événements réseau en quasi temps réel via <b>Apache Kafka</b>.<br/>"
                  "• <b>Variété :</b> Données hétérogènes multi-sources (CDR voix, volumes internet, transactions financières et profils clients).", callout_style)
    ]]
    callout_table = Table(callout_data, colWidths=[174*mm])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 8))

    # Section 2: Architecture Globale
    story.append(Paragraph("2. Architecture Globale du Pipeline", h1_style))

    arch_data = [
        [Paragraph("Couche", table_header_style), Paragraph("Composant", table_header_style), Paragraph("Rôle & Responsabilité Technique", table_header_style)],
        [
            Paragraph("<b>1. Ingestion</b>", table_cell_bold),
            Paragraph("Apache Kafka & Zookeeper", table_cell_style),
            Paragraph("Producteur streaming simulant les flux CDRs de la flotte télécom vers des topics dédiés (calls, data, recharges).", table_cell_style)
        ],
        [
            Paragraph("<b>2. Processing</b>", table_cell_bold),
            Paragraph("Apache Spark (PySpark)", table_cell_style),
            Paragraph("Calcul distribué des 46 features temporelles (rolling windows, tendances, récence) et scoring XGBoost distribué.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Storage</b>", table_cell_bold),
            Paragraph("Parquet (Lake) & MongoDB (NoSQL)", table_cell_style),
            Paragraph("Stockage froid historique (Parquet compressé Snappy) et base chaude NoSQL (MongoDB) pour servir le dashboard.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Dashboard</b>", table_cell_bold),
            Paragraph("FastAPI / Streamlit / Flask", table_cell_style),
            Paragraph("Visualisation en temps réel des KPIs de rétention, alertes sur les clients à haut risque et simulateur d'offres.", table_cell_style)
        ],
        [
            Paragraph("<b>5. Packaging</b>", table_cell_bold),
            Paragraph("Docker & Docker Compose", table_cell_style),
            Paragraph("Orchestration de l'ensemble des conteneurs pour une démonstration immédiate et portable (<code>docker compose up</code>).", table_cell_style)
        ],
    ]
    arch_table = Table(arch_data, colWidths=[30*mm, 44*mm, 100*mm])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
    ]))
    story.append(arch_table)

    # Page Break -> Page 2 (Steps 1 to 4)
    story.append(PageBreak())

    story.append(Paragraph("3. Plan d'Exécution Détaillé (Étapes 1 à 7)", h1_style))

    steps_part1 = [
        (
            "Étape 1 : Initialisation & Structuration du Projet",
            "Mise en place de l'environnement et de l'architecture logicielle standard Big Data.",
            [
                "Configuration du dépôt local synchronisé avec <code>https://github.com/AhmedChannoufii/telecom-churn-bigdata-pipeline</code>.",
                "Création de l'arborescence professionnelle : <code>src/ingestion/</code>, <code>src/processing/</code>, <code>src/storage/</code>, <code>src/dashboard/</code>, <code>docker/</code>, <code>models/</code>.",
                "Définition du fichier des dépendances <code>requirements.txt</code> et initialisation de la documentation technique (README.md)."
            ]
        ),
        (
            "Étape 2 : Migration des Artefacts ML & Synthétiseur de Données",
            "Valorisation du travail du PFE et simulation de données réseau scalables.",
            [
                "Importation des artefacts ML validés : <code>xgb_model.pkl / xgb_model.json</code>, <code>scaler.pkl</code> et <code>model_config.json</code>.",
                "Validation du dictionnaire des 46 variables exigées par le modèle (tendances d'appels, récence internet, activité forfaits, etc.).",
                "Développement d'un <b>Générateur de Données Synthétiques (Data Simulator)</b> produisant les flux réalistes de CDRs pour tester le passage à l'échelle."
            ]
        ),
        (
            "Étape 3 : Pipeline d'Ingestion Streaming avec Apache Kafka",
            "Gestion des flux massifs et asynchrones du réseau télécom.",
            [
                "Mise en place de l'infrastructure Kafka + Zookeeper (ou Kafka KRaft) via Docker.",
                "Création des 5 Topics Kafka spécialisés : <code>cdr-sortant</code>, <code>cdr-entrant</code>, <code>cdr-data</code>, <code>cdr-recharges</code>, <code>cdr-ussd</code>.",
                "Développement du script <b>Kafka Producer multi-flux</b> en Python envoyant les messages sérialisés en JSON avec débit réglable."
            ]
        ),
        (
            "Étape 4 : Moteur de Calcul Distribué avec Apache Spark (PySpark)",
            "Le cœur Big Data : Feature Engineering distribué et Inférence ML.",
            [
                "Mise en place du cluster Spark (Master + Worker) et initialisation de la <code>SparkSession</code> avec support Streaming et connecteurs.",
                "Implémentation des agrégations et fenêtrages temporels distribués (<code>groupBy('CODE_CONTRAT')</code>, calcul des moyennes mobiles, pentes d'évolution).",
                "Construction dynamique du vecteur des 46 features conformément aux entrées attendues par le modèle.",
                "Scoring prédictif distribué : application du modèle XGBoost sous forme d'UDF (User Defined Function) pour calculer le score de Churn en direct."
            ]
        )
    ]

    for title, subtitle, bullets in steps_part1:
        step_box = []
        step_box.append(Paragraph(title, h2_style))
        step_box.append(Paragraph(f"<i>{subtitle}</i>", ParagraphStyle('SubSub', parent=body_style, textColor=colors.HexColor("#4A5568"))))
        for bullet in bullets:
            step_box.append(Paragraph(f"• {bullet}", bullet_style))
        step_box.append(Spacer(1, 4))
        story.append(KeepTogether(step_box))

    # Page Break -> Page 3 (Steps 5 to 7 + Deliverables)
    story.append(PageBreak())

    steps_part2 = [
        (
            "Étape 5 : Couche de Persistance Hybride (Data Lake & Base NoSQL)",
            "Stockage froid pour l'historique et stockage chaud pour l'opérationnel.",
            [
                "<b>Stockage Froid (Data Lake) :</b> Sauvegarde des données brutes et enrichies au format optimisé <b>Parquet</b> partitionné par mois/date.",
                "<b>Stockage Chaud (NoSQL MongoDB) :</b> Persistance en continu des prédictions clients, alertes critiques et scores de probabilité.",
                "Création d'index MongoDB performants sur <code>CODE_CONTRAT</code> et <code>churn_probability</code> pour des requêtes instantanées (&lt; 10 ms)."
            ]
        ),
        (
            "Étape 6 : Dashboard Décisionnel & Alerting Rétention",
            "Restitution opérationnelle pour les équipes métier (Marketing & Rétention).",
            [
                "Développement d'un Dashboard interactif moderne (Streamlit ou Flask).",
                "Indicateurs clés en direct : Taux global de churn, volume de flux traités par seconde, distribution des niveaux de risque.",
                "Tableau dynamique des <b>Top Clients à Risque Élevé</b> avec affichage des facteurs déclencheurs (chute de recharge, baisse d'activité).",
                "Simulateur de rétention : tester une réduction tarifaire ou un bonus data et observer la diminution du score de churn."
            ]
        ),
        (
            "Étape 7 : Conteneurisation Intégrale & Guide de Démonstration",
            "Automatisation du déploiement pour une démonstration fluide le jour de la soutenance.",
            [
                "Création du fichier <code>docker-compose.yml</code> unifié orchestrant Kafka, Spark, MongoDB et le Dashboard.",
                "Vérification de la résilience et du démarrage 'One-Click' via <code>docker compose up -d</code>.",
                "Rédaction du guide de soutenance pas-à-pas avec commandes d'injection de données et scénarios de démo en direct."
            ]
        )
    ]

    for title, subtitle, bullets in steps_part2:
        step_box = []
        step_box.append(Paragraph(title, h2_style))
        step_box.append(Paragraph(f"<i>{subtitle}</i>", ParagraphStyle('SubSub', parent=body_style, textColor=colors.HexColor("#4A5568"))))
        for bullet in bullets:
            step_box.append(Paragraph(f"• {bullet}", bullet_style))
        step_box.append(Spacer(1, 4))
        story.append(KeepTogether(step_box))

    story.append(Spacer(1, 6))

    # Section 4: Matrice des Livrables
    story.append(Paragraph("4. Synthèse des Livrables Académiques", h1_style))

    eval_data = [
        [Paragraph("Composant Clé", table_header_style), Paragraph("Réalisation Technique", table_header_style), Paragraph("Validation Soutenance", table_header_style)],
        [
            Paragraph("<b>Architecture Distribuée</b>", table_cell_bold),
            Paragraph("Pipeline découplé : Ingestion (Kafka) + Traitement (Spark) + Stockage (Mongo/Parquet).", table_cell_style),
            Paragraph("Diagramme d'architecture & déploiement Docker multi-nœuds.", table_cell_style)
        ],
        [
            Paragraph("<b>Calcul Distribué (PySpark)</b>", table_cell_bold),
            Paragraph("Agrégation massive sur 6 tables et calcul dynamique de 46 variables temporelles.", table_cell_style),
            Paragraph("Exécution visible sur l'interface Spark UI (DAG & Jobs).", table_cell_style)
        ],
        [
            Paragraph("<b>Intelligence Artificielle</b>", table_cell_bold),
            Paragraph("Intégration du modèle prédictif XGBoost du PFE (F1-Score: 88.7%) en inférence distribuée.", table_cell_style),
            Paragraph("Score de churn calculé et mis à jour en continu.", table_cell_style)
        ],
        [
            Paragraph("<b>Interface Décisionnelle</b>", table_cell_bold),
            Paragraph("Tableau de bord de monitoring temps réel avec système d'alerting rétention.", table_cell_style),
            Paragraph("Démonstration en direct d'injection de données et d'alertes instantanées.", table_cell_style)
        ],
    ]
    eval_table = Table(eval_data, colWidths=[38*mm, 78*mm, 58*mm])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
    ]))
    story.append(eval_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")

if __name__ == '__main__':
    out_dir = r"c:\Big_data_project"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "Plan_Projet_Big_Data_Telecom_Churn.pdf")
    build_pdf(pdf_path)
