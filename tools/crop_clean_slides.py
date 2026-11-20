from PIL import Image

f = Image.open("preview_red/exact_ref_50fps/frame_0080.png")
# The monitor screen in the video has black/beige borders around it!
# Let's find the inner slide coordinates inside the 1920x1080 video!
# In frame 80, the inner slide display is roughly from x: 74 to 1846 (width 1772), y: 74 to 1010 (height 936)
# Let's crop the actual slide from frame 80!
slide_crop = f.crop((70, 70, 1850, 1010))
slide_crop.save("preview_red/frame80_slide_clean.png")

# Also let's inspect frame 0001 (Slide 1) clean
f1 = Image.open("preview_red/exact_ref_50fps/frame_0001.png")
slide1_crop = f1.crop((70, 70, 1850, 1010))
slide1_crop.save("preview_red/frame01_slide_clean.png")

print(f"Slide crop size: {slide_crop.size}")
