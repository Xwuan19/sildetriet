from PIL import Image

im = Image.open("assets/lenin_hero_clean.png")
print("lenin_hero_clean size:", im.size, "mode:", im.mode)
preview = im.resize((480, int(im.height * 480 / im.width)))
preview.save("preview_red/lenin_hero_clean_preview.png")
print("Saved preview_red/lenin_hero_clean_preview.png")
