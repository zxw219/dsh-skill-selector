param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ArgsFromCaller
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir
$Python = Join-Path $SkillDir ".venv\Scripts\python.exe"
$Entry = Join-Path $ScriptDir "semantic_recall.py"

if (-not (Test-Path -LiteralPath $Python)) {
    Write-Error "Missing local environment. Run scripts/setup.ps1 first."
    exit 1
}

& $Python -X utf8 $Entry @ArgsFromCaller
exit $LASTEXITCODE
