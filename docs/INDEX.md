# 📖 Index Dokumentace

Úplný přehled dokumentace a souborů projektu.

## 🏠 Hlavní Dokumentace

| Soubor | Účel |
|--------|------|
| [README.md](../README.md) | Hlavní dokumentace - Úvod a přehled projektu |
| [LICENSE](../LICENSE) | MIT License |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Pokyny pro přispívání |
| [requirements.txt](../requirements.txt) | Python závislosti |

## 📚 Podrobná Dokumentace

| Soubor | Obsah |
|--------|-------|
| [QUICKSTART.md](QUICKSTART.md) | Rychlý start - Jak začít |
| [TECHNICAL.md](TECHNICAL.md) | Technické detaily a algoritmy |
| INDEX.md | Tento soubor |

## 📁 Struktura Projektu

```
vizual-objem/
├── 📄 README.md              ← ZAČNĚTE ZDE
├── 📄 requirements.txt       
├── 📄 .gitignore            
├── 📄 LICENSE               
├── 📄 CONTRIBUTING.md       
├── 📄 mila.tif              (vstupní DEM data)
│
├── 📁 src/                  → Python skripty
│   ├── run_all.py           (spusť všechny analýzy)
│   ├── analyze_mountain.py  
│   ├── calculate_volume.py  
│   ├── visualizations.py    
│   ├── generate_report.py   
│   └── generate_report_txt.py
│
├── 📁 data/                 → Vstupní data
│   └── (mila.tif by měl být zde)
│
├── 📁 output/               → Vygenerované soubory
│   ├── volume_results.txt
│   ├── *.pdf               (PDF reporty)
│   ├── *.stl               (3D modely)
│   └── *.ply               (3D data)
│
├── 📁 assets/               → Obrázky a média
│   ├── 01_prehlad_analyza.png
│   ├── 02_3d_vizualizace.png
│   ├── 03_srovnani_metod.png
│   ├── hory_vizualizace.png
│   └── Map.jpg
│
└── 📁 docs/                 → Dokumentace
    ├── QUICKSTART.md
    ├── TECHNICAL.md
    └── INDEX.md             (tento soubor)
```

## 🚀 Nástroje a Skripty

### Spouštění Analýz

```bash
# Všechny analýzy najednou
python src/run_all.py

# Jednotlivé skripty
python src/analyze_mountain.py      # Analýza reliéfu
python src/calculate_volume.py      # Výpočet objemu
python src/visualizations.py        # Vytvoření grafů
python src/generate_report_txt.py   # Textový report
python src/generate_report.py       # PDF report
```

### Průvodce Jednotlivými Úkoly

1. **Instalace a Setup** → [QUICKSTART.md](QUICKSTART.md)
2. **Spuštění Projektu** → [QUICKSTART.md](QUICKSTART.md)
3. **Technické Detaily** → [TECHNICAL.md](TECHNICAL.md)
4. **Algoritmické Vysvětlení** → [TECHNICAL.md](TECHNICAL.md)

## 📊 Výstupní Formáty

| Typ | Lokace | Popis |
|-----|--------|-------|
| PNG | `assets/` | Vizualizace a grafy |
| PDF | `output/` | Profesionální report |
| TXT | `output/` | Textová forma reportu |
| STL | `output/` | 3D model pro tisk |
| PLY | `output/` | 3D data pro vizualizaci |

## 🔍 Hledáte...

### ...jak začít?
→ Přečtěte si [README.md](../README.md) a [QUICKSTART.md](QUICKSTART.md)

### ...informace o instalaci?
→ [QUICKSTART.md](QUICKSTART.md) - Instalace a Spuštění

### ...technické podrobnosti?
→ [TECHNICAL.md](TECHNICAL.md) - Algoritmy a Implementace

### ...jak přispět?
→ [CONTRIBUTING.md](../CONTRIBUTING.md) - Pokyny pro přispívání

### ...specifikace projektu?
→ [TECHNICAL.md](TECHNICAL.md) - Technická Dokumentace

### ...výstupní soubory?
→ `output/` složka nebo [README.md](../README.md) - Výsledky

## ✅ Checklist pro Nové Uživatele

- [ ] Přečtěte si [README.md](../README.md)
- [ ] Nainstalujte Python 3.8+
- [ ] Následujte [QUICKSTART.md](QUICKSTART.md)
- [ ] Spusťte `python src/run_all.py`
- [ ] Kontrola výstupů v `output/` a `assets/`
- [ ] Ověřte v QGIS (volitelně)

## 📞 Kontakt a Podpora

Autor: **Michal Pikeska** (MetrPikeska)
Obor: SKOLA_NTB - 4. LS - VIZUL

---

**Poslední aktualizace:** 09. 04. 2026  
**Status:** ✅ Kompletní a prověřený
