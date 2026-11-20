import numpy as np
from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)

# Let's inspect colors along some points:
# Background near top-left: (x=10, y=10)
print("Top-left (background):", arr[10, 10])
# Background near left edge (x=10, y=300):
print("Left edge (background):", arr[300, 10])
# Background near top (x=200, y=10):
print("Top edge (background):", arr[10, 200])

# Cap color (x=350, y=70):
print("Cap (dark blue/black):", arr[70, 350])
# Forehead color (x=330, y=200):
print("Forehead (skin tone):", arr[200, 330])
# Coat color (x=500, y=550):
print("Coat (grey/black):", arr[550, 500])
# Lapel color (x=430, y=600):
print("Lapel (khaki grey):", arr[600, 430])
