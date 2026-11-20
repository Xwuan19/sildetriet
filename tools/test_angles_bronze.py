# -*- coding: utf-8 -*-
import subprocess

ps_test = r"""
$path_gltf = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()

$angles = @(
    @{y = 160; name = "angle_160"},
    @{y = 190; name = "angle_190"},
    @{y = 210; name = "angle_210"},
    @{y = 230; name = "angle_230"}
)

$i = 1
foreach ($a in $angles) {
    $s = $pres.Slides.Add($i, 12)
    $shp = $s.Shapes.Add3DModel($path_gltf, 0, -1, 150, 40, 450, 580)
    $shp.Model3D.RotationX = -90
    $shp.Model3D.RotationY = $a.y
    $shp.Model3D.RotationZ = 0
    $out_png = (Join-Path (Get-Location) ("preview_red\" + $a.name + ".png"))
    $s.Export($out_png, "PNG", 960, 540)
    Write-Output ("Exported " + $a.name)
    $i++
}

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_angles_bronze.ps1", "w", encoding="utf-8") as f:
    f.write(ps_test)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_angles_bronze.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
