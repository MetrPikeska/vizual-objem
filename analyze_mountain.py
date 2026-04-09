import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from scipy import ndimage
from scipy.interpolate import griddata

# ===== 1. NAČTENÍ DAT =====
img_path = 'mila.tif'
img = Image.open(img_path)
elevation_data = np.array(img, dtype=np.float32)

print("="*70)
print("ANALÝZA DIGITÁLNÍHO MODELU RELIÉFU (DMR)")
print("="*70)

# Informace o datech
height, width = elevation_data.shape
min_elev = elevation_data.min()
max_elev = elevation_data.max()
mean_elev = elevation_data.mean()
std_elev = elevation_data.std()

print(f"\n1. METADATA SOUBORU")
print(f"-" * 70)
print(f"   Název souboru: {img_path}")
print(f"   Rozměry (Y × X):  {height} × {width} pixelů")
print(f"   Minimální výška:  {min_elev:.2f} m")
print(f"   Maximální výška:  {max_elev:.2f} m")
print(f"   Průměrná výška:   {mean_elev:.2f} m")
print(f"   Std. odchylka:    {std_elev:.2f} m")
print(f"   Celkový rozsah:   {max_elev - min_elev:.2f} m")

# Velikost pixelu v metrech (typicky 1m × 1m pro DMR)
pixel_size = 1.0  # metrů
area_per_pixel = pixel_size * pixel_size

print(f"\n2. ROZLIŠENÍ A KALIBRACI")
print(f"-" * 70)
print(f"   Velikost pixelu:  {pixel_size} m × {pixel_size} m")
print(f"   Plocha pixelu:    {area_per_pixel} m²")
print(f"   Celková plocha:   {width * height * area_per_pixel / 1e6:.2f} km²")

# ===== 2. IDENTIFIKACE HORY =====
# Pata hory se určuje jako minimální elevace v oblastech
# Lze definovat různými metodami

# Metoda 1: Nejnižší vrstevnice
base_elevation_absolute = min_elev

# Metoda 2: Prahová hodnota (75. percentil výšky)
threshold_75 = np.percentile(elevation_data, 75)

# Metoda 3: Lokální analýza - identifikace vrcholu
peak_location = np.unravel_index(np.argmax(elevation_data), elevation_data.shape)
peak_elevation = elevation_data[peak_location]

print(f"\n3. IDENTIFIKACE HORY")
print(f"-" * 70)
print(f"   Vrchol hory na: řádek {peak_location[0]}, sloupec {peak_location[1]}")
print(f"   Výška vrcholu:  {peak_elevation:.2f} m")
print(f"   Pata hory (min): {base_elevation_absolute:.2f} m")
print(f"   Relativní výška: {peak_elevation - base_elevation_absolute:.2f} m")

# ===== 3. RŮZNÉ METODY VÝPOČTU OBJEMU =====
print(f"\n4. VÝPOČET OBJEMU - RŮZNÉ METODY")
print(f"-" * 70)

# METODA A: Přímý součet (sum elevací × plocha)
# Předpokládá, že se počítá od nulové hladiny
volume_direct = np.sum(elevation_data) * area_per_pixel
print(f"\n   A) METODA PŘÍMÉHO SOUČTU (od ref. hladiny 0m)")
print(f"      Princip: V = Σ(elevace_i) × plocha_pixelu")
print(f"      Výsledek: {volume_direct:.2f} m³")
print(f"      Výsledek: {volume_direct/1e6:.6f} km³")

# METODA B: Objem od paty hory (400m - podle QGIS)
# Počítáme od úpratoře 400m nahoru (jak to dělá QGIS)
ref_level = 400.0  # Úpratoř hory podle QGIS
pixels_above_400 = elevation_data >= ref_level
elevation_above_400 = elevation_data[pixels_above_400]
elevation_relative_400 = elevation_above_400 - ref_level
volume_from_base = np.sum(elevation_relative_400) * area_per_pixel
pixels_count_400 = np.sum(pixels_above_400)
print(f"\n   B) METODA OD ÚPRATOŘE 400m (podle QGIS)")
print(f"      Princip: V = Σ(elevace_i - 400m) × plocha pro pixely > 400m")
print(f"      Pixely nad 400m: {pixels_count_400}")
print(f"      Výsledek: {volume_from_base:.2f} m³")
print(f"      Výsledek: {volume_from_base/1e6:.6f} km³")

