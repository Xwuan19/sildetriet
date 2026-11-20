from PIL import Image, ImageFilter
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGB")
arr = np.array(im)
h, w, _ = arr.shape

r = arr[:, :, 0].astype(float)
g = arr[:, :, 1].astype(float)
b = arr[:, :, 2].astype(float)

# Background red criteria:
is_bg_red = (r > 75) & (r > 1.8 * g) & (r > 1.8 * b)

# Also in the top-right corner behind cap:
# There is a crowd banner or dark red:
# Everything to the right of cap (y < 230, x > 600) is background if not part of cap
is_top_right_bg = np.zeros((h, w), dtype=bool)
for y in range(0, 230):
    for x in range(580, w):
        if r[y, x] > 90 and (r[y, x] > 1.5 * g[y, x] or r[y, x] > 1.5 * b[y, x]):
            is_top_right_bg[y, x] = True

# Also to the left of Lenin:
# Cap edge x:
# For each y from 0 to 750, let's find the left edge of Lenin
is_bg = is_bg_red | is_top_right_bg

# Save mask
mask_img = Image.fromarray(((~is_bg) * 255).astype(np.uint8))
mask_img.save("preview_red/test_lenin_raw_mask.png")
print("Saved test_lenin_raw_mask.png")
