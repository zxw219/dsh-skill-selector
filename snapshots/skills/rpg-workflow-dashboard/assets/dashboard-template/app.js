const statusLabel = {
  ready: '已就绪', building: '生成中',
  done: '已完成', running: '运行中', waiting: '等待中',
  locked: '未解锁', blocked: '阻塞', confirm: '需重试', fallback: '已兜底', abandoned: '废弃'
};
const statusClass = s => `status-${s || 'waiting'}`;
const clamp = n => Math.max(0, Math.min(100, Number(n || 0)));
const fmtEta = m => Number(m || 0) <= 0 ? '≈ 00 分钟' : `≈ ${String(Math.ceil(m)).padStart(2, '0')} 分钟`;
const esc = v => String(v ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));

function badge(status) {
  const label = statusLabel[status] || status || '等待中';
  if (status === 'waiting') {
    return `<span class="status-badge ${statusClass(status)}">${label} <span class="dots"><span></span><span></span><span></span></span></span>`;
  }
  return `<span class="status-badge ${statusClass(status)}">${label}</span>`;
}

function sprite(status) {
  if (status === 'done' || status === 'ready') return '<div class="pixel-flag"></div>';
  if (status === 'running' || status === 'building') return '<div class="robot"><i class="antenna"></i><i class="hammer"></i></div>';
  if (status === 'locked') return '<div class="lock-chest"></div>';
  if (status === 'blocked') return '<div class="lock-chest" style="border-color:#ff6b93"></div>';
  return '<div class="sleep-z"><span>Z</span><span>Z</span><span>Z</span></div>';
}

function partySprite(thread) {
  const avatar = thread.avatar || 'scout';
  const status = thread.status || 'waiting';
  return `<img class="party-avatar generated-sprite ${avatar} ${status}" src="./assets/characters/${avatar}.png" alt="${thread.role || thread.title || ''}" title="${thread.title || ''} · ${thread.skill || ''}" />`;
}

function mapIcon(status) {
  if (status === 'done') return '<div class="map-icon done">✓</div>';
  if (status === 'running') return '<div class="map-icon running">★</div>';
  if (status === 'confirm') return '<div class="map-icon confirm">↻</div>';
  if (status === 'fallback') return '<div class="map-icon fallback">↯</div>';
  if (status === 'locked') return '<div class="map-icon locked">▣</div>';
  if (status === 'blocked') return '<div class="map-icon blocked">!</div>';
  return '<div class="map-icon waiting">…</div>';
}

async function loadState() {
  try {
    const res = await fetch('/api/status?ts=' + Date.now(), { cache: 'no-store' });
    if (!res.ok) throw new Error('api unavailable');
    return await res.json();
  } catch {
    const res = await fetch('./state.json?ts=' + Date.now(), { cache: 'no-store' });
    return await res.json();
  }
}

function applyThemeAndLabels(state) {
  const meta = state.meta || {};
  const theme = meta.theme || {};
  Object.entries(theme).forEach(([key, value]) => {
    if (!/^[a-z0-9-]+$/i.test(key)) return;
    if (typeof value !== 'string') return;
    document.documentElement.style.setProperty(`--${key}`, value);
  });

  const labels = meta.labels || {};
  const set = (selector, value) => {
    if (!value) return;
    const el = document.querySelector(selector);
    if (el) el.textContent = value;
  };
  set('.progress-card .metric-label', labels.progress);
  set('.phase-card .metric-label', labels.phase);
  set('.eta-card .metric-label', labels.eta);
  set('.quest-panel .eyebrow', labels.mapEyebrow);
  set('.quest-panel h2', labels.mapTitle);
  set('.narration-panel .eyebrow', labels.narrationEyebrow);
  set('.narration-panel h2', labels.narrationTitle);
  set('.thread-panel .eyebrow', labels.partyEyebrow);
  set('.thread-panel h2', labels.partyTitle);
  set('.log-panel .eyebrow', labels.logEyebrow);
  set('.log-panel h2', labels.logTitle);
  set('.artifact-panel .eyebrow', labels.artifactEyebrow);
  set('.artifact-panel h2', labels.artifactTitle);
  set('.clear-ribbon', labels.clearRibbon);
  set('.clear-kicker', labels.clearKicker);
  set('.clear-next', labels.clearNext);
}

