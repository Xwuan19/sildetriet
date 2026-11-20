# -*- coding: utf-8 -*-
import subprocess

ps_script = """
$pptx = (Resolve-Path "test_morph.pptx").Path
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptx, $false, $false, $false)
$mp4 = Join-Path (Get-Location) "test_morph.mp4"
if (Test-Path $mp4) { Remove-Item $mp4 -Force }
$pres.CreateVideo($mp4, $true, 2, 720, 30, 85)
$timeout = 30
while ($pres.CreateVideoStatus -eq 1 -and $timeout -gt 0) {
    Start-Sleep -Seconds 1
    $timeout--
}
Write-Output ("CreateVideo status: " + $pres.CreateVideoStatus)
$pres.Close()
$ppt.Quit()
if (Test-Path $mp4) { Get-Item $mp4 | Select-Object Name, Length }
"""

res = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Error:", res.stderr)
