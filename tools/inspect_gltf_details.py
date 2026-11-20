# -*- coding: utf-8 -*-
import json
import os

gltf_file = r"assets\models3d\lenin_seattle\Lenin_Statue_@_Seattle.gltf"
with open(gltf_file, "r", encoding="utf-8") as f:
    d = json.load(f)

print("Keys:", d.keys())
print("Meshes:", len(d.get("meshes", [])))
for i, m in enumerate(d.get("meshes", [])):
    prims = m.get("primitives", [])
    print(f"Mesh {i}: {len(prims)} prims, attributes: {list(prims[0].get('attributes', {}).keys()) if prims else 'none'}")
