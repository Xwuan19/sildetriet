import numpy as np
from PIL import Image, ImageDraw, ImageFilter

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGB")
arr = np.array(im)
h, w, _ = arr.shape

# 1. Color-based red background detector:
# The background red has very low Green and Blue:
r = arr[:, :, 0].astype(float)
g = arr[:, :, 1].astype(float)
b = arr[:, :, 2].astype(float)

# Background is characterized by strong red dominance over green and blue:
# Red background: r > 65 and g < 45 and b < 45 and (r - g) > 35 and (r - b) > 35
# However, inside Lenin's face: r is high, but g is ALSO high (> 80), b is high (> 60).
# In his red tie: r is around 120-170, but it's well inside the chest area (x: 350-450, y: 500-600).
# In his lips/cheeks: g is > 70.
# So red background:
is_bg_color = (r > 60) & (g < 48) & (b < 48) & ((r - g) > 35) & ((r - b) > 35)

# Also behind the head on the right (x > 500, y < 450), there is the red flag/crowd:
# Let's inspect that region.

# 2. Polygon mask:
pts = [
    (0, 750),
    (0, 715),
    (30, 675),
    (65, 624),
    (75, 612),
    (105, 580),
    (135, 550),
    (170, 515),
    (210, 475),
    (250, 435),
    (275, 405),
    (288, 385),
    (280, 370),
    (265, 360),
    (250, 345),
    (244, 325),
    (247, 300),
    (254, 275),
    (252, 260),
    (242, 248),
    (238, 235),
    (248, 222),
    (245, 195),
    (242, 175),
    (235, 162),
    (240, 145),
    (248, 125),
    (258, 100),
    (275, 75),
    (300, 48),
    (330, 28),
    (365, 14),
    (410, 12),
    (455, 20),
    (500, 40),
    (545, 70),
    (580, 105),
    (605, 140),
    (615, 165),
    (575, 185),  # closer to ear
    (550, 215),  # closer to ear
    (530, 245),
    (525, 275),
    (530, 310),
    (540, 350),
    (555, 395),
    (575, 435),
    (605, 480),
    (635, 530),
    (660, 590),
    (680, 660),
    (700, 720),
    (700, 750),
]

poly_mask = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(poly_mask)
draw.polygon(pts, fill=255)
poly_arr = np.array(poly_mask) > 0

# Combine: Inside polygon AND NOT background color
# EXCEPT inside the chest area (y > 450, x > 250, x < 550) where red tie/lapel shadows are
is_tie_zone = (arr[:, :, 0] > 0)
yy, xx = np.mgrid[0:h, 0:w]
tie_zone = (yy > 500) & (yy < 680) & (xx > 340) & (xx < 460)

final_mask = poly_arr & (~is_bg_color | tie_zone)

# Use PIL flood fill to fill holes:
# Invert mask, flood fill from (0,0), then invert back
bg_flood = Image.new("L", (w + 2, h + 2), 0)
mask_pil = Image.fromarray((final_mask * 255).astype(np.uint8))
# Feather slightly
mask_feather = mask_pil.filter(ImageFilter.GaussianBlur(radius=1.0))

cutout = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cutout.paste(im, (0, 0), mask_feather)
cutout.save("preview_red/lenin_cutout_v2.png")
print("Saved lenin_cutout_v2.png")
