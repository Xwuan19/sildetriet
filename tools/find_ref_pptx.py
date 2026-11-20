import os
from pathlib import Path

# Search for any pptx file in Downloads or current folder
for root, dirs, files in os.walk(r"C:\Users\ADMIN"):
    if any(k in root for k in ["node_modules", ".git", "AppData\\Local\\Microsoft", "AppData\\Local\\Google"]):
        continue
    for f in files:
        if f.lower().endswith(".pptx") and not "Triet_hoc_Mac_Lenin_Loi_chao" in f:
            print(os.path.join(root, f))
