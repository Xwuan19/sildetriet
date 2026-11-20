from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)

for y in range(10, 450, 20):
    for x in range(200, 450):
        c = arr[y, x]
        # Skin tone has green > 45, or cap highlight has green > 35, blue > 30
        if c[1] > 35 and c[2] > 25:
            print(f"y={y}: skin/highlight at x={x}, c={c}")
            break
