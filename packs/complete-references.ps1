$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$utf8=[Text.UTF8Encoding]::new($false)
$headers=@{'User-Agent'='DSH-Prompt-Workbench-Source-Pack'}
$catalog=[IO.File]::ReadAllText((Join-Path $root 'catalog.json'))|ConvertFrom-Json
$provenance=[IO.File]::ReadAllText((Join-Path $root 'provenance.json'))|ConvertFrom-Json
$files=[Collections.Generic.List[object]]::new()
foreach($file in $provenance.files){$files.Add($file)}
foreach($source in $catalog.sources|Where-Object {$_.kind -eq 'skill' -or $_.id -eq 'visual-cookbook'}){
 $tree=Invoke-RestMethod -Uri ('https://api.github.com/repos/'+$source.repository+'/git/trees/'+$source.revision+'?recursive=1') -Headers $headers -TimeoutSec 60
 foreach($entry in $tree.tree|Where-Object type -eq 'blob'){
  $relative=$null
  if($source.id -eq 'image-prompt-reverse' -and $entry.path -match '^(README_en\.md|RELEASE_NOTES\.md|tests/.*\.md)$'){$relative='image-prompt-reverse/'+$entry.path}
  if($source.id -eq 'prompt-reverse-engineer' -and $entry.path -match '^tools/fixtures/semantic_[^/]+\.json$'){$relative='prompt-reverse-engineer/'+$entry.path}
  if($relative){
   $dest=Join-Path $root $relative
   if(Test-Path -LiteralPath $dest){throw ('Refusing overwrite: '+$dest)}
   [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest))|Out-Null
   $url='https://raw.githubusercontent.com/'+$source.repository+'/'+$source.revision+'/'+$entry.path
   Invoke-WebRequest -Uri $url -Headers $headers -TimeoutSec 60 -OutFile $dest
   $files.Add([pscustomobject]@{sourceId=$source.id;upstreamPath=$entry.path;localPath=$relative;url=$url;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $dest).Hash.ToLowerInvariant();bytes=(Get-Item -LiteralPath $dest).Length})
  }
 }
 foreach($file in $files|Where-Object sourceId -eq $source.id){
  $entry=$tree.tree|Where-Object path -eq $file.upstreamPath
  if(-not $entry){throw ('Missing upstream entry '+$file.upstreamPath)}
  $bytes=[IO.File]::ReadAllBytes((Join-Path $root $file.localPath))
  $header=[Text.Encoding]::UTF8.GetBytes(('blob '+$bytes.Length+[char]0))
  $inputBytes=[byte[]]::new($header.Length+$bytes.Length)
  [Array]::Copy($header,0,$inputBytes,0,$header.Length); [Array]::Copy($bytes,0,$inputBytes,$header.Length,$bytes.Length)
  $gitSha=[Convert]::ToHexString([Security.Cryptography.SHA1]::HashData($inputBytes)).ToLowerInvariant()
  if($gitSha -ne $entry.sha){throw ('Upstream Git blob mismatch: '+$file.localPath)}
  $file|Add-Member -NotePropertyName upstreamGitBlob -NotePropertyValue $gitSha
 }
 if($source.kind -eq 'skill'){$source.includedFiles=@($files|Where-Object sourceId -eq $source.id).Count}
}
[IO.File]::WriteAllText((Join-Path $root 'catalog.json'),(ConvertTo-Json -InputObject $catalog -Depth 100)+"`n",$utf8)
$provenance.files=@($files)
[IO.File]::WriteAllText((Join-Path $root 'provenance.json'),(ConvertTo-Json -InputObject $provenance -Depth 100)+"`n",$utf8)
Write-Output ('Preserved '+$files.Count+' upstream files; '+@($files|Where-Object upstreamGitBlob).Count+' verified against upstream Git blob IDs.')
