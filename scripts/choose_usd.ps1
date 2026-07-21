param([string[]]$Candidates)

$allRanked = @()
foreach ($c in $Candidates) {
  $uv = Get-ChildItem -Path $c -Recurse -Filter "usdview.exe" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
  $allRanked += [PSCustomObject]@{ Path=$c; Score = if ($uv){[int]($uv.LastWriteTime.ToFileTimeUtc())} else {0} }
}
$ranked = $allRanked | Sort-Object Score -Descending

if ($ranked.Count -eq 0) { return $null }

return $ranked[0].Path

