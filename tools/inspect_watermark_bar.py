from PIL import Image

im = Image.open("preview_red/ref_slide1_clean.png")
w, h = im.size
print(f"Size: {w}x{h}")

# The watermark bar at the bottom:
# Let's inspect pixels from y=850 to 945
for y in range(850, 945, 10):
    print(f"y={y}: center pixel={im.getpixel((840, y))[:3]}, left pixel={im.getpixel((100, y))[:3]}")
