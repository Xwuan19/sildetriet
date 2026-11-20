from PIL import Image
import numpy as np

im = Image.open("assets/master_stage_bg.png").convert("RGB")
arr = np.array(im, dtype=float)
h, w, _ = arr.shape

# In the region x: 1000 to 1100, y: 780 to 945:
# It is RED background!
# Let's sample red background at x=980, y=780..945:
for y in range(780, h):
    red_val = arr[y, 970, :].copy()
    for x in range(980, 1100):
        # Blend from red_val on left to red_val on right
        arr[y, x, :] = red_val

# And for the coat at x >= 1100, y >= 800:
# Make it clean dark charcoal:
for y in range(800, h):
    fade = (y - 800) / (h - 800)
    for x in range(1100, w):
        top_c = arr[795, x, :]
        arr[y, x, :] = top_c * (1.0 - fade * 0.8) + np.array([12.0, 14.0, 16.0]) * (fade * 0.8)

# Now smooth the transition boundary near x=1100 at y > 780
for y in range(780, h):
    arr[y, 1095:1105, :] = arr[y, 1095:1105, :].mean(axis=0)

im_out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
im_out.save("assets/master_stage_bg.png")
im_out.save("preview_red/master_stage_bg_clean4.png")
print("Saved clean4!")
