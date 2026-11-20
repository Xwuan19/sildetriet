from PIL import Image, ImageDraw
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png")
w, h = im.size

# Let's define key boundary points around Lenin's silhouette:
# Starting from bottom-left (0, 750):
pts = [
    (0, 750),
    (0, 720),
    (30, 680),
    (68, 624),   # Coat bump on left
    (80, 615),
    (110, 580),
    (160, 530),
    (210, 480),
    (270, 430),  # Collar start
    (310, 400),
    (290, 370),  # Chin / beard base
    (250, 340),  # Beard tip
    (245, 300),  # Beard mid
    (252, 270),  # Mustache
    (242, 235),  # Nose tip
    (250, 220),  # Nose bridge
    (245, 180),  # Forehead
    (235, 155),  # Cap peak tip
    (250, 120),  # Cap visor curve
    (260, 90),
    (270, 70),   # Cap front bump
    (310, 30),
    (360, 15),   # Cap top
    (420, 15),
    (480, 35),
    (540, 75),
    (585, 125),  # Cap back corner
    (605, 165),
    (580, 200),  # Head back
    (540, 240),  # Neck back
    (535, 290),
    (550, 350),  # Collar back
    (565, 410),  # Shoulder start
    (600, 460),
    (640, 520),
    (670, 600),
    (690, 680),
    (700, 750),  # Bottom right
]

overlay = im.copy()
draw = ImageDraw.Draw(overlay)
draw.line(pts + [pts[0]], fill=(0, 255, 0), width=3)
overlay.save("preview_red/test_boundary_line.png")
print("Saved test_boundary_line.png")
