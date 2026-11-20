from PIL import Image, ImageDraw, ImageFilter
import numpy as np

# Fine-tuned silhouette points:
pts = [
    # Bottom left of coat
    (0, 750),
    (0, 715),
    (25, 675),
    (65, 624),   # Coat shoulder point
    (80, 612),
    (105, 580),
    (135, 550),
    (170, 515),
    (210, 475),
    (250, 435),
    (275, 405),  # Lapel top near neck
    (288, 385),
    (280, 370),  # Under chin/beard curve
    (265, 360),
    (250, 345),  # Lower beard
    (244, 325),  # Beard tip
    (247, 300),  # Mid beard
    (254, 275),  # Upper beard
    (252, 260),  # Mustache corner
    (242, 248),  # Mustache top
    (238, 235),  # Nose tip
    (248, 222),  # Nose bridge
    (245, 195),  # Eyebrow / brow bone
    (242, 175),  # Forehead
    (235, 162),  # Visor tip
    (240, 145),  # Visor top edge
    (248, 125),  # Visor band
    (258, 100),  # Cap fold
    (275, 75),   # Cap front slant
    (300, 48),
    (330, 28),   # Cap crown
    (365, 14),   # Cap apex
    (410, 12),
    (455, 20),
    (500, 40),
    (545, 70),
    (580, 105),  # Cap back fold
    (605, 140),  # Cap back edge
    (615, 165),  # Cap back tip
    (595, 190),  # Under cap back
    (565, 215),  # Hair back
    (538, 245),  # Ear / jaw angle
    (532, 275),  # Neck
    (535, 310),  # Collar back
    (545, 350),  # Coat collar back
    (560, 395),  # Shoulder start
    (580, 435),
    (610, 480),
    (640, 530),
    (665, 590),
    (685, 660),
    (700, 720),
    (700, 750),  # Bottom right
]

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGBA")
w, h = im.size

# Create high-res mask
mask = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(mask)
draw.polygon(pts, fill=255)

# Slight Gaussian blur on mask for realistic antialiasing
mask_feather = mask.filter(ImageFilter.GaussianBlur(radius=1.2))

# Composite into transparent PNG
cutout = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cutout.paste(im, (0, 0), mask_feather)

cutout.save("preview_red/lenin_cutout_test.png")
print("Saved lenin_cutout_test.png")
