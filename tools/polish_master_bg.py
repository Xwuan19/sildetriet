from PIL import Image, ImageFilter
import numpy as np

im = Image.open("preview_red/master_stage_bg.png").convert("RGB")
arr = np.array(im)
h, w, _ = arr.shape

# Fix the white speck near x=80..130, y=590..610
# In that area, replace with surrounding red
patch = arr[570:590, 80:130, :]
arr[590:610, 80:130, :] = patch

# Fix bottom at y=870 to 945:
# For x from 980 to 1680 (under Lenin's coat):
# Sample the coat colors at y=860..870
coat_sample = arr[860:868, 980:1680, :].mean(axis=0)
for y in range(868, h):
    fade = (y - 868) / (h - 868)
    # Blend downwards to dark charcoal/ink (18, 16, 20)
    target = np.array([18, 16, 20], dtype=float)
    arr[y, 980:1680, :] = (coat_sample * (1.0 - fade * 0.7) + target * (fade * 0.7)).astype(np.uint8)

# For x < 980 (red background):
bg_sample = arr[860:868, :980, :].mean(axis=0)
for y in range(868, h):
    fade = (y - 868) / (h - 868)
    # Blend downwards to rich dark red (28, 4, 8)
    target = np.array([28, 4, 8], dtype=float)
    arr[y, :980, :] = (bg_sample * (1.0 - fade * 0.8) + target * (fade * 0.8)).astype(np.uint8)

im_clean = Image.fromarray(arr)
# Save as master background asset!
im_clean.save("assets/master_stage_bg.png")
im_clean.save("preview_red/master_stage_bg_clean.png")
print("Saved assets/master_stage_bg.png!")
