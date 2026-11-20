import os
from pathlib import Path

for root, dirs, files in os.walk(r"C:\Users\ADMIN"):
    if any(k in root for k in ["node_modules", ".git", "AppData\\Local\\Microsoft"]):
        continue
    for f in files:
        if f.lower().endswith((".ttf", ".otf")):
            if any(k in f.lower() for k in ["goth", "fraktur", "old", "blackletter", "textura", "chancellor"]):
                print(os.path.join(root, f))
