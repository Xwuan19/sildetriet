from PIL import Image

im = Image.open("assets/master_stage_bg.png")
for y in range(850, 945, 10):
    print(f"y={y}: x=1000:{im.getpixel((1000, y))}, x=1050:{im.getpixel((1050, y))}, x=1100:{im.getpixel((1100, y))}")
