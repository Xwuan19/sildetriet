from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
w, h = im.size
print(f"Size: {w}x{h}")

# Let's inspect points along Lenin's silhouette:
# Cap top:
# At y=0..100, where is the cap?
# Let's print out pixel values across several rows to trace the edge between background (red) and Lenin (cap/face/coat):
# Background red has: R > 120, G < 40, B < 40 (high red, very low green/blue)
# Cap has: dark colors (R < 80, G < 80, B < 80) or dark charcoal/brown
# Face has: R > 150, G > 90, B > 60 (flesh tone has significant green and blue!)
# Overcoat has: dark charcoal (R < 70, G < 70, B < 70)
arr = np.array(im)
r = arr[:, :, 0].astype(float)
g = arr[:, :, 1].astype(float)
b = arr[:, :, 2].astype(float)

# Background red ratio: R / (G + B + 1e-5)
# In pure red background, R is 120-200, G is 5-30, B is 5-30. Ratio is > 3.0!
# On Lenin's face, R is ~190, G is ~120, B is ~90. Ratio is 190 / 210 = 0.9!
# On Lenin's cap, R is ~50, G is ~45, B is ~45. Ratio is 50 / 90 = 0.55!
# On Lenin's coat, R is ~40, G is ~38, B is ~40. Ratio is 40 / 78 = 0.51!
ratio = r / (g + b + 1.0)
print("Background sample ratio:", ratio[100, 100])
print("Lenin face sample ratio:", ratio[200, 450])
print("Lenin cap sample ratio:", ratio[100, 500])
print("Lenin coat sample ratio:", ratio[600, 500])
