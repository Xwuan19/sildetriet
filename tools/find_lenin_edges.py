from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)
h, w, _ = arr.shape

# For each row y, let's scan from left to right and right to left to find the edge
print("Scanning right edge around y=100 to y=350:")
for y in range(80, 360, 20):
    # Scan from x=680 backwards to 450:
    for x in range(680, 450, -2):
        r, g, b = arr[y, x][:3]
        # In red flag: g < 20, r > 80, (r - g) > 65
        # In hat / ear / neck / coat:
        if y < 180: # Hat area
            # Hat has darker r or higher g/b ratio: r < 75 or (r-g < 45)
            if r < 75 or (r - g < 45):
                print(f"y={y}: hat back edge at x={x}, color={r, g, b}")
                break
        elif y < 270: # Ear / neck area
            if g > 30 or r < 80 or (r - g < 80):
                print(f"y={y}: ear/hair edge at x={x}, color={r, g, b}")
                break
        else: # Coat back area
            if g > 35 or r < 75 or (r - g < 60):
                print(f"y={y}: coat edge at x={x}, color={r, g, b}")
                break
