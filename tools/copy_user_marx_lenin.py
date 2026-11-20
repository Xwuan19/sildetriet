from PIL import Image
import shutil

src = r"C:\Users\ADMIN\AppData\Local\Temp\opencode\uploads\ff2ce66e-e1af-4dcd-a6f3-371237481d50\image.png"
dst = r"assets\marx_lenin_user_raw.png"
shutil.copy(src, dst)

im = Image.open(dst)
print(f"Copied to {dst}: size={im.size}, mode={im.mode}")
