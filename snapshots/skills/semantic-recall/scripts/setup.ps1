param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir
$VenvDir = Join-Path $SkillDir ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$Requirements = Join-Path $ScriptDir "requirements.txt"

if (-not (Test-Path -LiteralPath $VenvPython)) {
    & $Python -m venv $VenvDir
}

& $VenvPython -m ensurepip --upgrade
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r $Requirements

Write-Output "Semantic Recall environment is ready: $VenvPython"
