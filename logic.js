export function classify(skill) {
  const text=`${skill.name} ${skill.description}`;
  if(/^(mj-browser|gpt-image$|imagegen$)|生成渠道|提交生成/.test(text))return 'execution';
  if(/分镜|storyboard|cinema-dna/i.test(text))return 'storyboard';
  if(/视频.*提示词|video.*prompt|seedance|cinedance/i.test(text))return 'video';
  if(/图像.*提示词|图片.*提示词|生图.*提示词|image.*prompt|风格复刻/i.test(text))return 'image';
  if(/^(cinematography-|color-grading-|dialogue-|directing-|msv3-|shot-design-)|camera-lens|acting-performance/.test(skill.name))return 'knowledge';
  if(/小说|novel|故事|剧本|写作|台词|writing/i.test(text))return 'writing';
  if(/browser|浏览器|网页|搜索|检索/i.test(text))return 'browser';
  if(/office|docx|xlsx|pptx|pdf|文档|表格/i.test(text))return 'documents';
  if(/blender|三维|3D/i.test(text))return '3d';
  if(/代码|coding|开发|debug|git/i.test(text))return 'coding';
  return 'other';
}
export function localizeSkill(skill, localizations={}) {
  const card=localizations[skill.id];
  if(!card)return skill;
  return {...skill,originalTitle:skill.title,originalDescription:skill.description,originalWhenToUse:skill.whenToUse,title:card.title,description:card.description,whenToUse:card.whenToUse??card.description,keywords:card.keywords??[]};
}
export function skillSearchText(s) {
  return [s.id,s.title,s.description,s.whenToUse,s.originalTitle,s.originalDescription,s.originalWhenToUse,...Object.values(s.familyTitle??{}),...Object.values(s.familyDescription??{}),...(s.keywords??[]),...(s.platforms??[])].filter(Boolean).join(' ').toLowerCase();
}
export function rankSkills(skills,query='') {
  const words=query.toLowerCase().trim().split(/\s+/).filter(Boolean);
  return skills.map(s=>{const matches=words.filter(w=>skillSearchText(s).includes(w)).length;return {s,matches,score:matches*10+(s.favorite?4:0)+(s.status==='keep'?3:0)-(s.status==='retired'?1000:0)};})
    .filter(x=>!words.length||x.matches>0)
    .sort((a,b)=>b.score-a.score||a.s.title.localeCompare(b.s.title)).map(x=>x.s);
}
export function makeUsePrompt(skill,brief) {
  const load=skill.id.startsWith('pack:')
    ?`请完整读取技能入口 ${skill.path}，并按需读取其参考文档。`
    :skill.userInvocable?`/${skill.id}`:`请调用 skill 工具加载「${skill.id}」，再按其方法完成任务；不可用时明确说明。`;
  return `${load}\n\n我的需求：\n${brief}\n\n本次主要使用「${skill.title}」。按我明确要求的交付方式完成；需要素材时说明缺少什么，不编造参考内容。`;
}
export function makeCombinedPrompt(skills,primaryId,roles,brief) {
  const primary=skills.find(s=>s.id===primaryId);
  const helpers=skills.filter(s=>s.id!==primaryId);
  const load=s=>s.id.startsWith('pack:')?`请完整读取技能入口 ${s.path}，按需读取其参考文档。`:s.userInvocable?`/${s.id}`:`请调用 skill 工具加载「${s.id}」；无法加载时明确说明。`;
  const duty=s=>roles[s.id]||(s.id===primaryId?'负责整体方案、最终交付格式和整合结果。':'仅就本技能擅长的部分补充主任务，不另行接管完整流程。');
  return `组合使用技能 · 一份整合结果\n\n我的需求：\n${brief}\n\n主技能：${primary.title}（${primary.id}）\n职责：${duty(primary)}\n\n辅助技能（按以下顺序提供补充）：\n${helpers.map((s,i)=>`${i+1}. ${s.title}（${s.id}）\n   职责：${duty(s)}`).join('\n')}\n\n加载所选技能：\n${[primary,...helpers].map(load).join('\n\n')}\n\n执行方式：先明确任务和所需素材，再按上述辅助顺序吸收相关方法，最后由主技能整合为一份结果。辅助技能只承担列明的职责，不重复启动各自的整套流程。这是同一对话中的协作说明，不代表多个代理并行执行。\n\n用户本次任务和交付要求优先，主技能负责统一输出格式。方法冲突时说明取舍；存在影响目标的实质矛盾或缺少素材时先指出，不编造已加载或已执行的结果。只要求文本时不自动生图、提交网站或使用付费生成；需要外部操作时仍以用户已明确要求的范围为准，辅助技能的默认步骤不扩大范围。\n\n最终简要注明实际采用的技能及分工。组合整体评价不能直接视为某一个技能的独立质量。`;
}
export function recommendSkills(skills,brief) {
  const q=brief.toLowerCase();
  const concepts=[['视频','video','seedance','运镜'],['图片','图像','生图','image','头像','人像'],['分镜','storyboard'],['小说','novel','写作'],['剧本','script','台词'],['浏览器','browser','网页'],['搜索','search','检索'],['表格','excel','xlsx'],['文档','word','docx'],['幻灯','ppt','演示'],['pdf'],['blender','三维','3d'],['代码','coding','debug'],['反推','逆向','reverse'],['mj','midjourney'],['表演','acting','动作'],['摄影','镜头','camera'],['调色','grading']];
  const wanted=concepts.filter(group=>group.some(word=>q.includes(word)));
  const words=q.split(/[\s,，。；;：:！？!?]+/).filter(w=>w.length>1);
  return skills.filter(s=>s.available&&s.status!=='retired').map(s=>{
    const text=skillSearchText(s);
    const matches=wanted.filter(group=>group.some(word=>text.includes(word)));
    const exact=words.filter(w=>text.includes(w));
    return {s,score:matches.length*10+exact.length*3+(s.favorite?2:0)+(s.status==='keep'?1:0),matches,exact};
  }).filter(x=>x.matches.length||x.exact.length).sort((a,b)=>b.score-a.score||a.s.id.localeCompare(b.s.id)).map(x=>({...x.s,reason:'用途匹配：'+[...x.matches.map(g=>g.find(w=>q.includes(w))),...x.exact].filter((v,i,a)=>a.indexOf(v)===i).slice(0,4).join('、')}));
}
const stringValue=v=>typeof v==='string'?v:typeof v?.en==='string'?v.en:typeof v?.cn==='string'?v.cn:'';
export function composeResource(resource,request={}) {
  const values={};
  for(const [k,v] of Object.entries(resource.defaults??{}))values[k]=stringValue(v);
  for(const variable of Array.isArray(resource.variables)?resource.variables:[])values[variable.name]=stringValue(variable.defaultValue)||values[variable.name]||'';
  const raw=resource.raw??{};
  for(const [k,v] of Object.entries(raw.environment_variables??{}))if(!values[k])values[k]=stringValue(v?.default??v?.default_value??'');
  for(const [k,v] of Object.entries(request.variables??{})) {
    if(typeof v!=='string'||v.length>3000)throw Error('模板变量必须是 3000 字以内的文本');
    values[k]=v;
  }
  if(request.aspectRatio&&/midjourney|^mj$/i.test(request.model??'Midjourney'))values.ASPECT_RATIO=request.aspectRatio;
  let template=stringValue(resource.prompt)||stringValue(resource.template)||stringValue(resource.content)||stringValue(raw.prompt_template)||stringValue(resource.prompt_template);
  if(!template)throw Error('该资源没有可用的提示词模板');
  const missing=new Set(),occurrences={};
  const selections=resource.selections??{};
  let prompt=template.replace(/\{\{\s*([^{}]+?)\s*\}\}|\{([A-Za-z_][\w-]*)\}/g,(match,a,b)=>{
    const key=a??b,index=occurrences[key]??0;occurrences[key]=index+1;
    const indexed=key+'-'+index;
    const value=Object.hasOwn(request.variables??{},indexed)?values[indexed]:Object.hasOwn(request.variables??{},key)?values[key]:stringValue(selections[indexed])||values[key];
    if(value?.trim())return value;missing.add(key);return match;
  });
  const model=typeof request.model==='string'?request.model:'Midjourney';
  const notes=[];
  if(/midjourney|^mj$/i.test(model)) {
    if(request.aspectRatio){if(!/^\d{1,3}:\d{1,3}$/.test(request.aspectRatio)||request.aspectRatio.split(':').some(n=>+n===0))throw Error('画幅格式应为正整数比例，例如 16:9');prompt=prompt.replace(/\s*--ar\s+\d+:\d+/g,'')+' --ar '+request.aspectRatio;}
    notes.push('这是文本模板转换；上游样图可能来自其他模型。MJ 专有版本、sref 与角色参考需另行配置验证。');
  }
  if(missing.size)notes.push('仍有未填写变量，请补充后使用。');
  return {prompt,variables:values,missingVariables:[...missing],sourceUrl:resource.sourceUrl,mediaUrls:resource.mediaUrls??[],notes};
}
