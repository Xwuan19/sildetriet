# -*- coding: utf-8 -*-
import subprocess

ps_script = r"""
$path = "C:\Users\ADMIN\Downloads\sildetriet\assets\models3d\thingiverse-573194\files\lenin.stl"
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$pres = $ppt.Presentations.Add()
$slide1 = $pres.Slides.Add(1, 12)

Write-Output "Trying Add3DModel..."
# Parameters: FileName, LinkToFile, SaveWithDocument, Left, Top, Width, Height
# LinkToFile: msoFalse = 0, SaveWithDocument: msoTrue = -1 (or 1)
try {
    $shp1 = $slide1.Shapes.Add3DModel($path, 0, -1, 100, 100, 300, 300)
    Write-Output ("Shape created: " + $shp1.Name + ", Type: " + $shp1.Type)
    $m3d = $shp1.Model3D
    Write-Output ("Model3D: " + ($m3d -ne $null))
    Write-Output ("RotationX: " + $m3d.RotationX)
    Write-Output ("RotationY: " + $m3d.RotationY)
    Write-Output ("RotationZ: " + $m3d.RotationZ)
} catch {
    Write-Output ("Error: " + $_.Exception.Message)
}

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_insert_3d_win.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_insert_3d_win.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
