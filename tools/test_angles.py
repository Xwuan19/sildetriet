# -*- coding: utf-8 -*-
import subprocess

ps_code = r"""
$path_obj = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Seattle.obj")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()

$angles = @(
    @{x = -90; y = 0; z = 0; name = "rot_neg90_x"},
    @{x = 90; y = 0; z = 0; name = "rot_pos90_x"},
    @{x = 0; y = 0; z = -90; name = "rot_neg90_z"},
    @{x = 0; y = 0; z = 90; name = "rot_pos90_z"},
    @{x = -90; y = 90; z = 0; name = "rot_neg90x_pos90y"},
    @{x = -90; y = -90; z = 0; name = "rot_neg90x_neg90y"},
    @{x = -90; y = 180; z = 0; name = "rot_neg90x_180y"}
)

$i = 1
foreach ($a in $angles) {
    $s = $pres.Slides.Add($i, 12)
    $shp = $s.Shapes.Add3DModel($path_obj, 0, -1, 200, 50, 400, 500)
    $shp.Model3D.RotationX = $a.x
    $shp.Model3D.RotationY = $a.y
    $shp.Model3D.RotationZ = $a.z
    $out_png = (Join-Path (Get-Location) ("preview_red\" + $a.name + ".png"))
    $s.Export($out_png, "PNG", 960, 540)
    Write-Output ("Exported " + $a.name)
    $i++
}

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_angles.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_angles.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
