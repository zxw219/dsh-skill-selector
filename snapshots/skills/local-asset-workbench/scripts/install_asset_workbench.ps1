[CmdletBinding()]
param(
  [string]$InstallDir = (Join-Path $env:LOCALAPPDATA "LocalAssetWorkbench"),
  [string]$WorkspaceRoot = (Join-Path ([Environment]::GetFolderPath("MyDocuments")) "AssetWorkbenchData"),
  [string]$PrimaryProjectPath = "",
  [string]$DailyPracticePath = "",
  [string]$NodePath = "",
  [ValidateRange(1024, 65535)][int]$Port = 5177,
  [switch]$ResetConfig,
  [switch]$NoShortcut,
  [switch]$SkipStart
)

$ErrorActionPreference = "Stop"
$isWindowsPlatform = $env:OS -eq "Windows_NT"

function Resolve-NodeExecutable([string]$Requested) {
  $candidates = @()
  if ($Requested) { $candidates += $Requested }
  $command = Get-Command node -ErrorAction SilentlyContinue
  if ($command) { $candidates += $command.Source }
  $candidates += @(
    (Join-Path $env:ProgramFiles "nodejs\node.exe"),
    (Join-Path $env:LOCALAPPDATA "Programs\nodejs\node.exe")
  )
  foreach ($candidate in ($candidates | Select-Object -Unique)) {
    if ($candidate -and (Test-Path -LiteralPath $candidate -PathType Leaf)) {
      & $candidate --version | Out-Null
      if ($LASTEXITCODE -eq 0) { return (Resolve-Path -LiteralPath $candidate).Path }
    }
  }
  throw "未找到 Node.js。请安装 Node.js 18+，或通过 -NodePath 传入 node.exe 的完整路径。"
}

function New-Project([string]$Id, [string]$Name, [string]$Path) {
  [ordered]@{
    id = $Id
    name = $Name
    path = $Path
    scanRoots = @(".")
  }
}

$skillRoot = Split-Path -Parent $PSScriptRoot
$appSource = Join-Path $skillRoot "assets\app"
if (-not (Test-Path -LiteralPath (Join-Path $appSource "server.js"))) {
  throw "Skill 包不完整：缺少 assets\app\server.js"
}

$node = Resolve-NodeExecutable $NodePath
$InstallDir = [IO.Path]::GetFullPath($InstallDir)
$WorkspaceRoot = [IO.Path]::GetFullPath($WorkspaceRoot)
if (-not $PrimaryProjectPath) { $PrimaryProjectPath = Join-Path $WorkspaceRoot "项目" }
if (-not $DailyPracticePath) { $DailyPracticePath = Join-Path $WorkspaceRoot "每日练习" }
$referencePath = Join-Path $WorkspaceRoot "精选参考"
$pendingPath = Join-Path $WorkspaceRoot "待确认"
$miscPath = Join-Path $WorkspaceRoot "杂项"

$folders = @($InstallDir, $WorkspaceRoot, $PrimaryProjectPath, $DailyPracticePath, $referencePath, $pendingPath, $miscPath)
foreach ($folder in $folders) { New-Item -ItemType Directory -Path $folder -Force | Out-Null }

Copy-Item -Path (Join-Path $appSource "*") -Destination $InstallDir -Recurse -Force

