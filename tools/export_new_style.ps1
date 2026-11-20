$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pptx = (Resolve-Path "preview_red/test_slide2_new_style.pptx").Path
    $outDir = Join-Path (Resolve-Path "preview_red").Path "test_new_style_export"
    if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
    $pres = $ppt.Presentations.Open($pptx, $true, $false, $false)
    $pres.Export($outDir, "PNG", 1920, 1080)
    $pres.Close()
    Write-Host "Exported new style successfully!"
} finally {
    $ppt.Quit()
}
