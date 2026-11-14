import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';
import { z } from 'zod';
import { classify, composeResource, localizeSkill, makeCombinedPrompt, makeUsePrompt, recommendSkills, rankSkills } from './logic.js';
import { OriginalLibrary, originals, youmindFolder, projectWorkbenchOpen } from './originals.js';
import { openOriginalInChrome } from './chrome.js';
import { ManualSkillMode, selectionMarker } from './manual-mode.js';
import { assignSkillFamilies } from './families.js';

export const inject = ['skills', 'commands', 'tools', 'storageDomain', 'workingDirectory', 'agents', 'agentPresets', 'sessionProjections'];
const base = new URL('./', import.meta.url);
const json = async path => JSON.parse(await readFile(new URL(path, base), 'utf8'));
const bounded = (value, max = 6000) => typeof value === 'string' ? value.slice(0, max) : '';
const statuses = new Set(['testing', 'keep', 'watch', 'retired']);
const reviewSchema = z.object({id:z.string(),skillId:z.string(),trialId:z.string().optional(),rating:z.number().int().min(1).max(5),note:z.string(),time:z.string()});
const trialSchema = z.object({id:z.string(),skillId:z.string(),skillTitle:z.string(),brief:z.string(),model:z.string(),prompt:z.string(),time:z.string(),sessionId:z.string(),kind:z.literal('combination').optional(),primaryId:z.string().optional(),members:z.array(z.object({skillId:z.string(),title:z.string(),role:z.string(),isPrimary:z.boolean()})).optional()});
const choiceSchema = z.object({status:z.enum(['testing','keep','watch','retired']),favorite:z.boolean(),updatedAt:z.string()});

