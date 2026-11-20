$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$root = Split-Path -Parent $PSScriptRoot
$fontsDir = Join-Path $root 'fonts'
$pptx = Join-Path $root 'Triet_hoc_Mac_Lenin_Nhom_4.pptx'
$preview = Join-Path $root 'preview_red'
$pngDir = Join-Path $preview 'nhom4_png'
$pdf = Join-Path $preview 'Triet_hoc_Mac_Lenin_Nhom_4.pdf'
$tmp = Join-Path $preview '_embedded_nhom4.pptx'

New-Item -ItemType Directory -Force -Path $preview, $pngDir | Out-Null
if (Test-Path $tmp) { Remove-Item $tmp -Force }
if (Test-Path $pdf) { Remove-Item $pdf -Force }
Get-ChildItem $pngDir -Filter '*.PNG' -ErrorAction SilentlyContinue | Remove-Item -Force

Add-Type -Namespace SlideFont -Name Api -MemberDefinition @'
[DllImport("gdi32.dll", SetLastError=true, CharSet=CharSet.Unicode)] public static extern int AddFontResourceExW(string lpFileName, uint fl, IntPtr pdv);
[DllImport("user32.dll")] public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, IntPtr lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
'@

Get-ChildItem $fontsDir -Filter '*.ttf' | ForEach-Object {
    [SlideFont.Api]::AddFontResourceExW($_.FullName, 0x10, [IntPtr]::Zero) | Out-Null
}
$dummy = [UIntPtr]::Zero
[SlideFont.Api]::SendMessageTimeout([IntPtr]0xffff, 0x001D, [UIntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$dummy) | Out-Null

$key = 'HKCU:\Software\Microsoft\Office\16.0\PowerPoint\Options'
if (-not (Test-Path $key)) { New-Item -Path $key -Force | Out-Null }
New-ItemProperty -Path $key -Name 'EmbedTrueTypeFonts' -Value 1 -PropertyType DWord -Force | Out-Null
New-ItemProperty -Path $key -Name 'EmbedOnlyUsedCharacters' -Value 1 -PropertyType DWord -Force | Out-Null

$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pres = $ppt.Presentations.Open($pptx, $false, $false, $false)
    $pres.SaveAs($tmp, 24, -1)
    $pres.Close()
    Copy-Item $tmp $pptx -Force

    $pres = $ppt.Presentations.Open($pptx, $true, $false, $false)
    $pres.SaveAs($pdf, 32)
    $pres.Export($pngDir, 'PNG', 1920, 1080)
    $pres.Close()
    Write-Output "Đã xuất PDF: $pdf"
    Write-Output "Đã xuất PNG: $pngDir"
} finally {
    $ppt.Quit()
    if (Test-Path $tmp) { Remove-Item $tmp -Force }
}
