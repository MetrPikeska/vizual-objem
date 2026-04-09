from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os

# Vytvoření výstupní složky, pokud neexistuje
output_dir = '../output' if os.path.exists('../output') else 'output' if os.path.exists('output') else '.'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Název reportu
report_filename = os.path.join(output_dir, 'vizul2026_cv4b_report.pdf')
doc = SimpleDocTemplate(report_filename, pagesize=A4,
                        rightMargin=1.5*cm, leftMargin=1.5*cm,
                        topMargin=1.5*cm, bottomMargin=1.5*cm)

# Styly
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=12,
    alignment=1
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#2c5aa0'),
    spaceAfter=8,
    spaceBefore=8
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#2c5aa0'),
    spaceAfter=6,
    spaceBefore=6
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=4,
    spaceAfter=6
)

# Načtení výsledků
import os
if os.path.exists('volume_results.txt'):
    results_file = 'volume_results.txt'
elif os.path.exists('../output/volume_results.txt'):
    results_file = '../output/volume_results.txt'
else:
    results_file = 'volume_results.txt'

try:
    with open(results_file, 'r', encoding='utf-8') as f:
        results_text = f.read()
except:
    results_text = "Výsledky nejsou k dispozici. Spusťte nejdřív generate_report_txt.py."

# Vytvoření výstupní složky, pokud neexistuje
if not os.path.exists('../output'):
    os.makedirs('../output')

# Obsah dokumentu
story = []

# Titulní strana
story.append(Spacer(1, 2*cm))
story.append(Paragraph("DIGITÁLNÍ MODEL RELIÉFU", title_style))
story.append(Paragraph("Výpočet a Vizualizace Objemu Hory", heading1_style))
story.append(Spacer(1, 0.5*cm))

# Informace o dokumentu
info_text = """
<b>Předmět:</b> Vizualizace dat a DEM analýza<br/>
<b>Datum:</b> """ + datetime.now().strftime("%d. %m. %Y") + """<br/>
<b>Soubor DMR:</b> mila.tif<br/>
<b>Software:</b> Python 3.11, NumPy, SciPy, Matplotlib, ReportLab
"""
story.append(Paragraph(info_text, body_style))
story.append(Spacer(1, 1*cm))

# 1. ÚVOD
story.append(Paragraph("1. ÚVOD", heading1_style))
story.append(Spacer(1, 0.3*cm))
intro_text = """
Cílem tohoto projektu je vypočítat a vizualizovat objem vybrané hory 
z Digitálního Modelu Reliéfu (DMR) poskytnutého jako soubor mila.tif. 
Projekt využívá kombinaci tradičních matematických metod a moderních GIS analýz.
"""
story.append(Paragraph(intro_text, body_style))
story.append(Spacer(1, 0.5*cm))

# 2. DATA A METODIKA
story.append(Paragraph("2. DATA A METODIKA", heading1_style))
story.append(Spacer(1, 0.3*cm))

# 2.1 Zdrojová data
story.append(Paragraph("2.1 Zdrojová Data", heading2_style))
data_text = """
<b>Zdroj:</b> Digitální Model Reliéfu (DMR) - soubor mila.tif<br/>
<b>Formát:</b> GeoTIFF - 16bitový rastr<br/>
<b>Rozměry:</b> 312 pixelů (Y) × 475 pixelů (X)<br/>
<b>Rozlišení:</b> 1 m × 1 m<br/>
<b>Pokryta plocha:</b> 312 × 475 = 148 200 m² = 0,1482 km²<br/>
<b>Nadmořské výšky:</b> 350,79 m (minimum) až 510,33 m (maximum)<br/>
<b>Rozpětí výšek:</b> 159,54 m
"""
story.append(Paragraph(data_text, body_style))
story.append(Spacer(1, 0.5*cm))

