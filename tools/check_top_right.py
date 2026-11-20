from PIL import Image

im1 = Image.open("preview_red/ref_slide1_clean.png")
# Crop top right of lenin in slide 1:
crop_tr1 = im1.crop((980 + 400, 140, 980 + 700, 140 + 200))
crop_tr1.save("preview_red/check_tr1.png")
print("Saved check_tr1.png")