export class PromptWorkbench {
  constructor(ctx, domain, curated, groups, packs, library=new OriginalLibrary(base), localizations={}, families=[]) { Object.assign(this,{ctx,domain,curated,groups,packs,library,localizations,families}); }
  registry(agent) { return this.ctx.agentPresets.serviceFor(agent,'skills') ?? this.ctx.skills; }
  async catalog(agent) {
    const registry=this.registry(agent), cwd=await this.ctx.workingDirectory.ensure(agent);
    const snapshot=await registry.snapshot({cwd,scope:agent});
    // A failed provider may leave other providers' valid entries usable.
    // Keep the completeness flag visible; never promote missing entries to available.
    const live=snapshot.skills;
    const byId=new Map(live.map(s=>[s.name,s]));
    const all=new Map(this.curated.map(s=>{const active=byId.get(s.id);return [s.id,{...s,description:active?.description??s.description,whenToUse:active?.whenToUse??s.whenToUse,path:active?.path,source:active?.source,provider:active?.provider,userInvocable:active?.invocation.userInvocable===true,modelInvocable:active?.invocation.modelInvocable===true,origin:'existing',available:!!active&&(active.invocation.modelInvocable||active.invocation.userInvocable)}];}));
    for(const s of live) {
      const c=classify(s);
      if(!all.has(s.name)&&c) all.set(s.name,{id:s.name,title:s.name,description:s.description,whenToUse:s.whenToUse??s.description,category:c,platforms:[],sideEffects:'请在试用前查看技能说明。',origin:'existing',available:s.invocation.modelInvocable||s.invocation.userInvocable,userInvocable:s.invocation.userInvocable,modelInvocable:s.invocation.modelInvocable,source:s.source,provider:s.provider,path:s.path});
    }
    for(const [id, folder, title] of [['image-prompt-reverse','image-prompt-reverse','图片反推与增强'],['prompt-reverse-engineer','prompt-reverse-engineer','多模态提示词逆向']]) {
      all.set('pack:'+id,{id:'pack:'+id,title,description:'新增资源包：独立试用原项目的方法，保留来源与参考文档。',whenToUse:id==='image-prompt-reverse'?'从参考图还原画面并探索增强方向':'将图片、文案、视频或剧本拆解为提示词',category:'reverse',platforms:['Midjourney','通用模型'],sideEffects:'工作台试用仅输出提示词。视频依赖与抽帧尚未自动执行。',origin:'new',available:true,path:fileURLToPath(new URL('packs/'+folder+'/SKILL.md',base))});
    }
    const result=assignSkillFamilies([...all.values()],this.families).map(s=>{
      const choice=this.domain.table('choices').get(s.id)??{status:'testing',favorite:false};
      const reviews=[...this.domain.table('reviews').entries()].map(([,r])=>r).filter(r=>r.skillId===s.id&&this.domain.table('trials').get(r.trialId)?.kind!=='combination');
      return {...localizeSkill(s,this.localizations),...choice,reviewCount:reviews.length,averageRating:reviews.length?Number((reviews.reduce((n,r)=>n+r.rating,0)/reviews.length).toFixed(1)):null};
    });
    Object.defineProperty(result,'complete',{value:snapshot.complete});
    return result;
  }
  async execute(request,agent,signal) {
    if(!request||typeof request!=='object') throw Error('请求格式错误');
    if(signal?.aborted) throw Error('操作已取消');
    const action=request.action;
    if(this.manualMode)await this.manualMode.ensure(agent);
    if(['setManualMode','setAllowlist','setDefaultAllowlist'].includes(action))throw Error('权限设置仅允许通过选择器中的用户操作修改');
    if(action==='manualMode')return {manualMode:await this.manualMode?.status(agent)};
    if(action==='open')return {ok:true,workbenchOpen:{token:randomUUID(),time:Date.now()},notice:'在当前对话右侧打开技能选择页，选择网页工具后才打开浏览器。'};
    if(action==='originals')return {items:originals};
    if(action==='openWebsite')return openOriginalInChrome(request.id);
    if(action==='activate'){
      if(request.id!=='youmind')throw Error('网页工具请从技能选择页点击进入Chrome 新窗口');
      if(this.manualMode?.enabled(agent)) {
        await this.library.sync();
        return {id:'youmind',...await this.execute({action:'use',skillId:'ai-image-prompts-skill',brief:bounded(request.brief).trim()||'请按作者原版图像提示词库流程，先询问我需要什么图片，再检索推荐并按选择改写。'},agent,signal)};
      }
      return {id:'youmind',...await this.library.activate(request.brief)};
    }
    if(action==='library')return this.library.search(request);
    if(action==='refresh')return this.library.sync(true);
    if(action==='list') {
      const all=await this.catalog(agent);
      const skills=rankSkills(all,bounded(request.query,500)).filter(s=>!request.category||request.category==='all'||s.category===request.category);
      return {skills,originals,families:this.families,manualMode:await this.manualMode?.status(agent),catalogComplete:all.complete,groups:this.groups,sources:this.packs.catalog.sources,stats:{total:all.length,available:all.filter(s=>s.available).length,reviewed:all.filter(s=>s.reviewCount).length,retired:all.filter(s=>s.status==='retired').length},notice:all.complete?'停用仅影响本工作台，DSH 全局技能开关由技能管理器控制。':'部分技能来源尚未完成发现，当前显示已发现项目；缺失项不代表已删除。可刷新重试，已发现技能可继续试用。'};
    }
    if(action==='recommend') {
      const brief=bounded(request.brief,1000).trim();if(!brief)throw Error('请先说说你想做什么');
      const catalog=await this.catalog(agent);
      return {skills:recommendSkills(catalog,brief),catalogComplete:catalog.complete,notice:'按技能用途和关键词匹配，展示全部匹配项；不是效果评分。没有匹配时可浏览分类或换一种说法。'};
    }
    if(action==='use') {
      const skillId=bounded(request.skillId,200),brief=bounded(request.brief).trim();if(!brief)throw Error('请填写你的需求');
      const candidate=(await this.catalog(agent)).find(s=>s.id===skillId);
      if(!candidate?.available||candidate.status==='retired')throw Error('该技能不可用或已隐藏，请刷新或恢复后使用');
      if(candidate.origin==='existing') {
        const definition=await this.registry(agent).get(skillId,{cwd:await this.ctx.workingDirectory.ensure(agent,signal),scope:agent,signal});
        if(!definition||!(definition.invocation.modelInvocable||definition.invocation.userInvocable))throw Error('该技能当前无法加载，请刷新后重试');
        candidate.userInvocable=definition.invocation.userInvocable;
      }
      const id=randomUUID();
      const prompt=this.manualMode?.enabled(agent)?`${selectionMarker(id)}\n\n本轮使用「${candidate.title}」（${skillId}），所选完整技能由选择器注入，无须调用 skill 工具。\n\n我的需求：\n${brief}\n\n仅采用已选择技能，依赖其他技能时请我补选。` : makeUsePrompt(candidate,brief);
      const trial={id,skillId,skillTitle:candidate.title,brief,model:'按需求',prompt,time:new Date().toISOString(),sessionId:agent.id};
      await this.domain.table('trials').put(trial.id,trial);
      return {trial,prompt,notice:'已保存使用记录。填入当前对话后检查并发送；尚未执行技能或提交外部服务。'};
    }
    if(action==='combine') {
      const ids=[...new Set(Array.isArray(request.ids)?request.ids:[])];
      const primaryId=bounded(request.primaryId,200),brief=bounded(request.brief).trim();
      if(ids.length<2||ids.some(id=>typeof id!=='string'||id.length>200))throw Error('组合使用请至少选择两个技能');
      if(!ids.includes(primaryId))throw Error('请从所选技能中指定一个主技能');
      if(!brief)throw Error('请填写你的需求');
      if(request.roles!==undefined&&(!request.roles||typeof request.roles!=='object'||Array.isArray(request.roles)))throw Error('分工格式错误');
      const roles={};
      for(const [id,value] of Object.entries(request.roles??{})) {
        if(!ids.includes(id)||typeof value!=='string'||value.length>1000)throw Error('分工应为所选技能的 1000 字以内文本');
        roles[id]=value.trim();
      }
      const catalog=await this.catalog(agent),candidates=ids.map(id=>catalog.find(s=>s.id===id));
      if(candidates.some(s=>!s?.available||s.status==='retired'))throw Error('所选技能不可用或已隐藏，请刷新或恢复后使用');
      const cwd=await this.ctx.workingDirectory.ensure(agent,signal);
      for(const candidate of candidates.filter(s=>s.origin==='existing')) {
        const definition=await this.registry(agent).get(candidate.id,{cwd,scope:agent,signal});
        if(!definition||!(definition.invocation.modelInvocable||definition.invocation.userInvocable))throw Error('该技能当前无法加载，请刷新后重试：'+candidate.id);
        candidate.userInvocable=definition.invocation.userInvocable;
      }
      const ordered=[candidates.find(s=>s.id===primaryId),...candidates.filter(s=>s.id!==primaryId)];
      const members=ordered.map(s=>({skillId:s.id,title:s.title,role:roles[s.id]||(s.id===primaryId?'负责整体方案、最终交付格式和整合结果。':'仅就本技能擅长的部分补充主任务，不另行接管完整流程。'),isPrimary:s.id===primaryId}));
      const id=randomUUID();
      const ordinary=makeCombinedPrompt(candidates,primaryId,roles,brief);
      const prompt=this.manualMode?.enabled(agent)?`${selectionMarker(id)}\n\n${ordinary.replace(/加载所选技能：[\s\S]*?\n\n执行方式：/,'所选完整技能由选择器注入，无须调用 skill 工具；依赖其他技能时请我补选。\n\n执行方式：')}`:ordinary;
      const trial={id,kind:'combination',primaryId,members,skillId:primaryId,skillTitle:'组合：'+ordered.map(s=>s.title).join(' + '),brief,model:'组合使用',prompt,time:new Date().toISOString(),sessionId:agent.id};
      await this.domain.table('trials').put(trial.id,trial);
      return {trial,prompt,notice:'组合草稿已保存。请先预览分工，再加入当前草稿并自行发送；尚未执行任何技能。评价记录针对组合整体，不计入单个技能的平均分。'};
    }
    if(action==='setStatus'||action==='feedback') {
      const skillId=bounded(request.skillId,200);
      const savedTrial=action==='feedback'&&request.trialId?this.domain.table('trials').get(bounded(request.trialId,100)):undefined;
      if(savedTrial?.skillId!==skillId&&!(await this.catalog(agent)).some(s=>s.id===skillId))throw Error('找不到该技能');
      if(savedTrial?.kind==='combination'&&(request.status!==undefined||request.favorite!==undefined))throw Error('组合整体评价不能修改单个技能状态，请在技能卡片中单独调整');
      if(request.status!==undefined&&!statuses.has(request.status))throw Error('无效的状态');
      if(action==='feedback') {
        if(!Number.isInteger(request.rating)||request.rating<1||request.rating>5)throw Error('评分必须为 1 至 5');
        const trialId=bounded(request.trialId,100)||undefined;
        if(trialId&&this.domain.table('trials').get(trialId)?.skillId!==skillId)throw Error('评价与测试技能不匹配');
        const review={id:randomUUID(),skillId,trialId,rating:request.rating,note:bounded(request.note,2000),time:new Date().toISOString()};
        await this.domain.table('reviews').put(review.id,review);
      }
      if(request.status!==undefined||request.favorite!==undefined) {
        const old=this.domain.table('choices').get(skillId)??{status:'testing',favorite:false};
        await this.domain.table('choices').put(skillId,{status:request.status??old.status,favorite:typeof request.favorite==='boolean'?request.favorite:old.favorite,updatedAt:new Date().toISOString()});
      }
      return {ok:true,skillId,notice:'已保存。原技能文件和 DSH 全局启用状态未更改。'};
    }
    if(action==='history')return {trials:[...this.domain.table('trials').entries()].map(([,v])=>v).sort((a,b)=>b.time.localeCompare(a.time)).slice(0,200),reviews:[...this.domain.table('reviews').entries()].map(([,v])=>v).sort((a,b)=>b.time.localeCompare(a.time)).slice(0,500)};
    if(action==='resources') {
      const key={prompts:'prompts',styles:'styles',fill:'fill'}[request.kind];if(!key)throw Error('无效的资源类型');
      const q=bounded(request.query,200).toLowerCase();
      return {items:this.packs[key].filter(x=>!q||JSON.stringify(x).toLowerCase().includes(q)).slice(0,60),sources:this.packs.catalog.sources,notice:'当前为注明来源的精选子集，未自动同步整个上游库。'};
    }
    if(action==='compose') {
      const key={prompts:'prompts',styles:'styles',fill:'fill'}[request.kind];
      const resource=key&&this.packs[key].find(x=>x.id===request.id);if(!resource)throw Error('找不到该资源');
      return composeResource(resource,request);
    }
    if(action==='export') return {schemaVersion:1,exportedAt:new Date().toISOString(),choices:Object.fromEntries(this.domain.table('choices').entries()),trials:Object.fromEntries(this.domain.table('trials').entries()),reviews:Object.fromEntries(this.domain.table('reviews').entries())};
    throw Error('未知操作：'+bounded(action,80));
  }
}

