import { randomUUID } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const MARKER = /^\[DSH技能选择:([a-f0-9-]{36})\]\s*$/m;
const POLICY = '手动技能模式已开启。普通对话不自动加载任何技能；旧目录不再代表本轮调用许可。用户需要技能时，可调用 prompt_workbench 的 open/recommend 展示选择器。只有用户直接发送 /技能名 或选择器使用草稿，才加载其中明确选择的技能。不得通过 skill 工具、读取其他技能入口、命令行或委托代理绕过选择；所选技能提到其他技能时，请用户补选。本轮已加载内容会留在聊天历史中，不代表以后普通消息继续授权新技能。';
const textOf = message => (message.content ?? []).filter(b => b.type === 'text').map(b => b.text).join('\n');
const injection = (text, source) => ({ id: randomUUID(), role: 'user', content: [{type:'text',text}], source });
const idsOf = trial => trial.kind === 'combination' ? trial.members.map(m => m.skillId) : [trial.skillId];
export const selectionMarker = id => `[DSH技能选择:${id}]`;

export class ManualSkillMode {
  constructor(ctx, settings, service) { Object.assign(this, {ctx, settings, service}); }
  enabled() { return this.settings.global.get().enabled; }
  status() { return {enabled:this.enabled(),scope:'profile',notice:'当前配置下所有对话统一生效。普通消息不自动加载技能；发送选择草稿或 /技能名 才加载。已加载的历史内容不会清除。关闭后恢复原调用规则。'}; }
  async set(enabled) {
    if (typeof enabled !== 'boolean') throw Error('手动模式必须为布尔值');
    await this.settings.global.set({enabled});
    return {manualMode:this.status()};
  }
  guard(exec) {
    if (this.enabled() && exec.name === 'skill') return {reason:'手动技能模式：请从选择器选择并发送使用草稿，或直接发送 /技能名；不允许模型自行加载技能。',info:{name:'ManualSkillMode',code:'MANUAL_SKILL_REQUIRED'}};
  }
  async enter(payload, next) {
    // Prepend this outer listener so the returned decision already includes the native catalog/invocations.
    const decision = await next();
    if (decision.kind === 'reject' || !this.enabled()) return decision;
    const {agent, signal} = payload;
    const direct = payload.messages.filter(m => m.role === 'user' && m.source?.kind === 'user');
    const permitted = new Set();
    const selected = [];
    for (const message of direct) {
      const body = textOf(message);
      // Only standalone slash lines at the beginning of a direct message are commands.
      const leading = body.trimStart().split(/\r?\n/);
      for (const line of leading) {
        const match = /^\/([a-z0-9]+(?:-[a-z0-9]+)*)\s*$/.exec(line.trim());
        if (!match) break;
        permitted.add(match[1]);
      }
      const marker = MARKER.exec(body);
      if (!marker) continue;
      const trial = this.service.domain.table('trials').get(marker[1]);
      if (!trial || trial.sessionId !== agent.id || !body.trimStart().startsWith(selectionMarker(trial.id))) continue;
      // A reference must be submitted together with its complete saved draft; quoting a tool response is insufficient.
      if (!body.includes(trial.prompt)) continue;
      for (const id of idsOf(trial)) { permitted.add(id); selected.push(id); }
    }
    const messages = decision.messages.filter(m => m.source?.kind !== 'skill-catalog' && (m.source?.kind !== 'skill-invocation' || permitted.has(m.source.name)));
    const present = new Set(messages.filter(m => m.source?.kind === 'skill-invocation').map(m => m.source.name));
    const cwd = selected.length ? await this.ctx.workingDirectory.ensure(agent,signal) : undefined;
    for (const id of new Set(selected)) {
      if (present.has(id)) continue;
      signal?.throwIfAborted();
      let content, resourceBase;
      if (id.startsWith('pack:')) {
        const candidate = (await this.service.catalog(agent)).find(s => s.id === id);
        if (!candidate?.available || candidate.status === 'retired') throw Error('所选技能包已不可用，请重新选择：'+id);
        content = await readFile(candidate.path,'utf8');
        resourceBase = {kind:'directory',path:candidate.path.replace(/[\\/][^\\/]+$/,'')};
      } else {
        const definition = await this.service.registry(agent).get(id,{cwd,scope:agent,signal});
        if (!definition || !(definition.invocation.userInvocable || definition.invocation.modelInvocable)) throw Error('所选技能已不可用，请重新选择：'+id);
        content = definition.content; resourceBase = definition.resourceBase;
      }
      messages.push(injection(`<skill_content name="${id}">\n${resourceBase ? '<skill_resources>\n'+JSON.stringify(resourceBase)+'\n相对参考资源从上述位置读取。\n</skill_resources>\n' : ''}<skill_instructions>\n${content}\n</skill_instructions>\n</skill_content>`, {kind:'skill-invocation',name:id,form:'instructions'}));
    }
    // Publish an empty replacement catalog, including its durable provenance, to retire earlier automatic catalogs.
    messages.push(injection(POLICY,{kind:'skill-catalog',form:'catalog',entries:[],update:true}));
    return {...decision,messages};
  }
}
