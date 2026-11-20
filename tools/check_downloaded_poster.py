from PIL import Image

p = r"C:\Users\ADMIN\Downloads\images1615341-lanh-tu-lenin-vi-dai-qua-loat-tranh-co-dong-hung-huc-khi-the-hinh-3.jpg"
im = Image.open(p)
print(f"File size={im.size}, mode={im.mode}")
im.save("preview_red/check_poster_original.png")
