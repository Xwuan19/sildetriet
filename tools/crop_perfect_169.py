from PIL import Image

# Load slide1_bg_restored before any smearing:
# Reconstruct by taking:
# center from slide1_bg_restored.png
# top-right from ref_slide1_clean.png
# bottom-left from ref_slide1_clean.png

im_center = Image.open("preview_red/slide1_bg_restored.png")
im_s1 = Image.open("preview_red/ref_slide1_clean.png")

# Patch top right
im_center.paste(im_s1.crop((1400, 0, 1680, 250)), (1400, 0))
# Patch bottom left
im_center.paste(im_s1.crop((0, 600, 250, 880)), (0, 600))

# Now let's crop the active, watermark-free 16:9 area:
# y from 0 to 880 (height = 880)
# width = 880 * 16 / 9 = 1564.44 -> 1564
# x from (1680 - 1564) // 2 = 58 to 58 + 1564 = 1622
crop_169 = im_center.crop((58, 0, 1622, 880))
crop_169 = crop_169.resize((1920, 1080), Image.Resampling.LANCZOS)
crop_169.save("assets/master_stage_bg.png")
crop_169.save("preview_red/master_stage_bg_1080p.png")
print("Saved 1920x1080 master_stage_bg_1080p.png!")
