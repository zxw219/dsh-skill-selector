const fs = require('fs');
const path = require('path');

const statePath = path.join(__dirname, 'state.json');
const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
const [cmd, ...args] = process.argv.slice(2);

const ACTIVE_STATUSES = ['blocked', 'confirm', 'running', 'building', 'waiting', 'fallback'];
const WATCHED_STATUSES = new Set(['running', 'building']);

function isoNow() {
  return new Date().toISOString();
}

function nowHHMM() {
  return new Date().toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
}

function statusLabel(s) {
  return ({
    ready: '已就绪',
    building: '生成中',
    done: '已完成',
    running: '运行中',
    waiting: '等待中',
    locked: '未解锁',
    blocked: '阻塞',
    confirm: '需确认',
    fallback: '已兜底',
    abandoned: '废弃'
  }[s] || s || '等待中');
}

function save() {
  state.meta = state.meta || {};
  state.meta.updatedAt = isoNow();
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2), 'utf8');
}

function addEvent(type, text) {
  state.events = state.events || [];
  state.events.push({ time: nowHHMM(), type, text });
  if (state.events.length > 60) state.events = state.events.slice(-60);
}

function markRunStatus(status) {
  state.meta = state.meta || {};
  state.meta.runStatus = status;
}

function startRun({ title, subtitle, phase, note } = {}) {
  const runId = `run-${Date.now()}`;
  state.meta = state.meta || {};
  state.meta.runId = runId;
  state.meta.runStatus = 'running';
  if (title) state.meta.taskTitle = title;
  if (subtitle) state.meta.subtitle = subtitle;
  delete state.finalConclusion;

  for (const step of state.steps || []) {
    if (step.id === 'brief') {
      step.status = 'running';
      step.progress = 8;
      step.note = note || '新任务已开跑，正在同步子线程';
    } else {
      step.status = 'waiting';
      step.progress = 0;
      step.note = '等待前置步骤完成';
    }
  }

  for (const thread of state.threads || []) {
    thread.status = 'waiting';
    thread.progress = 0;
    thread.current = '候场中，等待主控派发';
    thread.retryCount = 0;
    thread.timedOut = false;
    thread.timeoutReason = '';
    thread.lastHeartbeatAt = isoNow();
    thread.deadlineAt = new Date(Date.now() + Number(thread.timeoutSeconds || getWatchdog().timeoutSeconds || 300) * 1000).toISOString();
    thread.heartbeatLabel = '刚刚';
  }

  state.summary = {
    status: 'running',
    progress: 8,
    etaMinutes: 8,
    currentPhase: phase || '任务启动',
    heartbeat: note || '新任务已启动，通关页已收起，地图正在更新。'
  };
  state.events = [];
  state.artifacts = [];
  addEvent('start', `新任务启动：${state.meta.taskTitle || '未命名任务'}`);
}

function getWatchdog() {
  state.meta = state.meta || {};
  state.meta.watchdog = {
    enabled: true,
    timeoutSeconds: 90,
    retryLimit: 1,
    fallbackOnFinalTimeout: true,
    ...(state.meta.watchdog || {})
  };
  return state.meta.watchdog;
}

function parseTime(value) {
  const n = Date.parse(value || '');
  return Number.isFinite(n) ? n : 0;
}

function findThread(id) {
  return (state.threads || []).find(t =>
    t.id === id ||
    t.title === id ||
    t.threadId === id ||
    t.role === id
  );
}

function findStepForThread(thread) {
  if (!thread) return null;
  return (state.steps || []).find(s =>
    s.id === thread.location ||
    s.thread === thread.title ||
    s.thread === thread.role
  );
}

function ensureRuntime() {
  const watchdog = getWatchdog();
  const fallbackTime = state.meta?.updatedAt || state.meta?.startedAt || isoNow();
  for (const thread of state.threads || []) {
    if (thread.retryCount == null) thread.retryCount = 0;
    if (thread.maxRetries == null) thread.maxRetries = Number(watchdog.retryLimit || 1);
    if (thread.timeoutSeconds == null) thread.timeoutSeconds = Number(watchdog.timeoutSeconds || 90);
    if (!thread.lastHeartbeatAt) thread.lastHeartbeatAt = fallbackTime;
    if (!thread.deadlineAt) {
      thread.deadlineAt = new Date(parseTime(thread.lastHeartbeatAt) + Number(thread.timeoutSeconds || 90) * 1000).toISOString();
    }
  }
}

function syncStep(thread, statusOverride) {
  const step = findStepForThread(thread);
  if (!step) return;
  const nextStatus = statusOverride || thread.status;
  if (nextStatus === 'fallback') {
    step.status = 'fallback';
    step.progress = Math.max(Number(step.progress || 0), Number(thread.progress || 0), 85);
  } else if (nextStatus === 'confirm' || nextStatus === 'blocked') {
    step.status = nextStatus;
    step.progress = Math.max(Number(step.progress || 0), Number(thread.progress || 0));
  } else if (nextStatus === 'running' || nextStatus === 'building') {
    step.status = 'running';
    step.progress = Number(thread.progress || step.progress || 0);
  } else if (nextStatus === 'done') {
    step.status = 'done';
    step.progress = 100;
  }
  step.note = thread.current || step.note || `${thread.role || thread.title}：${statusLabel(nextStatus)}`;
}

