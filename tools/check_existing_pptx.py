import zipfile
import os

files = [
    r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx",
    r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Chuan_Morph.pptx",
]

for f in files:
    if os.path.exists(f):
        print("=== Checking:", f, "===")
        with zipfile.ZipFile(f, 'r') as z:
            media = [n for n in z.namelist() if n.startswith("ppt/media/")]
            print(f"Media count: {len(media)}")
            for m in media[:15]:
                info = z.getinfo(m)
                print(f"  {m} ({info.file_size} bytes)")
