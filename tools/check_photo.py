from PIL import Image

p = r"C:\Users\ADMIN\Downloads\photo_2026-11-17_17-17-54.jpg"
im = Image.open(p)
print(f"photo_2026-11-17_17-17-54.jpg: size={im.size}, mode={im.mode}")
im.resize((300, 300)).save("preview_red/check_photo_marx.png")
