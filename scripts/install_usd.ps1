Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Configuration
$DL = "C:\Downloads\openusd\openusd-windows-prebuilt"  # Update this if your download is elsewhere
$repo = "C:\openusd-live-control"
$opsLog = Join-Path $repo "logs\OPERATIONS_LOG.md"

function Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $msg"
    Add-Content $opsLog "`n$msg"
}

Write-Host "======================================"
Write-Host "OpenUSD Installation Script"
Write-Host "======================================"
Write-Host ""

# Step 1: Verify download
Write-Host "Step 1: Verifying prebuilt USD..."
if (-not (Test-Path $DL)) {
    Log "BLOCKER: Extracted OpenUSD not found at $DL"
    Log "Please download prebuilt OpenUSD and extract to: $DL"
    Log "See DOWNLOAD_USD.md for instructions"
    throw "No USD found at $DL"
}

$usdviewPath = Join-Path $DL "bin\usdview.exe"
if (-not (Test-Path $usdviewPath)) {
    Log "BLOCKER: usdview.exe not found at $usdviewPath"
    Log "The extracted USD must contain bin\usdview.exe"
    throw "Invalid USD structure at $DL"
}

Log "✓ Found valid USD at $DL with usdview.exe"

# Step 2: Archive current C:\USD
Write-Host "Step 2: Archiving current C:\USD..."
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveRoot = "C:\_Archive"
$arch = Join-Path $archiveRoot "USD_$stamp"
New-Item -ItemType Directory -Force -Path $arch | Out-Null

if (Test-Path "C:\USD") {
    $oldUSD = Join-Path $arch "OLD_C_USD"
    Log "Archiving C:\USD to $oldUSD"
    Move-Item -Force "C:\USD" $oldUSD
    Log "✓ Current USD archived"
} else {
    Log "No existing C:\USD to archive"
}

# Step 3: Move prebuilt to C:\USD
Write-Host "Step 3: Installing prebuilt USD to C:\USD..."
Log "Moving $DL to C:\USD"
Move-Item -Force $DL "C:\USD"
Log "✓ USD installed to C:\USD"

# Step 4: Sanity checks
Write-Host "Step 4: Verifying USD installation..."
$checks = @(
    "C:\USD\bin\usdview.exe",
    "C:\USD\lib",
    "C:\USD\lib\python"
)

foreach ($path in $checks) {
    if (Test-Path $path) {
        Log "✓ Found: $path"
    } else {
        Log "BLOCKER: Missing required path: $path"
        throw "Incomplete USD installation"
    }
}

# Step 5: Recreate venv
Write-Host "Step 5: Recreating Python virtual environment..."
cd $repo
if (Test-Path ".venv") {
    Remove-Item -Recurse -Force ".venv"
    Log "Removed old .venv"
}

Log "Creating new virtual environment with Python 3.10 or 3.11..."
$venvCreated = $false
try {
    py -3.10 -m venv .venv 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Log "✓ Created venv with Python 3.10"
        $venvCreated = $true
    }
} catch {
    Log "Python 3.10 not available, trying 3.11..."
}

if (-not $venvCreated) {
    py -3.11 -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Log "✓ Created venv with Python 3.11"
        $venvCreated = $true
    } else {
        Log "BLOCKER: Could not create venv with Python 3.10 or 3.11"
        throw "venv creation failed"
    }
}

# Step 6: Run env check
Write-Host "Step 6: Testing pxr module import..."
Log "Running scripts\env.bat for pxr verification"
& ".\scripts\env.bat"

Start-Sleep -Seconds 2  # Give it time to write logs\env.txt

# Step 7: Parse results
Write-Host "Step 7: Verifying results..."
$envTxt = Join-Path $repo "logs\env.txt"
if (Test-Path $envTxt) {
    $content = Get-Content $envTxt -Raw
    if ($content -match "pxr ok") {
        Log "✓✓✓ ENV READY: pxr ok with USD_ROOT=C:\USD"
        
        # Get Python version from venv
        & ".\.venv\Scripts\python.exe" --version 2>&1 | ForEach-Object {
            Log "Python version: $_"
        }
        
        # Create env.ready flag
        New-Item -ItemType File -Force -Path ".\env.ready" | Out-Null
        Log "✓ Created env.ready flag"
        
        # Handoff note
        Log ""
        Log "========================================" 
        Log "HANDOFF: Agent 2 may launch scripts\run_usdview.bat"
        Log "Expect: [usdview-bridge] Listening on 127.0.0.1:8765"
        Log "Log file: logs\viewer.log"
        Log "========================================"
        Log ""
        Log "SUCCESS: Environment setup complete!"
        Log "Archive location: $arch"
        
        Write-Host ""
        Write-Host "======================================"
        Write-Host "✓✓✓ SUCCESS ✓✓✓"
        Write-Host "======================================"
        Write-Host "OpenUSD is installed and verified!"
        Write-Host "env.ready flag created"
        Write-Host "Ready for viewer and API development"
        Write-Host "======================================"
        
    } else {
        Log "BLOCKER: pxr import failed after installing prebuilt USD"
        Log "Error: $content"
        Log "Check Python version compatibility (should be 3.10 or 3.11)"
        Log "The prebuilt USD might have been built for a different Python version"
        throw "pxr import failed - see logs\env.txt"
    }
} else {
    Log "BLOCKER: logs\env.txt was not created by env.bat"
    throw "env.bat did not produce output"
}

