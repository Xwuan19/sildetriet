from PIL import Image

for p in ["assets/lenin_warm.png", "assets/lenin_medallion.png"]:
    im = Image.open(p)
    print(f"{p}: size={im.size}, mode={im.mode}")