# METODA C: Aproximace konusem (cone approximation)
# Pro horu se často používá přibližný model kuželu
# V_cone = (1/3) × π × r² × h
height_mountain = peak_elevation - base_elevation_absolute

# Aproximace poloměru - vzdálenost od vrcholu k okraji
distances = np.zeros_like(elevation_data, dtype=float)
for i in range(height):
    for j in range(width):
        distances[i, j] = np.sqrt((i - peak_location[0])**2 + (j - peak_location[1])**2)

# Průměrný poloměr (do místa kde výška klesne na 50% max výšky)
half_height_threshold = base_elevation_absolute + height_mountain * 0.5
half_height_pixels = elevation_data > half_height_threshold
if np.sum(half_height_pixels) > 0:
    avg_distance = np.mean(distances[half_height_pixels])
    radius_cone = avg_distance * pixel_size
    volume_cone = (1/3) * np.pi * radius_cone**2 * height_mountain
else:
    radius_cone = np.mean(distances[elevation_data > threshold_75]) * pixel_size
    volume_cone = (1/3) * np.pi * radius_cone**2 * height_mountain

print(f"\n   C) APROXIMACE KUŽELEM")
print(f"      Princip: V = (1/3) × π × r² × h")
print(f"      Výška kužele:   {height_mountain:.2f} m")
print(f"      Poloměr základny: {radius_cone:.2f} m")
print(f"      Výsledek: {volume_cone:.2f} m³")
print(f"      Výsledek: {volume_cone/1e6:.6f} km³")

# METODA D: Aproximace paraboloidem
# V_paraboloid = (1/2) × π × r² × h
volume_paraboloid = 0.5 * np.pi * radius_cone**2 * height_mountain
print(f"\n   D) APROXIMACE PARABOLOIDEM")
print(f"      Princip: V = (1/2) × π × r² × h")
print(f"      Výsledek: {volume_paraboloid:.2f} m³")
print(f"      Výsledek: {volume_paraboloid/1e6:.6f} km³")

# METODA E: Simpsonův vzorec (pro řezy vrstevnicemi)
# Rozdělíme horu na horizontální vrstvy a sčítáme plochy
layer_thickness = 1.0  # 1 metr mezi vrstvami
layers = np.arange(base_elevation_absolute, max_elev + layer_thickness, layer_thickness)
volumes_simpson = []

for i in range(len(layers) - 2):
    h1 = layers[i]
    h2 = layers[i + 1]
    h3 = layers[i + 2]
    
    area1 = np.sum((elevation_data >= h1) & (elevation_data < h2)) * area_per_pixel
    area2 = np.sum((elevation_data >= h2) & (elevation_data < h3)) * area_per_pixel
    area3 = np.sum((elevation_data >= h3) & (elevation_data < h3 + layer_thickness)) * area_per_pixel
    
    # Simpsonův vzorec: V = (Δh/3) × (S₁ + 4×S₂ + S₃)
    delta_h = layer_thickness
    v_segment = (delta_h / 3) * (area1 + 4*area2 + area3)
    volumes_simpson.append(v_segment)

volume_simpson = sum(volumes_simpson)
print(f"\n   E) SIMPSONŮV VZOREC (vrstevničná analýza)")
print(f"      Princip: V = Σ (Δh/3 × (S₁ + 4×S₂ + S₃))")
print(f"      Počet vrstev: {len(layers) - 1}")
print(f"      Tloušťka vrstvy: {layer_thickness} m")
print(f"      Výsledek: {volume_simpson:.2f} m³")
print(f"      Výsledek: {volume_simpson/1e6:.6f} km³")

