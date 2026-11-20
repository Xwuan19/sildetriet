from PIL import Image
import numpy as np

im = Image.open("assets/master_stage_bg.png").convert("RGB")
arr = np.array(im, dtype=float)
h, w, _ = arr.shape

# Smooth bottom vignette from y=850 to 945:
# At y=850, factor is 0. At y=945, factor is 0.85
# Target color is deep Soviet inky crimson (24, 4, 8) for the red side, and (18, 14, 18) for the coat side
for y in range(840, h):
    t = (y - 840) / (h - 840)
    # Smoothstep curve: 3*t^2 - 2*t^3
    s = t * t * (3.0 - 2.0 * t)
    for x in range(w):
        if x > 1000:
            target = np.array([16.0, 14.0, 16.0])
        else:
            target = np.array([24.0, 4.0, 8.0])
        arr[y, x, :] = arr[y, x, :] * (1.0 - s * 0.90) + target * (s * 0.90)

im_out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
im_out.save("assets/master_stage_bg.png")
im_out.save("preview_red/master_stage_bg_clean3.png")
print("Saved clean3!")
