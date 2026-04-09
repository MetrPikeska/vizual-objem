#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hlavní skript - Spuštění všech analýz a generování reportů
Digitální Model Reliéfu - Analýza Hory
"""

import os
import sys
import subprocess
import time

def print_header(title):
    """Tisk záhlaví"""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")

def run_script(script_name, description):
    """Spuštění Python skriptu s error handlingem"""
    print(f"[{time.strftime('%H:%M:%S')}] Spouštím: {description}...")
    try:
        result = subprocess.run([sys.executable, script_name], capture_output=False)
        if result.returncode == 0:
            print(f"✓ {description} - HOTOVO\n")
            return True
        else:
            print(f"✗ {description} - CHYBA (exit code: {result.returncode})\n")
            return False
    except Exception as e:
        print(f"✗ {description} - CHYBA: {str(e)}\n")
        return False

def main():
    """Hlavní funkce"""
    print_header("DIGITÁLNÍ MODEL RELIÉFU - ANALÝZA HORY")
    
    # Příprava
    print("📋 Příprava analýzy...\n")
    
    # Přepnutí do src directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) != 'src':
        if os.path.exists(os.path.join(script_dir, 'src')):
            os.chdir(os.path.join(script_dir, 'src'))
    
    # Spuštění skriptů
    scripts = [
        ('analyze_mountain.py', '📊 Analýza digitálního modelu reliéfu'),
        ('calculate_volume.py', '📐 Výpočet objemu hory'),
        ('visualizations.py', '🎨 Vytváření vizualizací'),
        ('generate_report_txt.py', '📄 Generování textového reportu'),
        ('generate_report.py', '📕 Generování PDF reportu'),
    ]
    
    results = []
    start_time = time.time()
    
    for script_name, description in scripts:
        if os.path.exists(script_name):
            results.append(run_script(script_name, description))
        else:
            print(f"⚠ Soubor {script_name} nebyl nalezen!\n")
            results.append(False)
    
    # Shrnutí výsledků
    elapsed_time = time.time() - start_time
    print_header("SHRNUTÍ VÝSLEDKŮ")
    
    for (_, desc), success in zip(scripts, results):
        status = "✓ HOTOVO" if success else "✗ CHYBA"
        print(f"{status}: {desc}")
    
    total = len(results)
    successful = sum(results)
    failed = total - successful
    
    print(f"\n{'─'*70}")
    print(f"Celkově: {successful}/{total} skriptů uspělo")
    print(f"Čas zpracování: {elapsed_time:.2f} sekund")
    print(f"{'─'*70}\n")
    
    # Umístění výstupů
    print("📂 Výstupní soubory:")
    print("   • Vizualizace: ../assets/ (PNG obrázky)")
    print("   • Reporty: ../output/ (PDF, TXT, STL, PLY)")
    
    print_header("ANALÝZA DOKONČENA")
    
    if failed == 0:
        print("✓ Všechny analýzy proběhly úspěšně!")
        return 0
    else:
        print(f"⚠ {failed} skriptů se nezdařilo. Zkontrolujte chyby výše.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
