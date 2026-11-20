from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)

for y in range(10, 180, 10):
    for x in range(200, 500):
        c = arr[y, x]
        # Cap is dark, not pure bright red
        # Red background has R > 120 and R > 3*G
        if not (c[0] > 110 and c[0] > 2.5 * c[1] and c[0] > 2.5 * c[2]):
            print(f"y={y}: cap left edge at x={x}, c={c}")
            break
