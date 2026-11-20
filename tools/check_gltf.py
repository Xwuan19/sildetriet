# -*- coding: utf-8 -*-
import json
import os

gltf_path = r"assets\models3d\lenin_seattle\Lenin_Statue_@_Seattle.gltf"
with open(gltf_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Images:", len(data.get("images", [])))
for img in data.get("images", []):
    print(" - Image uri:", img.get("uri"))

print("Materials:", len(data.get("materials", [])))
print("Meshes:", len(data.get("meshes", [])))
print("Nodes:", len(data.get("nodes", [])))
