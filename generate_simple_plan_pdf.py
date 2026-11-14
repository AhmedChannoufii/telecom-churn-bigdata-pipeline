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
        
        # Header (page 2)
        if self._pageNumber > 1:
            self.drawString(16 * mm, 287 * mm, "PROJET BIG DATA : PIPELINE PYSPARK TÉLÉCOM")
            self.setFont("Helvetica", 8)
            self.drawRightString(194 * mm, 287 * mm, "Plan d'Exécution & Guide de Soutenance")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(16 * mm, 284 * mm, 194 * mm, 284 * mm)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(16 * mm, 12 * mm, 194 * mm, 12 * mm)
        self.setFont("Helvetica", 8)
        self.drawString(16 * mm, 8 * mm, "Projet Big Data - Ahmed Channoufi")
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(194 * mm, 8 * mm, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#1A365D")   # Deep navy
    secondary = colors.HexColor("#2B6CB0") # Blue
    text_dark = colors.HexColor("#2D3748") # Charcoal
    bg_light = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#CBD5E0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=primary,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=secondary,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=text_dark,
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=1.5
    )

    box_text_style = ParagraphStyle(
        'BoxText',
        parent=body_style,
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1A365D")
    )

    speech_text_style = ParagraphStyle(
        'SpeechText',
        parent=body_style,
        fontName='Helvetica-Oblique',
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
        leading=10.5,
        textColor=text_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=primary
    )

    story = []

    # === PAGE 1 : Architecture & Les 4 Étapes ===
    story.append(Paragraph("PLAN DE PROJET BIG DATA (VERSION SIMPLE & COMPLÈTE)", title_style))
    story.append(Paragraph("Pipeline PySpark & Machine Learning pour la Prédiction du Churn Télécom", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=secondary, spaceBefore=0, spaceAfter=6))

    # Meta card
    meta_data = [
        [
            Paragraph("<b>Étudiant :</b> Ahmed Channoufi", body_style),
            Paragraph("<b>Dépôt GitHub :</b> telecom-churn-bigdata-pipeline", body_style)
        ],
        [
            Paragraph("<b>Technologie Principale :</b> Apache Spark (PySpark)", body_style),
            Paragraph("<b>Format de Stockage :</b> Apache Parquet (Data Lake)", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[90*mm, 90*mm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 0.8, border_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # 1. Idée Clé Simple
    story.append(Paragraph("1. L'Idée Simple du Projet (Ce qu'on résout)", h1_style))
    simple_box = [[
        Paragraph(
            "• <b>Le Problème :</b> Dans un opérateur télécom (Tunisie Telecom), les fichiers de consommation (appels, internet, recharges) contiennent des millions de lignes. Un script classique avec Pandas sature la mémoire vive et plante.<br/>"
            "• <b>La Solution Big Data :</b> On utilise <b>Apache Spark (PySpark)</b> pour traiter ces données volumineuses de façon distribuée, rapide et efficace.<br/>"
            "• <b>La Valeur Métier :</b> Le modèle Machine Learning prédit les clients qui risquent de partir (Churn), sauvegardés en format <b>Parquet</b> et visualisés sur un <b>Dashboard Streamlit</b>.",
            box_text_style
        )
    ]]
    box_table = Table(simple_box, colWidths=[180*mm])
    box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#BEE3F8")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(box_table)
    story.append(Spacer(1, 4))

    # 2. Architecture en 4 Blocs
    story.append(Paragraph("2. L'Architecture en 4 Blocs Simples", h1_style))
    
    arch_data = [
        [Paragraph("Étape", table_header_style), Paragraph("Outil / Fichier", table_header_style), Paragraph("Rôle dans le Projet", table_header_style)],
        [
            Paragraph("<b>1. Données Brutes</b>", table_cell_bold),
            Paragraph("Fichiers CSV Télécom", table_cell_style),
            Paragraph("Logs de consommation : appels sortants/entrants, volume internet, recharges et profils clients.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Traitement Big Data</b>", table_cell_bold),
            Paragraph("<b>Apache Spark (PySpark)</b>", table_cell_style),
            Paragraph("Calcul distribué avec les <b>Spark DataFrames</b> : agrégations par client et jointures par <code>CODE_CONTRAT</code>.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Prédiction ML</b>", table_cell_bold),
            Paragraph("Modèle XGBoost + Parquet", table_cell_style),
            Paragraph("Calcul du score de Churn par client et persistance dans un fichier <b>Parquet</b> compressé.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Visualisation</b>", table_cell_bold),
            Paragraph("Dashboard Streamlit", table_cell_style),
            Paragraph("Affichage clair : taux de churn global et liste des clients à risque à contacter en priorité.", table_cell_style)
        ]
    ]
    arch_table = Table(arch_data, colWidths=[32*mm, 46*mm, 102*mm])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 4))

    # 3. Les 4 Étapes de Réalisation
    story.append(Paragraph("3. Les 4 Étapes Simples de Réalisation", h1_style))

    steps = [
        (
            "Étape 1 : Préparation du Projet et des Artefacts PFE",
            [
                "Mise en place de l'arborescence : <code>data/</code>, <code>models/</code>, <code>src/</code>.",
                "Importation des artefacts ML validés du PFE (<code>xgb_model.pkl</code>, <code>scaler.pkl</code>, <code>model_config.json</code>)."
            ]
        ),
        (
            "Étape 2 : Le Script PySpark ETL (Traitement Distribué)",
            [
                "Charger les fichiers CSV dans des <b>Spark DataFrames</b>.",
                "Agrégation par contrat : somme des durées d'appels, volume internet consommé, montant des recharges.",
                "Jointure rapide de l'ensemble des tables sur la clé unique <code>CODE_CONTRAT</code>."
            ]
        ),
        (
            "Étape 3 : Inférence du Modèle & Export au Format Parquet",
            [
                "Application du modèle XGBoost pour attribuer à chaque client un score de Churn (probabilité entre 0 et 1).",
                "Sauvegarde des résultats au format <b>Parquet</b> (format standard de l'industrie Big Data, compact et ultra-rapide)."
            ]
        ),
        (
            "Étape 4 : Dashboard Décisionnel avec Streamlit",
            [
                "Création d'une interface web épurée qui lit directement le fichier Parquet généré.",
                "Visualisation graphique du taux de désabonnement et filtre des clients les plus critiques.",
                "Lancement en une ligne de commande : <code>streamlit run app.py</code>."
            ]
        )
    ]

    for title, bullets in steps:
        story.append(Paragraph(title, h2_style))
        for bullet in bullets:
            story.append(Paragraph(f"• {bullet}", bullet_style))
        story.append(Spacer(1, 2))

    # === FORCE PAGE BREAK -> EXACTLY PAGE 2 ===
    story.append(PageBreak())

    # === PAGE 2 : Guide Oral & Questions/Réponses ===
    story.append(Paragraph("4. Guide de Présentation Orale (Ce que tu dis à la Professeure)", h1_style))
    story.append(Paragraph(
        "Ce discours est conçu pour être fluide, professionnel et facile à retenir mot à mot :",
        body_style
    ))

    discours = [
        (
            "1. Introduction (30 secondes) :",
            "« Madame, pour mon projet Big Data, j'ai voulu faire le pont avec mon sujet de PFE sur la prédiction du Churn Télécom. Dans la réalité d'un opérateur comme Tunisie Telecom, les volumes de données d'appels, d'internet et de recharges se comptent en millions de transactions quotidiennes. Un script classique avec Pandas est incapable de monter en charge et sature rapidement la mémoire de la machine. »"
        ),
        (
            "2. Le Cœur Big Data avec PySpark (1 minute) :",
            "« C'est pour cette raison que j'ai développé une solution basée sur <b>Apache Spark (PySpark)</b>. Spark me permet de :<br/>"
            "• Charger de gros volumes de données en parallèle via les <b>Spark DataFrames</b>.<br/>"
            "• Réaliser des calculs d'agrégation distribués (somme de consommation, fréquence des recharges, volume data).<br/>"
            "• Réaliser des jointures optimisées entre plusieurs sources de données grâce au <code>CODE_CONTRAT</code>. »"
        ),
        (
            "3. La Prédiction & le Stockage Parquet (30 secondes) :",
            "« Une fois les variables calculées par PySpark, j'applique mon modèle Machine Learning (XGBoost) pour évaluer la probabilité de résiliation de chaque client. Les prédictions sont ensuite stockées au format <b>Parquet</b>, le format standard du Big Data, qui offre une excellente compression et des temps de lecture record par rapport à un simple CSV. »"
        ),
        (
            "4. La Démonstration du Dashboard (1 minute) :",
            "« Enfin, j'ai développé une interface simple avec <b>Streamlit</b>. En un clic, l'équipe commerciale peut visualiser le taux de Churn global et cibler immédiatement les clients prioritaires avec des offres de fidélisation adaptées. »"
        )
    ]

    for title, text in discours:
        speech_box = []
        speech_box.append(Paragraph(f"<b>{title}</b>", h2_style))
        speech_box.append(Paragraph(f"<i>{text}</i>", speech_text_style))
        speech_box.append(Spacer(1, 3))
        story.append(KeepTogether(speech_box))

    story.append(Spacer(1, 6))

    # 5. Questions Probables de la Professeure & Réponses
    story.append(Paragraph("5. Les Questions Fréquentes de la Professeure & Tes Réponses", h1_style))

    qa_data = [
        [Paragraph("Question Possible de la Professeure", table_header_style), Paragraph("Ta Réponse Claire & Précise", table_header_style)],
        [
            Paragraph("<b>« Pourquoi avoir choisi PySpark au lieu de Pandas ? »</b>", table_cell_bold),
            Paragraph("Pandas charge tout en RAM sur un seul cœur CPU, ce qui bloque dès que les données dépassent la mémoire. PySpark distribue les calculs sur plusieurs cœurs ou machines sans saturer la mémoire.", table_cell_style)
        ],
        [
            Paragraph("<b>« Pourquoi sauvegarder en Parquet plutôt qu'en CSV ? »</b>", table_cell_bold),
            Paragraph("Parquet est un format colonnaire compressé. Il réduit la taille du stockage jusqu'à 75% et permet de lire uniquement les colonnes nécessaires sans scanner tout le fichier.", table_cell_style)
        ],
        [
            Paragraph("<b>« Comment le modèle ML s'intègre-t-il avec Spark ? »</b>", table_cell_bold),
            Paragraph("Spark prépare et agrège la donnée brute pour construire les features exactes attendues, puis le modèle applique la formule prédictive pour noter chaque client.", table_cell_style)
        ],
        [
            Paragraph("<b>« Est-ce que ce pipeline est réutilisable chaque mois ? »</b>", table_cell_bold),
            Paragraph("Oui, il suffit de déposer les nouveaux fichiers mensuels dans le dossier et de relancer le script PySpark pour obtenir les nouvelles prédictions actualisées.", table_cell_style)
        ]
    ]
    qa_table = Table(qa_data, colWidths=[65*mm, 115*mm])
    qa_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
    ]))
    story.append(qa_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Simple 2-page PDF generated at: {filename}")

if __name__ == '__main__':
    out_dir = r"c:\Big_data_project"
    pdf_path = os.path.join(out_dir, "Plan_Projet_Big_Data_Version_Simple.pdf")
    build_pdf(pdf_path)
