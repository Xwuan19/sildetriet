import os
from pathlib import Path

# Search for input_file_0.png or any file named *input_file*
for root, dirs, files in os.walk(r"C:\Users\ADMIN"):
    if any(k in root for k in ["node_modules", ".git"]):
        continue
    for f in files:
        if "input_file" in f.lower():
            print(os.path.join(root, f))
