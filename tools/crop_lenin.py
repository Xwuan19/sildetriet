from PIL import Image

im = Image.open("preview_red/video_1080p_frames/f_004.png")
# The video frame has black monitor borders around the slide.
# Let's crop just the slide canvas from f_004.png!
# Monitor screen border: let's find the exact bounding box of the slide canvas.
# In f_004.png, size is 1920x1080.
# The slide inside the screen is approx:
# x: ~110 to 1810, y: ~60 to 910
# Let's crop the Lenin portrait specifically:
w, h = im.size
lenin_crop = im.crop((int(0.55 * w), int(0.18 * h), int(0.92 * w), int(0.88 * h)))
lenin_crop.save("preview_red/video_lenin_crop.png")
print("Saved preview_red/video_lenin_crop.png")
