from PIL import Image

im = Image.open("preview_red/video_1080p_frames/f_004.png")
# Let's check dimensions and find the exact screen border
w, h = im.size
print(f"Size: {w}x{h}")
# Let's crop just the slide canvas from f_004
# The black bezel is around x=85 to 1835, y=55 to 1030
# Let's find exact coordinates
crop_screen = im.crop((85, 55, 1835, 1025))
crop_screen.save("preview_red/f004_screen_crop.png")
print("Saved f004_screen_crop.png")
