# -*- coding: utf-8 -*-
import subprocess

ps_code = r"""
$path_lenin = "C:\Users\ADMIN\Downloads\sildetriet\assets\models3d\thingiverse-573194\files\lenin.stl"
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()

# Set widescreen 16:9 (13.333 x 7.5 inches)
$pres.PageSetup.SlideWidth = 13.333 * 72
$pres.PageSetup.SlideHeight = 7.5 * 72

# Slide 1
$s1 = $pres.Slides.Add(1, 12)
$m1 = $s1.Shapes.Add3DModel($path_lenin, 0, -1, 550, 60, 360, 420)
$m1.Name = "!!HERO_3D"
$m1.Model3D.RotationY = -25
$m1.Model3D.RotationX = 8

# Slide 2
$s2 = $pres.Slides.Add(2, 12)
$m2 = $s2.Shapes.Add3DModel($path_lenin, 0, -1, 650, 70, 300, 350)
$m2.Name = "!!HERO_3D"
$m2.Model3D.RotationY = 55
$m2.Model3D.RotationX = 12
$s2.SlideShowTransition.EntryEffect = 3915 # Morph
$s2.SlideShowTransition.Duration = 2.0
$s2.SlideShowTransition.AdvanceOnTime = -1
$s2.SlideShowTransition.AdvanceTime = 3.0

# Slide 3
$s3 = $pres.Slides.Add(3, 12)
$m3 = $s3.Shapes.Add3DModel($path_lenin, 0, -1, 520, 50, 380, 440)
$m3.Name = "!!HERO_3D"
$m3.Model3D.RotationY = 10
$m3.Model3D.RotationX = 5
$s3.SlideShowTransition.EntryEffect = 3915 # Morph
$s3.SlideShowTransition.Duration = 2.0
$s3.SlideShowTransition.AdvanceOnTime = -1
$s3.SlideShowTransition.AdvanceTime = 3.0

$test_file = (Join-Path (Get-Location) "preview_red\test_3d_morph_deck.pptx")
$pres.SaveAs($test_file)

# Test video export
$mp4_file = (Join-Path (Get-Location) "preview_red\test_3d_morph.mp4")
if (Test-Path $mp4_file) { Remove-Item $mp4_file -Force }
Write-Output "Exporting test 3D morph video..."
$pres.CreateVideo($mp4_file, $true, 2, 720, 30, 85)

$timeout = 60
$elapsed = 0
while ($pres.CreateVideoStatus -eq 1 -and $elapsed -lt $timeout) {
    Start-Sleep -Seconds 1
    $elapsed++
}
Write-Output ("Video status: " + $pres.CreateVideoStatus)

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_3d_video.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_3d_video.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
