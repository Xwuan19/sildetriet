from PIL import Image
import numpy as np

im = Image.open("assets/master_stage_bg.png").convert("RGB")
arr = np.array(im, dtype=float)
h, w, _ = arr.shape

# Slide 2 effect:
# Lenin on the right is shaded in deep crimson (red tone, lower luminance)
# The left side remains deep rich wine/crimson red.
# In ref_slide2_clean:
# The right side has R around 90-130, G around 10-25, B around 10-25.
# Let's apply a smooth crimson shading overlay:
# For x > 800 (where Lenin is):
# Reduce green and blue by 60%, reduce red slightly by 30%, so it becomes an atmospheric crimson engraving!

arr_dim = arr.copy()
# Dim the right side:
for x in range(w):
    factor = 0.0
    if x > 800:
        factor = (x - 800) / (w - 800) # 0 to 1
    # Red channel
    arr_dim[:, x, 0] = arr[:, x, 0] * (1.0 - factor * 0.25)
    # Green channel (heavily suppressed to turn into red tone)
    arr_dim[:, x, 1] = arr[:, x, 1] * (1.0 - factor * 0.70)
    # Blue channel (heavily suppressed)
    arr_dim[:, x, 2] = arr[:, x, 2] * (1.0 - factor * 0.70)

# Also overall subtle contrast/darkness boost so text on Slide 2 has crystal-clear contrast!
arr_dim = arr_dim * 0.88 + np.array([15.0, 2.0, 4.0]) * 0.12

im_dim = Image.fromarray(np.clip(arr_dim, 0, 255).astype(np.uint8))
im_dim.save("assets/stage_bg_dimmed.png")
im_dim.save("preview_red/stage_bg_dimmed_preview.png")
print("Saved assets/stage_bg_dimmed.png!")
