from PIL import Image

f80 = Image.open("preview_red/frame80_slide_clean.png")
# "Nội Dung Trình Bày" in f80 is roughly x: 990 to 1640, y: 100 to 220
header = f80.crop((990, 100, 1640, 220))
header.save("preview_red/crop_header_gothic.png")
print("Saved crop_header_gothic.png")
