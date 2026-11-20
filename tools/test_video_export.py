# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PPTX = str(ROOT / "Triet_hoc_Mac_Lenin_Loi_chao.pptx")
MP4 = str(ROOT / "preview_red" / "morph_preview.mp4")

ps_script = f"""
$pptx = '{PPTX}'
$mp4 = '{MP4}'
if (Test-Path $mp4) {{ Remove-Item $mp4 -Force }}

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
try {{
    $pres = $ppt.Presentations.Open($pptx, $false, $false, $false)
    Write-Output "Starting CreateVideo..."
    $pres.CreateVideo($mp4, $true, 4, 720, 30, 85)
    
    # Wait until status is in progress or queued
    Start-Sleep -Seconds 1
    $timeout = 90
    while (($pres.CreateVideoStatus -eq 0 -or $pres.CreateVideoStatus -eq 1) -and $timeout -gt 0) {{
        Start-Sleep -Seconds 1
        $timeout--
        Write-Output ("Status: " + $pres.CreateVideoStatus + " (remaining " + $timeout + "s)")
    }}
    Write-Output ("Final Status: " + $pres.CreateVideoStatus)
    $pres.Close()
}} finally {{
    $ppt.Quit()
}}

if (Test-Path $mp4) {{
    Write-Output ("Video created! Size: " + (Get-Item $mp4).Length)
}} else {{
    Write-Output "Video not found!"
}}
"""

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
