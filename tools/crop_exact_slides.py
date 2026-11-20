from PIL import Image

BOX = (120, 70, 1800, 1015)

# Let's crop slide1 at t=6.0 (before transition)
im_s1 = Image.open("preview_red/slide1_t6.0.png")
s1_crop = im_s1.crop(BOX)
s1_crop.save("preview_red/ref_slide1_clean.png")

# Let's crop slide 2 at 8.5s
im_s2 = Image.open("preview_red/slide2_full_1080p.png")
s2_crop = im_s2.crop(BOX)
s2_crop.save("preview_red/ref_slide2_clean.png")

print(f"Clean cropped sizes: {s1_crop.size}, {s2_crop.size}")
