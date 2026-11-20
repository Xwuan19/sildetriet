import zipfile
from pathlib import Path

for name in ["mau 6_19.10.pptx", "mau 5_1810.pptx", "23.4.pptx"]:
    p = Path(r"C:\Users\ADMIN\Downloads\SlidePPT\examppt") / name
    with zipfile.ZipFile(p, 'r') as z:
        print(f"--- {name} ---")
        for n in z.namelist():
            if n.startswith("ppt/media/"):
                print(n, z.getinfo(n).file_size)