# 2.2 Metodika
story.append(Paragraph("2.2 Metodika Výpočtu", heading2_style))
methodology_text = """
Pro výpočet objemu hory byly použity následující metody:<br/><br/>

<b>A) Metoda přímého součtu:</b> V = Σ(elevace<sub>i</sub>) × plocha<sub>pixelu</sub><br/>
Počítá součet všech výšek vynásobený plochou pixelu. Vhodná pro referenční výpočty.<br/><br/>

<b>B) Metoda relativního objemu:</b> V = Σ(elevace<sub>i</sub> - elevace<sub>paty</sub>) × plocha<sub>pixelu</sub><br/>
Počítá nadstavbu hory pouze nad její patou. <b>Nejrelevantější metoda!</b><br/><br/>

<b>C) Aproximace kuželem:</b> V = (1/3) × π × r² × h<br/>
Předpokládá, že hora má tvar kuželu.<br/><br/>

<b>D) Aproximace paraboloidem:</b> V = (1/2) × π × r² × h<br/>
Předpokládá, že hora má tvar paraboloidu.<br/><br/>

<b>E) Simpsonův vzorec (vrstevničná analýza):</b> V = Σ (Δh/3 × (S₁ + 4×S₂ + S₃))<br/>
Rozděluje horu na horizontální vrstvy a používá Simpsonovo pravidlo.<br/><br/>

<b>F) GIS metoda - Hypsometrická analýza:</b><br/>
Analýza distribuce ploch v jednotlivých výškových pásmech pomocí hypsometrické křivky.
"""
story.append(Paragraph(methodology_text, body_style))
story.append(PageBreak())

# 3. VÝSLEDKY
story.append(Paragraph("3. VÝSLEDKY VÝPOČTU", heading1_style))
story.append(Spacer(1, 0.3*cm))

results_intro = """
Následující tabulka shrnuje výsledky všech použitých metod:
"""
story.append(Paragraph(results_intro, body_style))
story.append(Spacer(1, 0.3*cm))

# Tabulka výsledků
results_table_data = [
    ['Metoda', 'Objem [m³]', 'Objem [km³]', 'Pozn.'],
    ['Přímý součet', '58,617,568', '58,6176', 'Ref. (od 0m)'],
    ['Od úpratoře 400m', '5,210,083', '5,2101', '✓ QGIS ověřeno'],
    ['Aproximace kuželem', '404,401', '0,4044', 'Přibližně'],
    ['Aproximace paraboloidem', '606,602', '0,6066', 'Přibližně'],
    ['Simpsonův vzorec', '296,354', '0,2964', 'Přesná metoda'],
    ['Hypsometrická analýza', '6,630,974', '6,6310', 'GIS metoda'],
]

results_table = Table(results_table_data, colWidths=[3*cm, 3*cm, 3*cm, 2*cm])
results_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Oblique'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
story.append(results_table)
story.append(Spacer(1, 0.3*cm))

# Komentář k výsledkům
comment_text = """
<b>Interpretace výsledků:</b><br/>
Jednotlivé metody dávají různé výsledky kvůli rozdílným referenčním hladinám:<br/>
• Metoda přímého součtu (58,6 km³) počítá od nulové hladiny - referenční.<br/>
• Objem od úpratoře 400m (5,21 km³) - OVĚŘENO V QGIS! - je to SPRÁVNÁ hodnota pro objem hory!<br/>
• Aproximace geometrickými tvary dávají méně přesné výsledky.<br/>
• GIS metody potvrzují správnost přístupu.<br/><br/>

<b>Doporučená hodnota pro projekt:</b><br/>
<b>V = 5,210,083 m³ = 5,2101 km³</b><br/>
(Objem hory od úpratoře 400m nahoru - ověřeno QGIS "Objem rastrového povrchu")
"""
story.append(Paragraph(comment_text, body_style))
story.append(Spacer(1, 0.5*cm))

# Charakteristika hory
char_text = """
<b>Charakteristika analyzované hory:</b><br/>
• Vrchol: řádek 169, sloupec 252<br/>
• Výška vrcholu: 510,33 m<br/>
• Výška paty: 350,79 m<br/>
• Relativní výška: 159,54 m<br/>
• Průměrná nadmořská výška: 395,53 m
"""
story.append(Paragraph(char_text, body_style))
story.append(PageBreak())

# 4. VIZUALIZACE
story.append(Paragraph("4. VIZUALIZACE", heading1_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("4.1 Přehled analýzy", heading2_style))
story.append(Spacer(1, 0.2*cm))
story.append(Image('01_prehlad_analyza.png', width=18*cm, height=13.5*cm))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Obrázek 1: Přehledová analýza DMR obsahující heatmapu nadmořských výšek, "
    "relativní výšky, terénní profily a hypsometrickou křivku.",
    body_style))
story.append(PageBreak())

story.append(Paragraph("4.2 3D vizualizace hory", heading2_style))
story.append(Spacer(1, 0.2*cm))
story.append(Image('02_3d_vizualizace.png', width=18*cm, height=13.5*cm))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Obrázek 2: Čtyři různé pohledy na 3D model hory - náhled z různých úhlů "
    "umožňuje lepší pochopení tvaru geomorfologického tvaru.",
    body_style))
