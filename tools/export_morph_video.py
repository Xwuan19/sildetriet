# -*- coding: utf-8 -*-
"""Export PPTX with Morph transitions to MP4 video and inspect transition frames."""
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PPTX = ROOT / "Triet_hoc_Mac_Lenin_Loi_chao.pptx"
MP4 = ROOT / "preview_red" / "morph_preview.mp4"

ps_script = f"""
$pptx = "{str(PPTX).replace('\\', '\\\\')}"
$mp4 = "{str(MP4).replace('\\', '\\\\')}"

if (Test-Path $mp4) {{ Remove-Item $mp4 -Force }}

$ppt = New-Object -ComObject PowerPoint.Application
try {{
    $pres = $ppt.Presentations.Open($pptx, $false, $false, $false)
    # Default second per slide = 2, vertical resolution = 1080, fps = 30, quality = 85
    $pres.CreateVideo($mp4, $true, 2, 1080, 30, 85)
    
    $timeout = 60
    while ($pres.CreateVideoStatus -eq 1 -and $timeout -gt 0) {{
        Start-Sleep -Seconds 1
        $timeout--
        Write-Host -NoNewline "."
    }}
    Write-Host ""
    Write-Output ("CreateVideo status: " + $pres.CreateVideoStatus)
    $pres.Close()
}} finally {{
    $ppt.Quit()
}}

if (Test-Path $mp4) {{
    Get-Item $mp4 | Select-Object Name, Length
}} else {{
    Write-Error "Video file not found!"
}}
"""

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
