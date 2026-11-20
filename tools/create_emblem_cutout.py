import numpy as np
from PIL import Image, ImageFilter

im = Image.open("preview_red/emblem_crop_raw.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape
print(f"Emblem raw size: {w}x{h}")

# In emblem_crop_raw, the background is deep red, while the star and hammer-sickle are bright shiny gold!
# Gold color has high Red (> 180), high Green (> 140), and low-to-medium Blue (around 20-80).
# Background red has high Red (> 80), but very low Green (< 30) and very low Blue (< 30)!
# Let's test the gold mask:
r = arr[:, :, 0].astype(float)
g = arr[:, :, 1].astype(float)
b = arr[:, :, 2].astype(float)

is_gold = (g > 55) & (r > 100) & (r - g < 120)

mask = (is_gold * 255).astype(np.uint8)
mask_pil = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(radius=0.8))

cutout = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cutout.paste(im, (0, 0), mask_pil)
cutout.save("assets/soviet_gold_emblem.png")
cutout.save("preview_red/test_emblem_cutout.png")
print("Saved assets/soviet_gold_emblem.png")