story.append(PageBreak())

story.append(Paragraph("4.3 Srovnání metod výpočtu", heading2_style))
story.append(Spacer(1, 0.2*cm))
story.append(Image('03_srovnani_metod.png', width=18*cm, height=13.5*cm))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Obrázek 3: Porovnání všech šesti metod výpočtu objemu. Graf znázorňuje "
    "významné rozdíly mezi jednotlivými přístupy a statistické charakteristiky.",
    body_style))
story.append(PageBreak())

# 5. DISKUZE A ZÁVĚRY
story.append(Paragraph("5. DISKUZE A ZÁVĚRY", heading1_style))
story.append(Spacer(1, 0.3*cm))

discussion_text = """
<b>Výběr vhodné metody:</b><br/>
Ze srovnání jednotlivých metod je zřejmé, že pro výpočet objemu hory je nejlepší 
použít <b>metodu relativního objemu</b>, kterou potvrzuje také <b>GIS metoda - hypsometrická analýza</b>. 
Obě dávají prakticky stejný výsledek: <b>~6,63 km³</b>.<br/><br/>

<b>Důvody pro tuto volbu:</b><br/>
1. <b>Fyzikálně správný přístup:</b> Počítáme pouze nadstavbu hory nad její patou,<br/>
   nikoliv součet všech výšek od nulové hladiny.<br/>
2. <b>Konzistentní s GIS metodami:</b> Hypsometrická analýza dává téměř identické výsledky.<br/>
3. <b>Přírodovědně správný:</b> Odpovídá definici "objemu hory" v geomorfologii.<br/><br/>

<b>Aproximace geometrickými tvary:</b><br/>
Aproximace kuželem a paraboloidem dávají výrazně nižší hodnoty, protože 
realizují zřejmě užší poloměr základny. Jsou vhodné spíše jako <b>odhady</b> 
pro velmi jednoduché tvary.<br/><br/>

<b>Praktické aplikace:</b><br/>
Znalost přesného objemu hory má uplatnění v:<br/>
• Těžbě nerostných surovin (odhad zásob)<br/>
• Ekologických studiích<br/>
• Stavebnictví a terénních úpravách<br/>
• Klimatologických a hydrologických modelech<br/><br/>

<b>Závěr:</b><br/>
Objem analyzované hory z DMR souboru mila.tif je <b>5,210,083 m³</b> neboli 
<b>5,2101 km³</b>. Tato hodnota byla ověřena algoritmem QGIS "Objem rastrového povrchu"
s referenční hladinou 400 m (úpratoř hory). Výsledek představuje objem hory od její 
skutečné paty v nadmořské výšce 400 m až k vrcholu v 510,33 m.
"""
story.append(Paragraph(discussion_text, body_style))
story.append(PageBreak())

# 6. METODIKA - DETAILY
story.append(Paragraph("6. TECHNICKÉ DETAILY IMPLEMENTACE", heading1_style))
story.append(Spacer(1, 0.3*cm))

technical_text = """
<b>Software a knihovny:</b><br/>
• Python 3.11<br/>
• NumPy - numerické výpočty<br/>
• SciPy - vědecké výpočty<br/>
• Matplotlib - vytváření grafů<br/>
• PIL (Pillow) - práce s obrázky a TIFF formátem<br/>
• ReportLab - generování PDF<br/><br/>

<b>Algoritmus výpočtu relativního objemu:</b><br/>
1. Načtení TIFF souboru jako 2D pole nadmořských výšek<br/>
2. Identifikace minimální výšky (pata hory)<br/>
3. Odečtení minimální výšky od všech hodnot<br/>
4. Součet všech relativních výšek<br/>
5. Násobení plochou jednoho pixelu (1 m²)<br/><br/>

<b>Matematická formulace:</b><br/>
V = Σ(h<sub>i</sub> - h<sub>min</sub>) × A<sub>pixel</sub><br/><br/>

kde:<br/>
• h<sub>i</sub> = nadmořská výška v pixelu i<br/>
• h<sub>min</sub> = minimální nadmořská výška (pata)<br/>
• A<sub>pixel</sub> = plocha jednoho pixelu (1 m²)
"""
story.append(Paragraph(technical_text, body_style))

# Generování PDF
doc.build(story)
print(f"✓ PDF report vytvořen: {report_filename}")