function heartbeatAgeSeconds(thread, now = Date.now()) {
  const last = parseTime(thread.lastHeartbeatAt);
  if (!last) return null;
  return Math.max(0, Math.floor((now - last) / 1000));
}

function recompute() {
  const steps = state.steps || [];
  const total = steps.length
    ? Math.round(steps.reduce((n, s) => n + (Number(s.progress) || 0), 0) / steps.length)
    : 0;
  const active = ACTIVE_STATUSES
    .map(status => steps.find(s => s.status === status))
    .find(Boolean);
  const eta = steps
    .filter(s => !['done', 'abandoned', 'fallback'].includes(s.status))
    .reduce((n, s) => {
      const est = Number(s.estimateMinutes || 0);
      const progress = Math.max(0, Math.min(100, Number(s.progress || 0)));
      return n + Math.ceil(est * (100 - progress) / 100);
    }, 0);
  const flagged = (state.threads || []).filter(t => ['blocked', 'confirm', 'fallback'].includes(t.status));

  state.summary = state.summary || {};
  state.summary.progress = total;
  state.summary.etaMinutes = eta;
  state.summary.currentPhase = active ? active.label : '最终交付';
  state.summary.status = active ? (active.status === 'waiting' ? 'running' : active.status) : 'done';
  state.summary.heartbeat = flagged.length
    ? `看门狗：${flagged.map(t => `${t.role || t.title}${statusLabel(t.status)}`).join('、')}；主控可重试或兜底`
    : (active ? `${active.thread || '主控线程'}：${active.note || statusLabel(active.status)}` : '所有步骤已完成，等待主控汇报');
}

function monitor() {
  ensureRuntime();
  const watchdog = getWatchdog();
  const now = Date.now();
  const changes = [];
  if (!watchdog.enabled) return changes;

  for (const thread of state.threads || []) {
    const age = heartbeatAgeSeconds(thread, now);
    thread.heartbeatAgeSeconds = age;
    thread.heartbeatLabel = age == null ? '无心跳' : `${age}s 前`;
    if (!WATCHED_STATUSES.has(thread.status)) continue;

    const timeoutSeconds = Number(thread.timeoutSeconds || watchdog.timeoutSeconds || 90);
    if (age == null || age <= timeoutSeconds) continue;

    const maxRetries = Number(thread.maxRetries ?? watchdog.retryLimit ?? 1);
    thread.timedOut = true;
    thread.timeoutReason = `${age}s 未收到心跳，超过 ${timeoutSeconds}s 阈值`;

    if (Number(thread.retryCount || 0) < maxRetries) {
      thread.status = 'confirm';
      thread.current = `${thread.timeoutReason}；等待主控重试`;
      syncStep(thread, 'confirm');
      addEvent('confirm', `${thread.role || thread.title} 心跳超时，等待重试`);
      changes.push(`${thread.role || thread.title}: retry-needed`);
    } else if (watchdog.fallbackOnFinalTimeout) {
      thread.status = 'fallback';
      thread.progress = Math.max(Number(thread.progress || 0), 90);
      thread.current = `${thread.timeoutReason}；已触发主控兜底`;
      thread.fallbackAt = isoNow();
      syncStep(thread, 'fallback');
      addEvent('confirm', `${thread.role || thread.title} 重试后仍超时，主控兜底`);
      changes.push(`${thread.role || thread.title}: fallback`);
    } else {
      thread.status = 'blocked';
      thread.current = `${thread.timeoutReason}；已阻塞`;
      syncStep(thread, 'blocked');
      addEvent('blocked', `${thread.role || thread.title} 心跳超时并阻塞`);
      changes.push(`${thread.role || thread.title}: blocked`);
    }
  }
  recompute();
  return changes;
}

ensureRuntime();

