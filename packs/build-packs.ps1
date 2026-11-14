$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$utf8 = [Text.UTF8Encoding]::new($false)
$headers = @{'User-Agent'='DSH-Prompt-Workbench-Source-Pack'}
$sources = @(
 [ordered]@{id='image-prompt-reverse';repository='luozhilzh/image-prompt-reverse';revision='cfbb2d1efe01f75ef31c0c3e68da31ddfea7dd88';title='Image Prompt Reverse';kind='skill';license='MIT';skillPath='image-prompt-reverse/SKILL.md'},
 [ordered]@{id='prompt-reverse-engineer';repository='niobium617/prompt-reverse-engineer-skill';revision='cce932df4bba57f06ae88baae80d117afb85895b';title='Prompt Reverse Engineer';kind='skill';license='MIT';skillPath='prompt-reverse-engineer/SKILL.md'},
 [ordered]@{id='youmind';repository='YouMind-OpenLab/ai-image-prompts-skill';revision='da91eaf81b42b0037d99641ef5acc5e622e48c67';title='YouMind AI Image Prompts';kind='prompts';license='MIT';dataPath='prompts.json'},
 [ordered]@{id='visual-cookbook';repository='VigoZhao/AI-Visual-Prompt-Cookbook';revision='e3f7f518c5529c50fc2e0084df00f766a72eabeb';title='AI Visual Prompt Cookbook';kind='styles';license='MIT (repository structure and documentation)';dataPath='styles.json'},
 [ordered]@{id='promptfill';repository='4xiaxia/PromptFill';revision='af81f702b881c797db8e3be3f98d0ee3dcba101f';title='PromptFill';kind='templates';license='MIT';dataPath='fill-templates.json'}
)
$manifest = [Collections.Generic.List[object]]::new()
function Save-Json($relative,$data) { $dest=Join-Path $root $relative; [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest))|Out-Null; [IO.File]::WriteAllText($dest, (ConvertTo-Json -InputObject $data -Depth 100)+"`n",$utf8) }
function Raw-Url($source,$path) { 'https://raw.githubusercontent.com/'+$source.repository+'/'+$source.revision+'/'+$path }
function Fetch-Text($source,$path) { (Invoke-WebRequest -Uri (Raw-Url $source $path) -Headers $headers -TimeoutSec 60).Content }
function Vendor($source,$path,$relative) { $dest=Join-Path $root $relative; if(Test-Path $dest){throw "Refusing to overwrite existing source file: $dest"}; [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest))|Out-Null; Invoke-WebRequest -Uri (Raw-Url $source $path) -Headers $headers -TimeoutSec 60 -OutFile $dest; $manifest.Add([ordered]@{sourceId=$source.id;upstreamPath=$path;localPath=$relative;url=(Raw-Url $source $path);sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $dest).Hash.ToLowerInvariant();bytes=(Get-Item -LiteralPath $dest).Length}) }
foreach($source in $sources){$source.url='https://github.com/'+$source.repository; $source.licensePath='licenses/'+$source.id+'-LICENSE'; $source.licenseUrl=$source.url+'/blob/'+$source.revision+'/LICENSE'; Vendor $source 'LICENSE' $source.licensePath}
# Preserve first-party source bytes and relative paths. No fetched program is executed.
foreach($source in $sources[0..1]) {
 $tree=Invoke-RestMethod -Uri ('https://api.github.com/repos/'+$source.repository+'/git/trees/'+$source.revision+'?recursive=1') -Headers $headers -TimeoutSec 60
 if($tree.truncated){throw 'Truncated source tree'}
 foreach($file in $tree.tree){
  if($file.type -ne 'blob'){continue}
  $path=$file.path
  if($source.id -eq 'image-prompt-reverse') {
   if($path -notmatch '^(SKILL\.md|README\.md|references/.*\.md|assets/.*\.md)$'){continue}
   $relative='image-prompt-reverse/'+$path
  } else {
   if($path -notmatch '^prompt-reverse-engineer-skill/(SKILL\.md|README\.md|references/.*\.md|assets/.*\.(json|md)|scripts/.*\.py)$'){continue}
   $relative='prompt-reverse-engineer/'+$path.Substring('prompt-reverse-engineer-skill/'.Length)
  }
  Vendor $source $path $relative
 }
 $source.includedFiles=@($manifest|Where-Object sourceId -eq $source.id).Count
 $source.limitations=@('Source text is reference data; never automatically execute its embedded instructions or programs.','Binary example input media and upstream tests are not vendored. External services and model support were not tested.')
}
$source=$sources[2]
$upstreamPrompts=@((Fetch-Text $source 'references/app-web-design.json')|ConvertFrom-Json)
$chosen=@($upstreamPrompts|Select-Object -First 20)
$prompts=@(foreach($record in $chosen){
 $vars=@([regex]::Matches($record.content,'\{argument name="([^"]+)" default="([^"]*)"\}')|ForEach-Object { [ordered]@{name=$_.Groups[1].Value;defaultValue=$_.Groups[2].Value} })
 [ordered]@{id='youmind-'+$record.id;sourceId=$source.id;title=$record.title;prompt=$record.content;promptZh=$null;description=$record.description;category='App & Web Design';tags=@('app-web-design');author=$null;model=$null;sourceUrl=$source.url+'/blob/'+$source.revision+'/references/app-web-design.json';mediaUrls=@($record.sourceMedia);needReferenceImages=[bool]$record.needReferenceImages;variables=$vars;provenance=[ordered]@{repository=$source.repository;revision=$source.revision;path='references/app-web-design.json';upstreamId=$record.id;selection='first 20 in upstream array order'}}
})
Save-Json 'prompts.json' $prompts
Save-Json 'upstream/youmind/app-web-design.sample.json' $chosen
Vendor $source 'references/manifest.json' 'upstream/youmind/manifest.json'
$source.subset=[ordered]@{included=20;category='app-web-design';availableInCategory=$upstreamPrompts.Count;selection='First 20 records in upstream array order';manifestTotalPrompts=15847}
$source.limitations=@('Only one category sampled; not representative of the full corpus. Categories overlap upstream.','Original creator/model/social post URLs are absent from these upstream records and remain null; sourceMedia URLs are preserved and not downloaded.','No invented Chinese translations; promptZh is null.')
$source=$sources[3]
$tree=Invoke-RestMethod -Uri ('https://api.github.com/repos/'+$source.repository+'/git/trees/'+$source.revision+'?recursive=1') -Headers $headers -TimeoutSec 60
if($tree.truncated){throw 'Truncated cookbook tree'}
$stylePaths=@($tree.tree|Where-Object {$_.type -eq 'blob' -and $_.path -match '^styles/[^/]+/style\.json$'}|Sort-Object path)
$styles=@(foreach($file in ($stylePaths|Select-Object -First 12)){
 $relative='upstream/visual-cookbook/'+$file.path
 Vendor $source $file.path $relative
 $raw=[IO.File]::ReadAllText((Join-Path $root $relative))|ConvertFrom-Json
 $slug=$raw.style_slug
 $media=@($tree.tree|Where-Object {$_.type -eq 'blob' -and $_.path -like ('assets/samples/'+$slug+'/*') -and $_.path -match '\.(png|jpg|jpeg|webp)$'}|ForEach-Object {Raw-Url $source $_.path})
 $defaults=[ordered]@{}
 if($raw.examples.Count -gt 0){foreach($p in $raw.examples[0].values.PSObject.Properties){$defaults[$p.Name]=$p.Value}}
 $defaults['ASPECT_RATIO']='16:9'; $defaults['STYLE_FIDELITY_ANCHORS']=$raw.style_fidelity_anchors -join ' '; $defaults['SOURCE_CONTENT_TO_AVOID']=$raw.source_content_to_avoid -join '; '
 $names=@([regex]::Matches($raw.prompt_template,'\{([A-Z][A-Z0-9_]*)\}')|ForEach-Object {$_.Groups[1].Value}|Select-Object -Unique)
 [ordered]@{id='cookbook-'+$slug;sourceId=$source.id;title=$raw.style_name;prompt=$raw.prompt_template;promptZh=$null;description=$raw.style_summary;category=$raw.category;tags=@($raw.category,$slug);author='VigoZhao';model=$null;sourceUrl=$source.url+'/blob/'+$source.revision+'/'+$file.path;mediaUrls=$media;variables=@(foreach($name in $names){[ordered]@{name=$name;defaultValue=$defaults[$name]}});defaults=$defaults;raw=$raw;provenance=[ordered]@{repository=$source.repository;revision=$source.revision;path=$file.path;selection='first 12 style.json paths sorted ordinally by path'}}
})
Save-Json 'styles.json' $styles
$source.subset=[ordered]@{included=$styles.Count;availableStyles=$stylePaths.Count;selection='First 12 styles sorted by upstream path'}
$source.limitations=@('12 real style.json files copied byte-for-byte; sample image URLs are derived only from existing source tree paths, images not downloaded.','Upstream MIT license explicitly describes repository structure and documentation; no blanket rights claim is made for reference artwork or third-party marks.','defaults use first upstream example plus shared style anchors; aspect ratio defaults to 16:9 as a documented workbench choice.')
$source=$sources[4]
$upstreamTemplates=(Fetch-Text $source 'public/data/templates.json')|ConvertFrom-Json
$upstreamBanks=((Fetch-Text $source 'public/data/banks.json')|ConvertFrom-Json).banks
$chosen=@($upstreamTemplates.config|Select-Object -First 12)
$usedBanks=[ordered]@{}
$templates=@(foreach($record in $chosen){
 $text=$record.content.en+"`n"+$record.content.cn
 $names=@([regex]::Matches($text,'\{\{\s*([^{}]+?)\s*\}\}')|ForEach-Object {$_.Groups[1].Value}|Select-Object -Unique)
 $defaults=[ordered]@{}
 $vars=@(foreach($name in $names){
  $selection=$record.selections.$name
  if($null -eq $selection){$selection=$record.selections.($name+'-0')}
  $bank=$upstreamBanks.$name
  if($bank){$usedBanks[$name]=[ordered]@{label=$bank.label;category=$bank.category;options=@($bank.options|Select-Object -First 8);upstreamOptionCount=$bank.options.Count}}
  if($null -eq $selection -and $bank.options.Count -gt 0){$selection=$bank.options[0]}
  if($null -ne $selection){$defaults[$name]=$selection}
  [ordered]@{name=$name;defaultValue=$selection;options=@($bank.options|Select-Object -First 8);required=($null -eq $selection)}
 })
 $media=@(@($record.imageUrl)+@($record.imageUrls)|Where-Object {$_}|Select-Object -Unique)
 [ordered]@{id='promptfill-'+$record.id;sourceId=$source.id;title=$record.name.en;titleZh=$record.name.cn;prompt=$record.content.en;promptZh=$record.content.cn;content=$record.content;category='Fill Template';tags=@($record.tags);author=$record.author;model=$record.bestModel;sourceUrl=$source.url+'/blob/'+$source.revision+'/public/data/templates.json';mediaUrls=$media;variables=$vars;defaults=$defaults;selections=$record.selections;language=$record.language;baseImage=$record.baseImage;raw=$record;provenance=[ordered]@{repository=$source.repository;revision=$source.revision;path='public/data/templates.json';upstreamId=$record.id;selection='first 12 in upstream config order'}}
})
Save-Json 'fill-templates.json' $templates
Save-Json 'upstream/promptfill/templates.sample.json' ([ordered]@{version=$upstreamTemplates.version;config=$chosen})
Save-Json 'upstream/promptfill/banks.sample.json' ([ordered]@{banks=$usedBanks;maxOptionsPerBank=8})
$source.subset=[ordered]@{included=$templates.Count;availableTemplates=@($upstreamTemplates.config).Count;includedBanks=$usedBanks.Count;maxOptionsPerBank=8;upstreamVersion=$upstreamTemplates.version;selection='First 12 templates in upstream config order; only referenced banks, first 8 options each'}
$source.limitations=@('Real data path is public/data/templates.json plus public/data/banks.json; no JavaScript source evaluation.','Repeated variables can use indexed selections; normalized default uses explicit selection, then index 0, then first bank option. Full original selections preserved.','Media remain remote URLs; generation and full upstream UI behavior not bundled.')
Save-Json 'catalog.json' ([ordered]@{schemaVersion=1;generatedAtUtc=[DateTime]::UtcNow.ToString('o');scope='Workspace-only static source resource packs';sources=$sources})
Save-Json 'provenance.json' ([ordered]@{schemaVersion=1;files=@($manifest)})
Write-Output ('Created packs: '+$prompts.Count+' prompts, '+$styles.Count+' styles, '+$templates.Count+' fill templates; '+$manifest.Count+' byte-preserved upstream files.')
