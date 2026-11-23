const http = require('http');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const statePath = path.join(root, 'state.json');
const port = Number(process.env.PORT || 17321);

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

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

function readJson() {
  return JSON.parse(fs.readFileSync(statePath, 'utf8'));
}

function writeJson(data) {
  data.meta = data.meta || {};
  data.meta.updatedAt = isoNow();
  fs.writeFileSync(statePath, JSON.stringify(data, null, 2), 'utf8');
}

function send(res, code, body, type = 'application/json; charset=utf-8') {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(body);
}

function collect(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', c => data += c);
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

function addEvent(state, type, text) {
  state.events = state.events || [];
  state.events.push({ time: nowHHMM(), type, text });
  if (state.events.length > 60) state.events = state.events.slice(-60);
}

function getWatchdog(state) {
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

function findThread(state, id) {
  return (state.threads || []).find(t =>
    t.id === id ||
    t.title === id ||
    t.threadId === id ||
    t.role === id
  );
}

function findStepForThread(state, thread) {
  if (!thread) return null;
  return (state.steps || []).find(s =>
    s.id === thread.location ||
    s.thread === thread.title ||
    s.thread === thread.role
  );
}

function ensureRuntime(state) {
  const watchdog = getWatchdog(state);
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

function heartbeatAgeSeconds(thread, now = Date.now()) {
  const last = parseTime(thread.lastHeartbeatAt);
  if (!last) return null;
  return Math.max(0, Math.floor((now - last) / 1000));
}

function syncStepFromThread(state, thread, statusOverride) {
  const step = findStepForThread(state, thread);
  if (!step) return;
  const nextStatus = statusOverride || thread.status;
  if (nextStatus === 'fallback') {
    step.status = 'fallback';
    step.progress = Math.max(Number(step.progress || 0), Number(thread.progress || 0), 85);
    step.note = thread.current || `${thread.role || thread.title} 已由主控兜底`;
    return;
  }
  if (nextStatus === 'confirm' || nextStatus === 'blocked') {
    step.status = nextStatus;
    step.progress = Math.max(Number(step.progress || 0), Number(thread.progress || 0));
    step.note = thread.current || `${thread.role || thread.title} ${statusLabel(nextStatus)}`;
    return;
  }
  if (nextStatus === 'running' || nextStatus === 'building') {
    step.status = 'running';
    step.progress = Number(thread.progress || step.progress || 0);
    step.note = thread.current || step.note || `${thread.role || thread.title} 正在处理`;
    return;
  }
  if (nextStatus === 'done') {
    step.status = 'done';
    step.progress = 100;
    step.note = thread.current || step.note || `${thread.role || thread.title} 已完成`;
  }
}

function heartbeat(state, id, patch = {}) {
  ensureRuntime(state);
  state.meta = state.meta || {};
  state.meta.runStatus = 'running';
  const thread = findThread(state, id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  const watchdog = getWatchdog(state);
  const timeoutSeconds = Number(patch.timeoutSeconds ?? thread.timeoutSeconds ?? watchdog.timeoutSeconds ?? 90);
  Object.assign(thread, {
    status: patch.status || 'running',
    progress: patch.progress == null ? Number(thread.progress || 0) : Number(patch.progress),
    current: patch.current || patch.note || thread.current || '线程心跳正常',
    timeoutSeconds,
    lastHeartbeatAt: isoNow(),
    deadlineAt: new Date(Date.now() + timeoutSeconds * 1000).toISOString(),
    timedOut: false,
    timeoutReason: ''
  });
  if (patch.location) thread.location = patch.location;
  syncStepFromThread(state, thread);
  addEvent(state, 'running', `${thread.role || thread.title} 心跳：${thread.current}`);
  recompute(state);
  return thread;
}

function retryThread(state, id, note = '') {
  ensureRuntime(state);
  state.meta = state.meta || {};
  state.meta.runStatus = 'running';
  const thread = findThread(state, id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  const timeoutSeconds = Number(thread.timeoutSeconds || getWatchdog(state).timeoutSeconds || 90);
  thread.retryCount = Number(thread.retryCount || 0) + 1;
  thread.status = 'running';
  thread.current = note || `第 ${thread.retryCount} 次重试窗口已开启，等待线程重新回报`;
  thread.lastHeartbeatAt = isoNow();
  thread.deadlineAt = new Date(Date.now() + timeoutSeconds * 1000).toISOString();
  thread.timedOut = false;
  thread.timeoutReason = '';
  syncStepFromThread(state, thread, 'running');
  addEvent(state, 'running', `${thread.role || thread.title} 进入第 ${thread.retryCount} 次重试窗口`);
  recompute(state);
  return thread;
}

function fallbackThread(state, id, note = '') {
  ensureRuntime(state);
  const thread = findThread(state, id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  thread.status = 'fallback';
  thread.progress = Math.max(Number(thread.progress || 0), 90);
  thread.current = note || '线程超时，主控已启用兜底结论';
  thread.fallbackAt = isoNow();
  thread.timedOut = true;
  syncStepFromThread(state, thread, 'fallback');
  addEvent(state, 'confirm', `${thread.role || thread.title} 已启用主控兜底`);
  recompute(state);
  return thread;
}

function applyWatchdog(state, { writeEvents = true } = {}) {
  ensureRuntime(state);
  const watchdog = getWatchdog(state);
  if (!watchdog.enabled) return [];
  const now = Date.now();
  const changes = [];

  for (const thread of state.threads || []) {
    const age = heartbeatAgeSeconds(thread, now);
    thread.heartbeatAgeSeconds = age;
    thread.heartbeatLabel = ['done', 'ready'].includes(thread.status)
      ? '已完成'
      : (age == null ? '无心跳' : `${age}s 前`);

    if (!WATCHED_STATUSES.has(thread.status)) continue;

    const timeoutSeconds = Number(thread.timeoutSeconds || watchdog.timeoutSeconds || 90);
    if (age == null || age <= timeoutSeconds) continue;

    const maxRetries = Number(thread.maxRetries ?? watchdog.retryLimit ?? 1);
    thread.timedOut = true;
    thread.timeoutReason = `${age}s 未收到心跳，超过 ${timeoutSeconds}s 阈值`;

    if (Number(thread.retryCount || 0) < maxRetries) {
      thread.status = 'confirm';
      thread.current = `${thread.timeoutReason}；等待主控重试`;
      syncStepFromThread(state, thread, 'confirm');
      changes.push({ id: thread.id, status: 'confirm', action: 'retry-needed' });
      if (writeEvents) addEvent(state, 'confirm', `${thread.role || thread.title} 心跳超时，等待重试`);
    } else if (watchdog.fallbackOnFinalTimeout) {
      thread.status = 'fallback';
      thread.progress = Math.max(Number(thread.progress || 0), 90);
      thread.current = `${thread.timeoutReason}；已触发主控兜底`;
      thread.fallbackAt = isoNow();
      syncStepFromThread(state, thread, 'fallback');
      changes.push({ id: thread.id, status: 'fallback', action: 'fallback' });
      if (writeEvents) addEvent(state, 'confirm', `${thread.role || thread.title} 重试后仍超时，主控兜底`);
    } else {
      thread.status = 'blocked';
      thread.current = `${thread.timeoutReason}；已阻塞`;
      syncStepFromThread(state, thread, 'blocked');
      changes.push({ id: thread.id, status: 'blocked', action: 'blocked' });
      if (writeEvents) addEvent(state, 'blocked', `${thread.role || thread.title} 心跳超时并阻塞`);
    }
  }
  recompute(state);
  return changes;
}

function recompute(state) {
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
  const blocked = (state.threads || []).filter(t => ['blocked', 'confirm', 'fallback'].includes(t.status));

  state.summary = state.summary || {};
  state.summary.progress = total;
  state.summary.etaMinutes = eta;
  state.summary.currentPhase = active ? active.label : (state.summary.currentPhase || '最终交付');
  state.summary.status = active ? (active.status === 'waiting' ? 'running' : active.status) : 'done';
  state.meta = state.meta || {};
  if (active) state.meta.runStatus = 'running';
  if (blocked.length) {
    state.summary.heartbeat = `看门狗：${blocked.map(t => `${t.role || t.title}${statusLabel(t.status)}`).join('、')}；主控可重试或兜底`;
  } else {
    state.summary.heartbeat = active
      ? `${active.thread || '主控线程'}：${active.note || statusLabel(active.status)}`
      : (state.summary.heartbeat || '所有步骤已完成，等待主控线程汇报最终结果');
  }
}

function startRun(state, body = {}) {
  const runId = `run-${Date.now()}`;
  state.meta = state.meta || {};
  state.meta.runId = runId;
  state.meta.runStatus = 'running';
  state.meta.taskTitle = body.taskTitle || body.title || state.meta.taskTitle || '新任务';
  state.meta.subtitle = body.subtitle || state.meta.subtitle || '主控线程正在派发任务';
  delete state.finalConclusion;

  const firstStepId = body.firstStepId || 'brief';
  for (const step of state.steps || []) {
    if (step.id === firstStepId) {
      step.status = 'running';
      step.progress = Number(body.progress ?? 8);
      step.note = body.note || '新任务已开跑，正在同步子线程';
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
    thread.deadlineAt = new Date(Date.now() + Number(thread.timeoutSeconds || getWatchdog(state).timeoutSeconds || 300) * 1000).toISOString();
    thread.heartbeatLabel = '刚刚';
  }

  state.summary = {
    status: 'running',
    progress: Number(body.progress ?? 8),
    etaMinutes: Number(body.etaMinutes ?? 8),
    currentPhase: body.phase || '任务启动',
    heartbeat: body.heartbeat || '新任务已启动，通关页已收起，地图正在更新。'
  };
  state.events = [];
  state.artifacts = [];
  addEvent(state, 'start', `新任务启动：${state.meta.taskTitle}`);
  return state;
}

function demoAdvance() {
  const state = readJson();
  applyWatchdog(state, { writeEvents: false });
  const order = ['brief', 'research', 'build', 'test', 'review', 'deliver'];
  const steps = state.steps || [];
  const running = steps.find(s => s.status === 'running');
  if (running) {
    running.progress = Math.min(100, Number(running.progress || 0) + 18);
    if (running.progress >= 100) {
      running.progress = 100;
      running.status = 'done';
      running.note = '本阶段已完成，结果已回传主控';
      const next = steps.find(s => s.id === order[order.indexOf(running.id) + 1]);
      if (next) {
        next.status = 'running';
        next.progress = Math.max(8, Number(next.progress || 0));
        next.note = `${next.thread || '子线程'}正在接手处理`;
      }
      addEvent(state, 'done', `${running.label} 完成`);
      if (next) addEvent(state, 'running', `${next.label} 开始`);
    } else {
      addEvent(state, 'running', `${running.label} 推进到 ${running.progress}%`);
    }
  }
  recompute(state);
  writeJson(state);
  return state;
}

function forceStale(state, id, seconds = 999) {
  ensureRuntime(state);
  const thread = findThread(state, id);
  if (!thread) throw new Error(`找不到线程：${id}`);
  const then = new Date(Date.now() - Number(seconds) * 1000).toISOString();
  thread.lastHeartbeatAt = then;
  thread.deadlineAt = new Date(Date.now() - 1000).toISOString();
  thread.status = thread.status === 'done' ? 'running' : (thread.status || 'running');
  thread.current = thread.current || '模拟心跳变旧';
  addEvent(state, 'waiting', `${thread.role || thread.title} 被设为旧心跳，用于测试看门狗`);
  recompute(state);
  return thread;
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://localhost:${port}`);

    if (req.method === 'GET' && (url.pathname === '/api/status' || url.pathname === '/api/state')) {
      const state = readJson();
      const changes = applyWatchdog(state, { writeEvents: true });
      if (changes.length) writeJson(state);
      return send(res, 200, JSON.stringify(state));
    }
    if (req.method === 'GET' && url.pathname === '/api/health') {
      return send(res, 200, JSON.stringify({ ok: true, port }));
    }
    if (req.method === 'POST' && (url.pathname === '/api/status' || url.pathname === '/api/state')) {
      const body = await collect(req);
      const state = JSON.parse(body || '{}');
      applyWatchdog(state, { writeEvents: false });
      writeJson(state);
      return send(res, 200, JSON.stringify({ ok: true }));
    }
    if (req.method === 'POST' && url.pathname === '/api/start-run') {
      const body = JSON.parse(await collect(req) || '{}');
      const state = readJson();
      startRun(state, body);
      writeJson(state);
      return send(res, 200, JSON.stringify({ ok: true, state }));
    }
    if (req.method === 'POST' && url.pathname === '/api/heartbeat') {
      const body = JSON.parse(await collect(req) || '{}');
      const state = readJson();
      const thread = heartbeat(state, body.id || body.threadId || body.role, body);
      writeJson(state);
      return send(res, 200, JSON.stringify({ ok: true, thread, state }));
    }
    if (req.method === 'POST' && url.pathname === '/api/retry-thread') {
      const body = JSON.parse(await collect(req) || '{}');
      const state = readJson();
      const thread = retryThread(state, body.id || body.threadId || body.role, body.note);
      writeJson(state);
      return send(res, 200, JSON.stringify({ ok: true, thread, state }));
    }
    if (req.method === 'POST' && url.pathname === '/api/fallback-thread') {
      const body = JSON.parse(await collect(req) || '{}');
      const state = readJson();
      const thread = fallbackThread(state, body.id || body.threadId || body.role, body.note);
      writeJson(state);
      return send(res, 200, JSON.stringify({ ok: true, thread, state }));
    }
    if (req.method === 'POST' && url.pathname === '/api/watchdog') {
      const state = readJson();
      const changes = applyWatchdog(state, { writeEvents: true });
      writeJson(state);
      return send(res, 200, JSON.stringify({ ok: true, changes, state }));
    }
    if (req.method === 'POST' && url.pathname === '/api/demo-timeout') {
      const body = JSON.parse(await collect(req) || '{}');
      const state = readJson();
      forceStale(state, body.id || 't-style', body.seconds || 999);
      const changes = applyWatchdog(state, { writeEvents: true });
      writeJson(state);
      return send(res, 200, JSON.stringify({ ok: true, changes, state }));
    }
    if (req.method === 'POST' && url.pathname === '/api/demo-advance') {
      return send(res, 200, JSON.stringify(demoAdvance()));
    }

    const safePath = decodeURIComponent(url.pathname);
    let filePath = safePath === '/' ? path.join(root, 'index.html') : path.join(root, safePath);
    filePath = path.resolve(filePath);
    if (!filePath.startsWith(root)) return send(res, 403, 'Forbidden', 'text/plain; charset=utf-8');
    fs.readFile(filePath, (err, data) => {
      if (err) return send(res, 404, 'Not found', 'text/plain; charset=utf-8');
      send(res, 200, data, mime[path.extname(filePath).toLowerCase()] || 'application/octet-stream');
    });
  } catch (err) {
    send(res, 500, JSON.stringify({ ok: false, error: String(err.message || err) }));
  }
});

server.listen(port, '127.0.0.1', () => {
  console.log(`Thread Quest Board: http://127.0.0.1:${port}`);
});
