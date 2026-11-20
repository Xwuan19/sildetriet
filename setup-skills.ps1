$ErrorActionPreference = 'Stop'

$root = 'C:\Users\ACER\Downloads\sildetriet'
$dl   = Join-Path $root '.download'
$tmp  = Join-Path $dl 'tmp'
$tools = Join-Path $root 'tools'
$skills = Join-Path $root '.opencode\skills'

New-Item -ItemType Directory -Force -Path $dl, $tmp, $tools, $skills | Out-Null

$repos = @(
    @{ Key='PPT-Design-Skill';       Owner='sunchaokun';          Repo='PPT-Design-Skill';       Branch='main'   },
    @{ Key='huashu-design';          Owner='alchaincyf';          Repo='huashu-design';          Branch='master' },
    @{ Key='guizang-ppt-skill';      Owner='op7418';              Repo='guizang-ppt-skill';      Branch='main'   },
    @{ Key='academic-pptx-skill';    Owner='Gabberflast';         Repo='academic-pptx-skill';    Branch='main'   },
    @{ Key='agent-research-skills';  Owner='lingzhi227';          Repo='agent-research-skills';  Branch='main'   },
    @{ Key='ppt-master';             Owner='hugohe3';             Repo='ppt-master';             Branch='main'   },
    @{ Key='Paper2Slides';           Owner='HKUDS';               Repo='Paper2Slides';           Branch='main'   },
    @{ Key='350-layout-compositions';Owner='nevertoday';          Repo='350-layout-compositions';Branch='main'   }
)

foreach ($r in $repos) {
    $dest = Join-Path $tools $r.Key
    if ((Test-Path $dest) -and ((Test-Path (Join-Path $dest 'README.md')) -or (Test-Path (Join-Path $dest 'SKILL.md')))) {
        Write-Host "SKIP (already in tools) $($r.Key)"
        continue
    }

    $zip = Join-Path $dl ($r.Key + '.zip')
    $url = "https://codeload.github.com/$($r.Owner)/$($r.Repo)/zip/refs/heads/$($r.Branch)"
    if ((Test-Path $zip) -and ((Get-Item $zip).Length -gt 0)) {
        Write-Host "SKIP DOWNLOAD (cached) $($r.Owner)/$($r.Repo)"
    } else {
        Write-Host "DOWNLOAD $($r.Owner)/$($r.Repo) -> $zip"
        & curl.exe -L --fail --silent --show-error -o $zip $url
        if ($LASTEXITCODE -ne 0) { throw "Download failed: $url" }
    }

    $ex = Join-Path $tmp $r.Key
    if (Test-Path $ex) { Remove-Item -Recurse -Force $ex }
    New-Item -ItemType Directory -Force -Path $ex | Out-Null
    $oldEap = $ErrorActionPreference
    $ErrorActionPreference = 'SilentlyContinue'
    & tar.exe -xf $zip -C $ex 2>$null
    $tarCode = $LASTEXITCODE
    $ErrorActionPreference = $oldEap

    $src = Get-ChildItem -Directory -Path $ex | Select-Object -First 1
    if (-not $src -or -not (Test-Path (Join-Path $src.FullName 'README.md')) -and -not (Test-Path (Join-Path $src.FullName 'SKILL.md'))) {
        throw "Extract produced no usable repo for $($r.Key) (tar exit $tarCode)"
    }
    if ($tarCode -ne 0) { Write-Host "WARN tar exit $tarCode for $($r.Key) but content is complete" }

    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Move-Item -Path $src.FullName -Destination $dest
    Write-Host "OK $dest"
}

function Copy-IntoSkill([string]$from, [string]$name) {
    $dst = Join-Path $skills $name
    if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Copy-Item -Path (Join-Path $from '*') -Destination $dst -Recurse -Force
}

# Install true skills with their supporting files.
Copy-IntoSkill (Join-Path $tools 'huashu-design')       'huashu-design'
Copy-IntoSkill (Join-Path $tools 'guizang-ppt-skill')   'guizang-ppt-skill'
Copy-IntoSkill (Join-Path $tools 'academic-pptx-skill') 'academic-pptx'
Copy-IntoSkill (Join-Path $tools 'agent-research-skills') 'agent-research-skills'

# ppt-design-skill stores SKILL.md in a subdir named "skill"; flatten so OpenCode
# derives the skill ID from the directory name instead of the literal id "skill".
Copy-IntoSkill (Join-Path $tools 'PPT-Design-Skill\skill') 'ppt-design-skill'

# Remove the duplicated slide-generation skill from the research bundle.
$dup = Join-Path $skills 'agent-research-skills\skills\slide-generation'
if (Test-Path $dup) { Remove-Item -Recurse -Force $dup; Write-Host "Removed duplicate: $dup" }

Write-Host 'DONE'
