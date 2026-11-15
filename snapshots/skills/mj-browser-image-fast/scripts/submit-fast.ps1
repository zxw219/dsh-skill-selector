param(
    [Parameter(Mandatory = $true)][string]$Prompt,
    [Parameter(Mandatory = $true)][string]$ChannelUrl,
    [string]$BrowserInstance,
    [string]$AccountLabel,
    [string]$SessionId,
    [string]$BskPath = 'C:\Users\Administrator\.local\bin\bsk.exe',
    [switch]$NoSubmit
)

$ErrorActionPreference = 'Stop'
$t0 = Get-Date
$stage = 'init'
$sent = $false
$warn = ''
$elapsed = { ((Get-Date) - $t0).TotalSeconds }

function Step([string]$label) {
    Write-Verbose ("{0,7:N2}s  {1}" -f (& $elapsed), $label)
}

function Fail([string]$reason) {
    $line = 'FAILED stage={0} reason="{1}" elapsed={2:N2}s sent={3}' -f $stage, $reason, (& $elapsed), $sent.ToString().ToLower()
    Write-Output $line
    if ($warn) { Write-Output $warn }
    exit 1
}

function Bsk {
    $out = (& $BskPath @args 2>&1 | Out-String)
    if ([string]::IsNullOrWhiteSpace($out)) { return $null }
    try { return ($out | ConvertFrom-Json) } catch { return $null }
}

function Sync {
    $r = Bsk cooperate sync --session $session --json
    if ($null -eq $r) { Fail 'sync returned nothing' }
    if ($r.PSObject.Properties.Name -contains 'ok' -and -not $r.ok) { Fail ('sync failed: ' + $r.code) }
    return $r
}

function Norm([string]$s) {
    if ($null -eq $s) { return '' }
    $s = [regex]::Replace($s, '<[^>]+>', ' ')
    $s = [System.Net.WebUtility]::HtmlDecode($s)
    $s = [regex]::Replace($s, '[\u200b\u200c\u200d\ufeff]', '')
    return [regex]::Replace($s, '\s+', '')
}

# ---------- guards ----------
$stage = 'validate'
if ($Prompt.Trim().StartsWith('/')) { Fail 'prompt must not include the /imagine prefix' }
if ($ChannelUrl -notmatch '^https://discord\.com/channels/\d+/\d+') { Fail 'invalid ChannelUrl' }
if (-not (Test-Path -LiteralPath $BskPath)) { Fail "bsk not found at $BskPath" }

$full = '/imagine prompt: ' + $Prompt.Trim()
$expect = Norm('/imagine prompt' + $Prompt.Trim())

if ($Prompt -notmatch '--ar\s|--aspect\s') {
    $warn = 'WARN: no --ar in prompt, Midjourney will use its 1:1 default'
}

# ---------- browser + session ----------
$stage = 'browser'
$browsers = @(Bsk browsers --json)
if ($null -eq $browsers -or $browsers.Count -eq 0) { Fail 'no browser connected (open Chrome with the BrowserSkill extension)' }
if (-not $BrowserInstance) { $BrowserInstance = $browsers[0].instance_id }
if (-not $BrowserInstance) { Fail 'cannot determine browser instance id' }

$session = $null
if ($SessionId) {
    $stage = 'session'
    $list = @(Bsk session list --json)
    foreach ($s0 in $list) {
        if ($s0 -and $s0.session_id -eq $SessionId) { $session = $SessionId }
    }
    if (-not $session) { Step 'saved session unavailable, starting a new one' }
}
if (-not $session) {
    $stage = 'session'
    $st = Bsk session start --browser $BrowserInstance --no-focus --width 2560 --height 1392 --json
    if ($null -eq $st -or -not $st.session_id) { Fail 'session start failed' }
    $session = $st.session_id
    $nav = Bsk navigate $ChannelUrl --session $session --wait-until domcontentloaded --timeout 10s --json
    if ($null -eq $nav) { Fail 'navigate failed' }
    Start-Sleep -Milliseconds 500
}
Step "session $session ready"