function renderSummary(state) {
  const meta = state.meta || {};
  const summary = state.summary || {};
  const subtitleEl = document.getElementById('taskSubtitle');
  if (subtitleEl) subtitleEl.textContent = `${meta.taskTitle || '未命名任务'} · ${meta.subtitle || meta.mode || ''}`;
  document.getElementById('totalProgress').textContent = `${clamp(summary.progress)}%`;
  document.getElementById('totalProgressBar').style.width = `${clamp(summary.progress)}%`;
  document.getElementById('eta').textContent = fmtEta(summary.etaMinutes);
  document.getElementById('currentPhase').textContent = summary.currentPhase || '等待任务';
  document.getElementById('currentStatus').textContent = statusLabel[summary.status] || summary.status || '等待中';
  document.getElementById('heartbeat').textContent = summary.heartbeat || '等待主控线程更新状态';
  const updated = meta.updatedAt ? new Date(meta.updatedAt) : new Date();
  document.getElementById('syncTime').textContent = `最后同步：${updated.toLocaleTimeString('zh-CN', { hour12: false })}`;
}

function renderQuest(state) {
  const steps = state.steps || [];
  const threads = state.threads || [];
  const road = `
    <svg class="map-road" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <path class="road-shadow" d="M 10 30 H 50 H 86 V 70 H 50 H 10" />
      <path class="road-line" d="M 10 30 H 50 H 86 V 70 H 50 H 10" />
    </svg>`;
  document.getElementById('questPath').innerHTML = road + steps.map((step, idx) => `
    <article class="quest-node ${step.status || 'waiting'}">
      <div class="map-tile">
        <span class="node-index">${String(idx + 1).padStart(2, '0')}</span>
        ${mapIcon(step.status)}
        <div class="party-stack">
          ${threads.filter(t => (t.location === step.id || t.title === step.thread) && ['running','blocked','confirm','fallback'].includes(t.status)).map(t => partySprite(t)).join('')}
        </div>
      </div>
      <div class="node-label">${step.label}</div>
      <div class="node-note">${step.status === 'running' ? '当前片场' : (step.status === 'done' ? '已点亮' : step.status === 'fallback' ? '主控兜底' : step.status === 'confirm' ? '待重试' : step.status === 'locked' ? '未解锁' : '候场')}</div>
    </article>
  `).join('');

  const active = steps.find(s => s.status === 'blocked')
    || steps.find(s => s.status === 'confirm')
    || steps.find(s => s.status === 'running')
    || steps.find(s => s.status === 'waiting')
    || steps.find(s => s.status === 'fallback')
    || steps[steps.length - 1];
  const detail = document.getElementById('activeDetail');
  if (!active) { detail.innerHTML = ''; return; }
  detail.innerHTML = `
    <div class="big-sprite">${sprite(active.status)}</div>
    <div>
      <h3>当前焦点：${active.label || '等待任务'} · ${statusLabel[active.status] || active.status}</h3>
      <p>${active.note || '等待主控线程写入下一步。'}<br>负责：${active.thread || '主控线程'} · 进度 ${clamp(active.progress)}% · 预估 ${active.estimateMinutes || 0} 分钟</p>
      <div class="pixel-progress"><i style="width:${clamp(active.progress)}%"></i></div>
    </div>
  `;
}

function renderThreads(state) {
  document.getElementById('threadList').innerHTML = (state.threads || []).map(t => `
    <article class="thread-card ${t.status || 'waiting'}">
      <div class="avatar">${partySprite(t)}</div>
      <div>
        <div class="thread-title"><strong>${t.role || t.title}</strong>${badge(t.status)}</div>
        <div class="thread-meta"><b>${shortSkill(t)}</b><br><span>${t.current || ''}</span></div>
        <div class="thread-watch">${threadWatch(t)}</div>
        <div class="thread-mini">
          <div class="pixel-progress"><i style="width:${clamp(t.progress)}%"></i></div>
          <span class="mono">${clamp(t.progress)}%</span>
        </div>
      </div>
    </article>
  `).join('');
}

function threadWatch(thread) {
  const heartbeat = thread.heartbeatLabel
    || (thread.lastHeartbeatAt ? `${Math.max(0, Math.floor((Date.now() - new Date(thread.lastHeartbeatAt).getTime()) / 1000))}s 前` : '未记录');
  const retry = `${Number(thread.retryCount || 0)}/${Number(thread.maxRetries ?? 1)}`;
  if (thread.status === 'fallback') return `心跳 ${heartbeat} · 已兜底`;
  if (thread.status === 'confirm') return `心跳 ${heartbeat} · 等待重试 ${retry}`;
  if (thread.status === 'blocked') return `心跳 ${heartbeat} · 已阻塞`;
  return `心跳 ${heartbeat} · 重试 ${retry}`;
}

function shortSkill(thread) {
  const id = thread.id || thread.title || '';
  if (id.includes('reference') || thread.role === '参考猎人') return 'Skill：参考猎取';
  if (id.includes('style') || thread.role === '视觉炼金师') return 'Skill：视觉母版';
  if (id.includes('shot') || thread.role === '镜头工匠') return 'Skill：镜头语言';
  if (id.includes('review') || thread.role === '审片骑士') return 'Skill：审片迭代';
  return thread.skill || 'Skill：未指定';
}

