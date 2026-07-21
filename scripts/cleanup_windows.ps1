Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Log = Join-Path $PSScriptRoot "cleanup.log"
function Log($m){ "$([DateTime]::Now.ToString('yyyy-MM-dd HH:mm:ss')) $m" | Tee-Object -FilePath $Log -Append }

$repo = (Resolve-Path "$PSScriptRoot\..").Path
$archiveRoot = "C:\_Archive"; $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$session = Join-Path $archiveRoot "USD_$stamp"; New-Item -ItemType Directory -Force -Path $session | Out-Null

$roots = @("C:\","D:\")
$patterns = @("usd","openusd","pixar","rpr","radeonprorenderusd")
$allItems = @()
foreach($r in $roots){
  if (Test-Path $r){
    $allItems += Get-ChildItem $r -Directory -Recurse -ErrorAction SilentlyContinue |
      Where-Object {
        $n=$_.Name.ToLower()
        ($patterns | ForEach-Object{ $n -like "*$_*" }) -contains $true -and
        ($_.FullName -notlike "$repo*") -and ($_.FullName -notlike "C:\Windows*")
      }
  }
}
$cands = $allItems | Sort-Object FullName -Unique

$chooser = Join-Path $PSScriptRoot "choose_usd.ps1"
$primary = & $chooser -Candidates ($cands.FullName)
if (-not $primary){ Log "No USD install candidates found."; throw "No USD choice"; }
Log "Primary selected: $primary"

# Check if primary is already C:\USD or a subdirectory of it
$primaryIsInCUSD = $primary -like "C:\USD*"

if ((Test-Path "C:\USD") -and -not $primaryIsInCUSD){
  Log "Archiving existing C:\USD"; Move-Item -Force C:\USD (Join-Path $session "OLD_C_USD")
}

if ($primaryIsInCUSD){
  Log "Primary is already in C:\USD - no move needed"
} elseif (([IO.Path]::GetPathRoot($primary)).ToUpper() -eq "C:\"){
  Log "Move $primary -> C:\USD"; Move-Item -Force $primary C:\USD
}else{
  Log "Copy $primary -> C:\USD"; robocopy $primary C:\USD /E /NFL /NDL /NJH /NJS /NP | Out-Null
}

foreach($c in $cands){
  if ($c.FullName -ieq "C:\USD" -or $c.FullName -ieq $primary){ continue }
  $dest = Join-Path $session (Split-Path $c.FullName -Leaf)
  Log "Archive $($c.FullName) -> $dest"
  try { Move-Item -Force $c.FullName $dest } catch {
    robocopy $c.FullName $dest /E /NFL /NDL /NJH /NJS /NP | Out-Null
    try { Remove-Item -Force -Recurse $c.FullName } catch { Log "Left original in place (locked): $($c.FullName)" }
  }
}
Log "Cleanup complete. Canonical USD at C:\USD. Archive: $session"

