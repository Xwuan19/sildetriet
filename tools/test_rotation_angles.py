# -*- coding: utf-8 -*-
import subprocess

ps_code = r"""
$path_lenin = "C:\Users\ADMIN\Downloads\sildetriet\assets\models3d\thingiverse-573194\files\lenin.stl"
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()

# Slide 1
$s1 = $pres.Slides.Add(1, 12)
$m1 = $s1.Shapes.Add3DModel($path_lenin, 0, -1, 300, 100, 300, 300)
$m1.Name = "!!LENIN_3D"
$m1.Model3D.RotationY = 0

# Slide 2: test 180 degrees
$s2 = $pres.Slides.Add(2, 12)
$m2 = $s2.Shapes.Add3DModel($path_lenin, 0, -1, 300, 100, 300, 300)
$m2.Name = "!!LENIN_3D"
$m2.Model3D.RotationY = 180
$s2.SlideShowTransition.EntryEffect = 3915
$s2.SlideShowTransition.Duration = 2.0

# Slide 3: test 360 vs 359 degrees
$s3 = $pres.Slides.Add(3, 12)
$m3 = $s3.Shapes.Add3DModel($path_lenin, 0, -1, 300, 100, 300, 300)
$m3.Name = "!!LENIN_3D"
$m3.Model3D.RotationY = 359
$s3.SlideShowTransition.EntryEffect = 3915
$s3.SlideShowTransition.Duration = 2.0

$video_file = (Join-Path (Get-Location) "preview_red\test_rotation_check.mp4")
if (Test-Path $video_file) { Remove-Item $video_file -Force }
$pres.CreateVideo($video_file, $true, 1, 720, 30, 85)

$elapsed = 0
while ($pres.CreateVideoStatus -eq 1 -and $elapsed -lt 60) {
    Start-Sleep -Seconds 1
    $elapsed++
}
Write-Output ("Video export status: " + $pres.CreateVideoStatus)
$pres.Close()
$ppt.Quit()
"""

with open("tools/test_rotation_angles.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_rotation_angles.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