# ---------- locate composer ----------
$stage = 'locate'
$s = Sync
$m = $null
for ($i = 0; $i -lt 20; $i++) {
    $cand = [regex]::Matches($s.observation.text, '(?m)^\s*(@e\d+) textbox "([^"]*)"')
    $hits = @($cand | Where-Object {
            $lbl = $_.Groups[2].Value
            $lbl -notmatch '搜索|Search|筛选|Filter' -and ($lbl -match '发消息|Message #|Message @|消息')
        })
    if ($hits.Count -eq 1) { $m = $hits[0]; break }
    Start-Sleep -Milliseconds 400
    $s = Sync
}
if ($null -eq $m) {
    $all = [regex]::Matches($s.observation.text, '(?m)^\s*(@e\d+) textbox "([^"]*)"') | ForEach-Object { $_.Groups[1].Value + '=' + $_.Groups[2].Value }
    Fail ('composer not found; textboxes seen: ' + ($all -join ' | '))
}
$editor = $m.Groups[1].Value
$tabId = $s.tab_id

if ($AccountLabel) {
    $stage = 'account'
    if ($s.observation.text -notmatch [regex]::Escape($AccountLabel)) { Fail "account label '$AccountLabel' not visible on this tab" }
}

$stage = 'composer'
$lineRe = [regex]::Escape($editor) + ' textbox[^\r\n]*'
$line = ([regex]::Match($s.observation.text, $lineRe)).Value
if ($line -notmatch '\[empty\]') { Fail 'composer is not empty - refusing to overwrite a draft' }

# ---------- paste the whole command ----------
$stage = 'paste'
Set-Clipboard -Value $full
$r = Bsk press 'Ctrl+V' --session $session --ref $editor --context $s.context_id --observation $s.observation_id --timeout 8s --json
if ($null -eq $r) { Fail 'paste produced no reply' }
$s = Sync
Step 'pasted'

$stage = 'verify'
$formOk = $false
for ($i = 0; $i -lt 12; $i++) {
    if ($s.observation.text -match 'applicationCommand|form "/imagine') { $formOk = $true; break }
    Start-Sleep -Milliseconds 300
    $s = Sync
}
if (-not $formOk) { Fail 'command form did not appear after paste' }

$h = Bsk get-html --ref $editor --session $session --max-bytes 24000 --json
$html = $null
if ($h) {
    if ($h.PSObject.Properties.Name -contains 'html') { $html = $h.html }
    elseif ($h.PSObject.Properties.Name -contains 'content') { $html = $h.content }
}
if ($null -eq $html) { Fail 'could not read composer content for verification' }
$got = Norm $html
$want = Norm $expect
if ($got -ne $want) { Fail 'composer content does not match the prompt' }
Step 'content verified'

if ($NoSubmit) {
    $stage = 'cleanup'
    $null = Bsk press 'Ctrl+A' --session $session --ref $editor --context $s.context_id --observation $s.observation_id --json
    $s = Sync
    $null = Bsk press 'Backspace' --session $session --ref $editor --context $s.context_id --observation $s.observation_id --json
    Write-Output ('READY session={0} tab={1} elapsed={2:N2}s (verified, not submitted, composer cleared)' -f $session, $tabId, (& $elapsed))
    if ($warn) { Write-Output $warn }
    exit 0
}

# ---------- submit ----------
$stage = 'submit'
$null = Bsk press 'Enter' --session $session --ref $editor --context $s.context_id --observation $s.observation_id --timeout 8s --json
$s = Sync
$sent = ($s.observation.text -match '正在发送命令|Sending command') -or (([regex]::Match($s.observation.text, $lineRe)).Value -match '\[empty\]')
if (-not $sent) { Fail 'Enter pressed but the composer did not clear' }
Step 'submitted'

Write-Output ('SUBMITTED {0} elapsed={1:N2}s session={2} tab={3}' -f (Get-Date -Format 'HH:mm:ss'), (& $elapsed), $session, $tabId)
if ($warn) { Write-Output $warn }
exit 0
