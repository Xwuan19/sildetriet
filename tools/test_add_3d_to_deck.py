# -*- coding: utf-8 -*-
import subprocess

ps_test = r"""
$pptx_in = (Join-Path (Get-Location) "Triet_hoc_Mac_Lenin_Loi_chao.pptx")
$lenin_path = (Join-Path (Get-Location) "assets\models3d\thingiverse-573194\files\lenin.stl")
$marx_path = (Join-Path (Get-Location) "assets\models3d\thingiverse-4390524\files\Marx_Bust.stl")

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$pres = $ppt.Presentations.Open($pptx_in)

Write-Output ("Slides count: " + $pres.Slides.Count)

# Slide 1: Add 3D Lenin Model
$s1 = $pres.Slides.Item(1)
# Delete existing 2D Lenin image if any
foreach ($shp in $s1.Shapes) {
    if ($shp.Name -eq "!!LENIN_HERO") {
        $shp.Delete()
        break
    }
}
$m1 = $s1.Shapes.Add3DModel($lenin_path, 0, -1, 8.28 * 72, 0.45 * 72, 4.45 * 72, 6.75 * 72)
$m1.Name = "!!LENIN_3D"
$m1.Model3D.RotationY = -20
$m1.Model3D.RotationX = 10
Write-Output ("Added 3D Model to Slide 1: " + $m1.Name)

# Slide 2: Add 3D Lenin Model with rotated angle
$s2 = $pres.Slides.Item(2)
foreach ($shp in $s2.Shapes) {
    if ($shp.Name -eq "!!LENIN_HERO") {
        $shp.Delete()
        break
    }
}
$m2 = $s2.Shapes.Add3DModel($lenin_path, 0, -1, 9.20 * 72, 0.60 * 72, 3.80 * 72, 5.80 * 72)
$m2.Name = "!!LENIN_3D"
$m2.Model3D.RotationY = 50
$m2.Model3D.RotationX = 14
Write-Output ("Added 3D Model to Slide 2: " + $m2.Name)

# Slide 3: Add 3D Lenin Model or Marx
$s3 = $pres.Slides.Item(3)
foreach ($shp in $s3.Shapes) {
    if ($shp.Name -eq "!!LENIN_HERO") {
        $shp.Delete()
        break
    }
}
$m3 = $s3.Shapes.Add3DModel($lenin_path, 0, -1, 8.10 * 72, 0.40 * 72, 4.60 * 72, 6.90 * 72)
$m3.Name = "!!LENIN_3D"
$m3.Model3D.RotationY = 340 # ~ -20 degrees, completing a continuous dynamic rotation
$m3.Model3D.RotationX = 8
Write-Output ("Added 3D Model to Slide 3: " + $m3.Name)

$test_out = (Join-Path (Get-Location) "preview_red\test_deck_with_3d.pptx")
$pres.SaveAs($test_out)

# Export slide PNGs
$s1.Export((Join-Path (Get-Location) "preview_red\test_s1_3d.png"), "PNG", 1920, 1080)
$s2.Export((Join-Path (Get-Location) "preview_red\test_s2_3d.png"), "PNG", 1920, 1080)
$s3.Export((Join-Path (Get-Location) "preview_red\test_s3_3d.png"), "PNG", 1920, 1080)

Write-Output "Exported slide PNGs!"
$pres.Close()
$ppt.Quit()
"""

with open("tools/test_add_3d_to_deck.ps1", "w", encoding="utf-8") as f:
    f.write(ps_test)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_add_3d_to_deck.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