function makeNarration(state) {
  const summary = state.summary || {};
  const steps = state.steps || [];
  const threads = state.threads || [];
  const active = steps.find(s => s.status === 'blocked')
    || steps.find(s => s.status === 'confirm')
    || steps.find(s => s.status === 'running')
    || steps.find(s => s.status === 'waiting')
    || steps.find(s => s.status === 'fallback')
    || steps[steps.length - 1]
    || {};
  const waiting = threads.filter(t => t.status === 'waiting').length;
  const done = steps.filter(s => s.status === 'done').length;
  const total = steps.length || 1;
  const phase = active.label || summary.currentPhase || '未知阶段';
  const progress = clamp(summary.progress);

  if (active.status === 'blocked') {
    const blocked = threads.filter(t => t.status === 'blocked').map(t => t.role || t.title).join('、');
    return {
      title: '片场遭遇卡壳怪',
      text: `旁白：剧组在【${phase}】地块前停机。不是演员忘词，是${blocked || '某个后台角色'}被“超时史莱姆”抱住了脚踝。`,
      tip: '主控已兜底跑完本轮；下一步要处理后台线程回报超时。'
    };
  }
  if (active.status === 'confirm') {
    const waitingRetry = threads.filter(t => t.status === 'confirm').map(t => t.role || t.title).join('、');
    return {
      title: '看门狗叼来重试铃',
      text: `旁白：${waitingRetry || '某个后台角色'}的心跳钟停了一下。现在不是杀青，是该敲第二次场记板，让它重跑这一小段。`,
      tip: '主控可选择重试；若重试后仍超时，会自动进入兜底。'
    };
  }
  if (active.status === 'fallback') {
    const fallback = threads.filter(t => t.status === 'fallback').map(t => t.role || t.title).join('、');
    return {
      title: '主控兜底上场',
      text: `旁白：${fallback || '后台角色'}没能及时回报，主控导演披上雨衣亲自补位。片场不停机，先用临时结论继续往后走。`,
      tip: '后续可替换为子线程正式产物；当前流程不会被卡死。'
    };
  }
  if (progress >= 100 || !steps.some(s => s.status !== 'done' && s.status !== 'abandoned')) {
    return {
      title: '杀青宝箱开启',
      text: '旁白：片场六个地块全部点亮，杀青宝箱吱呀打开。主控把提示词、审片药方、发布文案和案例沉淀塞进片单。',
      tip: '下一步：主线程汇报最终结论。'
    };
  }
  if (active.status === 'running') {
    const worker = threads.find(t => t.status === 'running') || {};
    return {
      title: `${worker.role || '队友'}正在干活`,
      text: `旁白：${worker.role || '当前队友'}抵达【${phase}】。这一关只干一件事：${shortSkill(worker).replace('Skill：','')}。其余 ${waiting} 名角色在候场区等 Action。`,
      tip: `通关进度：${done}/${total}；预计还要 ${fmtEta(summary.etaMinutes).replace('≈ ', '')}。`
    };
  }
  const fallbackThreads = threads.filter(t => t.status === 'fallback');
  if (fallbackThreads.length && active.status === 'waiting') {
    return {
      title: '兜底队背着临时稿赶路',
      text: `旁白：${fallbackThreads.map(t => t.role || t.title).join('、')}已经由主控临时补位。现在队伍没有原地罚站，而是继续往【${phase}】走，等正式稿回来再替换。`,
      tip: `当前总进度 ${progress}%，ETA ${fmtEta(summary.etaMinutes)}。`
    };
  }
  return {
    title: '候场区待命',
    text: `旁白：下一站是【${phase}】。技能小队没有摸鱼，只是导演还没喊 Action，轨道、灯、药水和小板凳都备好了。`,
    tip: `当前总进度 ${progress}%，ETA ${fmtEta(summary.etaMinutes)}。`
  };
}

function renderNarration(state) {
  const el = document.getElementById('narrationBox');
  if (!el) return;
  const n = makeNarration(state);
  el.innerHTML = `
    <div class="narrator-tag">旁白</div>
    <strong>${n.title}</strong>
    <div class="rpg-dialogue">
      <p>${n.text}</p>
    </div>
    <div class="narration-tip">${n.tip}</div>
  `;
}

function renderEvents(state) {
  const events = (state.events || []).slice(-8).reverse();
  document.getElementById('eventLog').innerHTML = events.map(e => `
    <div class="event-row ${e.type || 'start'}">
      <time>${e.time || '--:--'}</time>
      <span class="event-icon">${e.type === 'done' ? '✓' : e.type === 'running' ? '▶' : e.type === 'waiting' ? '…' : e.type === 'blocked' ? '!' : '◆'}</span>
      <span>${e.text || ''}</span>
    </div>
  `).join('');
}

