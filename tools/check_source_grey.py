from PIL import Image

im = Image.open("preview_red/crop_clean_t_6.70.png")
print("At y=840..860, x=1050 in crop_clean_t_6.70:")
for y in range(830, 870, 5):
    print(f"y={y}: {im.getpixel((1050, y))}")
