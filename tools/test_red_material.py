# -*- coding: utf-8 -*-
import json
import subprocess

# Test 1: red baseColorFactor, metallic=0, roughness=1.0
with open("assets/models3d/lenin_seattle/Lenin_Statue_@_Seattle.gltf", "r", encoding="utf-8") as f:
    d = json.load(f)

d["materials"] = [
    {
        "name": "RedTest",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.8, 0.1, 0.1, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.9
        }
    }
]
for m in d.get("meshes", []):
    for p in m.get("primitives", []):
        p["material"] = 0

with open("preview_red/test_red_mat.gltf", "w", encoding="utf-8") as f:
    json.dump(d, f)

ps_test = r"""
$pptx = (Join-Path (Get-Location) "preview_red\test_mat.pptx")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$s1 = $pres.Slides.Add(1, 12)
$shp = $s1.Shapes.Add3DModel((Join-Path (Get-Location) "preview_red\test_red_mat.gltf"), 0, -1, 150, 40, 450, 580)
$s1.Export((Join-Path (Get-Location) "preview_red\test_red_render.png"), "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Output "Done test red"
"""
with open("preview_red/test_red.ps1", "w", encoding="utf-8") as f:
    f.write(ps_test)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "preview_red/test_red.ps1"], capture_output=True, text=True)
print(res.stdout)
