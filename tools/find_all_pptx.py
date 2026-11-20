import zipfile
from pathlib import Path

# Check if there are any other pptx files in C:\Users\ADMIN\Downloads\SlidePPT or other folders
for p in Path(r"C:\Users\ADMIN\Downloads").glob("**/*.pptx"):
    print("Found PPTX:", p)
