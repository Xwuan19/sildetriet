# -*- coding: utf-8 -*-
import json
import subprocess

colors = [
    ("Dark_Bronze", [0.35, 0.24, 0.15, 1.0], 0.1, 0.6),
    ("Warm_Bronze_Gold", [0.52, 0.38, 0.22, 1.0], 0.15, 0.5),
    ("Deep_Antique_Bronze", [0.25, 0.18, 0.12, 1.0], 0.05, 0.7),
    ("Ivory_Marble", [0.88, 0.85, 0.80, 1.0], 0.0, 0.8),
]

with open("assets/models3d/lenin_seattle/Lenin_Statue_@_Seattle.gltf", "r", encoding="utf-8") as f:
    base_dict = json.load(f)

for name, col, met, rough in colors:
    d = json.loads(json.dumps(base_dict))
    d["materials"] = [
        {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": col,
                "metallicFactor": met,
                "roughnessFactor": rough
            },
            "doubleSided": True
        }
    ]
    for m in d.get("meshes", []):
        for p in m.get("primitives", []):
            p["material"] = 0
            
    gltf_p = f"preview_red/test_{name}.gltf"
    with open(gltf_p, "w", encoding="utf-8") as out_f:
        json.dump(d, out_f)

ps_script = r"""
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$pres.PageSetup.SlideWidth = 13.333 * 72
$pres.PageSetup.SlideHeight = 7.50 * 72

$models = @("Dark_Bronze", "Warm_Bronze_Gold", "Deep_Antique_Bronze", "Ivory_Marble")
for ($i = 0; $i -lt $models.Count; $i++) {
    $name = $models[$i]
    $s = $pres.Slides.Add($i + 1, 12)
    # Set background crimson
    $bg = $s.Shapes.AddShape(1, 0, 0, 13.333 * 72, 7.50 * 72)
    $bg.Fill.Solid()
    $bg.Fill.ForeColor.RGB = 0x14126B # #6B1214 BGR
    $bg.Line.Visible = 0
    
    $m_path = (Join-Path (Get-Location) "preview_red\test_$name.gltf")
    $m = $s.Shapes.Add3DModel($m_path, 0, -1, 8.15 * 72, 0.25 * 72, 4.70 * 72, 6.60 * 72)
    $m.Model3D.RotationX = -90
    $m.Model3D.RotationY = 205
    $m.Model3D.RotationZ = 0
    
    $out_png = (Join-Path (Get-Location) "preview_red\test_col_$name.png")
    $s.Export($out_png, "PNG", 1920, 1080)
}

$pres.Close()
$ppt.Quit()
Write-Output "Done testing 4 colors!"
"""

with open("preview_red/run_color_tests.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "preview_red/run_color_tests.ps1"], capture_output=True, text=True)
print(res.stdout)
