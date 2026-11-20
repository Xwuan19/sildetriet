from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)

for y in range(200, 480, 20):
    for x in range(650, 400, -10):
        c = arr[y, x]
        # Skin / hair / collar:
        # Background is red flag (R > 130, G < 35, B < 35)
        # Collar or hair has G > 40 or R < 100
        if c[0] < 100 or c[1] > 40 or c[2] > 35:
            print(f"y={y}: neck/collar right edge at x={x}, c={c}")
            break
