import numpy as np
from PIL import Image

b1 = Image.open("preview_red/badge_crop_01.png").convert("RGBA")
arr = np.array(b1)
h, w, _ = arr.shape

# The badge is circular/wax scalloped in the center
# Background around it is dark red (R~120-150, G~0-15, B~0-15)
# Inside the wax seal: G is > 40!
g = arr[:, :, 1]
alpha = np.clip((g.astype(float) - 15) / 35.0, 0, 1) * 255
alpha[g < 12] = 0
alpha[g > 45] = 255

arr[:, :, 3] = alpha.astype(np.uint8)
clean_badge = Image.fromarray(arr)
bbox = clean_badge.getbbox()
if bbox:
    clean_badge = clean_badge.crop(bbox)

clean_badge.save("assets/soviet_wax_seal_badge.png")
print("Saved assets/soviet_wax_seal_badge.png:", clean_badge.size)
