# -*- coding: utf-8 -*-
import subprocess

script = """
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$pres = $ppt.Presentations.Add()
$slide = $pres.Slides.Add(1, 12)
Write-Output "--- Slide.Shapes methods ---"
$slide.Shapes | Get-Member | Where-Object { $_.Name -like "*3d*" -or $_.Name -like "*Model*" } | Select-Object Name, MemberType

Write-Output "--- Slide.Shapes.Add... methods ---"
$slide.Shapes | Get-Member | Where-Object { $_.Name -like "Add*" } | Select-Object Name

$pres.Close()
$ppt.Quit()
"""

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", script], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
