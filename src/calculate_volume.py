import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

# Načtení TIF souboru
# Detekce cesty k datovému souboru
if os.path.exists('mila.tif'):
    img_path = 'mila.tif'
elif os.path.exists('../mila.tif'):
    img_path = '../mila.tif'
elif os.path.exists('data/mila.tif'):
    img_path = 'data/mila.tif'
else:
    img_path = 'mila.tif'  # Výchozí cesta
img = Image.open(img_path)

# Převedení na NumPy array
elevation_data = np.array(img, dtype=np.float32)

# Informace o datech
print(f"Tvar dat (výška x šířka): {elevation_data.shape}")
print(f"Min výška: {elevation_data.min()}")
print(f"Max výška: {elevation_data.max()}")
print(f"Průměrná výška: {elevation_data.mean():.2f}")

# Velikost pixelu v metrech (lze upravit podle skutečného rozlišení)
pixel_size = 1.0  # 1 metr x 1 metr
area_per_pixel = pixel_size * pixel_size

# Výpočet objemu - součet všech výšek vynásobený plochou pixelu
volume = np.sum(elevation_data) * area_per_pixel

print(f"\n{'='*50}")
print(f"Objem hory: {volume:.2f} m³")
print(f"Objem hory: {volume/1e6:.6f} km³")
print(f"{'='*50}")

# Vizualizace hory
plt.figure(figsize=(12, 10))

# 2D heatmapa
plt.subplot(2, 1, 1)
plt.imshow(elevation_data, cmap='terrain')
plt.colorbar(label='Výška [m]')
plt.title('Výšková data - 2D pohled')
plt.xlabel('X [pixely]')
plt.ylabel('Y [pixely]')

# 3D vizualizace
from mpl_toolkits.mplot3d import Axes3D

ax = plt.subplot(2, 1, 2, projection='3d')

# Vytvoření X Y souřadnic
x = np.arange(0, elevation_data.shape[1])
y = np.arange(0, elevation_data.shape[0])
X, Y = np.meshgrid(x, y)

# 3D povrch
surf = ax.plot_surface(X, Y, elevation_data, cmap='terrain', alpha=0.9)
ax.set_xlabel('X [pixely]')
ax.set_ylabel('Y [pixely]')
ax.set_zlabel('Výška [m]')
ax.set_title('Výšková data - 3D pohled')
plt.colorbar(surf, ax=ax, label='Výška [m]')

plt.tight_layout()
plt.savefig('hory_vizualizace.png', dpi=150, bbox_inches='tight')
print(f"\nVizualizace uložena do: hory_vizualizace.png")
plt.show()
