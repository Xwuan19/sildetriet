# Cài 5 font của bộ slide cho riêng tài khoản Windows hiện tại (không cần quyền admin).
# Cách chạy: mở PowerShell tại thư mục này rồi gõ
#   powershell -ExecutionPolicy Bypass -File .\Cai_dat_font.ps1
# Sau khi cài, mở lại PowerPoint/Word để menu font nhận đủ.

$ErrorActionPreference = 'Stop'

# Hiển thị tiếng Việt đúng trong cửa sổ PowerShell.
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$fontsDir = Join-Path $PSScriptRoot 'fonts'
$userFontDir = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
$regKey = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'

$fonts = @(
    @{ File = 'PlayfairEditorial.ttf';        Label = 'Playfair Editorial (TrueType)' },
    @{ File = 'PlayfairEditorial-Italic.ttf'; Label = 'Playfair Editorial Italic (TrueType)' },
    @{ File = 'ScriptViet-Bold.ttf';          Label = 'Script Viet (TrueType)' },
    @{ File = 'BeVietnamPro-Regular.ttf';     Label = 'Be Vietnam Pro (TrueType)' },
    @{ File = 'BeVietnamPro-SemiBold.ttf';    Label = 'Be Vietnam Pro SemiBold (TrueType)' }
)

$missing = $fonts | Where-Object { -not (Test-Path (Join-Path $fontsDir $_.File)) }
if ($missing) {
    Write-Host 'Thiếu file font trong thư mục fonts:' -ForegroundColor Red
    $missing | ForEach-Object { Write-Host ('  - ' + $_.File) }
    exit 1
}

New-Item -ItemType Directory -Force -Path $userFontDir | Out-Null
if (-not (Test-Path $regKey)) { New-Item -Path $regKey -Force | Out-Null }

Add-Type -Namespace SlideFontInstall -Name Api -MemberDefinition @'
[DllImport("gdi32.dll", SetLastError=true, CharSet=CharSet.Unicode)] public static extern int AddFontResourceExW(string lpFileName, uint fl, IntPtr pdv);
[DllImport("gdi32.dll", SetLastError=true, CharSet=CharSet.Unicode)] public static extern bool RemoveFontResourceExW(string lpFileName, uint fl, IntPtr pdv);
[DllImport("user32.dll")] public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, IntPtr lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
'@

foreach ($f in $fonts) {
    $src = Join-Path $fontsDir $f.File
    $dst = Join-Path $userFontDir $f.File
    # Font đang được Windows nạp sẽ bị khoá; bản đã cài thì dùng luôn.
    if (Test-Path $dst) {
        Write-Host ('  đã có: ' + $f.File)
    } else {
        Copy-Item $src $dst -Force
        Write-Host ('  đã cài: ' + $f.File)
    }
    New-ItemProperty -Path $regKey -Name $f.Label -Value $f.File -PropertyType String -Force | Out-Null
    [void][SlideFontInstall.Api]::AddFontResourceExW($dst, 0, [IntPtr]::Zero)
}

# Gỡ bản "Dancing Script Bold" cũ (tên family chứa tên dành riêng của OFL) nếu máy đã từng cài.
$oldFile = Join-Path $userFontDir 'DancingScript-Bold.ttf'
if (Test-Path $oldFile) {
    [void][SlideFontInstall.Api]::RemoveFontResourceExW($oldFile, 0, [IntPtr]::Zero)
    Remove-Item $oldFile -Force -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $regKey -Name 'DancingScript-Bold (TrueType)' -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $regKey -Name 'Dancing Script Bold (TrueType)' -ErrorAction SilentlyContinue
    Write-Host '  đã gỡ font cũ Dancing Script Bold'
}

$r = [UIntPtr]::Zero
[void][SlideFontInstall.Api]::SendMessageTimeout([IntPtr]0xffff, 0x001D, [UIntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$r)

Write-Host ''
Write-Host 'Xong. Đã cài font cho tài khoản hiện tại.' -ForegroundColor Green
Write-Host 'Mở lại PowerPoint nếu đang mở. File PPTX vẫn hiển thị đúng cả khi máy chưa cài font,'
Write-Host 'vì font đã được nhúng sẵn trong file; cài font chỉ cần khi bạn muốn sửa chữ.'
