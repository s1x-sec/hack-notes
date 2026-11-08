<#
  sync-notes.ps1 - Mirror the Obsidian vault into Quartz content/, normalize
  Obsidian-only syntax for strict GitHub-Flavored Markdown, then commit and push.

  The source vault is treated as READ-ONLY and is never modified.
  Run by Task Scheduler every 30 min; also safe to run by hand.
  NOTE: keep this file ASCII-only so Windows PowerShell 5.1 parses it correctly.
#>

[CmdletBinding()]
param(
  [string]$Vault = "C:\Users\rodri\Documentos\Sync\HACK_NOTES",
  [string]$Repo  = "C:\Users\rodri\Documents\quartz-site",
  [switch]$NoPush          # skip git commit/push (used for first local run)
)

$ErrorActionPreference = "Stop"
$Content = Join-Path $Repo "content"
function Log($m) { Write-Output ("[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $m) }

# --- UTF-8 (no BOM) file writer -------------------------------------------
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Write-Text([string]$Path, [string]$Text) {
  [System.IO.File]::WriteAllText($Path, $Text, $Utf8NoBom)
}

# --- 0. Align local repo with remote so pushes stay fast-forward ----------
# (handles edits made directly on GitHub; content is regenerated from the
#  vault below, so adopting the remote tip loses nothing.)
if (-not $NoPush -and (Test-Path -LiteralPath (Join-Path $Repo ".git"))) {
  Push-Location -LiteralPath $Repo
  if ((git remote) -contains "origin") {
    Log "Aligning local repo with origin/main ..."
    git fetch origin --quiet
    if ($LASTEXITCODE -eq 0) {
      git reset --hard origin/main | Out-Null
    } else {
      Log "WARNING: git fetch failed (offline?) - continuing with local state."
    }
  }
  Pop-Location
}

# --- 1. Mirror vault -> content (deletions included), excluding vault config
Log "Mirroring vault -> content ..."
# robocopy exit codes 0-7 = success, 8+ = error
$null = robocopy $Vault $Content /MIR /XD ".obsidian" /NFL /NDL /NJH /NJS /NP /R:2 /W:2
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with code $LASTEXITCODE" }

# --- 2. Homepage: generate content/index.md from the HOME note ------------
$homeNote = Join-Path $Content "00 HOME\00 HOME.md"
$indexMd  = Join-Path $Content "index.md"
if (Test-Path -LiteralPath $homeNote) {
  $homeContent = [System.IO.File]::ReadAllText($homeNote)
  if ($homeContent -match "(?s)^---\s*\r?\n(.*?)\r?\n---") {
    if ($homeContent -notmatch "(?m)^title:\s*") {
      $homeContent = $homeContent -replace "(?s)^(---\s*\r?\n)", ('$1' + "title: HACK NOTES`n")
    }
  } else {
    $homeContent = "---`ntitle: HACK NOTES`n---`n`n" + $homeContent
  }
  Write-Text $indexMd $homeContent
}

# --- 3. Normalize every markdown file -------------------------------------
function Get-CellCount([string]$line) {
  $s = $line.Trim()
  if ($s.StartsWith("|")) { $s = $s.Substring(1) }
  if ($s.EndsWith("|"))   { $s = $s.Substring(0, $s.Length - 1) }
  return ($s -split "\|").Count
}

$delimRe = '^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$'
$fixedTables = 0; $fixedDataview = 0

Get-ChildItem -LiteralPath $Content -Recurse -File -Filter *.md | ForEach-Object {
  $p = $_.FullName
  $raw = [System.IO.File]::ReadAllText($p)
  if ($null -eq $raw) { return }
  $orig = $raw

  # 3a. Replace Dataview / DataviewJS fenced blocks (Quartz cannot execute them)
  $raw = [regex]::Replace($raw,
    '(?s)```+[ \t]*dataviewjs\b.*?```+',
    '> [!info] Vista dinamica (DataviewJS) - disponible solo en Obsidian.')
  $raw = [regex]::Replace($raw,
    '(?s)```+[ \t]*dataview\b.*?```+',
    '> [!info] Vista dinamica (Dataview) - disponible solo en Obsidian.')
  if ($raw -ne $orig) { $fixedDataview++ }

  # 3b. Fix GFM tables whose delimiter row column count != header row
  $lines = ($raw -replace "`r`n", "`n") -split "`n"
  $changed = $false
  for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match $delimRe -and $lines[$i].Contains("|") `
        -and $lines[$i-1].Trim() -ne "" -and $lines[$i-1].Contains("|")) {
      $hc = Get-CellCount $lines[$i-1]
      $dc = Get-CellCount $lines[$i]
      if ($hc -ge 1 -and $hc -ne $dc) {
        $lines[$i] = "|" + (" --- |" * $hc)
        $changed = $true
      }
    }
  }
  if ($changed) { $raw = ($lines -join "`n"); $fixedTables++ }

  if ($raw -ne $orig) { Write-Text $p $raw }
}
Log "Normalized: $fixedTables table(s), $fixedDataview dataview block(s)."

# --- 3b. Fix wikilinks so Quartz resolves them to exact slugs --------------
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py -and (Test-Path "C:\Users\rodri\AppData\Local\Programs\Python\Python313\python.exe")) {
  $py = "C:\Users\rodri\AppData\Local\Programs\Python\Python313\python.exe"
}
if ($py) {
  $linkScript = Join-Path $Repo "scripts\normalize_links.py"
  & $py -I $linkScript $Content --write 2>&1 | ForEach-Object { Log $_ }
} else {
  Log "WARNING: python not found - wikilink normalization skipped."
}

# --- 4. Commit and push ----------------------------------------------------
if ($NoPush) { Log "NoPush set - skipping git."; return }

Set-Location -LiteralPath $Repo
if (-not (Test-Path -LiteralPath (Join-Path $Repo ".git"))) {
  Log "No git repo - skipping commit/push."; return
}

git add -A | Out-Null
$pending = git status --porcelain
if ([string]::IsNullOrWhiteSpace($pending)) {
  Log "No changes to publish."
  return
}

$msg = "Sync notes " + (Get-Date -Format "yyyy-MM-dd HH:mm")
git commit -m $msg | Out-Null
Log "Committed: $msg"

$hasRemote = (git remote) -contains "origin"
if ($hasRemote) {
  git push origin HEAD                     # no 2>&1: native stderr would wrap as errors in PS 5.1
  if ($LASTEXITCODE -ne 0) { throw "git push failed" }
  Log "Pushed to origin."
} else {
  Log "No 'origin' remote - commit made locally only."
}