if (cmd === 'step') {
  const [id, status, progress = '0', ...noteParts] = args;
  const step = (state.steps || []).find(s => s.id === id);
  if (!step) throw new Error(`找不到步骤：${id}`);
  step.status = status;
  step.progress = Number(progress);
  if (noteParts.length) step.note = noteParts.join(' ');
  if (ACTIVE_STATUSES.includes(status)) markRunStatus('running');
  addEvent(status, `${step.label}：${step.note || status}`);
  recompute();
  save();
  console.log('OK');
} else if (cmd === 'thread') {
  const [id, status, progress = '0', ...currentParts] = args;
  const thread = findThread(id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  thread.status = status;
  thread.progress = Number(progress);
  if (currentParts.length) thread.current = currentParts.join(' ');
  if (ACTIVE_STATUSES.includes(status)) markRunStatus('running');
  if (['running', 'building'].includes(status)) {
    thread.lastHeartbeatAt = isoNow();
    thread.deadlineAt = new Date(Date.now() + Number(thread.timeoutSeconds || getWatchdog().timeoutSeconds) * 1000).toISOString();
    thread.timedOut = false;
  }
  syncStep(thread, status);
  addEvent(status, `${thread.title}：${thread.current || status}`);
  recompute();
  save();
  console.log('OK');
} else if (cmd === 'heartbeat') {
  const [id, progress = '', ...currentParts] = args;
  const thread = findThread(id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  markRunStatus('running');
  thread.status = 'running';
  if (progress !== '') thread.progress = Number(progress);
  if (currentParts.length) thread.current = currentParts.join(' ');
  thread.lastHeartbeatAt = isoNow();
  thread.deadlineAt = new Date(Date.now() + Number(thread.timeoutSeconds || getWatchdog().timeoutSeconds) * 1000).toISOString();
  thread.timedOut = false;
  thread.timeoutReason = '';
  syncStep(thread, 'running');
  addEvent('running', `${thread.role || thread.title} 心跳：${thread.current || '正常'}`);
  recompute();
  save();
  console.log('OK heartbeat');
} else if (cmd === 'retry') {
  const [id, ...noteParts] = args;
  const thread = findThread(id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  markRunStatus('running');
  thread.retryCount = Number(thread.retryCount || 0) + 1;
  thread.status = 'running';
  thread.current = noteParts.join(' ') || `第 ${thread.retryCount} 次重试窗口已开启，等待线程重新回报`;
  thread.lastHeartbeatAt = isoNow();
  thread.deadlineAt = new Date(Date.now() + Number(thread.timeoutSeconds || getWatchdog().timeoutSeconds) * 1000).toISOString();
  thread.timedOut = false;
  thread.timeoutReason = '';
  syncStep(thread, 'running');
  addEvent('running', `${thread.role || thread.title} 进入第 ${thread.retryCount} 次重试窗口`);
  recompute();
  save();
  console.log('OK retry');
} else if (cmd === 'fallback') {
  const [id, ...noteParts] = args;
  const thread = findThread(id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  thread.status = 'fallback';
  thread.progress = Math.max(Number(thread.progress || 0), 90);
  thread.current = noteParts.join(' ') || '线程超时，主控已启用兜底结论';
  thread.fallbackAt = isoNow();
  thread.timedOut = true;
  syncStep(thread, 'fallback');
  addEvent('confirm', `${thread.role || thread.title} 已启用主控兜底`);
  recompute();
  save();
  console.log('OK fallback');
} else if (cmd === 'stale') {
  const [id, seconds = '999'] = args;
  const thread = findThread(id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  thread.status = ['done', 'fallback'].includes(thread.status) ? 'running' : (thread.status || 'running');
  thread.lastHeartbeatAt = new Date(Date.now() - Number(seconds) * 1000).toISOString();
  thread.deadlineAt = new Date(Date.now() - 1000).toISOString();
  addEvent('waiting', `${thread.role || thread.title} 被设为旧心跳，用于测试看门狗`);
  recompute();
  save();
  console.log('OK stale');
} else if (cmd === 'watchdog' || cmd === 'monitor') {
  const changes = monitor();
  save();
  console.log(changes.length ? changes.join('\n') : 'OK no-change');
} else if (cmd === 'event') {
  const [type = 'start', ...textParts] = args;
  addEvent(type, textParts.join(' '));
  save();
  console.log('OK');
} else if (cmd === 'start-run' || cmd === 'start') {
  const [title = '新任务', subtitle = '主控线程正在派发任务'] = args;
  startRun({ title, subtitle });
  save();
  console.log(`OK start-run ${state.meta.runId}`);
} else {
  console.log(`用法：
  node dashboardctl.js start-run <任务标题> <副标题>
  node dashboardctl.js step <stepId> <done|running|waiting|blocked|confirm|fallback|locked> <progress> <说明>
  node dashboardctl.js thread <threadId或标题> <状态> <progress> <说明>
  node dashboardctl.js heartbeat <threadId或标题> <progress> <说明>
  node dashboardctl.js retry <threadId或标题> <说明>
  node dashboardctl.js fallback <threadId或标题> <兜底说明>
  node dashboardctl.js stale <threadId或标题> <多少秒前>
  node dashboardctl.js watchdog
  node dashboardctl.js event <类型> <说明>

示例：
  node dashboardctl.js start-run 白发剑姬提示词实测 15秒图生视频
  node dashboardctl.js heartbeat t-style 45 正在锁定材质光影
  node dashboardctl.js stale t-style 999
  node dashboardctl.js watchdog
  node dashboardctl.js retry t-style 重新发起视觉母版请求
  node dashboardctl.js fallback t-review 主控已生成预审药方`);
}
