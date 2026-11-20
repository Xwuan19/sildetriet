import numpy as np
from PIL import Image, ImageFilter, ImageDraw

# Load the raw mask
mask_im = Image.open("preview_red/test_lenin_raw_mask.png").convert("L")
arr = np.array(mask_im)
h, w = arr.shape

# Let's inspect the boundary of Lenin:
# For each y:
# The coat / cap starts at some x_min and ends at some x_max
# Let's define the boundary curve manually or semi-automatically with key points:
# Key points on Lenin's perimeter:
# Cap top-left: around (370, 10)
# Cap top-center: (480, 5)
# Cap top-right: (600, 40)
# Cap right overhang: (650, 90), (700, 130) -> goes to right edge
# Cap peak/visor: (340, 160)
# Eyebrow / temple: (350, 190)
# Nose tip: (345, 260)
# Mustache / upper lip: (355, 305)
# Beard tip: (350, 430), (370, 470)
# Chin / neck under beard: (410, 490)
# Coat lapel notch: (380, 520)
# Coat shoulder left: (280, 620), (100, 720), (0, 750)
# Bottom edge: (0, 750) to (700, 750)
# Right edge: (700, 750) up to (700, 130)

poly_points = [
    (375, 12),
    (440, 6),
    (510, 8),
    (580, 30),
    (640, 80),
    (685, 140),
    (700, 165),
    (700, 750),
    (0, 750),
    (0, 720),
    (80, 680),
    (140, 640),
    (240, 580),
    (320, 525),
    (360, 490),
    (345, 450),
    (345, 380),
    (355, 340),
    (348, 300),
    (342, 265),
    (352, 240),
    (340, 180),
    (335, 160),
    (348, 140),
    (340, 110),
    (360, 60),
    (375, 12)
]

solid_mask = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(solid_mask)
draw.polygon(poly_points, fill=255)

# Smooth the boundary slightly with 1px Gaussian blur
smooth_mask = solid_mask.filter(ImageFilter.GaussianBlur(radius=1.2))

# Load original Lenin image
im_lenin = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGBA")
cutout = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cutout.paste(im_lenin, (0, 0), smooth_mask)

cutout.save("assets/lenin_painted_cutout.png")
cutout.save("preview_red/lenin_painted_cutout_preview.png")
print("Saved assets/lenin_painted_cutout.png!")
