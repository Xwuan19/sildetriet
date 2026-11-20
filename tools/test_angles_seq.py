# -*- coding: utf-8 -*-
import subprocess

ps_code = r"""
$path_gltf = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()

# Let's test a sequence of Y angles from 150 to 300 to find the best 3 angles
$angles = @(
    @{y = 180; name = "angle_180"},
    @{y = 205; name = "angle_205"},
    @{y = 220; name = "angle_220"},
    @{y = 240; name = "angle_240"},
    @{y = 260; name = "angle_260"}
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

with open("tools/test_angles_seq.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_angles_seq.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
