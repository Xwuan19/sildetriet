from PIL import Image

im = Image.open("preview_red/ref_slide1_clean.png")
w, h = im.size

# Lenin bounding box in ref_slide1_clean.png:
# x is roughly from 950 to 1680 (right edge)
# y is roughly from 130 (cap) to 900 (bottom of coat before the bottom bar)
lenin_crop = im.crop((950, 130, 1680, 890))
lenin_crop.save("preview_red/lenin_clean_crop.png")
print(f"Lenin crop size: {lenin_crop.size}")
