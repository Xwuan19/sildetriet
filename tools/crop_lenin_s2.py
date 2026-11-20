from PIL import Image

im = Image.open("preview_red/ref_slide2_clean.png")
# Crop the exact same area as lenin_clean_crop.png
lenin_s2_crop = im.crop((950, 130, 1680, 890))
lenin_s2_crop.save("preview_red/lenin_s2_crop.png")
print("Saved lenin_s2_crop.png")
