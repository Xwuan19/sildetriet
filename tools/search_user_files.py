import os
from pathlib import Path

# Search entire Downloads, Desktop, Pictures for any image with Marx/Lenin or recently created
search_dirs = [
    Path(r"C:\Users\ADMIN\Downloads"),
    Path(r"C:\Users\ADMIN\Desktop"),
    Path(r"C:\Users\ADMIN\Pictures"),
]

for sdir in search_dirs:
    if sdir.exists():
        for root, dirs, files in os.walk(sdir):
            if any(k in root for k in ["node_modules", ".git", ".venv", "preview_red"]):
                continue
            for f in files:
                if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
                    p = Path(root) / f
                    # check if name contains marx or lenin or mac or triet
                    fn = f.lower()
                    if any(k in fn for k in ["marx", "lenin", "mac", "triet", "anh", "image", "photo", "screen"]):
                        print(p)
