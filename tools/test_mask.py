import numpy as np
from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
arr = np.array(im)
h, w, _ = arr.shape

# The background is strongly RED:
# In the background:
# R is high (> 80), but G is low (< 45) and B is low (< 45).
# Specifically, in the background:
# (R - G) > 50 and (R - B) > 50, and G < 60, B < 60!
# Let's test this background criterion across the image!

is_red_bg = (arr[:, :, 0] > 70) & (arr[:, :, 1] < 45) & (arr[:, :, 2] < 45) & ((arr[:, :, 0] - arr[:, :, 1]) > 40)

mask = np.ones((h, w), dtype=np.uint8) * 255
mask[is_red_bg] = 0

mask_im = Image.fromarray(mask)
mask_im.save("preview_red/test_mask.png")
print("Saved test_mask.png")
