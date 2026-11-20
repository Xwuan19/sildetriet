# -*- coding: utf-8 -*-
import subprocess

ps_code = """
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$slide = $pres.Slides.Add(1, 12)
$hasMethod = Get-Member -InputObject $slide.Shapes -Name "Add3DModel"
Write-Output ("Has Add3DModel: " + ($hasMethod -ne $null))
$pres.Close()
$ppt.Quit()
"""

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_code], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
