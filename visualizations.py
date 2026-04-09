import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches

# Načtení dat
img_path = 'mila.tif'
img = Image.open(img_path)
elevation_data = np.array(img, dtype=np.float32)

height, width = elevation_data.shape
min_elev = elevation_data.min()
max_elev = elevation_data.max()
mean_elev = elevation_data.mean()
pixel_size = 1.0

# Vypočtené hodnoty
peak_location = np.unravel_index(np.argmax(elevation_data), elevation_data.shape)
peak_elevation = elevation_data[peak_location]
base_elevation = min_elev
height_mountain = peak_elevation - base_elevation

# Relativní výšky (od paty)
elevation_relative = elevation_data - base_elevation

# ===== VELKOOBRÁZEK 1: Přehledový obrázek =====
fig = plt.figure(figsize=(16, 12))
fig.suptitle('DIGITÁLNÍ MODEL RELIÉFU - HORY', fontsize=18, fontweight='bold', y=0.98)

# 2D heatmapa
ax1 = plt.subplot(2, 3, 1)
im1 = ax1.imshow(elevation_data, cmap='terrain', origin='upper')
ax1.plot(peak_location[1], peak_location[0], 'r*', markersize=20, label='Vrchol')
cbar1 = plt.colorbar(im1, ax=ax1)
cbar1.set_label('Nadmořská výška [m]', rotation=270, labelpad=20)
ax1.set_title('Nadmořská výška - Heatmapa', fontweight='bold')
ax1.set_xlabel('X [pixely]')
ax1.set_ylabel('Y [pixely]')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Relativní výšky
ax2 = plt.subplot(2, 3, 2)
im2 = ax2.imshow(elevation_relative, cmap='YlOrRd', origin='upper')
ax2.plot(peak_location[1], peak_location[0], 'b*', markersize=20, label='Vrchol')
cbar2 = plt.colorbar(im2, ax=ax2)
cbar2.set_label('Relativní výška [m]', rotation=270, labelpad=20)
ax2.set_title('Relativní výška (od paty)', fontweight='bold')
ax2.set_xlabel('X [pixely]')
ax2.set_ylabel('Y [pixely]')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Profil terénního řezu (horizontální)
ax3 = plt.subplot(2, 3, 3)
profile_y = peak_location[0]
profile_horizontal = elevation_data[profile_y, :]
ax3.plot(profile_horizontal, 'b-', linewidth=2, label='Profil vodorovný')
ax3.plot(peak_location[1], peak_elevation, 'r*', markersize=15, label='Vrchol')
ax3.fill_between(range(width), base_elevation, profile_horizontal, alpha=0.3)
ax3.axhline(y=min_elev, color='g', linestyle='--', label='Pata')
ax3.set_title('Profil terénního řezu (vodorovně)', fontweight='bold')
ax3.set_xlabel('X [pixely]')
ax3.set_ylabel('Nadmořská výška [m]')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Profil terénního řezu (vertikální)
ax4 = plt.subplot(2, 3, 4)
profile_x = peak_location[1]
profile_vertical = elevation_data[:, profile_x]
ax4.plot(profile_vertical, 'g-', linewidth=2, label='Profil svislý')
ax4.plot(peak_location[0], peak_elevation, 'r*', markersize=15, label='Vrchol')
ax4.fill_between(range(height), base_elevation, profile_vertical, alpha=0.3, color='green')
ax4.axhline(y=min_elev, color='b', linestyle='--', label='Pata')
ax4.set_title('Profil terénního řezu (svisle)', fontweight='bold')
ax4.set_xlabel('Y [pixely]')
ax4.set_ylabel('Nadmořská výška [m]')
ax4.legend()
ax4.grid(True, alpha=0.3)

# Histogram nadmořských výšek
ax5 = plt.subplot(2, 3, 5)
ax5.hist(elevation_data.flatten(), bins=50, color='steelblue', edgecolor='black', alpha=0.7)
ax5.axvline(min_elev, color='g', linestyle='--', linewidth=2, label=f'Minimum: {min_elev:.1f}m')
ax5.axvline(max_elev, color='r', linestyle='--', linewidth=2, label=f'Maximum: {max_elev:.1f}m')
ax5.axvline(mean_elev, color='orange', linestyle='--', linewidth=2, label=f'Průměr: {mean_elev:.1f}m')
ax5.set_title('Histogram nadmořských výšek', fontweight='bold')
ax5.set_xlabel('Nadmořská výška [m]')
ax5.set_ylabel('Počet pixelů')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# Hypsometrická křivka
ax6 = plt.subplot(2, 3, 6)
elev_bins = np.linspace(min_elev, max_elev, 50)
areas_at_elevation = []
cumulative_areas = []
cum_area = 0

