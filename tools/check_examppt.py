import zipfile
from pathlib import Path

for p in sorted(Path(r"C:\Users\ADMIN\Downloads\SlidePPT\examppt").glob("*.pptx")):
    with zipfile.ZipFile(p, 'r') as z:
        media_count = len([n for n in z.namelist() if n.startswith("ppt/media/")])
        print(f"{p.name}: {media_count} media files")
