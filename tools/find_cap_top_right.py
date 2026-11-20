from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)

print("Top edge of cap:")
for x in range(320, 620, 30):
    for y in range(0, 150):
        c = arr[y, x]
        # Cap is darker than background red (background red is bright red R>110, G<35)
        # Cap top has skin/brown tone or dark shadow
        if c[0] < 100 or c[1] > 35:
            print(f"x={x}: cap top at y={y}, c={c}")
            break

print("\nRight edge of cap:")
for y in range(20, 200, 20):
    for x in range(650, 450, -10):
        c = arr[y, x]
        if c[0] < 100 or c[1] > 35:
            print(f"y={y}: cap right edge at x={x}, c={c}")
            break