for elev in elev_bins:
    pixels_above = elevation_data >= elev
    area = np.sum(pixels_above) * pixel_size * pixel_size / 1000000  # v km²
    areas_at_elevation.append(area)
    cum_area += area
    cumulative_areas.append(cum_area)

ax6.plot(elev_bins, areas_at_elevation, 'b-', linewidth=2, marker='o', markersize=3)
ax6.fill_between(elev_bins, areas_at_elevation, alpha=0.3)
ax6.set_title('Hypsometrická křivka', fontweight='bold')
ax6.set_xlabel('Nadmořská výška [m]')
ax6.set_ylabel('Plocha nad výškou [km²]')
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_prehlad_analyza.png', dpi=150, bbox_inches='tight')
print("✓ Uloženo: 01_prehlad_analyza.png")
plt.close()

# ===== VELKOOBRÁZEK 2: 3D VIZUALIZACE =====
fig = plt.figure(figsize=(16, 12))
fig.suptitle('3D VIZUALIZACE HORY', fontsize=18, fontweight='bold', y=0.98)

# Příprava dat
x = np.arange(0, width)
y = np.arange(0, height)
X, Y = np.meshgrid(x, y)

# 3D povrch - nadmořská výška
ax1 = plt.subplot(2, 2, 1, projection='3d')
surf1 = ax1.plot_surface(X, Y, elevation_data, cmap='terrain', alpha=0.9, edgecolor='none')
ax1.set_xlabel('X [pixely]')
ax1.set_ylabel('Y [pixely]')
ax1.set_zlabel('Nadmořská výška [m]')
ax1.set_title('3D model - Nadmořská výška', fontweight='bold')
cbar = plt.colorbar(surf1, ax=ax1, pad=0.1, shrink=0.8)
cbar.set_label('Výška [m]')

# 3D povrch - relativní výška
ax2 = plt.subplot(2, 2, 2, projection='3d')
surf2 = ax2.plot_surface(X, Y, elevation_relative, cmap='YlOrRd', alpha=0.9, edgecolor='none')
ax2.set_xlabel('X [pixely]')
ax2.set_ylabel('Y [pixely]')
ax2.set_zlabel('Relativní výška [m]')
ax2.set_title('3D model - Relativní výška (od paty)', fontweight='bold')
cbar = plt.colorbar(surf2, ax=ax2, pad=0.1, shrink=0.8)
cbar.set_label('Výška [m]')

# 3D perspektiva 1 - nadmořská výška
ax3 = plt.subplot(2, 2, 3, projection='3d')
surf3 = ax3.plot_surface(X, Y, elevation_data, cmap='terrain', alpha=0.9, edgecolor='none')
ax3.view_init(elev=20, azim=45)
ax3.set_xlabel('X [pixely]')
ax3.set_ylabel('Y [pixely]')
ax3.set_zlabel('Nadmořská výška [m]')
ax3.set_title('3D perspektiva (azimut 45°)', fontweight='bold')

# 3D perspektiva 2 - jiný úhel
ax4 = plt.subplot(2, 2, 4, projection='3d')
surf4 = ax4.plot_surface(X, Y, elevation_data, cmap='terrain', alpha=0.9, edgecolor='none')
ax4.view_init(elev=30, azim=135)
ax4.set_xlabel('X [pixely]')
ax4.set_ylabel('Y [pixely]')
ax4.set_zlabel('Nadmořská výška [m]')
ax4.set_title('3D perspektiva (azimut 135°)', fontweight='bold')

plt.tight_layout()
plt.savefig('02_3d_vizualizace.png', dpi=150, bbox_inches='tight')
print("✓ Uloženo: 02_3d_vizualizace.png")
plt.close()

# ===== VELKOOBRÁZEK 3: SROVNÁNÍ METOD =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('SROVNÁNÍ METOD VÝPOČTU OBJEMU', fontsize=16, fontweight='bold')

# Výpočet všech metod
volume_direct = np.sum(elevation_data) * pixel_size * pixel_size
volume_relative = np.sum(elevation_relative) * pixel_size * pixel_size

distances = np.zeros_like(elevation_data, dtype=float)
for i in range(height):
    for j in range(width):
        distances[i, j] = np.sqrt((i - peak_location[0])**2 + (j - peak_location[1])**2)

half_height_threshold = base_elevation + height_mountain * 0.5
half_height_pixels = elevation_data > half_height_threshold
if np.sum(half_height_pixels) > 0:
    avg_distance = np.mean(distances[half_height_pixels])
    radius_cone = avg_distance * pixel_size
