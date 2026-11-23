import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Couleurs
    c_navy = RGBColor(26, 54, 93)       # #1A365D
    c_blue = RGBColor(43, 108, 176)     # #2B6CB0
    c_coral = RGBColor(221, 107, 32)    # #DD6B20
    c_dark = RGBColor(45, 55, 72)       # #2D3748
    c_gray = RGBColor(113, 128, 150)    # #718096
    c_card_bg = RGBColor(237, 242, 247) # #EDF2F7
    c_white = RGBColor(255, 255, 255)
    c_green = RGBColor(40, 167, 69)

    def add_header(slide, title_text, category_text="PROJET BIG DATA"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = c_coral
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = c_navy
        p_title.space_before = Pt(3)

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = c_blue
        line.line.color.rgb = c_blue

    def add_footer(slide):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.4))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = "Pipeline Big Data : Prédiction du Churn & Rétention Proactive  |  Ahmed Channoufi"
        p.font.size = Pt(10)
        p.font.color.rgb = c_gray

    # =========================================================================
    # SLIDE 1 : Titre / Page de Garde
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "PROJET ACADÉMIQUE BIG DATA"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = c_coral

    p1 = tf1.add_paragraph()
    p1.text = "Pipeline Big Data : Prédiction du Churn & Rétention Proactive"
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = c_white
    p1.space_before = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Architecture Scalable, Détection en Temps Réel & Recommandation d'Offres Anti-Churn"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(190, 227, 248)
    p2.space_before = Pt(14)

    cbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.2), Inches(11.333), Inches(1.2))
    cbox.fill.solid()
    cbox.fill.fore_color.rgb = RGBColor(43, 108, 176)
    cbox.line.color.rgb = RGBColor(66, 153, 225)
    ctf = cbox.text_frame
    ctf.margin_top = Inches(0.2)
    cp1 = ctf.paragraphs[0]
    cp1.text = "Présenté par : Ahmed Channoufi"
    cp1.font.size = Pt(16)
    cp1.font.bold = True
    cp1.font.color.rgb = c_white
    cp2 = ctf.add_paragraph()
    cp2.text = "Technologies Clés : Apache Parquet, XGBoost, Large-Scale ETL, Streamlit"
    cp2.font.size = Pt(13)
    cp2.font.color.rgb = c_white
    cp2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2 : Problématique : Le Facteur Temps (Vélocité & Rétention)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problématique : Pourquoi la Vélocité est Vitale ?")
    add_footer(s2)

    v_data = [
        ("1. La Contrainte Temporelle", "La Fenêtre d'Intervention (< 48h)", 
         "Un client qui réduit ses recharges ou ses appels décide de résilier en quelques jours. Si le traitement Big Data prend des heures, le client aura DÉJÀ acheté une SIM concurrente. L'inférence doit être instantanée pour agir à temps."),
        ("2. Le Volume & la Variété", "Des Millions d'Événements Dispersés", 
         "Pour prédire le Churn, il faut croiser 6 sources massives (appels, internet, recharges, USSD, contrats). Pandas sature et plante en MemoryError sur ces volumes industriels."),
        ("3. L'Action de Rétention", "Transformer la Prédiction en Solution", 
         "Détecter le Churn ne suffit pas : il faut immédiatement attribuer l'offre de rétention personnalisée (Pass Data, Bonus Recharge, Remise VIP) pour retenir le client.")
    ]

    for i, (title, sub, desc) in enumerate(v_data):
        left = Inches(0.8 + i * 3.95)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.9), Inches(3.8), Inches(4.7))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = RGBColor(203, 213, 224)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.25)
        ctf.margin_top = Inches(0.3)
        
        p = ctf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p_sub = ctf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = c_coral
        p_sub.space_before = Pt(4)
        
        p_desc = ctf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = c_dark
        p_desc.space_before = Pt(14)

    # =========================================================================
    # SLIDE 3 : Architecture Globale du Pipeline
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Architecture Technique du Pipeline (4 Couches)")
    add_footer(s3)

    layers = [
        ("1. Ingestion Multi-Sources", "Logs Bruts Télécom", "CDRs Appels (Sortant/Entrant), Sessions Data, Recharges, Forfaits USSD."),
        ("2. Moteur de Calcul Scalable", "Préparation & ETL", "Fusion et alignement dynamique des 46 variables comportementales par contrat client."),
        ("3. Inférence Machine Learning", "XGBoost & Offres", "Calcul de la probabilité de Churn en 0.07s et attribution automatique de l'offre de rétention."),
        ("4. Data Lake & Dashboard", "Parquet & Streamlit", "Persistance optimisée en Apache Parquet Snappy et monitoring web avec simulateur d'offres.")
    ]

    for i, (l_title, l_tool, l_desc) in enumerate(layers):
        top = Inches(1.8 + i * 1.25)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.1))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card_bg if i % 2 == 0 else RGBColor(235, 248, 255)
        box.line.color.rgb = c_blue if i % 2 != 0 else RGBColor(203, 213, 224)
        
        btf = box.text_frame
        btf.word_wrap = True
        btf.margin_left = Inches(0.4)
        btf.margin_top = Inches(0.18)
        
        p = btf.paragraphs[0]
        p.text = f"{l_title}   |   {l_tool}"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p2 = btf.add_paragraph()
        p2.text = l_desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 4 : La Stratégie d'Offres de Rétention
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "La Solution Métier : Offres de Rétention Personnalisées")
    add_footer(s4)

    offers = [
        ("🎁 Pass Data Boost", "Consommateurs Internet", 
         "• Déclencheur : Baisse du volume data mensuel.\n• Offre : 10 Go offerts immédiatement.\n• Impact : Réactivation de l'usage data 4G/5G."),
        ("💰 Bonus Recharge", "Clients Sensibles au Prix", 
         "• Déclencheur : Chute du montant des recharges.\n• Offre : Bonus +100% sur la prochaine recharge.\n• Impact : Barrière financière anti-départ."),
        ("👑 Pack Fidélité VIP", "Clients à Forte Ancienneté", 
         "• Déclencheur : Client > 2 ans à haute valeur.\n• Offre : Appels illimités week-end + Remise 25%.\n• Impact : Reconnaissance et attachement à la marque."),
        ("⚡ Forfait Duo Famille", "Clients Modérés / Voix", 
         "• Déclencheur : Baisse générale des appels voix.\n• Offre : Appels gratuits vers 2 numéros favoris.\n• Impact : Fixation du cercle relationnel.")
    ]

    for i, (o_title, o_target, o_desc) in enumerate(offers):
        left = Inches(0.8 + i * 2.95)
        cbox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.9), Inches(2.85), Inches(4.7))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = c_card_bg
        cbox.line.color.rgb = RGBColor(203, 213, 224)
        
        ctf = cbox.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.2)
        ctf.margin_top = Inches(0.25)
        
        p = ctf.paragraphs[0]
        p.text = o_title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p_c = ctf.add_paragraph()
        p_c.text = o_target
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = c_coral
        p_c.space_before = Pt(3)
        
        p_d = ctf.add_paragraph()
        p_d.text = o_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = c_dark
        p_d.space_before = Pt(12)

    # =========================================================================
    # SLIDE 5 : Résultats Expérimentaux (34 000 Clients)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Validation Expérimentale sur 34 000 Clients")
    add_footer(s5)

    kpi_boxes = [
        ("34 000", "Volume Clients Analysés", "Jeu de données réel de test", c_navy),
        ("0.07 s", "Vitesse d'Inférence ML", "~490 000 clients / seconde (Temps réel)", c_green),
        ("6 001", "Offres Anti-Churn Générées", "17.65% de clients ciblés avant départ", c_coral),
        ("78.1%", "Gain de Stockage Parquet", "Compression Snappy pour le Data Lake", c_blue)
    ]

    for i, (val, title, note, color) in enumerate(kpi_boxes):
        left = Inches(0.8 + i * 2.95)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.9), Inches(2.85), Inches(2.2))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card_bg
        box.line.color.rgb = color
        
        btf = box.text_frame
        btf.word_wrap = True
        btf.margin_left = btf.margin_right = Inches(0.15)
        btf.margin_top = Inches(0.2)
        
        p = btf.paragraphs[0]
        p.text = val
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = color
        p.alignment = PP_ALIGN.CENTER
        
        p2 = btf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = c_dark
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(4)
        
        p3 = btf.add_paragraph()
        p3.text = note
        p3.font.size = Pt(10)
        p3.font.color.rgb = c_gray
        p3.alignment = PP_ALIGN.CENTER
        p3.space_before = Pt(4)

    bot_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.4), Inches(11.7), Inches(2.3))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = RGBColor(235, 248, 255)
    bot_card.line.color.rgb = c_blue
    bctf = bot_card.text_frame
    bctf.margin_left = Inches(0.3)
    bctf.margin_top = Inches(0.25)

    bp1 = bctf.paragraphs[0]
    bp1.text = "🎯 Analyse Métier & Proactivité :"
    bp1.font.size = Pt(14)
    bp1.font.bold = True
    bp1.font.color.rgb = c_navy

    bp2 = bctf.add_paragraph()
    bp2.text = "• Rétention Proactive : 6 001 abonnés reçoivent automatiquement une offre avant de résilier.\n• Rapidité d'Exécution : En moins d'un dixième de seconde, la flotte complète est scorée et segmentée.\n• Rentabilité Directe : Préserver 6 001 clients représente une économie financière majeure pour l'opérateur."
    bp2.font.size = Pt(12)
    bp2.font.color.rgb = c_dark
    bp2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6 : Benchmark Big Data (CSV vs Parquet)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Benchmark Expérimental : Format CSV vs Apache Parquet")
    add_footer(s6)

    rows = 5
    cols = 4
    table_shape = s6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.9), Inches(11.7), Inches(4.5))
    table = table_shape.table

    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(2.8)
    table.columns[3].width = Inches(3.4)

    t_data = [
        ["Métrique Évaluée", "Format CSV Classique", "Format Apache Parquet", "Bénéfice & Impact Big Data"],
        ["Taille sur Disque", "2.51 MB", "0.55 MB", "📉 Réduction de 78.1% de l'espace disque"],
        ["Temps d'Écriture", "124.5 secondes (~2 min)", "0.029 seconde", "🚀 Parquet est plus de 4 000x plus rapide"],
        ["Mode d'Organisation", "Ligne par ligne (Texte brut)", "Colonnaire compressé Snappy", "🎯 Standard officiel des Data Lakes"],
        ["Temps de Réaction", "Trop lent pour la rétention", "Instantané (< 48h Time-to-Action)", "⚡ Permet de sauver le client à temps"]
    ]

    for r_idx, row in enumerate(t_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = c_navy
                p.font.bold = True
                p.font.color.rgb = c_white
                p.font.size = Pt(13)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = c_white if r_idx % 2 != 0 else c_card_bg
                p.font.color.rgb = c_dark
                p.font.size = Pt(12)
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = c_navy

    # =========================================================================
    # SLIDE 7 : Démonstration du Dashboard & Simulateur d'Offres
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Dashboard & Simulateur de Rétention Proactive")
    add_footer(s7)

    d_features = [
        ("📊 KPIs en Direct", "Affichage instantané du volume de clients analysés, du nombre de churners et du taux de churn global."),
        ("🎯 Offres Recommandées", "Chaque client à risque dispose d'une offre personnalisée intégrée directement dans le tableau."),
        ("🎛️ Simulateur d'Offres (What-If)", "Module interactif permettant de sélectionner un client critique, de lui appliquer une offre et d'observer la chute de son risque de Churn."),
        ("⚡ Module Benchmark Intégré", "Comparatif dynamique CSV vs Parquet démontrant la nécessité du stockage colonnaire."),
        ("📥 Export pour Équipe Marketing", "Téléchargement en 1 clic de la liste des contrats ciblés avec leurs offres pour l'envoi immédiat de SMS promotionnels.")
    ]

    for i, (f_title, f_desc) in enumerate(d_features):
        top = Inches(1.8 + i * 1.0)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(0.88))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = c_blue if i == 2 else RGBColor(203, 213, 224)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.3)
        ctf.margin_top = Inches(0.15)
        
        p = ctf.paragraphs[0]
        p.text = f"{f_title} : "
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        run = p.add_run()
        run.text = f_desc
        run.font.bold = False
        run.font.color.rgb = c_dark
        run.font.size = Pt(12)

    # =========================================================================
    # SLIDE 8 : Conclusion & Bilan
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Conclusion & Valeur Ajoutée du Projet")
    add_footer(s8)

    c_left = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.7), Inches(4.7))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = RGBColor(235, 248, 255)
    c_left.line.color.rgb = c_blue
    ltf = c_left.text_frame
    ltf.margin_left = ltf.margin_right = Inches(0.35)
    ltf.margin_top = Inches(0.3)

    lp = ltf.paragraphs[0]
    lp.text = "✅ Valeur Technique Big Data :"
    lp.font.size = Pt(18)
    lp.font.bold = True
    lp.font.color.rgb = c_navy

    lp2 = ltf.add_paragraph()
    lp2.text = (
        "• Vélocité Maximale : Inférence en 0.07 seconde (~490 000 clients/sec), respectant la fenêtre critique d'intervention.\n\n"
        "• Stockage Optimisé : Gain de 78% de place disque grâce au format colonnaire Apache Parquet Snappy.\n\n"
        "• Scalabilité : Pipeline prêt à traiter des millions de CDRs quotidiens sans saturer la mémoire RAM."
    )
    lp2.font.size = Pt(12)
    lp2.font.color.rgb = c_dark
    lp2.space_before = Pt(14)

    c_right = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.7))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = c_card_bg
    c_right.line.color.rgb = c_coral
    rtf = c_right.text_frame
    rtf.margin_left = rtf.margin_right = Inches(0.35)
    rtf.margin_top = Inches(0.3)

    rp = rtf.paragraphs[0]
    rp.text = "🎯 Valeur Métier & Rétention :"
    rp.font.size = Pt(18)
    rp.font.bold = True
    rp.font.color.rgb = c_navy

    rp2 = rtf.add_paragraph()
    rp2.text = (
        "• Rétention Proactive : Sauver les clients AVANT leur départ effectif vers un opérateur concurrent.\n\n"
        "• Ciblage Intelligent : Attribution automatique d'offres adaptées au profil de consommation (Data, Recharge, VIP).\n\n"
        "• Simulation Décisionnelle : Outil What-If interactif pour mesurer la baisse du risque avant de lancer la campagne."
    )
    rp2.font.size = Pt(12)
    rp2.font.color.rgb = c_dark
    rp2.space_before = Pt(14)

    prs.save(output_path)
    print(f"Presentation regenerated at : {output_path}")

if __name__ == "__main__":
    target_main = r"c:\Big_data_project\Presentation_Big_Data_Telecom_Churn.pptx"
    target_v2 = r"c:\Big_data_project\Presentation_Big_Data_Telecom_Churn_v2.pptx"
    try:
        create_presentation(target_main)
        print(f"Succes: {target_main}")
    except PermissionError:
        print(f"Notice: {target_main} est ouvert dans PowerPoint. Sauvegarde sous version V2...")
        create_presentation(target_v2)
        print(f"Succes V2: {target_v2}")
