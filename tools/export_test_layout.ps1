$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pptx = (Resolve-Path "preview_red/test_slide2_layout.pptx").Path
    $outDir = Join-Path (Resolve-Path "preview_red").Path "test_slide2_export"
    if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
    $pres = $ppt.Presentations.Open($pptx, $true, $false, $false)
    $pres.Export($outDir, "PNG", 1920, 1080)
    $pres.Close()
    Write-Host "Exported test slide 2 layout successfully!"
} finally {
    $ppt.Quit()
}