else:
    radius_cone = np.mean(distances) * pixel_size

volume_cone = (1/3) * np.pi * radius_cone**2 * height_mountain
volume_paraboloid = 0.5 * np.pi * radius_cone**2 * height_mountain

layer_thickness = 1.0
layers = np.arange(base_elevation, max_elev + layer_thickness, layer_thickness)
volumes_simpson = []
for i in range(len(layers) - 2):
    h1 = layers[i]
    h2 = layers[i + 1]
    h3 = layers[i + 2]
    area1 = np.sum((elevation_data >= h1) & (elevation_data < h2)) * pixel_size * pixel_size
    area2 = np.sum((elevation_data >= h2) & (elevation_data < h3)) * pixel_size * pixel_size
    area3 = np.sum((elevation_data >= h3) & (elevation_data < h3 + layer_thickness)) * pixel_size * pixel_size
    v_segment = (layer_thickness / 3) * (area1 + 4*area2 + area3)
    volumes_simpson.append(v_segment)
volume_simpson = sum(volumes_simpson)

volume_hypsometric = 0
for i in range(len(elev_bins) - 1):
    area1 = areas_at_elevation[i] * 1e6
    area2 = areas_at_elevation[i + 1] * 1e6
    delta_h = elev_bins[i + 1] - elev_bins[i]
    volume_hypsometric += (area1 + area2) / 2 * delta_h

methods = {
    'Přímý\nsučet': volume_direct,
    'Relativní\nobjem': volume_relative,
    'Kužel': volume_cone,
    'Paraboloid': volume_paraboloid,
    'Simpson': volume_simpson,
    'Hypsometrická': volume_hypsometric
}

# Sloup
ax = axes[0, 0]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
bars = ax.bar(methods.keys(), list(methods.values()), color=colors, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Objem [m³]', fontweight='bold')
ax.set_title('Porovnání objemů - všechny metody', fontweight='bold')
ax.set_yscale('log')
ax.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height_bar = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height_bar,
            f'{height_bar:.0f}', ha='center', va='bottom', fontsize=9)

# Vyloučení přímého součtu (nejméně relevantní) a srovnání relevantních metod
ax = axes[0, 1]
methods_relevant = {k: v for k, v in methods.items() if k != 'Přímý\nsučet'}
colors_rel = [c for c, k in zip(colors, methods.keys()) if k != 'Přímý\nsučet']
bars = ax.bar(methods_relevant.keys(), list(methods_relevant.values()), 
              color=colors_rel, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Objem [m³]', fontweight='bold')
ax.set_title('Relevantní metody (bez přímého součtu)', fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height_bar = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height_bar,
            f'{height_bar:.0f}', ha='center', va='bottom', fontsize=9)

# Tabulka s čísliteli
ax = axes[1, 0]
ax.axis('tight')
ax.axis('off')
table_data = []
table_data.append(['Metoda', 'Objem [m³]', 'Objem [km³]'])
for name, vol in methods.items():
    clean_name = name.replace('\n', ' ')
    table_data.append([clean_name, f'{vol:,.0f}', f'{vol/1e6:.4f}'])

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.35, 0.35])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)

# Nastavit barvu hlavičky
for i in range(3):
    table[(0, i)].set_facecolor('#40466e')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Průměr a medián
ax = axes[1, 1]
ax.axis('off')
avg_vol = np.mean(list(methods.values()))
median_vol = np.median(list(methods.values()))
std_vol = np.std(list(methods.values()))

info_text = f"""
STATISTIKA VÝSLEDKŮ:

Průměrný objem:     {avg_vol:,.0f} m³
                    {avg_vol/1e6:.4f} km³

Medián objemu:      {median_vol:,.0f} m³
                    {median_vol/1e6:.4f} km³

Std. odchylka:      {std_vol:,.0f} m³

Min objem:          {min(methods.values()):,.0f} m³
Max objem:          {max(methods.values()):,.0f} m³
Rozpětí:            {(max(methods.values())-min(methods.values()))/avg_vol*100:.1f}%

DOPORUČENÁ HODNOTA pro report:
Relativní objem hory (od paty)
V = {volume_relative:,.0f} m³ = {volume_relative/1e6:.4f} km³
"""

ax.text(0.1, 0.5, info_text, fontsize=11, family='monospace',
        verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('03_srovnani_metod.png', dpi=150, bbox_inches='tight')
print("✓ Uloženo: 03_srovnani_metod.png")
plt.close()

print("\n✓ Všechny vizualizace vytvořeny!")
