from PIL import Image, ImageDraw, ImageFilter
import numpy as np

# Let's trace the exact boundary of Lenin
# We can do this with 60-80 precise points!
# Let's look closely at where each feature is:
# Forehead: x=242, y=175
# Brow: x=245, y=195
# Eye socket indent: x=250, y=210
# Nose bridge: x=248, y=222
# Nose tip: x=238, y=235
# Under nose: x=248, y=242
# Mustache top: x=242, y=248
# Mustache corner: x=252, y=260
# Upper lip: x=258, y=270
# Lower lip / goatee top: x=255, y=285
# Goatee bulge: x=247, y=305
# Beard tip: x=244, y=325
# Beard bottom: x=250, y=345
# Under chin: x=265, y=360
# Throat shadow: x=280, y=370
# Collar fold: x=288, y=385
# Shirt collar: x=275, y=405
# Coat lapel notch: x=245, y=435
# Left lapel outer edge:
# x=210, y=475
# x=170, y=515
# x=135, y=550
# x=105, y=580
# x=75, y=612
# x=65, y=624 (outer shoulder hook)
# x=55, y=640
# x=40, y=660
# x=25, y=675
# x=10, y=700
# x=0, y=715
# x=0, y=750 (bottom-left)

# Cap visor & crown:
# Visor tip: x=235, y=162
# Visor top corner: x=240, y=145
# Visor band seam: x=248, y=125
# Cap front fold: x=258, y=100
# Cap front puff: x=275, y=75
# Cap front top: x=300, y=48
# Cap crown slope: x=330, y=28
# Cap apex: x=365, y=14
# Cap crest: x=410, y=12
# Cap crest right: x=455, y=20
# Cap rear slope: x=500, y=40
# Cap rear puff: x=545, y=70
# Cap back fold: x=580, y=105
# Cap back rim: x=605, y=140
# Cap back tip: x=615, y=165
# Under cap rear indent: x=575, y=185
# Hair / neck top: x=550, y=215
# Neck / ear back: x=530, y=245
# Neck straight down: x=525, y=275
# Lower neck: x=530, y=310
# Coat collar back: x=540, y=350
# Shoulder seam: x=555, y=395
# Right shoulder slope:
# x=575, y=435
# x=605, y=480
# x=635, y=530
# x=660, y=590
# x=680, y=660
# x=700, y=720
# x=700, y=750 (bottom-right)

pts = [
    (0, 750), (0, 715), (10, 700), (25, 675), (40, 660), (55, 640),
    (65, 624), (75, 612), (105, 580), (135, 550), (170, 515), (210, 475),
    (245, 435), (275, 405), (288, 385), (280, 370), (265, 360), (250, 345),
    (244, 325), (247, 305), (255, 285), (258, 270), (252, 260), (242, 248),
    (248, 242), (238, 235), (248, 222), (250, 210), (245, 195), (242, 175),
    (235, 162), (240, 145), (248, 125), (258, 100), (275, 75), (300, 48),
    (330, 28), (365, 14), (410, 12), (455, 20), (500, 40), (545, 70),
    (580, 105), (605, 140), (615, 165), (575, 185), (550, 215), (530, 245),
    (525, 275), (530, 310), (540, 350), (555, 395), (575, 435), (605, 480),
    (635, 530), (660, 590), (680, 660), (700, 720), (700, 750),
]

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGBA")
w, h = im.size

mask = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(mask)
draw.polygon(pts, fill=255)
mask_feather = mask.filter(ImageFilter.GaussianBlur(radius=1.2))

cutout = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cutout.paste(im, (0, 0), mask_feather)
cutout.save("preview_red/lenin_cutout_clean.png")

# Also composite on dark red background to verify how it looks in presentation!
bg = Image.new("RGBA", (w, h), (142, 25, 29, 255))
comp = Image.alpha_composite(bg, cutout)
comp.save("preview_red/lenin_comp_preview.png")

print("Saved lenin_cutout_clean.png and lenin_comp_preview.png")
