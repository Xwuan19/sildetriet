import zipfile
import os

src = r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx"
out_dir = "preview_red/slideppt_media"
os.makedirs(out_dir, exist_ok=True)

with zipfile.ZipFile(src, 'r') as z:
    for n in z.namelist():
        if n.startswith("ppt/media/"):
            fname = os.path.basename(n)
            with open(os.path.join(out_dir, fname), "wb") as out_f:
                out_f.write(z.read(n))

print("Extracted media to", out_dir)
