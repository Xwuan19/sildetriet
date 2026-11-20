from PIL import Image

im = Image.open("preview_red/ref_slide1_clean.png")
for y in range(800, 870, 10):
    print(f"y={y}: x=1050:{im.getpixel((1050, y))}")
