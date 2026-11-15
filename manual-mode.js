import { randomUUID } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const MARKER = /^\[DSH技能选择:([a-f0-9-]{36})\]\s*$/m;
const LEGACY_POLICY = '手动技能模式已开启。普通对话不自动加载任何技能；旧目录不再代表本轮调用许可。用户需要技能时，可调用 prompt_workbench 的 open/recommend 展示选择器。只有用户直接发送 /技能名 或选择器使用草稿，才加载其中明确选择的技能。不得通过 skill 工具、读取其他技能入口、命令行或委托代理绕过选择；所选技能提到其他技能时，请用户补选。本轮已加载内容会留在聊天历史中，不代表以后普通消息继续授权新技能。';
const textOf = message => (message.content ?? []).filter(b => b.type === 'text').map(b => b.text).join('\n');
const injection = (text, source) => ({id:randomUUID(),role:'user',content:[{type:'text',text}],source});
const idsOf = trial => trial.kind === 'combination' ? trial.members.map(m => m.skillId) : [trial.skillId];
const escape = text => String(text).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
export const selectionMarker = id => `[DSH技能选择:${id}]`;

export class ManualSkillMode {
  constructor(ctx, settings, service) {
    Object.assign(this,{ctx,settings,service});
    this.published = new WeakMap();
    this.initializing = new Map();
    // Skills the user picked in this conversation (selection draft markers or leading /skill lines).
    // Guards consult this so a deliberate choice is usable without editing the persistent allowlist.
    this.granted = new Map();
    this.warned = new Map();
  }
  sessionId(agent) {
    if (!agent || typeof agent.id !== 'string' || !agent.id) throw Error('需要有效的当前对话');
    return agent.id;
  }
  async ensure(agent) {
    const id = this.sessionId(agent), table = this.settings.table('sessions');
    const existing = table.get(id);
    if (existing) return existing;
    if (!this.initializing.has(id)) {
      // Snapshot defaults once. Future default edits never rewrite existing conversations.
      // Default off: a fresh conversation must not start by blocking skills the user has not
      // allowlisted yet. Turning it on stays available from the panel for opt-in restriction.
      const initial = {enabled:false,allowlist:[...this.settings.global.get().allowlist]};
      const pending = table.put(id,initial).then(()=>initial).finally(()=>this.initializing.delete(id));
      this.initializing.set(id,pending);
    }
    return this.initializing.get(id);
  }
  enabled(agent) { return this.settings.table('sessions').get(this.sessionId(agent))?.enabled ?? false; }
  async status(agent) {
    const policy = await this.ensure(agent);
    return {...policy,allowlist:[...policy.allowlist],scope:'session',sessionId:agent.id,defaultAllowlist:[...this.settings.global.get().allowlist],notice:'开关和自动调用名单仅影响当前对话。新对话默认关闭手动模式，技能按原生规则调用；开启后才按白名单自动加载，白名单外仍可直接发送 /技能名 或选择草稿。关闭时恢复原生规则，历史技能内容不清除。'};
  }
  async set(agent, enabled) {
    if (typeof enabled !== 'boolean') throw Error('手动模式必须为布尔值');
    await this.ensure(agent);
    await this.settings.table('sessions').update(agent.id,current=>({...current,enabled}));
    return {manualMode:await this.status(agent)};
  }
  async setAllowlist(agent, ids, defaults = false) {
    if (!Array.isArray(ids) || ids.some(id=>typeof id !== 'string' || !id || id.length>200)) throw Error('白名单必须为技能 ID 数组');
    await this.ensure(agent);
    const values = [...new Set(ids)];
    const old = defaults ? this.settings.global.get().allowlist : this.settings.table('sessions').get(agent.id).allowlist;
    const added = values.filter(id=>!old.includes(id));
    if (added.length) {
      const cwd = await this.ctx.workingDirectory.ensure(agent);
      for (const id of added) {
        const definition = !id.startsWith('pack:') && await this.service.registry(agent).get(id,{cwd,scope:agent});
        if (!definition?.invocation?.modelInvocable) throw Error('此技能不能自动调用，请手动选择：'+id);
      }
    }
    if (defaults) await this.settings.global.set({allowlist:values});
    else await this.settings.table('sessions').update(agent.id,current=>({...current,allowlist:values}));
    return {manualMode:await this.status(agent)};
  }
  guard(exec) {
    if (exec.name !== 'skill') return;
    const agent = exec.agent;
    if (!agent?.id) return {reason:'技能加载需要明确的当前对话',info:{name:'ManualSkillMode',code:'SKILL_SESSION_REQUIRED'}};
    const policy = this.settings.table('sessions').get(agent.id);
    if (!policy?.enabled) return;
    let args = exec.arguments;
    if (typeof args === 'string') { try { args = JSON.parse(args); } catch { args = undefined; } }
    if (policy.allowlist.includes(args?.name)) return;
    if (this.granted.get(agent.id)?.has(args?.name)) return;
    return {reason:'此技能不在当前对话的自动调用白名单中，请从选择器选择并发送使用草稿，或直接发送 /技能名。',info:{name:'ManualSkillMode',code:'MANUAL_SKILL_REQUIRED'}};
  }
  previous(agent) {
    if (this.published.has(agent)) return this.published.get(agent);
    const session = agent.session;
    if (session?.eventAt && session.surface?.nodes) {
      const visible = new Set(session.surface.nodes);
      for (let index=session.seq-1;index>=0;index--) {
        const event = session.eventAt(index);
        if (event?.type !== 'user/message' || !visible.has(event.seq)) continue;
        const message = event.data;
        if (message.source?.kind === 'skill-selector-policy') return {enabled:message.source.enabled,key:message.source.policyKey};
        if (message.source?.kind === 'skill-catalog' && textOf(message) === LEGACY_POLICY) return {enabled:true};
      }
    }
  }
  async catalog(agent, signal, allowlist) {
    const snapshot = this.ctx.tools.get('skill',agent)
      ? await this.service.registry(agent).snapshot({cwd:await this.ctx.workingDirectory.ensure(agent,signal),scope:agent,signal})
      : {skills:[],complete:true};
    const allowed = allowlist && new Set(allowlist);
    return {entries:snapshot.skills.filter(s=>s.invocation.modelInvocable && (!allowed || allowed.has(s.name))).map(s=>({name:s.name,description:s.description})),complete:snapshot.complete};
  }
  catalogMessage({entries,complete}, restricted) {
    return injection('<available_skills>\n'+entries.map(s=>'- `'+s.name+'`: '+escape(s.description)).join('\n')+'\n</available_skills>\n'+(restricted?'当前目录仅包含本对话允许自动调用的技能；名单外技能需用户手动选择。':'当前目录替换此前的限制目录，恢复宿主原生调用规则。')+(!complete?' 技能发现尚未完整，仅显示已确认项目。':''),{kind:'skill-catalog',form:'catalog',entries,update:true,...(!complete?{incomplete:true}:{})});
  }
  async enter(payload, next) {
    const {agent,signal} = payload;
    await this.ensure(agent);
    const decision = await next();
    if (decision.kind === 'reject') return decision;
    const policy = this.settings.table('sessions').get(agent.id);
    const previous = this.previous(agent);
    const permitted = new Set(policy.allowlist), selected = [], stale = [];
    for (const message of payload.messages.filter(m=>m.role === 'user' && m.source?.kind === 'user')) {
      const body = textOf(message);
      for (const line of body.trimStart().split(/\r?\n/)) {
        const match = /^\/([a-z0-9]+(?:-[a-z0-9]+)*)\s*$/.exec(line.trim());
        if (!match) break;
        permitted.add(match[1]);
      }
      const marker = MARKER.exec(body);
      if (!marker) continue;
      const trial = this.service.domain.table('trials').get(marker[1]);
      // The marker is a 36-char UUID bound to exactly one trial row, so it cannot be guessed.
      // Proof of a deliberate choice = marker anchored at message start + same session + real
      // draft body after it. Requiring the whole draft verbatim (trial.prompt) used to void the
      // grant as soon as the user edited a single word, which read as "the skill never loaded".
      const after = body.trimStart().startsWith(marker[0]) ? body.trimStart().slice(marker[0].length).trim() : '';
      if (!trial || trial.sessionId !== agent.id || !after) {
        if (after) stale.push(marker[1]);
        continue;
      }
      for (const id of idsOf(trial)) { permitted.add(id); selected.push(id); }
    }
    this.granted.set(agent.id, permitted);
    const messages = policy.enabled ? decision.messages.filter(m=>m.source?.kind !== 'skill-catalog' && (m.source?.kind !== 'skill-invocation' || permitted.has(m.source.name))) : [...decision.messages];
    const present = new Set(messages.filter(m=>m.source?.kind === 'skill-invocation').map(m=>m.source.name));
    const cwd = selected.length ? await this.ctx.workingDirectory.ensure(agent,signal) : undefined;
    for (const id of new Set(selected)) {
      if (present.has(id)) continue;
      signal?.throwIfAborted();
      let content,resourceBase;
      if (id.startsWith('pack:')) {
        const candidate = (await this.service.catalog(agent)).find(s=>s.id === id);
        if (!candidate?.available || candidate.status === 'retired') throw Error('所选技能包已不可用，请重新选择：'+id);
        content = await readFile(candidate.path,'utf8');
        resourceBase = {kind:'directory',path:candidate.path.replace(/[\\/][^\\/]+$/,'')};
      } else {
        const definition = await this.service.registry(agent).get(id,{cwd,scope:agent,signal});
        if (!definition || !(definition.invocation.userInvocable || definition.invocation.modelInvocable)) throw Error('所选技能已不可用，请重新选择：'+id);
        content = definition.content; resourceBase = definition.resourceBase;
      }
      messages.push(injection(`<skill_content name="${id}">\n${resourceBase?'<skill_resources>\n'+JSON.stringify(resourceBase)+'\n相对参考资源从上述位置读取。\n</skill_resources>\n':''}<skill_instructions>\n${content}\n</skill_instructions>\n</skill_content>`,{kind:'skill-invocation',name:id,form:'instructions'}));
    }
    if (!policy.enabled) {
      if (previous?.enabled) {
        if (!messages.some(m=>m.source?.kind === 'skill-catalog')) messages.push(this.catalogMessage(await this.catalog(agent,signal),false));
        messages.push(injection('当前对话手动技能模式已关闭。此前手动限制和自动调用白名单限制已撤销，恢复本对话的宿主原生技能调用规则；不影响其他对话。',{kind:'skill-selector-policy',enabled:false,policyKey:'off'}));
      }
      this.published.set(agent,{enabled:false,key:'off'});
      return !previous?.enabled && !selected.length ? decision : {...decision,messages};
    }
    const catalog = await this.catalog(agent,signal,[...new Set([...policy.allowlist,...selected])]);
    const key = JSON.stringify({allowlist:policy.allowlist,entries:catalog.entries,complete:catalog.complete});
    if (!previous?.enabled || previous.key !== key) {
      messages.push(this.catalogMessage(catalog,true));
      messages.push(injection('当前对话手动技能模式已开启。允许自动调用的技能 ID：'+(policy.allowlist.join('、')||'无')+'。白名单外仅用户直接发送独立 /技能名 或完整选择草稿时加载；不得通过读取其他技能入口、命令行或委托代理绕过限制，涉及额外技能请用户补选。已加载历史不会清除。本对话设置不影响其他对话，其他旧目录和旧说明不再代表当前许可。',{kind:'skill-selector-policy',enabled:true,policyKey:key}));
      this.published.set(agent,{enabled:true,key});
    }
    if (stale.length) {
      const seen = this.warned.get(agent.id) ?? new Set();
      this.warned.set(agent.id,seen);
      const fresh = [...new Set(stale)].filter(id=>!seen.has(id));
      if (fresh.length) {
        fresh.forEach(id=>seen.add(id));
        const other = stale.filter(id=>!this.service.domain.table('trials').get(id));
        messages.push(injection('有 '+fresh.length+' 份技能选择草稿没有生效，因此本轮没有加载对应技能。原因：'+(other.length?'选择记录已失效，请重新从选择器生成草稿':'草稿属于其他对话，请在本对话重新生成使用草稿')+'。',{kind:'skill-selector-notice',stale:fresh.length}));
      }
    }
    return {...decision,messages};
  }
}
