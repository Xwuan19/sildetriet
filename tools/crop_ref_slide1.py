from PIL import Image

f = Image.open("preview_red/video_first_6s/f_023.png")
slide1 = f.crop((70, 70, 1850, 1010))
slide1.save("preview_red/ref_slide1_full.png")
print("Saved ref_slide1_full.png")
