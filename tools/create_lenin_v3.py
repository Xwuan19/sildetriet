import numpy as np
from PIL import Image, ImageDraw, ImageFilter

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGBA")
w, h = im.size

# Exact razor-sharp boundary points:
poly = [
    # Top of cap
    (365, 14),
    (410, 15),
    (455, 24),
    (500, 48),
    (535, 78),
    (565, 105),
    (575, 125),
    (585, 140),
    (595, 155),
    (605, 172),  # hat rim rear tip
    # Under the hat rim:
    (570, 175),
    (535, 180),
    (505, 188),  # head under rim
    (495, 205),
    (505, 220),  # top of ear
    (528, 235),  # ear outer rim
    (525, 255),  # ear bottom
    (490, 260),  # under ear / jawline
    (475, 275),  # neck back
    (525, 290),  # coat collar top
    (532, 315),  # coat collar outer curve
    (530, 335),
    (540, 355),
    (560, 375),  # right shoulder start
    (585, 400),
    (615, 435),
    (645, 485),
    (670, 545),
    (690, 615),
    (700, 670),
    (700, 750),  # bottom right
    (0, 750),    # bottom left
    (0, 720),
    (25, 680),
    (55, 635),
    (85, 595),
    (115, 560),
    (145, 530),
    (180, 495),
    (205, 465),
    (240, 435),
    (270, 400),  # collar fold
    (285, 370),  # throat/neck under chin
    (255, 350),  # bottom of beard
    (248, 335),  # beard tip
    (245, 310),  # goatee
    (248, 280),  # lower lip
    (244, 260),  # mustache
    (242, 245),  # upper lip / mustache fold
    (238, 235),  # nose tip
    (244, 220),  # nose bridge
    (244, 195),  # brow
    (242, 175),  # forehead
    (235, 160),  # cap visor tip
    (242, 140),  # visor top seam
    (255, 110),  # cap front crease
    (275, 75),   # cap front puff
    (310, 40),   # cap front slope
]

mask = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(mask)
draw.polygon(poly, fill=255)

# Subtle Gaussian blur for natural artistic edge (radius = 0.8)
mask_blur = mask.filter(ImageFilter.GaussianBlur(radius=0.8))

cutout = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cutout.paste(im, (0, 0), mask_blur)

cutout.save("preview_red/lenin_cutout_v3.png")
print("Saved preview_red/lenin_cutout_v3.png")
