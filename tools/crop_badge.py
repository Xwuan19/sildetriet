from PIL import Image

f80 = Image.open("preview_red/frame80_slide_clean.png")
# Badge 01 is located around x: 990 to 1065, y: 260 to 335
badge1 = f80.crop((990, 260, 1065, 335))
badge1.save("preview_red/badge_crop_01.png")
print("Saved badge_crop_01.png")
