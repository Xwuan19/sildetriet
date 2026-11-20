from PIL import Image
import numpy as np

# Load slide1_bg_restored (has clean Lenin and clean center)
im_center = Image.open("preview_red/slide1_bg_restored.png")
# Load ref_slide1_clean (has clean top-right and clean bottom-left)
im_slide1 = Image.open("preview_red/ref_slide1_clean.png")

w, h = im_center.size

# 1. Patch top right: x: 1400 to 1680, y: 0 to 250
patch_tr = im_slide1.crop((1400, 0, 1680, 250))
im_center.paste(patch_tr, (1400, 0))

# 2. Patch bottom left (Marx medallion in bottom left): x: 0 to 250, y: 600 to 880
# In ref_slide1_clean, what was at bottom left?
# At bottom left was the deep red background, and the small card "Trình bày: Tuyetkypowerpoint"
# Let's inspect ref_slide1_clean at x: 0 to 250, y: 600 to 880:
# In ref_slide1_clean, the card was at x: 380 to 850, y: 740 to 830.
# So x: 0 to 250, y: 600 to 880 in ref_slide1_clean is PURE RED BACKGROUND!
patch_bl = im_slide1.crop((0, 600, 250, 880))
im_center.paste(patch_bl, (0, 600))

# 3. Smooth the bottom 65px (y=880 to 945) seamlessly:
arr = np.array(im_center)
col_sample = arr[875:880, :, :].mean(axis=0).astype(np.uint8)
for y in range(880, h):
    fade = (y - 880) / (h - 880)
    target = np.array([30, 4, 8], dtype=float)
    arr[y, :, :] = (col_sample * (1.0 - fade * 0.8) + target * (fade * 0.8)).astype(np.uint8)

im_final_bg = Image.fromarray(arr)
im_final_bg.save("preview_red/master_stage_bg.png")
print("Saved master_stage_bg.png!")