$configPath = Join-Path $InstallDir "asset-browser.config.json"
if ($ResetConfig -or -not (Test-Path -LiteralPath $configPath)) {
  $downloads = Join-Path $env:USERPROFILE "Downloads"
  $config = [ordered]@{
    enabled = $true
    projects = @(
      (New-Project "main-projects" "项目" ([IO.Path]::GetFullPath($PrimaryProjectPath))),
      (New-Project "daily-practice" "每日练习" ([IO.Path]::GetFullPath($DailyPracticePath))),
      (New-Project "reference-library" "精选参考" ([IO.Path]::GetFullPath($referencePath))),
      (New-Project "pending-review" "待确认" ([IO.Path]::GetFullPath($pendingPath))),
      (New-Project "misc-library" "杂项" ([IO.Path]::GetFullPath($miscPath)))
    )
    automation = [ordered]@{
      inbox = [ordered]@{
        enabled = $false
        sourcePath = $downloads
        projectId = ""
        basePath = ""
        transferMode = "copy"
        settleSeconds = 8
        pollSeconds = 15
        routes = [ordered]@{
          image = "图片/{date}"
          video = "视频/{date}"
          audio = "音频/{date}"
          other = ""
        }
      }
      routing = [ordered]@{
        enabled = $false
        activeProfileId = ""
        useActiveForUnmatchedTypes = @("image", "video")
        fallbackProfileIds = [ordered]@{}
        profiles = @()
      }
      cleanup = [ordered]@{
        enabled = $false
        dryRun = $true
        intervalHours = 24
        retentionDays = 30
        quarantinePath = (Join-Path $downloads ".asset-workbench-quarantine")
        purgeEnabled = $false
        quarantineDays = 14
        onlyImported = $true
      }
    }
    deduplication = [ordered]@{
      enabled = $true
      exactContentOnly = $true
      sameDirectoryOnly = $true
      settleSeconds = 5
      recentSweepHours = 168
      retentionDays = 14
      quarantinePath = (Join-Path $InstallDir "duplicate-quarantine")
    }
  }
  $config | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $configPath -Encoding utf8
}

$launcherPath = Join-Path $InstallDir "启动资产工作台.vbs"
$nodeEscaped = $node.Replace('"', '""')
$serverEscaped = (Join-Path $InstallDir "server.js").Replace('"', '""')
$launcher = @"
Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = "$($InstallDir.Replace('"', '""'))"
shell.Environment("PROCESS")("PORT") = "$Port"
shell.Run Chr(34) & "$nodeEscaped" & Chr(34) & " " & Chr(34) & "$serverEscaped" & Chr(34), 0, False
WScript.Sleep 1000
shell.Run "http://localhost:$Port/", 1, False
"@
Set-Content -LiteralPath $launcherPath -Value $launcher -Encoding Unicode

$shortcutPath = ""
if (-not $NoShortcut -and $isWindowsPlatform) {
  $desktop = [Environment]::GetFolderPath("Desktop")
  $shortcutPath = Join-Path $desktop "资产工作台.lnk"
  $shell = New-Object -ComObject WScript.Shell
  $shortcut = $shell.CreateShortcut($shortcutPath)
  $shortcut.TargetPath = (Join-Path $env:WINDIR "System32\wscript.exe")
  $shortcut.Arguments = '"' + $launcherPath + '"'
  $shortcut.WorkingDirectory = $InstallDir
  $shortcut.Description = "打开本地资产工作台"
  $shortcut.Save()
}

if (-not $SkipStart) {
  if ($isWindowsPlatform) {
    $serverPath = Join-Path $InstallDir "server.js"
    $existing = Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" -ErrorAction SilentlyContinue |
      Where-Object { $_.CommandLine -and $_.CommandLine.IndexOf($serverPath, [StringComparison]::OrdinalIgnoreCase) -ge 0 }
    foreach ($process in $existing) {
      Stop-Process -Id $process.ProcessId -Force -ErrorAction SilentlyContinue
    }
    if ($existing) { Start-Sleep -Milliseconds 500 }
    $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($listener) {
      throw "端口 $Port 已被其他程序占用。请使用 -Port 指定其他端口。"
    }
    Start-Process -FilePath (Join-Path $env:WINDIR "System32\wscript.exe") -ArgumentList ('"' + $launcherPath + '"') -WindowStyle Hidden
  } else {
    Start-Process -FilePath $node -ArgumentList "server.js" -WorkingDirectory $InstallDir
  }
  $ready = $false
  for ($index = 0; $index -lt 24; $index += 1) {
    Start-Sleep -Milliseconds 250
    try {
      $response = Invoke-WebRequest -UseBasicParsing "http://localhost:$Port/api/projects" -TimeoutSec 2
      if ($response.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
  }
  if (-not $ready) { throw "资产工作台未能在端口 $Port 启动。" }
}

[ordered]@{
  ok = $true
  installDir = $InstallDir
  workspaceRoot = $WorkspaceRoot
  configPath = $configPath
  launcherPath = $launcherPath
  shortcutPath = $shortcutPath
  nodePath = $node
  port = $Port
  url = "http://localhost:$Port/"
} | ConvertTo-Json -Depth 5
