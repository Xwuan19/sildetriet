from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)
h, w, _ = arr.shape

# Let's inspect where the profile edge actually is:
# At y=260 (nose level):
# Scan from x=0 to 400
for y in [50, 100, 150, 200, 250, 260, 280, 300, 350, 400, 450, 500, 550, 600, 650]:
    row = arr[y, :450, :]
    # Find first pixel where G > 50 or R < 80 (not background red)
    # Background red is R > 100, G < 35, B < 35
    is_bg = (row[:, 0] > 90) & (row[:, 1] < 45) & (row[:, 2] < 45)
    non_bg = np.where(~is_bg)[0]
    if len(non_bg) > 0:
        first_x = non_bg[0]
        print(f"y={y}: profile starts at x={first_x}, color={row[first_x]}")
    else:
        print(f"y={y}: all background")
