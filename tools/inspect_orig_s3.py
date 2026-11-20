# -*- coding: utf-8 -*-
from PIL import Image

im = Image.open("archive/debug/tweak/Slide3.PNG")
w, h = im.size
print("Size:", w, h)
# Let's inspect where the circle is on Slide3.PNG
# We can search for the golden circular line