function renderArtifacts(state) {
  document.getElementById('artifactList').innerHTML = (state.artifacts || []).map(a => `
    <article class="artifact">
      <strong>${a.label || '产物'}</strong>
      <span>${statusLabel[a.status] || a.status || '等待中'} · ${a.path || ''}</span>
    </article>
  `).join('');
}

function isWorkflowClear(state) {
  const meta = state.meta || {};
  const summary = state.summary || {};
  const steps = state.steps || [];
  const threads = state.threads || [];
  const conclusion = state.finalConclusion;
  const runStatus = meta.runStatus || summary.status;
  if (!conclusion) return false;
  if (!['done', 'complete', 'clear'].includes(runStatus)) return false;
  if (summary.status !== 'done') return false;
  if (meta.runId && conclusion.runId !== meta.runId) return false;
  const stepClear = steps.length > 0 && steps.every(s => ['done', 'fallback', 'abandoned'].includes(s.status));
  const threadClear = threads.length === 0 || threads.every(t => ['done', 'ready', 'fallback', 'abandoned'].includes(t.status));
  return stepClear && threadClear;
}

function fallbackConclusion(state) {
  const meta = state.meta || {};
  const threads = state.threads || [];
  const avg = threads.length
    ? Math.round(threads.reduce((n, t) => n + Number(t.durationMs || 0), 0) / threads.length / 1000)
    : 0;
  return {
    title: '副本通关：影视多线程任务完成',
    subtitle: meta.subtitle || meta.taskTitle || '所有线程已完成，最终结论已汇总。',
    verdict: '可以进入下一轮。按子线程结论推进，不需要再回头翻流程。',
    stats: [
      { label: '总进度', value: `${clamp(state.summary?.progress)}%` },
      { label: '线程完成', value: `${threads.filter(t => ['done','ready'].includes(t.status)).length}/${threads.length || 0}` },
      { label: '平均耗时', value: avg ? `${avg} 秒` : '已完成' },
      { label: '看门狗', value: `${state.meta?.watchdog?.timeoutSeconds || 300} 秒` }
    ],
    sections: [
      { title: '核心结论', text: state.summary?.heartbeat || '所有步骤已完成。' },
      { title: '交付物', items: (state.artifacts || []).slice(0, 5).map(a => `${a.label}：${a.path}`) }
    ]
  };
}

function renderClearOverlay(state) {
  const overlay = document.getElementById('clearOverlay');
  if (!overlay) return;
  const clear = isWorkflowClear(state);
  overlay.hidden = !clear;
  document.body.classList.toggle('is-clear', clear);
  if (!clear) return;

  const data = state.finalConclusion || fallbackConclusion(state);
  const stats = data.stats || fallbackConclusion(state).stats;
  const sections = data.sections || [];
  const threads = state.threads || [];

  document.getElementById('clearTitle').textContent = data.title || '副本通关';
  document.getElementById('clearSubtitle').textContent = data.subtitle || '所有线程已完成。';
  document.getElementById('clearVerdict').textContent = data.verdict || '可以进入下一轮。';
  document.getElementById('clearStats').innerHTML = stats.map(s => `
    <div class="clear-stat">
      <span>${esc(s.label)}</span>
      <strong>${esc(s.value)}</strong>
    </div>
  `).join('');
  document.getElementById('clearSections').innerHTML = sections.map(section => `
    <article class="clear-card">
      <h3>${esc(section.title)}</h3>
      ${section.text ? `<p>${esc(section.text)}</p>` : ''}
      ${section.items ? `<ul>${section.items.map(item => `<li>${esc(item)}</li>`).join('')}</ul>` : ''}
    </article>
  `).join('');
  document.getElementById('clearParty').innerHTML = threads.map(t => `
    <div class="clear-member">
      ${partySprite(t)}
      <span>${esc(t.role || t.title)}</span>
    </div>
  `).join('');
}

function render(state) {
  applyThemeAndLabels(state);
  renderSummary(state);
  renderQuest(state);
  renderNarration(state);
  renderThreads(state);
  renderEvents(state);
  renderArtifacts(state);
  renderClearOverlay(state);
}

async function tick() {
  const state = await loadState();
  render(state);
}

async function demoAdvance() {
  try {
    const res = await fetch('/api/demo-advance', { method: 'POST' });
    if (!res.ok) throw new Error('demo unavailable');
    await tick();
  } catch {
    const btn = document.getElementById('demoBtn');
    if (!btn) return;
    btn.textContent = '需启动服务';
    setTimeout(() => btn.textContent = '演示推进', 1200);
  }
}

const demoBtn = document.getElementById('demoBtn');
if (demoBtn) demoBtn.addEventListener('click', demoAdvance);
tick();
setInterval(tick, 1500);
