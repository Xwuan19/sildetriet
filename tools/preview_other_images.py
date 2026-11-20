from PIL import Image

for name in ["image1.png", "image3.png", "image4.png"]:
    im = Image.open(f"preview_red/slideppt_media/{name}")
    preview = im.resize((960, 540))
    preview.save(f"preview_red/{name}_preview.png")
    print(f"Saved preview_red/{name}_preview.png")
