param(
    [string]$PythonPath = "$PSScriptRoot\.venv\Scripts\python.exe",
    [string]$SpecFile = "deleteAspect.spec",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
Push-Location -Path $PSScriptRoot
try {
    if (-not (Test-Path $PythonPath)) {
        throw "Python not found: $PythonPath"
    }

    $pyinstaller = Join-Path -Path (Split-Path $PythonPath) -ChildPath "pyinstaller.exe"
    if (-not (Test-Path $pyinstaller)) {
        Write-Host "PyInstaller not found. Installing via pip..."
        & $PythonPath -m pip install --upgrade pyinstaller
    }
    if (-not (Test-Path $pyinstaller)) {
        throw "PyInstaller executable not found after install: $pyinstaller"
    }

    $args = @("--noconfirm", "--distpath", "dist")
    if ($Clean) {
        $args = @("--clean") + $args
    }
    $args += $SpecFile

    & $pyinstaller @args
}
finally {
    Pop-Location
}
