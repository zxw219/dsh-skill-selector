$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Load($path){[IO.File]::ReadAllText((Join-Path $root $path))|ConvertFrom-Json}
function Assert($condition,$message){if(-not $condition){throw $message}}
$catalog=Load 'catalog.json'
Assert ($catalog.schemaVersion -eq 1) 'Unexpected schema version'
Assert ($catalog.sources.Count -eq 5) 'Expected exactly five sources'
$sourceIds=@($catalog.sources.id)
Assert (@($sourceIds|Select-Object -Unique).Count -eq 5) 'Duplicate source IDs'
foreach($source in $catalog.sources){
 Assert ($source.revision -match '^[a-f0-9]{40}$') 'Source revision not pinned'
 Assert (Test-Path -LiteralPath (Join-Path $root $source.licensePath)) 'License missing'
 if($source.skillPath){Assert (Test-Path -LiteralPath (Join-Path $root $source.skillPath)) 'Skill entry missing'}
 if($source.dataPath){Assert (Test-Path -LiteralPath (Join-Path $root $source.dataPath)) 'Dataset missing'}
}
$total=0
foreach($spec in @(@{path='prompts.json';count=20},@{path='styles.json';count=12},@{path='fill-templates.json';count=12})){
 $records=@(Load $spec.path)
 Assert ($records.Count -eq $spec.count) ('Wrong record count: '+$spec.path)
 Assert (@($records.id|Select-Object -Unique).Count -eq $records.Count) ('Duplicate ids: '+$spec.path)
 foreach($record in $records){
  Assert ($record.id -and $record.title -and $record.prompt) ('Empty identity/title/prompt: '+$record.id)
  Assert ($sourceIds -contains $record.sourceId) ('Unknown source: '+$record.id)
  $source=$catalog.sources|Where-Object id -eq $record.sourceId
  Assert ($record.provenance.revision -eq $source.revision) ('Revision mismatch: '+$record.id)
  Assert ($record.sourceUrl.Contains('/blob/'+$source.revision+'/')) ('Unpinned source URL: '+$record.id)
  foreach($url in $record.mediaUrls){Assert ($url -match '^https?://') ('Invalid media URL: '+$record.id)}
 }
 $total+=$records.Count
 Write-Output ($spec.path+': '+$records.Count+' valid records')
}
$provenance=Load 'provenance.json'
foreach($file in $provenance.files){
 $full=Join-Path $root $file.localPath
 Assert (Test-Path -LiteralPath $full) ('Missing source file: '+$file.localPath)
 Assert ((Get-FileHash -Algorithm SHA256 -LiteralPath $full).Hash.ToLowerInvariant() -eq $file.sha256) ('Hash mismatch: '+$file.localPath)
 Assert ((Get-Item -LiteralPath $full).Length -eq $file.bytes) ('Size mismatch: '+$file.localPath)
 if($file.upstreamGitBlob){
  $bytes=[IO.File]::ReadAllBytes($full)
  $header=[Text.Encoding]::UTF8.GetBytes(('blob '+$bytes.Length+[char]0))
  $inputBytes=[byte[]]::new($header.Length+$bytes.Length)
  [Array]::Copy($header,0,$inputBytes,0,$header.Length); [Array]::Copy($bytes,0,$inputBytes,$header.Length,$bytes.Length)
  $gitSha=[Convert]::ToHexString([Security.Cryptography.SHA1]::HashData($inputBytes)).ToLowerInvariant()
  Assert ($gitSha -eq $file.upstreamGitBlob) ('Git blob mismatch: '+$file.localPath)
 }
}
$prompts=@(Load 'prompts.json')
$originalPrompts=@(Load 'upstream/youmind/app-web-design.sample.json')
for($index=0;$index -lt $prompts.Count;$index++){
 Assert ($prompts[$index].prompt -ceq $originalPrompts[$index].content) 'YouMind prompt changed during normalization'
 Assert (($prompts[$index].mediaUrls -join "`n") -ceq ($originalPrompts[$index].sourceMedia -join "`n")) 'YouMind media changed'
}
foreach($style in @(Load 'styles.json')){
 $original=Load ('upstream/visual-cookbook/'+$style.provenance.path)
 Assert ($style.prompt -ceq $original.prompt_template) 'Style prompt changed during normalization'
}
$templates=@(Load 'fill-templates.json')
$originalTemplates=(Load 'upstream/promptfill/templates.sample.json').config
for($index=0;$index -lt $templates.Count;$index++){
 Assert ($templates[$index].prompt -ceq $originalTemplates[$index].content.en) 'English fill template changed'
 Assert ($templates[$index].promptZh -ceq $originalTemplates[$index].content.cn) 'Chinese fill template changed'
}
$allJson=@(Get-ChildItem -LiteralPath $root -Filter '*.json' -File -Recurse)
foreach($file in $allJson){$null=[IO.File]::ReadAllText($file.FullName)|ConvertFrom-Json}
Write-Output ('PASS: '+$catalog.sources.Count+' sources, '+$total+' normalized records, '+$provenance.files.Count+' source hashes, '+$allJson.Count+' JSON files parsed.')
