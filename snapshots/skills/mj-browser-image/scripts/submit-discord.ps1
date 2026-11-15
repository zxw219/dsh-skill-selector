#requires -Version 7.3
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [uri] $ChannelUrl,
    [Parameter(Mandatory)] [string] $BrowserInstance,
    [Parameter(Mandatory)] [string] $AccountLabel,
    [Parameter(Mandatory)] [string] $PromptFile,
    [string] $ReferencesFile,
    [string] $SessionId,
    [switch] $UploadLocalReferences
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$run = [ordered]@{
    stage = 'preflight'
    send_status = 'not_sent'
    session_id = $SessionId
    tab_id = $null
    channel = $ChannelUrl.AbsoluteUri
    clipboard_written = $false
    attachment_post = $null
    references = @()
    prompt = $null
}
$page = @{ Context = ''; Observation = ''; Text = '' }

function Invoke-Bsk {
    param([string[]] $Arguments)
    $raw = & $bsk @Arguments --json 2>&1
    $code = $LASTEXITCODE
    $reply = ($raw -join [Environment]::NewLine) | ConvertFrom-Json -ErrorAction Stop
    if ($code -ne 0 -or $null -eq $reply) {
        $errorDetail = [InvalidOperationException]::new("$($reply.code) $($reply.message)".Trim())
        $errorDetail.Data['effect_state'] = $reply.data.effect_state
        throw $errorDetail
    }
    $reply
}

function Sync-Page {
    $arguments = @('cooperate', 'sync', '--session', $run.session_id)
    if ($run.tab_id) { $arguments += @('--tab-id', "$($run.tab_id)") }
    $reply = Invoke-Bsk $arguments
    if ($reply.state.mode -ne 'ready' -or $reply.state.editing -or !$reply.context_id -or !$reply.tab_id) {
        throw 'BrowserSkill has not granted control of the task tab.'
    }
    if ($run.tab_id -and $reply.tab_id -ne $run.tab_id) { throw 'The task tab changed.' }
    if ($page.Context -and $reply.context_id -ne $page.Context) { throw 'The browser control context changed.' }
    $run.tab_id = $reply.tab_id
    $page.Context = $reply.context_id
    $page.Observation = $reply.observation_id
    if ($reply.observation.text) {
        $page.Text = $reply.observation.text
    } elseif ($reply.kind -ne 'unchanged' -or !$page.Text) {
        throw 'BrowserSkill did not return a usable page observation.'
    }
}

function Invoke-Tab {
    param([string[]] $Arguments)
    Invoke-Bsk ($Arguments + @('--session', $run.session_id, '--tab-id', "$($run.tab_id)", '--context', $page.Context))
}

function Get-Editor {
    $editors = [regex]::Matches($page.Text, '(?m)^\s*(@e\d+) textbox "(?:给 #.+? 发消息|Message #[^"]+?)(?: \[has-submenu\])?"')
    if ($editors.Count -ne 1) { throw 'The Discord channel message box could not be identified uniquely.' }
    $editors[0].Groups[1].Value
}

function Get-EditorState {
    param([string] $Editor)
    $reply = Invoke-Tab @('get-html', '--ref', $Editor, '--max-bytes', '24000')
    $html = $reply.html
    if (!$html -or $reply.truncated) { throw 'The input box could not be read in full.' }
    $rawText = [Net.WebUtility]::HtmlDecode(($html -creplace '<[^>]+>', ''))
    [pscustomobject]@{
        Text = ($rawText -creplace '[\u200b\ufeff]', '')
        RawText = $rawText
        Imagine = $html.Contains('applicationCommand__') -and $html.Contains('optionPillValue__') -and $rawText.StartsWith('/imagineprompt')
        Invalid = $html.Contains('erroredPill__') -or $html.Contains('aria-invalid="true"')
    }
}

function Read-Dom {
    param([string] $Expression)
    if (!$page.Observation) { throw 'A current observation is required to read Discord attachments.' }
    $reply = Invoke-Tab @('evaluate', $Expression, '--observation', $page.Observation)
    if (!$reply.ok) { throw 'BrowserSkill could not read the attachment state.' }
    $value = $reply.value ?? $reply.result
    if ($value -is [string]) { return ConvertFrom-Json -InputObject $value }
    if ($null -eq $value) { throw 'BrowserSkill returned no attachment state.' }
    $value
}

function Paste-Text {
    param([string] $Editor, [string] $Text)
    Set-Clipboard -Value $Text
    $run.clipboard_written = $true
    Invoke-Tab @('press', 'Ctrl+V', '--ref', $Editor, '--timeout', '5s') | Out-Null
}