# METODA F: GIS metoda - rasterová analýza (hypsometrická kurva)
print(f"\n   F) GIS METODA - HYPSOMETRICKÁ ANALÝZA")
print(f"      Princip: Analýza distribuce ploch v jednotlivých výškových pásmech")

# Vytvoření hypsometrické křivky
elev_bins = np.linspace(min_elev, max_elev, 50)
areas_at_elevation = []
cumulative_volumes = []

for elev in elev_bins:
    pixels_above = elevation_data >= elev
    area = np.sum(pixels_above) * area_per_pixel
    areas_at_elevation.append(area)

# Výpočet objemu z hypsometrické křivky (trapézová metoda)
volume_hypsometric = 0
for i in range(len(elev_bins) - 1):
    area1 = areas_at_elevation[i]
    area2 = areas_at_elevation[i + 1]
    delta_h = elev_bins[i + 1] - elev_bins[i]
    volume_hypsometric += (area1 + area2) / 2 * delta_h

print(f"      Počet výškových pásem: 50")
print(f"      Výsledek: {volume_hypsometric:.2f} m³")
print(f"      Výsledek: {volume_hypsometric/1e6:.6f} km³")

# ===== 4. SHRNUTÍ VÝSLEDKŮ =====
print(f"\n5. SROVNÁNÍ METOD")
print(f"-" * 70)

methods = {
    "Přímý součet": volume_direct,
    "Relativní objem": volume_from_base,
    "Aproximace kuželem": volume_cone,
    "Aproximace paraboloidem": volume_paraboloid,
    "Simpsonův vzorec": volume_simpson,
    "Hypsometrická analýza": volume_hypsometric
}

avg_volume = np.mean(list(methods.values()))

for name, volume in methods.items():
    deviation = ((volume - avg_volume) / avg_volume * 100)
    print(f"   {name:.<40} {volume:>15.2f} m³  ({deviation:+6.2f}%)")

print(f"\n   Průměrný objem: {avg_volume:.2f} m³")
print(f"   Průměrný objem: {avg_volume/1e6:.6f} km³")
print(f"   Min objem:      {min(methods.values()):.2f} m³")
print(f"   Max objem:      {max(methods.values()):.2f} m³")
print(f"   Rozdíl Max-Min: {(max(methods.values()) - min(methods.values()))/avg_volume*100:.2f}%")

# ===== 5. ULOŽENÍ VÝSLEDKŮ =====
results = {
    'methods': methods,
    'elevation_data': elevation_data,
    'peak_location': peak_location,
    'peak_elevation': peak_elevation,
    'base_elevation': base_elevation_absolute,
    'height_mountain': height_mountain,
    'radius_cone': radius_cone,
    'pixel_size': pixel_size,
    'avg_volume': avg_volume,
    'elev_bins': elev_bins,
    'areas_at_elevation': areas_at_elevation
}

# Uložení do textového souboru
with open('volume_results.txt', 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("ANALÝZA OBJEMU HORY Z DMR\n")
    f.write("="*70 + "\n\n")
    
    f.write("METADATA:\n")
    f.write(f"  Rozměry: {height} × {width} pixelů\n")
    f.write(f"  Elevace: {min_elev:.2f} - {max_elev:.2f} m\n")
    f.write(f"  Vrchol: ({peak_location[0]}, {peak_location[1]}) → {peak_elevation:.2f} m\n\n")
    
    f.write("VÝSLEDKY VÝPOČTU OBJEMU:\n")
    for name, volume in methods.items():
        f.write(f"  {name}: {volume:.2f} m³ ({volume/1e6:.6f} km³)\n")
    
    f.write(f"\nPRŮMĚRNÝ OBJEM: {avg_volume:.2f} m³\n")

print(f"\n✓ Výsledky uloženy do 'volume_results.txt'")
print(f"\n{'='*70}\n")
