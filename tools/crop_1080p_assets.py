from PIL import Image

f = Image.open("preview_red/exact_ref_50fps/frame_0080.png")
print("Frame 80 size:", f.size)

# Crop the worker & flag on bottom-left:
# x: 0 to 750, y: 300 to 1080
p_crop = f.crop((0, 300, 750, 1080))
p_crop.save("preview_red/frame80_poster.png")

# Crop Hammer & Sickle + Star on top-left:
# x: 50 to 550, y: 50 to 350
s_crop = f.crop((50, 50, 550, 350))
s_crop.save("preview_red/frame80_star_hammer.png")

# Crop Lenin watermark on the right:
# x: 1050 to 1920, y: 100 to 1080
l_crop = f.crop((1050, 100, 1920, 1080))
l_crop.save("preview_red/frame80_lenin_watermark.png")

print("Saved 1080p crops from frame 80!")
