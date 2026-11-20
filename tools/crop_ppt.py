from PIL import Image

im = Image.open("preview_red/video_1080p_frames/f_001.png")
# Crop the PowerPoint slide area
# The screen monitor is in the center
w, h = im.size
# Crop center monitor area: x from 0.2*w to 0.95*w, y from 0.2*h to 0.9*h
slide_crop = im.crop((int(0.28 * w), int(0.25 * h), int(0.92 * w), int(0.90 * h)))
slide_crop.save("preview_red/f001_ppt_crop.png")
print("Saved preview_red/f001_ppt_crop.png")
