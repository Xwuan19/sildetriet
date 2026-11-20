from PIL import Image

for idx in [1, 5, 10, 15, 20]:
    im = Image.open(f"preview_red/intro_slideshow/s_{idx:03d}.png")
    im.resize((480, 270)).save(f"preview_red/check_intro_{idx}.png")
print("Saved check intro")
