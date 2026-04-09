# Rychlý Start

## Instalace a Spuštění

### 1. Příprava prostředí

```bash
# Aktivace virtuálního prostředí
.venv\Scripts\activate

# Instalace závislostí (pokud Already installed ještě nebyly)
pip install -r requirements.txt
```

### 2. Spuštění všech analýz

```bash
# Detailní analýza hory
python src/analyze_mountain.py

# Výpočet objemu
python src/calculate_volume.py

# Vytvoření vizualizací
python src/visualizations.py

# Generování reportů
python src/generate_report.py
python src/generate_report_txt.py
```

### 3. Kontrola výsledků

Výsledky se nacházejí v `output/` složce:
- `volume_results.txt` - Výsledky výpočtů
- `*.pdf` - Vygenerované PDF reporty
- `*.stl` / `*.ply` - 3D modely

## Vstupní Data

Projekt očekává GeoTIFF soubor s názvem `mila.tif` v kořenovém adresáři nebo v `data/` složce.

```
Očekávaná struktura:
mila.tif (nebo data/mila.tif)
```

## Ověření v QGIS

1. Otevřete QGIS
2. Načtěte projekt: `data/projekt.qgz`
3. Načtěte layer: `data/mila.tif`
4. K ověření objemu použijte:
   - Menu: Raster → Analysis → Raster Surface Volume
   - Zaškrtni: Reference level = 400m
   - Porovnejte výsledek s `output/volume_results.txt`

## Troubleshooting

### Chyba: "mila.tif not found"
- Zkontrolujte, že soubor existuje v kořenovém adresáři nebo v `data/` složce
- Ověřte cestu v Python skriptech

### Vizualizace se neotevírá
- Ujistěte se, že matplotlib backend je správně nakonfigurován
- Zkuste přidat `plt.show()` na konec skriptů

### Instalace balíčků se nezdaří
- Aktualizujte pip: `python -m pip install --upgrade pip`
- Zkuste instalaci jednotlivých balíčků
