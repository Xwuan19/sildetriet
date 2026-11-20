# -*- coding: utf-8 -*-
import urllib.request
import json

for item_id in ["thingiverse-573194", "thingiverse-5901392"]:
    url = f"https://archive.org/metadata/{item_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"=== {item_id}: {data.get('metadata', {}).get('title')} ===")
            for f in data.get("files", []):
                name = f.get("name", "")
                if name.endswith((".stl", ".obj", ".glb", ".gltf", ".zip")):
                    print(f"  {name} ({f.get('size')} bytes)")
    except Exception as e:
        print("Error:", e)
