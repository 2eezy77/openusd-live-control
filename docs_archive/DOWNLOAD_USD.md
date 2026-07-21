# Download Prebuilt OpenUSD

## Required Action

Download a prebuilt OpenUSD installation for Windows with Python bindings and usdview.

## Download Location

Extract to: `C:\Downloads\openusd\openusd-windows-prebuilt`

## Required Structure

The extracted folder MUST contain:
```
C:\Downloads\openusd\openusd-windows-prebuilt\
├── bin\
│   └── usdview.exe          ← REQUIRED
├── lib\
│   └── python\
│       └── pxr\             ← REQUIRED (Python bindings)
├── plugin\
└── ... (other USD files)
```

## Download Options

### Option 1: NVIDIA Prebuilt Binaries (Recommended)

**URL**: https://developer.nvidia.com/usd

**Steps**:
1. Visit the NVIDIA USD download page
2. Look for "OpenUSD for Windows" prebuilt binaries
3. Download the appropriate version (Python 3.10 or 3.11 compatible)
4. Extract to `C:\Downloads\openusd\openusd-windows-prebuilt`

### Option 2: GitHub Releases

**URL**: https://github.com/PixarAnimationStudios/OpenUSD/releases

**Steps**:
1. Check for Windows prebuilt releases
2. Download the latest stable version
3. Extract to `C:\Downloads\openusd\openusd-windows-prebuilt`

### Option 3: Build from Source (Advanced)

**Requirements**:
- Visual Studio 2019 or 2022
- CMake 3.14+
- Python 3.10 or 3.11 with dev headers

**Steps**:
```powershell
# Clone OpenUSD
cd C:\Downloads\openusd
git clone https://github.com/PixarAnimationStudios/OpenUSD.git
cd OpenUSD

# Build (this will take 1-2 hours)
python build_scripts/build_usd.py `
  --python `
  --no-imaging `
  --no-examples `
  --build-variant release `
  C:\Downloads\openusd\openusd-windows-prebuilt
```

## Verification

After extraction, run this command to verify:

```powershell
Test-Path C:\Downloads\openusd\openusd-windows-prebuilt\bin\usdview.exe
# Should return: True
```

## What Happens Next

Once you've extracted the prebuilt USD:

1. The automation will archive the current incomplete `C:\USD`
2. Move your prebuilt USD to `C:\USD`
3. Create a fresh Python virtual environment
4. Verify pxr module imports work
5. Create `env.ready` flag
6. Proceed with viewer and JSON bridge setup

## Current Status

⏳ **Waiting**: Prebuilt USD download and extraction

📍 **Location**: `C:\Downloads\openusd\openusd-windows-prebuilt`

✅ **Ready**: Once `bin\usdview.exe` exists, re-run the setup automation

