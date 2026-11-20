# -*- coding: utf-8 -*-
import subprocess

ps_script = r"""
$path = "C:\Users\ADMIN\Downloads\sildetriet\assets\models3d\thingiverse-573194\files\lenin.stl"
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$slide1 = $pres.Slides.Add(1, 12)
$shp1 = $slide1.Shapes.Add3DModel($path, 0, -1, 100, 100, 300, 300)
$m3d = $shp1.Model3D

$m3d.RotationY = 45
$m3d.RotationX = 15
Write-Output ("After set -> RotationX: " + $m3d.RotationX + ", RotationY: " + $m3d.RotationY)

# Export slide as PNG to see what it looks like!
$test_png = (Join-Path (Get-Location) "preview_red\test_3d_render.png")
$slide1.Export($test_png, "PNG", 1920, 1080)
Write-Output "Exported 3D render to PNG!"

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_rotate_3d.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_rotate_3d.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