export async function apply(ctx) {
  const [curated,groups,catalog,prompts,styles,fill,localizations,familyData]=await Promise.all(['curated-skills.json','comparison-groups.json','packs/catalog.json','packs/prompts.json','packs/styles.json','packs/fill-templates.json','skill-localizations.json','skill-families.json'].map(json));
  const library=new OriginalLibrary(base);
  const skillPath=fileURLToPath(new URL(youmindFolder+'SKILL.md',base));
  const upstreamContent=await readFile(skillPath,'utf8');
  ctx.effect(()=>ctx.skills.register({name:'ai-image-prompts-skill',description:'作者原版完整图像提示词推荐库，包含全部分类及样图。按原版先推荐最多3条模板、选中后改写；使用前检查更新。',path:skillPath,source:'runtime',resourceBase:{kind:'directory',path:fileURLToPath(new URL(youmindFolder,base))},content:upstreamContent}));
  ctx.effect(()=>ctx.skills.register({name:'mj-prompt-workbench',description:'用户要打开技能选择器、找适合的技能、使用MJ提示词或打开工作台时，调用 prompt_workbench action=open 展示当前对话右侧技能选择页。选中网页工具才打开Chrome。',source:'runtime',content:'用户要求打开技能选择器、选择技能或打开提示词工作台时，调用 prompt_workbench({action:"open"})。按任务找技能可用 recommend，brief 为需求。普通使用用 use，skillId 和 brief 必填。组合使用用 combine，ids 至少两个，primaryId 为其中主技能，roles 按技能 id 填职责，brief 为共同需求；只生成预览草稿，不自动执行。返回启动草稿，不等于已执行技能。用户发送草稿后按指定技能执行。需要比较时由用户自行分支对话；feedback 记录主观评价，retired 仅隐藏工作台技能。只有用户选中网页工具后才打开Chrome。用户明确指名技能并要求直接完成时，加载该技能执行，无须再选。'}));
  const openSchema=z.object({token:z.string(),time:z.number()});
  const openState=openSchema.extend({pending:z.array(z.string())});
  const projection=await ctx.sessionProjections.register({key:'promptWorkbenchOpen',stateSchema:openState,init:()=>({token:'',time:0,pending:[]}),apply:projectWorkbenchOpen,wire:{viewSchema:openSchema,view:({token,time})=>({token,time})},stateVersion:1});
  ctx.effect(()=>()=>projection.dispose());
  const domain=await ctx.storageDomain.open({name:'prompt_workbench',version:1,tables:{choices:{valueSchema:choiceSchema},trials:{valueSchema:trialSchema},reviews:{valueSchema:reviewSchema}}});
  ctx.effect(()=>()=>domain.close());
  const service=new PromptWorkbench(ctx,domain,curated,groups,{catalog,prompts,styles,fill},library,localizations,familyData.families);
  const settings=await ctx.storageDomain.open({name:'skill_selector_sessions',version:1,global:{schema:z.object({allowlist:z.array(z.string())}),initial:{allowlist:[]}},tables:{sessions:{valueSchema:z.object({enabled:z.boolean(),allowlist:z.array(z.string())})}}});
  ctx.effect(()=>()=>settings.close());
  const manualMode=new ManualSkillMode(ctx,settings,service);
  service.manualMode=manualMode;
  ctx.effect(()=>ctx.tools.guard(exec=>manualMode.guard(exec)));
  ctx.on('agent/pre-step',(payload,next)=>manualMode.enter(payload,next),{prepend:true});
  ctx.effect(()=>ctx.commands.register({name:'prompt-workbench',description:'技能选择器：按任务找技能、使用和评价',input:{hint:'JSON 操作'},handler:async({agent,rawInput,signal})=>{
    try {const request=rawInput.trim()?JSON.parse(rawInput):{action:'list'};const value=request.action==='setManualMode'?await manualMode.set(agent,request.enabled):request.action==='setAllowlist'?await manualMode.setAllowlist(agent,request.ids):request.action==='setDefaultAllowlist'?await manualMode.setAllowlist(agent,request.ids,true):await service.execute(request,agent,signal);return {kind:'success',text:JSON.stringify(value)};}
    catch(error){return {kind:'error',text:error.message};}
  }}));
  ctx.effect(()=>ctx.tools.register({name:'prompt_workbench',description:'技能选择器。recommend 按 brief 用途匹配并返回全部匹配技能；use 用 skillId 和 brief 创建普通使用草稿（不执行），用户发送后加载对应技能；combine 用 ids、primaryId、roles（技能 id 到职责文本）、brief 生成主辅组合草稿预览（不执行）。用户要使用MJ提示词或选择技能时先用 open 打开当前对话右侧技能选择页，选中网页技能才打开浏览器。originals 查看3个完整版入口；openWebsite 按网站 id 在 Chrome 新窗口打开原版网站；activate id=youmind 使用作者完整技能；library 搜索完整库最多3条并展示样图；refresh 强制更新。list/feedback/setStatus/history/export 管理现有技能与试用。resources/compose 仅兼容旧样本入口，不是完整版。',parameters:{type:'object',properties:{action:{type:'string',enum:['open','originals','openWebsite','activate','library','refresh','list','recommend','use','combine','feedback','setStatus','history','resources','compose','export']},query:{type:'string'},category:{type:'string'},ids:{type:'array',items:{type:'string'}},brief:{type:'string'},primaryId:{type:'string'},roles:{type:'object',additionalProperties:{type:'string',maxLength:1000}},model:{type:'string'},skillId:{type:'string'},trialId:{type:'string'},rating:{type:'integer',minimum:1,maximum:5},note:{type:'string'},status:{type:'string',enum:['testing','keep','watch','retired']},favorite:{type:'boolean'},kind:{type:'string',enum:['prompts','styles','fill']},id:{type:'string'},variables:{type:'object',additionalProperties:{type:'string'}},aspectRatio:{type:'string'}},required:['action'],additionalProperties:false},output:{schema:{},render:(_args,value)=>[{type:'text',text:JSON.stringify(value)}]},execute:async(args,exec)=>{
    const agent=exec.agent&&ctx.agents.get(exec.agent.id);if(!agent)throw Error('需要有效的当前会话');return JSON.parse(JSON.stringify(await service.execute(args,agent,exec.signal)));
  }}));
}
