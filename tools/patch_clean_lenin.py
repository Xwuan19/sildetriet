from PIL import Image

im_base = Image.open("preview_red/raw_lenin_670.png").copy()
im_slide1 = Image.open("preview_red/ref_slide1_clean.png")

# Slide 1 crop corresponding to top right:
# raw_lenin_670 is from (980, 140, 1680, 890) of crop_clean_t_6.70.png
# Let's patch the region x: 450 to 700, y: 0 to 180
patch_s1 = im_slide1.crop((980 + 450, 140, 980 + 700, 140 + 180))
im_base.paste(patch_s1, (450, 0))

im_base.save("preview_red/lenin_full_clean_raw.png")
print("Saved lenin_full_clean_raw.png")
