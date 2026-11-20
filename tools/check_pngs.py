# -*- coding: utf-8 -*-
from PIL import Image

for path in ["archive/debug/png/Slide 1.PNG", "archive/debug/png/Slide 2.PNG", "archive/debug/tweak/Slide1.PNG", "archive/debug/tweak/Slide3.PNG"]:
    try:
        im = Image.open(path)
        print(f"{path}: size={im.size}")
    except Exception as e:
        print(f"Error {path}: {e}")
