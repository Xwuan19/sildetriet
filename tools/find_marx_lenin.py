import os
from pathlib import Path

# Search for any file with 'marx' or 'lenin' in name in Downloads
dl = Path(r"C:\Users\ADMIN\Downloads")
for root, dirs, files in os.walk(dl):
    for f in files:
        if any(w in f.lower() for w in ["marx", "lenin", "poster", "mac"]):
            print(os.path.join(root, f))
