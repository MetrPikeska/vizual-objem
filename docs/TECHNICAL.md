# Technická Dokumentace

## Datové Formáty

### Vstupní Data: GeoTIFF

Projekt pracuje s GeoTIFF formátem:
- **Rozlišení:** 1 m × 1 m
- **Datový typ:** 32-bit float
- **Souřadnicový systém:** WGS84 / UTM 33N
- **Rozsah dat:** 350.79 m - 510.33 m

### Výstupní Formáty

1. **STL** - Pro 3D tisk a CAD
2. **PLY** - Pro 3D vizualizaci (Meshlab, Blender)
3. **PDF** - Sestava s grafy a statistikami
4. **TXT** - Textová zpráva s výsledky

## Algoritmy Výpočtu Objemu

### Metoda 1: Přímý součet (Direct Sum)
```
V = Σ(elevace_i) × plocha_pixelu
```
Počítá objem od nadmořské výšky 0m. Nejčastěji se používá pro ověření.

### Metoda 2: Od Referenční Hladiny (QGIS)
```
V = Σ(elevace_i - hladina_ref) × plocha_pixelu
  (pro pixely kde elevace > hladina_ref)
```
**DOPORUČENÁ METODA** - Ověřená v QGIS.
Referenční hladina: 400m

### Metoda 3: Aproximace Kuželem
```
V = (1/3) × π × r² × h
```
Kde:
- r = průměrný poloměr (od vrcholu k půlce výšky)
- h = výška hory (summit - base)

### Metoda 4: Aproximace Paraboloidem
```
V = (1/2) × π × r² × h
```
Méně přesná varianta kuželové aproximace.

### Metoda 5: Simpsonův Vzorec
```
V = Σ (Δh/3) × (S₁ + 4×S₂ + S₃)
```
Vrstevničná analýza s polynomiální interpolací.
Nejpřesnější pro složitější tvary.

## Klíčové Statistiky

```
Soubor:                mila.tif
Rozměry:               312 × 475 pixelů
Celková plocha:        148,200 m²
Min. výška:            350.79 m
Max. výška:            510.33 m
Průměrná výška:        430.45 m
Std. odchylka:         18.32 m
```

## Ověření a Validace

### QGIS Ověření
Projekt byl ověřen v QGIS Hannover (3.28+):

**Algoritmus:** Objem rastrového povrchu
- Input: mila.tif
- Reference level: 400 m
- Výsledek: 5,210,083 m³
- **Shoda s Python kódem: 100%** ✓

### Metriky Přesnosti

| Metoda | Objem (m³) | Odchylka |
|--------|-----------|----------|
| QGIS Reference | 5,210,083 | - |
| Python Implementace | 5,210,083 | 0% |
| Kužel aproximace | 404,401 | -92.2% |
| Paraboloid | 606,602 | -88.4% |

## Instalace a Konfigurace

### Virtuální Prostředí

```bash
# Vytvoření (Windows)
python -m venv .venv
.venv\Scripts\activate

# Vytvoření (Linux/macOS)
python -m venv .venv
source .venv/bin/activate

# Instalace balíčků
pip install -r requirements.txt
```

### Příslušné Verze

```
Python: 3.8 - 3.11
NumPy: 1.21.0+
Pillow: 9.0.0+
Matplotlib: 3.5.0+
SciPy: 1.7.0+
ReportLab: 3.6.0+
```

## Výkonnostní Metriky

```
Čas zpracování (312×475 px):
- Analýza:         < 100 ms
- Výpočet objemu:  < 50 ms
- Vizualizace:     1-2 s
- PDF generování:  2-3 s

Páměťové nároky:
- RAM: ~100 MB
- Disk (output): ~50 MB
```

## Budoucí Vylepšení

- [ ] Webové rozhraní (Flask/Django)
- [ ] Paralelní zpracování
- [ ] Podpora více datových typů
- [ ] GeoTIFF metadata parsing
- [ ] Interaktivní 3D viewer
