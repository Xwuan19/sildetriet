from PIL import Image, ImageFilter
import numpy as np

im = Image.open("assets/emblem_gold_star.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

# Clean fringes:
# A pixel is part of the gold star if alpha > 120 and (R > 120 and G > 80)
# Pixels that are white fringe (R>220, G>220, B>200, near outer boundary) or low alpha should be removed:
is_white_fringe = (arr[:, :, 0] > 200) & (arr[:, :, 1] > 200) & (arr[:, :, 2] > 180) & (arr[:, :, 3] < 200)
arr[is_white_fringe, 3] = 0

# Clean outer boundary
alpha = arr[:, :, 3]
alpha[alpha < 100] = 0
arr[:, :, 3] = alpha

im_clean = Image.fromarray(arr)
# Trim transparent edges:
bbox = im_clean.getbbox()
if bbox:
    im_clean = im_clean.crop(bbox)

im_clean.save("assets/gold_star_clean.png")
print("Saved assets/gold_star_clean.png", im_clean.size)
