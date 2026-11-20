# -*- coding: utf-8 -*-
import os
import subprocess

lenin_stl = os.path.abspath("assets/models3d/thingiverse-573194/files/lenin.stl").replace("\\", "/")
marx_stl = os.path.abspath("assets/models3d/thingiverse-4390524/files/Marx_Bust.stl").replace("\\", "/")

ps_script = f"""
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$pres = $ppt.Presentations.Add()

Write-Output "Testing Add3DModel with Lenin STL: {lenin_stl}"
$slide1 = $pres.Slides.Add(1, 12) # ppLayoutBlank = 12
$shp1 = $slide1.Shapes.Add3DModel("{lenin_stl}", 0, 1, 100, 100, 300, 300)
Write-Output ("Shape created: " + $shp1.Name + ", Type: " + $shp1.Type)

# Inspect Model3DFormat
$m3d = $shp1.Model3D
Write-Output ("Model3D properties: " + ($m3d | Get-Member | Select-Object -ExpandProperty Name))
Write-Output ("Initial RotationX: " + $m3d.RotationX + ", RotationY: " + $m3d.RotationY + ", RotationZ: " + $m3d.RotationZ)

# Set rotation
$m3d.RotationY = 45
Write-Output ("New RotationY: " + $m3d.RotationY)

# Add slide 2 and morph
$slide2 = $pres.Slides.Add(2, 12)
$shp2 = $slide2.Shapes.Add3DModel("{lenin_stl}", 0, 1, 400, 100, 300, 300)
$shp2.Name = $shp1.Name # Match name for morph
$shp2.Model3D.RotationY = 180

# Configure Morph
$slide2.SlideShowTransition.EntryEffect = 3915 # Morph transition code
$slide2.SlideShowTransition.Duration = 2.0

$test_pptx = (Join-Path (Get-Location) "preview_red\\test_3d_morph.pptx")
$pres.SaveAs($test_pptx)
$pres.Close()
$ppt.Quit()
Write-Output "Saved test presentation successfully!"
"""

with open("tools/test_insert_3d.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_insert_3d.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
