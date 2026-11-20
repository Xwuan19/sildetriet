import numpy as np
from PIL import Image

# Load clean lenin
lenin = Image.open("assets/lenin_hero_clean.png").convert("RGBA")
arr = np.array(lenin, dtype=float)

# Tint Lenin to deep crimson watermark:
# Red channel stays medium-high, Green and Blue are heavily crushed, brightness reduced
# In image2.png:
# Lenin's face is R: 80-140, G: 5-25, B: 5-25
# Lenin's coat is R: 30-70, G: 0-10, B: 0-10
alpha = arr[:, :, 3]

# Convert to grayscale first to get luminance
gray = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
# Normalize gray to [0, 1]
gray_norm = gray / 255.0

# Map gray to crimson gradient:
# dark areas -> deep dark red [40, 5, 8]
# highlight areas -> crimson red [140, 20, 22]
r_chan = 35 + gray_norm * 115
g_chan = 4 + gray_norm * 20
b_chan = 6 + gray_norm * 22

watermark_arr = np.zeros_like(arr, dtype=np.uint8)
watermark_arr[:, :, 0] = np.clip(r_chan, 0, 255).astype(np.uint8)
watermark_arr[:, :, 1] = np.clip(g_chan, 0, 255).astype(np.uint8)
watermark_arr[:, :, 2] = np.clip(b_chan, 0, 255).astype(np.uint8)
# Set opacity: let's keep alpha as is or 75%
watermark_arr[:, :, 3] = (alpha * 0.85).astype(np.uint8)

lenin_wm = Image.fromarray(watermark_arr)
lenin_wm.save("assets/lenin_crimson_watermark.png")

# Now composite on stage background to see the full slide!
bg = Image.open("assets/master_stage_clean_bg.png").convert("RGBA").resize((1920, 1080))
poster = Image.open("assets/soviet_worker_flag_clean.png").convert("RGBA")
hs = Image.open("assets/soviet_hammer_sickle_clean.png").convert("RGBA")
star = Image.open("assets/soviet_3d_star_clean.png").convert("RGBA")

# Resize Lenin watermark to fill right side: height 1080, width proportional
wm_w, wm_h = lenin_wm.size
new_wm_h = 1080
new_wm_w = int(wm_w * (new_wm_h / wm_h))
lenin_wm_scaled = lenin_wm.resize((new_wm_w, new_wm_h), Image.Resampling.LANCZOS)

# Paste Lenin watermark on right: x=1000, y=50
bg.paste(lenin_wm_scaled, (1000, 40), lenin_wm_scaled)

# Paste Worker on bottom-left:
p_w, p_h = poster.size
new_ph = 720
new_pw = int(p_w * (new_ph / p_h))
poster_scaled = poster.resize((new_pw, new_ph), Image.Resampling.LANCZOS)
bg.paste(poster_scaled, (0, 360), poster_scaled)

# Paste Emblems on top-left:
hs_scaled = hs.resize((int(hs.width * 1.3), int(hs.height * 1.3)), Image.Resampling.LANCZOS)
star_scaled = star.resize((int(star.width * 1.3), int(star.height * 1.3)), Image.Resampling.LANCZOS)
bg.paste(hs_scaled, (140, 80), hs_scaled)
bg.paste(star_scaled, (320, 70), star_scaled)

bg.save("preview_red/full_stage_clean_test.png")
print("Saved preview_red/full_stage_clean_test.png!")