function Press-CheckedEnter {
    param([string] $Editor, [string] $RawText)
    $guard = ConvertTo-Json -InputObject @(@{target = $Editor; field = 'text'; equals = $RawText}) -Compress
    Invoke-Tab @('press', 'Enter', '--ref', $Editor, '--expect', $guard, '--timeout', '5s') | Out-Null
}

try {
    if (!$IsWindows) { throw 'This version requires PowerShell 7.3 or later on Windows.' }
    if ($ChannelUrl.AbsoluteUri -cnotmatch '^https://discord\.com/channels/[0-9]+/[0-9]+$') {
        throw 'Provide a Discord server text-channel URL.'
    }
    $bsk = (Get-Command bsk -CommandType Application -ErrorAction Stop).Source
    $prompt = [IO.File]::ReadAllText((Get-Item -LiteralPath $PromptFile).FullName).TrimEnd([char[]]@(13,10))
    if ([string]::IsNullOrWhiteSpace($prompt) -or $prompt.TrimStart().StartsWith('/')) {
        throw 'The prompt file must contain the prompt text without the /imagine command.'
    }
    $references = @()
    if ($ReferencesFile) {
        $references = @(Get-Content -LiteralPath $ReferencesFile -Raw -Encoding utf8 | ConvertFrom-Json)
    }
    foreach ($reference in $references) {
        if ($reference.role -notin @('image', 'style') -or ([bool]$reference.url -eq [bool]$reference.path)) {
            throw 'Each reference needs role image or style and exactly one url or path.'
        }
        if ($reference.url) {
            $uri = $null
            if (![uri]::TryCreate([string]$reference.url, [UriKind]::Absolute, [ref]$uri) -or
                $uri.Scheme -notin @('http','https') -or $uri.UserInfo -or $reference.url -match '\s') {
                throw 'A reference URL must be an HTTP(S) image address without embedded credentials.'
            }
            $run.references += @{role = $reference.role; source = [string]$reference.url; url = [string]$reference.url; path = $null}
        } else {
            if (!$UploadLocalReferences) { throw 'Local reference upload to this channel has not been authorized.' }
            if (![IO.Path]::IsPathFullyQualified([string]$reference.path)) { throw 'Provide an absolute reference file path.' }
            $file = Get-Item -LiteralPath $reference.path
            if ($file -isnot [IO.FileInfo] -or !$file.Length -or $file.Extension -notin @('.png','.jpg','.jpeg','.webp','.gif')) {
                throw 'The local reference is not a supported image file.'
            }
            $run.references += @{role = $reference.role; source = $file.FullName; path = $file.FullName; url = $null}
        }
    }
    if (($run.references.role -contains 'style') -and $prompt -match '(?i)(?:^|\s)--sref(?:\s|$)') {
        throw 'The prompt already contains --sref. Supply the complete style reference argument or use the reference manifest.'
    }
    $files = @($run.references.path | Where-Object { $_ } | Select-Object -Unique)
    $names = @($files | ForEach-Object { [IO.Path]::GetFileName($_) })
    if (@($names | Group-Object | Where-Object Count -gt 1).Count) {
        throw 'Local references with identical filenames cannot be matched safely in the same upload.'
    }

    $run.stage = 'window'
    Add-Type -AssemblyName System.Windows.Forms
    $area = [Windows.Forms.Screen]::PrimaryScreen.WorkingArea
    $size = @('--width', "$($area.Width)", '--height', "$($area.Height)")
    if ($SessionId) {
        $session = @(Invoke-Bsk @('session','list') | Where-Object session_id -ceq $SessionId)
        if ($session.Count -ne 1 -or $session[0].browser_instance_id -cne $BrowserInstance) {
            throw 'The saved session is unavailable or belongs to a different browser instance.'
        }
        Sync-Page
        Invoke-Bsk (@('window','resize','--session',$SessionId,'--context',$page.Context,'--observation',$page.Observation) + $size) | Out-Null
    } else {
        $start = Invoke-Bsk (@('session','start','--browser',$BrowserInstance,'--no-focus') + $size)
        if (!$start.session_id -or $start.browser_instance_id -cne $BrowserInstance) {
            throw 'BrowserSkill did not start a session on the selected browser instance.'
        }
        $run.session_id = $start.session_id
        $nav = Invoke-Bsk @('navigate',$run.channel,'--session',$run.session_id,'--wait-until','domcontentloaded','--timeout','10s')
        if ($nav.final_url -cne $run.channel -or !$nav.tab_id) { throw 'Discord redirected or did not open the requested channel.' }
        $run.tab_id = $nav.tab_id
    }

    $run.stage = 'channel'
    Sync-Page
    if ($page.Text -notmatch '(?m)^\s*@e\d+ textbox "(?:给 #.+? 发消息|Message #)') {
        $ready = Invoke-Tab @('wait-for-element','--selector','form [data-slate-editor=true][role=textbox]','--timeout','6s')
        if (!$ready.satisfied) { throw 'The Discord message box is not ready.' }
        Sync-Page
    }
    $tabs = Invoke-Bsk @('tab','list','--scope','agent','--session',$run.session_id)
    $tab = @(($tabs.tabs ?? $tabs) | Where-Object { ($_.tab_id ?? $_.id) -eq $run.tab_id })
    if ($tab.Count -ne 1 -or $tab[0].url -cne $run.channel -or $tab[0].borrowed -eq $true -or $tab[0].ownership -eq 'borrowed') {
        throw 'The active task tab is not the requested Discord channel.'
    }
    $accountRegion = [regex]::Match($page.Text, '(?m)^(?<indent>[ \t]*)region "(?:用户状态和设置|User status and settings)"[^\r\n]*\r?\n(?<body>(?:\k<indent>[ \t]+[^\r\n]*\r?\n)*)')
    $accountPattern = '(?m)^\s*@e\d+ button "' + [regex]::Escape($AccountLabel) + '"'
    if (!$accountRegion.Success -or $accountRegion.Groups['body'].Value -cnotmatch $accountPattern) {
        throw 'The Discord account label differs from the one specified by the host.'
    }
    $editor = Get-Editor
    $draft = Get-EditorState $editor
    if ($draft.Invalid -or ($draft.Text -ne '' -and (!$draft.Imagine -or $draft.Text -cne '/imagineprompt'))) {
        throw 'The channel already contains a draft or the command slot is invalid.'
    }

    if ($files.Count) {
        $run.stage = 'upload_references'
        if ($draft.Text) { throw 'Upload requires an empty message box before opening /imagine.' }
        $readAttachments = '(() => { const form = document.querySelector("form [data-slate-editor=true]")?.closest("form"); if (!form) return null; const list = form.querySelector("[class*=channelAttachmentArea]"); return { count: list?.querySelectorAll("li").length ?? 0, text: list?.innerText ?? "", titles: [...(list?.querySelectorAll("[title]") ?? [])].map(e => e.title) }; })()'
        if ((Read-Dom $readAttachments).count -ne 0) { throw 'The composer already contains attachments.' }
        $marker = 'MJ 参考图 ' + [guid]::NewGuid().ToString('N').Substring(0, 12)
        $run.attachment_post = @{marker = $marker; status = 'not_sent'; files = $files}
        $upload = @('upload','--ref',$editor,'--mode','drop','--timeout','20s')
        foreach ($file in $files) { $upload += @('--file',$file) }
        Invoke-Tab $upload | Out-Null
        Sync-Page
        $editor = Get-Editor
        $preview = Read-Dom $readAttachments
        if ($preview.count -ne $names.Count) { throw 'The attachment preview count differs from the requested files.' }
        foreach ($name in $names) {
            if ($name -cnotin $preview.titles -and !($preview.text -split '\r?\n' -ccontains $name)) {
                throw "The attachment preview could not be verified for $name."
            }
        }
        if ((Get-EditorState $editor).Text -cne '') { throw 'An unrelated draft appeared in the upload composer.' }
        Paste-Text $editor $marker
        $draft = Get-EditorState $editor
        if ($draft.Text -cne $marker -or $draft.Imagine -or $draft.Invalid) { throw 'The attachment message marker could not be verified.' }
        $run.stage = 'post_attachments'
        $run.attachment_post.status = 'send_unknown'
        Press-CheckedEnter $editor $draft.RawText
        $run.attachment_post.status = 'enter_pressed'
        $run.stage = 'read_attachment_links'
        $markerJson = ConvertTo-Json -InputObject $marker -Compress
        $expression = '(() => { const marker = ' + $markerJson + '; const messages = [...document.querySelectorAll("[id^=message-content-]")].filter(e => e.innerText.trim() === marker); if (messages.length !== 1) return { links: [] }; const row = messages[0].closest("li, [role=listitem]"); return { links: [...new Set([...(row?.querySelectorAll("a[href]") ?? [])].map(a => a.href).filter(h => /^https:\/\/cdn\.discordapp\.com\/attachments\//.test(h)))] }; })()'
        $deadline = [DateTimeOffset]::UtcNow.AddSeconds(8)
        do {
            Sync-Page
            $post = Read-Dom $expression
            foreach ($link in $post.links) {
                $uri = [uri]$link
                if ($uri.Segments.Count -ne 5 -or $uri.Segments[2].TrimEnd('/') -ne $ChannelUrl.Segments[3].TrimEnd('/')) { continue }
                $name = [uri]::UnescapeDataString($uri.Segments[-1])
                foreach ($ref in $run.references | Where-Object { $_.path -and [IO.Path]::GetFileName($_.path) -ceq $name }) {
                    if ($ref.url -and $ref.url -cne $link) { throw "More than one attachment link matches $name." }
                    $ref.url = $link
                }
            }
            $missing = @($run.references | Where-Object { !$_.url })
            if ($missing.Count -and [DateTimeOffset]::UtcNow -lt $deadline) { Start-Sleep -Milliseconds 350 }
        } while ($missing.Count -and [DateTimeOffset]::UtcNow -lt $deadline)
        if ($missing.Count) { throw ('Attachment links could not be verified for: ' + ($missing.source -join ', ')) }
        $run.attachment_post.status = 'links_verified'
        $editor = Get-Editor
        $draft = Get-EditorState $editor
        if ($draft.Text -cne '') { throw 'The attachment composer did not clear after posting.' }
    }

    $imageUrls = @($run.references | Where-Object role -eq 'image' | ForEach-Object url)
    $styleUrls = @($run.references | Where-Object role -eq 'style' | ForEach-Object url)
    if ($imageUrls.Count) { $prompt = ($imageUrls -join ' ') + ' ' + $prompt }
    if ($styleUrls.Count) { $prompt += ' --sref ' + ($styleUrls -join ' ') }
    $run.prompt = $prompt

    $run.stage = 'select_imagine'
    if (!$draft.Imagine) {
        Invoke-Tab @('click', $editor, '--timeout','5s') | Out-Null
        Paste-Text $editor '/imagine'
        Sync-Page
        $candidate = [regex]::Matches($page.Text, '(?m)^\s*(@e\d+) option "/imagine prompt Create images with Midjourney Midjourney Bot"[^\r\n]*')
        if (!$candidate.Count) {
            $candidate = [regex]::Matches($page.Text, '(?m)^\s*(@e\d+) button "/imagine prompt Create images with Midjourney Midjourney Bot"[^\r\n]*')
        }
        if ($candidate.Count -ne 1) { throw 'The Midjourney Bot /imagine candidate was not identified uniquely.' }
        if ($candidate[0].Value -match '\[selected\]') {
            $guard = ConvertTo-Json -InputObject @(
                @{target = $candidate[0].Groups[1].Value; field = 'attribute'; attribute = 'aria-selected'; equals = 'true'}
            ) -Compress
            Invoke-Tab @('press','Enter','--ref',$editor,'--expect',$guard,'--timeout','5s') | Out-Null
        } else {
            Invoke-Tab @('click',$candidate[0].Groups[1].Value,'--timeout','5s') | Out-Null
        }
        Sync-Page
        $editor = Get-Editor
    }
    $draft = Get-EditorState $editor
    if (!$draft.Imagine -or $draft.Invalid -or $draft.Text -cne '/imagineprompt') {
        throw 'Discord did not open an empty Midjourney /imagine prompt slot.'
    }
    $slot = [regex]::Matches($page.Text, '(?m)^\s*(@e\d+) button "prompt [^"]*"\s+\[ctx: /imagine prompt')
    if ($slot.Count -ne 1) { throw 'The prompt slot control was not identified uniquely.' }
    $run.stage = 'paste_prompt'
    Invoke-Tab @('click', $slot[0].Groups[1].Value, '--timeout','5s') | Out-Null
    Paste-Text $editor $prompt
    $draft = Get-EditorState $editor
    if (!$draft.Imagine -or $draft.Invalid -or $draft.Text -cne ('/imagineprompt' + $prompt)) {
        throw 'The prompt slot text did not match the prepared prompt.'
    }

    $run.stage = 'send_imagine'
    $run.send_status = 'send_unknown'
    Press-CheckedEnter $editor $draft.RawText
    $run.send_status = 'enter_pressed'
    $run.stage = 'done'
    $run.sent_at = [DateTimeOffset]::UtcNow.ToString('o')
    [pscustomobject]$run | ConvertTo-Json -Depth 8
} catch {
    if ($run.send_status -eq 'send_unknown' -and $_.Exception.Data['effect_state'] -eq 'none') {
        $run.send_status = 'not_sent'
    }
    if ($run.stage -eq 'post_attachments' -and $_.Exception.Data['effect_state'] -eq 'none') {
        $run.attachment_post.status = 'not_sent'
    }
    $run.error = $_.Exception.Message
    [pscustomobject]$run | ConvertTo-Json -Depth 8
    exit 1
}
