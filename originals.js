import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run=promisify(execFile);
export const youmindFolder='full/youmind/ai-image-prompts-skill-39c0c0033904de9c164df3ec2245d3b44526df04/';
export class OriginalLibrary {
  constructor(base){this.base=base;this.root=new URL(youmindFolder,base);this.pending=null;}
  async sync(force=false){
    if(this.pending)return this.pending;
    this.pending=(async()=>{
      const stamp=new URL('references/.last-updated',this.root);
      let before='';try{before=await readFile(stamp,'utf8');}catch{}
      // The upstream --check skips existing files even when stale. Use its own --force for a real refresh.
      const refresh=force||!before||!Number.isFinite(Number(before.trim()))||Date.now()-Number(before.trim())>24*3600*1000;
      const {stdout,stderr}=await run(process.execPath,[fileURLToPath(new URL('scripts/setup.js',this.root)),refresh?'--force':'--check'],{env:{...process.env,ELECTRON_RUN_AS_NODE:'1'},timeout:120000,maxBuffer:1024*1024,windowsHide:true});
      if(/Could not fetch manifest|Falling back to existing local manifest|file\(s\) failed|Warning \(non-fatal\)/i.test(stdout+stderr))throw Error('上游同步未完整成功，请重试。'+(stdout+stderr).slice(-1500));
      const manifest=await this.manifest();
      for(const c of manifest.categories){const records=await this.category(c.file);if(!Array.isArray(records)||records.length!==c.count)throw Error('上游分类数据无效或更新不完整：'+c.file);}
      let after='';try{after=await readFile(stamp,'utf8');}catch{}
      if((refresh||!before)&&(!after||before===after))throw Error('上游更新未完成，请重试。'+(stdout+stderr).slice(-1500));
      return {updated:after!==before,updatedAt:after?new Date(Number(after.trim())).toISOString():null,log:(stdout+stderr).slice(-2000),notice:'按作者原版 setup.js 执行；每次使用检查时效，主动更新使用 --force。'};
    })().finally(()=>{this.pending=null;});return this.pending;
  }
  async manifest(){return JSON.parse(await readFile(new URL('references/manifest.json',this.root),'utf8'));}
  async category(file){if(!/^[a-z0-9-]+\.json$/.test(file))throw Error('无效的上游分类文件名');return JSON.parse(await readFile(new URL('references/'+file,this.root),'utf8'));}
  async search(request={}){
    await this.sync(false);
    const manifest=await this.manifest(),query=String(request.query??'').toLowerCase().trim(),words=query.split(/\s+/).filter(Boolean);
    const categories=manifest.categories.filter(c=>!request.category||c.slug===request.category);
    if(!categories.length)throw Error('上游没有该分类，请先读取分类清单');
    if(!query&&!request.id)return {categories:manifest.categories,items:[],notice:'请提供主题和用途后检索；先推荐原始模板，选中后再改写。'};
    const found=new Map();
    for(const c of categories)for(const p of await this.category(c.file)){
      if(!p.sourceMedia?.length)continue;
      if(request.id&&String(p.id)!==String(request.id))continue;
      const hay=[p.title,p.description,p.content].join(' ').toLowerCase();
      const score=words.reduce((n,w)=>n+(hay.includes(w)?1:0),0);
      if(!request.id&&words.length&&!score)continue;
      const previous=found.get(String(p.id));if(!previous||score>previous.score)found.set(String(p.id),{...p,score,category:c.slug});
    }
    return {categories:manifest.categories,items:[...found.values()].sort((a,b)=>b.score-a.score).slice(0,3),notice:'最多3条原始完整提示词；展示每条 sourceMedia[0] 样图、≤100字符预览及来源。用户选中后再改写。',attribution:'提示词由 [YouMind.com](https://youmind.com) 通过公开社区搜集 ❤️',manifestTotal:manifest.totalPrompts};
  }
  async activate(brief=''){
    const sync=await this.sync(false);
    return {prompt:`请调用 skill 工具加载 ai-image-prompts-skill，按作者完整流程使用。若不可用，完整读取：${fileURLToPath(new URL('SKILL.md',this.root))}。先了解我的需求，使用 prompt_workbench action=library 从完整本地分类库检索；需要时可按相对路径读取原版文件。每次使用先按原版检查更新，手动刷新用 action=refresh。每次最多推荐3条原始模板，必须展示样图、来源与≤100字符预览，保留完整提示词供选中后改写；不要提前混编模板。遵守原作者归属说明。\n\n我的需求：${String(brief).slice(0,6000)||'请先询问我想做什么图片。'}`,sync};
  }
}
export const originals=[
 {id:'youmind',title:'AI Image Prompts · 完整提示词库',kind:'skill',skillId:'ai-image-prompts-skill',description:'作者原版完整分类库、样图推荐、选中后改写；每次使用检查更新。'},
 {id:'visual-cookbook',title:'AI Visual Prompt Cookbook · 原版画廊',kind:'web',url:'https://prompts.vigocreativeai.com/site/',description:'作者在线完整186套风格。浏览样图、复制完整JSON，按作者说明替换变量。'},
 {id:'promptfill',title:'Prompt Fill · 原版编辑器',kind:'web',url:'https://www.aipromptfill.com/',description:'作者在线完整版：248套模板、完整词库、变量编辑、预览和导入导出。'}
];
export function projectWorkbenchOpen(state,event){
 if(event.type==='tool/call'&&event.data.name==='prompt_workbench'){
  try{if(JSON.parse(event.data.arguments).action==='open')return {...state,pending:[...(state.pending??[]),event.data.callId].slice(-20)};}catch{}
 }
 if(event.type!=='tool/result')return state;
 const message=event.data.message,pending=state.pending??[];
 if(!pending.includes(message.toolCallId))return state;
 const next={...state,pending:pending.filter(id=>id!==message.toolCallId)};
 if(message.isError)return next;
 for(const block of message.content??[]){
  if(block.type!=='text')continue;
  try{const marker=JSON.parse(block.text).workbenchOpen;
   if(marker&&typeof marker.token==='string'&&typeof marker.time==='number')return {...next,token:marker.token,time:marker.time};
  }catch{}
 }
 return next;
}
