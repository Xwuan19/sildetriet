# -*- coding: utf-8 -*-
import json

with open("assets/models3d/lenin_seattle/Lenin_Statue_@_Seattle.gltf", "r", encoding="utf-8") as f:
    d = json.load(f)

print("Images:", len(d.get("images", [])))
for img in d.get("images", []):
    print("  img:", img)
print("Textures:", len(d.get("textures", [])))
print("Materials:", len(d.get("materials", [])))
for mat in d.get("materials", []):
    print("  mat:", mat)
