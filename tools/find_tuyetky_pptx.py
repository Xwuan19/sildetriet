import os
from pathlib import Path

for root, dirs, files in os.walk(r"C:\Users\ADMIN"):
    if any(k in root for k in ["node_modules", ".git", "AppData\\Local\\Microsoft", "AppData\\Local\\Google"]):
        continue
    for f in files:
        if any(w in f.lower() for w in ["tuyetky", "quan diem", "nha nuoc", "chu nghia mac"]):
            print(os.path.join(root, f))
