from PIL import Image

im2 = Image.open("preview_red/ref_slide2_clean.png")

# Sculpted banner:
# x: ~0 to 760, y: ~220 to 920
banner_crop = im2.crop((0, 220, 780, 920))
banner_crop.save("preview_red/banner_crop_raw.png")

# Gold emblem (Hammer & sickle + star):
# x: ~220 to 580, y: ~60 to 330
emblem_crop = im2.crop((230, 60, 580, 330))
emblem_crop.save("preview_red/emblem_crop_raw.png")

print("Saved banner_crop_raw.png and emblem_crop_raw.png")
