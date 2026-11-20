# Nhúng font vào PPTX và xuất PDF/PNG.
# Chỉ cần chạy sau khi build_deck.py vừa dựng lại file .pptx.
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$root = Split-Path -Parent $PSScriptRoot
$fontsDir = Join-Path $root 'fonts'
$pptx = Join-Path $root 'Triet_hoc_Mac_Lenin_Loi_chao.pptx'
$preview = Join-Path $root 'preview_red'
$pngDir = Join-Path $preview 'final_png'
$pdf = Join-Path $preview 'Triet_hoc_Mac_Lenin_Loi_chao.pdf'
$tmp = Join-Path $preview '_embedded.pptx'

New-Item -ItemType Directory -Force -Path $preview, $pngDir | Out-Null
if (Test-Path $tmp) { Remove-Item $tmp -Force }
if (Test-Path $pdf) { Remove-Item $pdf -Force }
Get-ChildItem $pngDir -Filter '*.PNG' -ErrorAction SilentlyContinue | Remove-Item -Force

Add-Type -Namespace SlideFont -Name Api -MemberDefinition @'
[DllImport("gdi32.dll", SetLastError=true, CharSet=CharSet.Unicode)] public static extern int AddFontResourceExW(string lpFileName, uint fl, IntPtr pdv);
[DllImport("user32.dll")] public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, IntPtr lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
'@

# Nạp đúng 5 font deck dùng vào session hiện tại để PowerPoint nhìn thấy trước khi nhúng.
$fontFiles = @(
    'PlayfairEditorial.ttf',
    'PlayfairEditorial-Italic.ttf',
    'ScriptViet-Bold.ttf',
    'BeVietnamPro-Regular.ttf',
    'BeVietnamPro-SemiBold.ttf'
)
$fontFiles | ForEach-Object {
    [void][SlideFont.Api]::AddFontResourceExW((Join-Path $fontsDir $_), 0, [IntPtr]::Zero)
}
$r = [UIntPtr]::Zero
[void][SlideFont.Api]::SendMessageTimeout([IntPtr]0xffff, 0x001D, [UIntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$r)

# Bật tuỳ chọn nhúng font của PowerPoint (HKCU, không cần quyền admin).
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
    Write-Output 'Đã nhúng font và lưu file PPTX chính thức.'

    $pres = $ppt.Presentations.Open($pptx, $true, $false, $false)
    $pres.SaveAs($pdf, 32)
    $pres.Export($pngDir, 'PNG', 1920, 1080)
    $pres.Close()
    Write-Output ('Đã xuất PDF: ' + $pdf)
    Write-Output ('Đã xuất PNG: ' + $pngDir)
} finally {
    $ppt.Quit()
    if (Test-Path $tmp) { Remove-Item $tmp -Force }
}
