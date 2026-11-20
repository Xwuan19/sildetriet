import numpy as np
from PIL import Image, ImageDraw, ImageFilter

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGBA")
w, h = im.size

# High-precision contour coordinates for Lenin:
poly = [
    # Hat crown top & right
    (365, 14),   # top apex
    (410, 15),
    (455, 24),
    (500, 48),
    (535, 78),
    (565, 110),
    (575, 130),
    (585, 145),
    (595, 160),
    (600, 172),  # hat rightmost rim tip
    # Under hat rim to head/ear
    (560, 180),
    (535, 190),
    (525, 205),
    (535, 225),  # ear outer lobe
    (535, 255),  # ear bottom / jaw angle
    (540, 275),  # collar top
    # Coat right shoulder & arm
    (555, 305),
    (575, 350),
    (605, 410),
    (635, 475),
    (660, 545),
    (685, 625),
    (700, 680),
    (700, 750),  # bottom right
    (0, 750),    # bottom left
    (0, 725),
    (20, 695),
    (45, 660),
    (75, 620),   # coat left shoulder
    (105, 580),
    (135, 545),
    (170, 505),
    (205, 465),
    (235, 435),  # coat lapel notch
    (265, 400),  # collar fold
    (265, 365),  # throat
    (245, 335),  # beard tip
    (244, 310),  # goatee
    (250, 280),  # lower lip
    (245, 260),  # mustache
    (238, 238),  # nose tip
    (246, 218),  # nose bridge
    (245, 195),  # brow
    (242, 175),  # forehead
    (235, 160),  # cap visor tip
    (242, 140),  # visor seam
    (255, 110),  # cap front fold
    (275, 75),   # cap front puff
    (310, 40),
]

mask = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(mask)
draw.polygon(poly, fill=255)

# Subtle anti-aliased edge (blur 1.2px)
mask_blur = mask.filter(ImageFilter.GaussianBlur(radius=1.0))

cutout = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cutout.paste(im, (0, 0), mask_blur)

# Save test
cutout.save("preview_red/lenin_perfect_cutout.png")
cutout.save("assets/lenin_painted_cutout.png")
print("Saved assets/lenin_painted_cutout.png successfully!")
