# -*- coding: utf-8 -*-
import subprocess

ps_test = r"""
$path_gltf = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Statue_@_Seattle.gltf")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$s1 = $pres.Slides.Add(1, 12)

try {
    Write-Output "Adding 3D model from gltf..."
    $shp = $s1.Shapes.Add3DModel($path_gltf, 0, -1, 100, 50, 400, 500)
    Write-Output ("Shape created: " + $shp.Name + ", Type: " + $shp.Type)
    $m3d = $shp.Model3D
    Write-Output ("RotationX: " + $m3d.RotationX + ", RotationY: " + $m3d.RotationY)
    $s1.Export((Join-Path (Get-Location) "preview_red\test_seattle_render.png"), "PNG", 1920, 1080)
    Write-Output "Rendered seattle lenin to PNG successfully!"
} catch {
    Write-Output ("Error: " + $_.Exception.Message)
}

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_seattle_ppt.ps1", "w", encoding="utf-8") as f:
    f.write(ps_test)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_seattle_ppt.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
