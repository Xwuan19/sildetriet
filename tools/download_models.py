# -*- coding: utf-8 -*-
import os
import urllib.request
import zipfile

out_dir = os.path.abspath("assets/models3d")
os.makedirs(out_dir, exist_ok=True)

targets = [
    ("thingiverse-573194", "Bust_of_Lenin_573194.zip"),
    ("thingiverse-4390524", "Karl_Marx_Bust__4390524.zip"),
]

for identifier, zip_name in targets:
    url = f"https://archive.org/download/{identifier}/{zip_name}"
    local_zip = os.path.join(out_dir, zip_name)
    print(f"Downloading {url}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp, open(local_zip, "wb") as f:
        f.write(resp.read())
    print(f"Downloaded {local_zip} ({os.path.getsize(local_zip)} bytes)")

    # Extract
    extract_folder = os.path.join(out_dir, identifier)
    with zipfile.ZipFile(local_zip, "r") as z:
        z.extractall(extract_folder)
        print(f"Extracted to {extract_folder}:")
        for member in z.namelist():
            print(f"  - {member}")
