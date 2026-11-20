from PIL import Image

im = Image.open("preview_red/intro_frames/f_001.png")
# Zoom into Slide 1 and Slide 2 thumbnails
t1_t2 = im.crop((80, 240, 275, 480))
t1_t2.save("preview_red/t1_t2_f001.png")
print("Saved t1_t2_f001.png")
