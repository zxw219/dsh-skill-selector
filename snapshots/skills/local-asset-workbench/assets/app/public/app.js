const state = {
  projectRoot: "",
  configEnabled: true,
  projects: [],
  selectedProject: "",
  cases: [],
  selectedCase: "",
  assets: [],
  selectedAsset: null,
  movingAsset: null,
  categoryFilter: "",
  statusFilter: "",
  typeFilter: "",
  query: "",
  sort: "newest",
  compactReverse: true,
  automation: null,
  generationTickets: [],
  autoRefreshTimer: null,
  deferredRefresh: null,
  caseGroupOpen: {},
  draggedProjectId: "",
  suppressProjectClick: false
};

const els = {
  sidebar: document.querySelector(".sidebar"),
  sidebarLayout: document.querySelector("#sidebarLayout"),
  projectList: document.querySelector("#projectList"),
  projectNameInput: document.querySelector("#projectNameInput"),
  projectPathInput: document.querySelector("#projectPathInput"),
  projectScanRootsInput: document.querySelector("#projectScanRootsInput"),
  addProjectButton: document.querySelector("#addProjectButton"),
  caseList: document.querySelector("#caseList"),
  categoryFilters: document.querySelector("#categoryFilters"),
  statusFilters: document.querySelector("#statusFilters"),
  typeFilters: document.querySelector("#typeFilters"),
  refreshButton: document.querySelector("#refreshButton"),
  refreshStatus: document.querySelector("#refreshStatus"),
  workflowEnabled: document.querySelector("#workflowEnabled"),
  autoRefresh: document.querySelector("#autoRefresh"),
  compactReverse: document.querySelector("#compactReverse"),
  caseTitle: document.querySelector("#caseTitle"),
  assetCount: document.querySelector("#assetCount"),
  searchInput: document.querySelector("#searchInput"),
  sortSelect: document.querySelector("#sortSelect"),
  assetGrid: document.querySelector("#assetGrid"),
  detailName: document.querySelector("#detailName"),
  detailPreview: document.querySelector("#detailPreview"),
  detailBody: document.querySelector("#detailBody"),
  closeDetail: document.querySelector("#closeDetail"),
  quickMoveAsset: document.querySelector("#quickMoveAsset"),
  moveAssetDialog: document.querySelector("#moveAssetDialog"),
  moveAssetSummary: document.querySelector("#moveAssetSummary"),
  moveTargetProject: document.querySelector("#moveTargetProject"),
  moveTargetFolder: document.querySelector("#moveTargetFolder"),
  moveCustomFolder: document.querySelector("#moveCustomFolder"),
  moveTargetName: document.querySelector("#moveTargetName"),
  confirmMoveAsset: document.querySelector("#confirmMoveAsset"),
  cancelMoveAsset: document.querySelector("#cancelMoveAsset"),
  moveAssetMessage: document.querySelector("#moveAssetMessage"),
  generationButton: document.querySelector("#generationButton"),
  generationDialog: document.querySelector("#generationDialog"),
  generationProject: document.querySelector("#generationProject"),
  generationProfile: document.querySelector("#generationProfile"),
  generationKind: document.querySelector("#generationKind"),
  generationGenerator: document.querySelector("#generationGenerator"),
  generationEpisode: document.querySelector("#generationEpisode"),
  generationScene: document.querySelector("#generationScene"),
  generationShot: document.querySelector("#generationShot"),
  generationRole: document.querySelector("#generationRole"),
  generationVersion: document.querySelector("#generationVersion"),
  generationModel: document.querySelector("#generationModel"),
  generationDestination: document.querySelector("#generationDestination"),
  generationNameStem: document.querySelector("#generationNameStem"),
  generationPrompt: document.querySelector("#generationPrompt"),
  generationNegative: document.querySelector("#generationNegative"),
  createGenerationTicket: document.querySelector("#createGenerationTicket"),
  createAndArmGeneration: document.querySelector("#createAndArmGeneration"),
  refreshGenerationTickets: document.querySelector("#refreshGenerationTickets"),
  generationSummary: document.querySelector("#generationSummary"),
  generationTickets: document.querySelector("#generationTickets"),
  automationButton: document.querySelector("#automationButton"),
  automationDialog: document.querySelector("#automationDialog"),
  inboxEnabled: document.querySelector("#inboxEnabled"),
  activeProfile: document.querySelector("#activeProfile"),
  moveAfterArchive: document.querySelector("#moveAfterArchive"),
  inboxSourcePath: document.querySelector("#inboxSourcePath"),
  inboxProject: document.querySelector("#inboxProject"),
  inboxPollSeconds: document.querySelector("#inboxPollSeconds"),
  inboxBasePath: document.querySelector("#inboxBasePath"),
  useCurrentCase: document.querySelector("#useCurrentCase"),
  routeImage: document.querySelector("#routeImage"),
  routeVideo: document.querySelector("#routeVideo"),
  routeAudio: document.querySelector("#routeAudio"),
  routeOther: document.querySelector("#routeOther"),
  cleanupEnabled: document.querySelector("#cleanupEnabled"),
  retentionDays: document.querySelector("#retentionDays"),
  cleanupIntervalHours: document.querySelector("#cleanupIntervalHours"),
  quarantinePath: document.querySelector("#quarantinePath"),
  cleanupDryRun: document.querySelector("#cleanupDryRun"),
  purgeEnabled: document.querySelector("#purgeEnabled"),
  quarantineDays: document.querySelector("#quarantineDays"),
  saveAutomation: document.querySelector("#saveAutomation"),
  previewOrganizer: document.querySelector("#previewOrganizer"),
  runOrganizer: document.querySelector("#runOrganizer"),
  previewCleanup: document.querySelector("#previewCleanup"),
  runCleanup: document.querySelector("#runCleanup"),
  automationSummary: document.querySelector("#automationSummary"),
  automationResult: document.querySelector("#automationResult")
};

const userStatuses = ["可用", "局部可用", "参考可用", "暂存", "丢弃"];
const categoryLabels = {
  videoResult: "视频结果",
  generatedAsset: "生成资产",
  reference: "输入参考",
  reverse: "视频反推/抽帧",
  audio: "音频资产",
  "": "全部资产"
};

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  const kb = bytes / 1024;
  if (kb < 1024) return `${kb.toFixed(1)} KB`;
  const mb = kb / 1024;
  if (mb < 1024) return `${mb.toFixed(1)} MB`;
  return `${(mb / 1024).toFixed(1)} GB`;
}

function statusClass(status) {
  if (status === "可用") return "good";
  if (status === "可用但需优化" || status === "局部可用") return "partial";
  if (status === "参考可用" || status === "不通过但有参考价值") return "ref";
  if (status === "暂存" || status === "未评估") return "hold";
  if (status === "丢弃" || status === "不通过") return "drop";
  return "unknown";
}

function displayStatus(asset) {
  return asset.userStatus || asset.initialStatus || "待用户判断";
}

function includesAny(text, words) {
  return words.some((word) => text.includes(word));
}

function slashPath(text) {
  return String(text || "").replaceAll("\\", "/");
}

function pathTokens(asset) {
  const casePath = slashPath(`${asset.caseId}/${asset.caseRelPath || ""}/${asset.name || ""}`);
  const projectPath = slashPath(`${asset.relPath || ""}/${asset.name || ""}`);
  return {
    original: `${casePath} ${projectPath}`,
    lower: `${casePath} ${projectPath}`.toLowerCase()
  };
}

function assetCategory(asset) {
  const { original, lower } = pathTokens(asset);
  if (
    asset.kind === "contact" ||
    asset.kind === "frame" ||
    includesAny(original, ["反推", "抽帧", "拆帧", "视频学习", "contact_sheet", "逐帧"]) ||
    includesAny(lower, ["/frames/", "/frame_extract", "/reverse", "/storyboard_reverse", "/video_reverse", "frame_", "contact_sheet"])
  ) {
    return "reverse";
  }

  if (asset.kind === "audio") {
    return "audio";
  }

  if (
    includesAny(lower, [
      "/input/",
      "/inputs/",
      "/source/",
      "/sources/",
      "/reference/",
      "/references/",
      "/refs/",
      "/samples/",
      "/raw/",
      "/原始素材/",
      "/输入参考/",
      "/参考素材/"
    ]) ||
    includesAny(original, ["输入参考", "参考素材", "原始素材", "外部参考", "源素材"]) ||
    includesAny(lower, ["source_", "input_", "ref_", "_ref."])
  ) {
    return "reference";
  }

  if (
    asset.kind === "video" ||
    includesAny(lower, [
      "/videos/",
      "/video_results/",
      "/video-result/",
      "/video-result",
      "/final_videos/",
      "/exports/",
      "/renders/",
      "/rendered/"
    ]) ||
    includesAny(original, ["成片", "视频结果", "最终视频", "可用版", "实测"]) ||
    includesAny(lower, ["seedance", "dreamina", "higgsfield"])
  ) {
    return "videoResult";
  }

  if (
    includesAny(lower, [
      "/generated_covers/",
      "/generated/",
      "/generations/",
      "/outputs/",
      "/output/",
      "/assets/",
      "/images/",
      "/covers/",
      "/candidates/"
    ]) ||
    includesAny(original, ["母版", "机制母版", "首帧", "尾帧", "角色卡", "设定", "候选", "测试图", "资产图", "封面", "道具", "场景"]) ||
    includesAny(lower, ["generated", "candidate", "cover", "final", "regen", "character_design"])
  ) {
    return "generatedAsset";
  }

  if (asset.kind === "image") return "generatedAsset";
  return "generatedAsset";
}

function enrichAsset(asset) {
  if (asset.category) return asset;
  const category = assetCategory(asset);
  return {
    ...asset,
    category,
    categoryLabel: categoryLabels[category] || "全部资产"
  };
}

function absolutePath(asset) {
  if (asset.isGroup) return `${state.projectRoot}/${asset.groupDir}`;
  return `${state.projectRoot}/${asset.relPath}`;
}

async function api(path, options) {
  const response = await fetch(path, {
    headers: { "content-type": "application/json" },
    ...options
  });
  if (!response.ok) {
    const text = await response.text();
    try {
      const data = JSON.parse(text);
      throw new Error(data.error || text);
    } catch (error) {
      if (error instanceof SyntaxError) throw new Error(text);
      throw error;
    }
  }
  return response.json();
}

async function loadConfig() {
  const data = await api("/api/config");
  state.configEnabled = data.enabled !== false;
  state.automation = data.automation || state.automation;
  els.workflowEnabled.checked = state.configEnabled;
  renderAutomationForm();
}

async function loadProjects() {
  const data = await api("/api/projects");
  state.projects = data.projects;
  if (!state.selectedProject && state.projects[0]) state.selectedProject = state.projects[0].id;
  renderProjects();
  renderAutomationProjects();
}

function renderAutomationProjects() {
  if (!els.inboxProject) return;
  const selected = state.automation?.inbox?.projectId || els.inboxProject.value || state.selectedProject;
  els.inboxProject.innerHTML = "";
  for (const project of state.projects) {
    const option = document.createElement("option");
    option.value = project.id;
    option.textContent = `${project.name}${project.exists ? "" : "（路径缺失）"}`;
    els.inboxProject.append(option);
  }
  if (state.projects.some((project) => project.id === selected)) els.inboxProject.value = selected;
}

function renderAutomationForm() {
  const automation = state.automation;
  if (!automation || !els.inboxSourcePath) return;
  const inbox = automation.inbox || {};
  const cleanup = automation.cleanup || {};
  document.querySelectorAll(".legacy-route-field").forEach((element) => {
    element.hidden = Boolean(automation.routing?.enabled);
  });
  els.inboxEnabled.checked = Boolean(inbox.enabled);
  els.moveAfterArchive.checked = inbox.transferMode === "move";
  renderAutomationProfiles();
  els.inboxSourcePath.value = inbox.sourcePath || "";
  els.inboxPollSeconds.value = inbox.pollSeconds || 15;
  els.inboxBasePath.value = inbox.basePath || "";
  els.routeImage.value = inbox.routes?.image ?? "assets/inbox/images";
  els.routeVideo.value = inbox.routes?.video ?? "assets/inbox/videos";
  els.routeAudio.value = inbox.routes?.audio ?? "assets/inbox/audio";
  els.routeOther.value = inbox.routes?.other ?? "";
  els.cleanupEnabled.checked = Boolean(cleanup.enabled);
  els.retentionDays.value = cleanup.retentionDays || 30;
  els.cleanupIntervalHours.value = cleanup.intervalHours || 24;
  els.quarantinePath.value = cleanup.quarantinePath || "";
  els.cleanupDryRun.checked = cleanup.dryRun !== false;
  els.purgeEnabled.checked = Boolean(cleanup.purgeEnabled);
  els.quarantineDays.value = cleanup.quarantineDays || 14;
  renderAutomationProjects();
}

function renderAutomationProfiles() {
  if (!els.activeProfile) return;
  const routing = state.automation?.routing;
  els.activeProfile.innerHTML = "";
  if (!routing?.enabled || !routing.profiles?.length) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "未启用多项目分流";
    els.activeProfile.append(option);
    els.activeProfile.disabled = true;
    els.automationButton.textContent = "下载收件箱";
    return;
  }
  els.activeProfile.disabled = false;
  for (const profile of routing.profiles) {
    const option = document.createElement("option");
    option.value = profile.id;
    option.textContent = profile.name;
    els.activeProfile.append(option);
  }
  els.activeProfile.value = routing.activeProfileId;
  const active = routing.profiles.find((profile) => profile.id === routing.activeProfileId);
  els.automationButton.textContent = active ? `收件箱 · ${active.name}` : "下载收件箱";
}

function numericValue(element, fallback) {
  const value = Number(element.value);
  return Number.isFinite(value) ? value : fallback;
}

function collectAutomationForm() {
  return {
    inbox: {
      enabled: els.inboxEnabled.checked,
      sourcePath: els.inboxSourcePath.value.trim(),
      projectId: els.inboxProject.value,
      basePath: els.inboxBasePath.value.trim(),
      startedAt: state.automation?.inbox?.startedAt || null,
      transferMode: els.moveAfterArchive.checked ? "move" : "copy",
      moveApprovedAt: state.automation?.inbox?.moveApprovedAt || null,
      settleSeconds: state.automation?.inbox?.settleSeconds || 8,
      pollSeconds: numericValue(els.inboxPollSeconds, 15),
      routes: {
        image: els.routeImage.value.trim(),
        video: els.routeVideo.value.trim(),
        audio: els.routeAudio.value.trim(),
        other: els.routeOther.value.trim()
      }
    },
    routing: state.automation?.routing ? {
      ...state.automation.routing,
      activeProfileId: els.activeProfile.value || state.automation.routing.activeProfileId
    } : { enabled: false, profiles: [] },
    cleanup: {
      enabled: els.cleanupEnabled.checked,
      dryRun: els.cleanupDryRun.checked,
      intervalHours: numericValue(els.cleanupIntervalHours, 24),
      retentionDays: numericValue(els.retentionDays, 30),
      quarantinePath: els.quarantinePath.value.trim(),
      purgeEnabled: els.purgeEnabled.checked,
      quarantineDays: numericValue(els.quarantineDays, 14),
      onlyImported: true
    }
  };
}

async function saveAutomationSettings({ quiet = false } = {}) {
  const automation = collectAutomationForm();
  let confirmCleanup = false;
  let confirmPurge = false;
  let confirmMove = false;
  if (automation.inbox.transferMode === "move") {
    confirmMove = window.confirm("确认启用自动转移？工具会在目标文件完整校验成功后，从下载文件夹移走原件。");
    if (!confirmMove) return false;
  }
  if (automation.cleanup.enabled && !automation.cleanup.dryRun) {
    confirmCleanup = window.confirm("确认启用实际清理？到期文件会先移入隔离区；只处理已归档且内容核对一致的原文件。");
    if (!confirmCleanup) return false;
  }
  if (automation.cleanup.purgeEnabled) {
    confirmPurge = window.confirm(`确认允许隔离区中的文件在 ${automation.cleanup.quarantineDays} 天后永久清空？`);
    if (!confirmPurge) return false;
  }
  const data = await api("/api/automation/settings", {
    method: "POST",
    body: JSON.stringify({ automation, confirmMove, confirmCleanup, confirmPurge })
  });
  state.automation = data.automation;
  renderAutomationForm();
  if (!quiet) showAutomationMessage("设置已保存", "自动归档和清理策略已经更新。");
  return true;
}

function showAutomationMessage(title, message, isError = false) {
  els.automationSummary.textContent = title;
  els.automationResult.innerHTML = "";
  const paragraph = document.createElement("p");
  paragraph.className = isError ? "result-error" : "";
  paragraph.textContent = message;
  els.automationResult.append(paragraph);
}

function showAutomationResult(title, data) {
  const groups = [
    ["planned", "准备归档"],
    ["imported", "已归档"],
    ["alreadyImported", "已归档过"],
    ["pending", "等待下载完成"],
    ["ignored", "已忽略"],
    ["candidates", "准备移入隔离区"],
    ["quarantined", "已移入隔离区"],
    ["purged", "已清空"],
    ["protectedItems", "受保护未处理"],
    ["failed", "失败"]
  ].filter(([key]) => Array.isArray(data[key]));
  const total = groups.reduce((sum, [key]) => sum + data[key].length, 0);
  els.automationSummary.textContent = `${title} · ${groups.map(([key, label]) => `${label} ${data[key].length}`).join(" / ")}`;
  els.automationResult.innerHTML = "";
  if (!total) {
    const empty = document.createElement("p");
    empty.textContent = "没有需要处理的文件。";
    els.automationResult.append(empty);
    return;
  }
  for (const [key, label] of groups) {
    if (!data[key].length) continue;
    const section = document.createElement("section");
    const heading = document.createElement("h4");
    heading.textContent = `${label}（${data[key].length}）`;
    section.append(heading);
    const list = document.createElement("ul");
    for (const item of data[key].slice(0, 50)) {
      const row = document.createElement("li");
      const destination = item.destinationPath ? ` → ${item.destinationPath}` : "";
      const profile = item.profileName ? `[${item.profileName}] ` : "";
      row.textContent = `${profile}${item.name || item.sourcePath || "文件"}${destination}${item.reason ? ` · ${item.reason}` : ""}`;
      list.append(row);
    }
    if (data[key].length > 50) {
      const row = document.createElement("li");
      row.textContent = `其余 ${data[key].length - 50} 项未展开`;
      list.append(row);
    }
    section.append(list);
    els.automationResult.append(section);
  }
}

async function runAutomationAction(path, title, { saveFirst = false, confirmRun = false } = {}) {
  try {
    if (saveFirst && !await saveAutomationSettings({ quiet: true })) return;
    if (confirmRun && !window.confirm("确认执行本轮实际清理？符合条件的文件会移入隔离区。")) return;
    showAutomationMessage("正在处理", "正在核对文件，请稍候……");
    const data = await api(path, {
      method: "POST",
      body: JSON.stringify({ automation: collectAutomationForm(), confirm: confirmRun })
    });
    showAutomationResult(data.dryRun ? `${title}（仅预演）` : title, data);
    await loadAssets();
  } catch (error) {
    showAutomationMessage("操作未完成", error.message, true);
  }
}

async function openAutomationDialog() {
  await loadConfig();
  await loadProjects();
  els.automationDialog.showModal();
  try {
    const status = await api("/api/automation/status");
    if (status.organizerPreview) showAutomationResult("当前收件箱", status.organizerPreview);
    else if (status.organizerError) showAutomationMessage("需要设置", status.organizerError);
  } catch (error) {
    showAutomationMessage("状态读取失败", error.message, true);
  }
}

function generationStatusLabel(status) {
  return {
    draft: "已登记",
    awaiting_download: "等待下一个下载",
    generated: "已生成，待归档",
    archived: "已归档",
    cancelled: "已取消"
  }[status] || status || "未知";
}

function renderGenerationSelectors() {
  const projectValue = els.generationProject.value || state.selectedProject;
  els.generationProject.innerHTML = "";
  for (const project of state.projects) {
    const option = document.createElement("option");
    option.value = project.id;
    option.textContent = project.name;
    els.generationProject.append(option);
  }
  if (state.projects.some((project) => project.id === projectValue)) {
    els.generationProject.value = projectValue;
  }

  const profiles = state.automation?.routing?.profiles || [];
  const requestedProfile = els.generationProfile.value || state.automation?.routing?.activeProfileId || "";
  const requestedProfileData = profiles.find((profile) => profile.id === requestedProfile);
  const profileValue = requestedProfileData?.projectId === els.generationProject.value ? requestedProfile : "";
  els.generationProfile.innerHTML = "";
  const none = document.createElement("option");
  none.value = "";
  none.textContent = "按项目自动安排";
  els.generationProfile.append(none);
  for (const profile of profiles) {
    const option = document.createElement("option");
    option.value = profile.id;
    option.textContent = profile.name;
    els.generationProfile.append(option);
  }
  if ([...els.generationProfile.options].some((option) => option.value === profileValue)) {
    els.generationProfile.value = profileValue;
  }
}

function collectGenerationForm() {
  return {
    projectId: els.generationProject.value,
    profileId: els.generationProfile.value,
    kind: els.generationKind.value,
    generator: els.generationGenerator.value,
    episode: els.generationEpisode.value.trim(),
    scene: els.generationScene.value.trim(),
    shot: els.generationShot.value.trim(),
    role: els.generationRole.value.trim(),
    version: Number(els.generationVersion.value || 1),
    model: els.generationModel.value.trim(),
    destinationPath: els.generationDestination.value.trim(),
    nameStem: els.generationNameStem.value.trim(),
    prompt: els.generationPrompt.value.trim(),
    negativePrompt: els.generationNegative.value.trim(),
    sourceContext: { createdFrom: "asset-browser-ui" }
  };
}

async function generationAction(ticketId, action, body = {}) {
  await api(`/api/generation/tickets/${encodeURIComponent(ticketId)}/${action}`, {
    method: "POST",
    body: JSON.stringify(body)
  });
  await loadGenerationTickets();
}

async function revealGenerationOutput(ticket, output) {
  await api("/api/reveal", {
    method: "POST",
    body: JSON.stringify({ projectId: ticket.projectId, path: output.relativePath })
  });
}

function renderGenerationTickets() {
  els.generationTickets.innerHTML = "";
  const tickets = state.generationTickets;
  const activeCount = tickets.filter((ticket) => ["draft", "awaiting_download", "generated"].includes(ticket.status)).length;
  els.generationSummary.textContent = `${tickets.length} 个最近任务 · ${activeCount} 个进行中`;
  if (!tickets.length) {
    els.generationTickets.textContent = "尚无生成任务。";
    return;
  }

  for (const ticket of tickets) {
    const card = document.createElement("article");
    card.className = `generation-ticket status-${ticket.status}`;
    const head = document.createElement("div");
    head.className = "generation-ticket-head";
    const title = document.createElement("strong");
    title.textContent = ticket.nameStem;
    const badge = document.createElement("span");
    badge.className = "generation-ticket-badge";
    badge.textContent = generationStatusLabel(ticket.status);
    head.append(title, badge);

    const meta = document.createElement("p");
    meta.textContent = `${ticket.projectName} · ${ticket.kind === "video" ? "视频" : "图片"} · ${ticket.generator}${ticket.scene ? ` · ${ticket.scene}` : ""}${ticket.shot ? ` · ${ticket.shot}` : ""}`;
    const pathLine = document.createElement("p");
    pathLine.className = "mono generation-path";
    pathLine.textContent = ticket.outputs?.[0]?.relativePath || `${ticket.destinationRelativePath}\\${ticket.nameStem}`;
    card.append(head, meta, pathLine);

    const actions = document.createElement("div");
    actions.className = "generation-ticket-actions";
    if (ticket.status === "draft" || ticket.status === "generated") {
      const arm = document.createElement("button");
      arm.type = "button";
      arm.textContent = "等待下一个下载";
      arm.addEventListener("click", () => generationAction(ticket.id, "arm").catch((error) => window.alert(error.message)));
      actions.append(arm);
    }
    if (ticket.status === "awaiting_download") {
      const cancel = document.createElement("button");
      cancel.type = "button";
      cancel.textContent = "停止等待";
      cancel.addEventListener("click", () => generationAction(ticket.id, "cancel", { reason: "用户停止等待" }).catch((error) => window.alert(error.message)));
      actions.append(cancel);
    }
    if (ticket.outputs?.length) {
      const revealButton = document.createElement("button");
      revealButton.type = "button";
      revealButton.textContent = "在文件夹中查看";
      revealButton.addEventListener("click", () => revealGenerationOutput(ticket, ticket.outputs[0]).catch((error) => window.alert(error.message)));
      actions.append(revealButton);
    }
    if (actions.childElementCount) card.append(actions);
    els.generationTickets.append(card);
  }
}

async function loadGenerationTickets() {
  const data = await api("/api/generation/tickets?limit=60");
  state.generationTickets = data.tickets || [];
  renderGenerationTickets();
}

async function createGenerationTicket({ arm = false } = {}) {
  const payload = collectGenerationForm();
  if (!payload.projectId) throw new Error("请选择归属项目");
  if (!payload.prompt) throw new Error("请写入本次实际使用的提示词");
  const data = await api("/api/generation/tickets", {
    method: "POST",
    body: JSON.stringify(payload)
  });
  if (arm) await generationAction(data.ticket.id, "arm");
  else await loadGenerationTickets();
  return data.ticket;
}

async function openGenerationDialog() {
  await loadConfig();
  await loadProjects();
  renderGenerationSelectors();
  await loadGenerationTickets();
  els.generationDialog.showModal();
}

async function loadCases() {
  if (!state.selectedProject) return;
  const data = await api(`/api/cases?project=${encodeURIComponent(state.selectedProject)}`);
  state.projectRoot = data.projectRoot;
  state.cases = data.cases;
  if (!state.cases.some((item) => item.id === state.selectedCase)) {
    const dateCases = state.cases.filter((item) => /^\d{4}-\d{2}-\d{2}$/.test(pathParts(item.relPath || item.id)[0] || ""));
    const defaultCase = state.cases.length && dateCases.length === state.cases.length
      ? [...dateCases].sort((a, b) => String(b.relPath).localeCompare(String(a.relPath)))[0]
      : state.cases[0];
    state.selectedCase = defaultCase?.id || "";
  }
  renderCases();
}

async function loadAssets() {
  if (!state.selectedCase) return;
  state.deferredRefresh = null;
  const data = await api(`/api/assets?project=${encodeURIComponent(state.selectedProject)}&case=${encodeURIComponent(state.selectedCase)}`);
  state.assets = data.assets;
  if (state.selectedAsset) {
    state.selectedAsset = state.assets.find((asset) => asset.id === state.selectedAsset.id) || null;
  }
  render();
  els.refreshStatus.textContent = `上次刷新 ${new Date().toLocaleTimeString()}`;
}

function activeDetailMedia() {
  const media = els.detailPreview.querySelector("video, audio");
  return media || null;
}

async function performBackgroundRefresh(options = {}) {
  if (options.reloadProjects) await loadProjects();
  if (options.reloadCases) await loadCases();
  await loadAssets();
}

function deferBackgroundRefresh(options = {}) {
  const previous = state.deferredRefresh || {};
  state.deferredRefresh = {
    reloadProjects: Boolean(previous.reloadProjects || options.reloadProjects),
    reloadCases: Boolean(previous.reloadCases || options.reloadCases || options.reloadProjects)
  };
  els.refreshStatus.textContent = "预览打开期间已暂停自动刷新";
}

async function requestBackgroundRefresh(options = {}) {
  const media = activeDetailMedia();
  if (media) {
    deferBackgroundRefresh(options);
    return false;
  }
  await performBackgroundRefresh(options);
  return true;
}

async function flushDeferredRefresh() {
  const pending = state.deferredRefresh;
  if (!pending) return;
  state.deferredRefresh = null;
  await performBackgroundRefresh(pending);
}

function renderProjects() {
  els.projectList.innerHTML = "";
  for (const item of state.projects) {
    const button = document.createElement("button");
    button.className = `project-item${item.id === state.selectedProject ? " active" : ""}`;
    button.dataset.projectId = item.id;
    button.draggable = true;
    const handle = document.createElement("span");
    handle.className = "project-drag-handle";
    handle.textContent = "⠿";
    handle.title = "拖动调整顺序";
    handle.setAttribute("aria-hidden", "true");
    const name = document.createElement("span");
    name.className = "project-name";
    name.textContent = item.name;
    const status = document.createElement("span");
    status.className = `project-status ${item.exists ? "online" : "missing"}`;
    status.textContent = item.exists ? "可用" : "缺失";
    button.append(handle, name, status);
    button.title = item.path;
    button.addEventListener("dragstart", (event) => {
      state.draggedProjectId = item.id;
      state.suppressProjectClick = true;
      button.classList.add("dragging");
      if (event.dataTransfer) {
        event.dataTransfer.effectAllowed = "move";
        event.dataTransfer.setData("text/plain", item.id);
      }
    });
    button.addEventListener("dragend", () => {
      button.classList.remove("dragging");
      state.draggedProjectId = "";
      window.setTimeout(() => {
        state.suppressProjectClick = false;
      }, 120);
    });
    button.addEventListener("click", async () => {
      if (state.suppressProjectClick) return;
      state.selectedProject = item.id;
      state.selectedCase = "";
      state.selectedAsset = null;
      setCategoryFilter("");
      renderProjects();
      await loadCases();
      await loadAssets();
    });
    els.projectList.append(button);
  }
}

async function saveProjectOrder() {
  const projectIds = [...els.projectList.querySelectorAll(".project-item")]
    .map((item) => item.dataset.projectId)
    .filter(Boolean);
  const data = await api("/api/projects/reorder", {
    method: "POST",
    body: JSON.stringify({ projectIds })
  });
  state.projects = data.projects;
  renderProjects();
  renderAutomationProjects();
  els.refreshStatus.textContent = "项目顺序已保存";
}

function wireProjectReorder() {
  els.projectList.addEventListener("dragover", (event) => {
    const dragging = els.projectList.querySelector(".project-item.dragging");
    if (!dragging) return;
    event.preventDefault();
    if (event.dataTransfer) event.dataTransfer.dropEffect = "move";
    const target = event.target.closest(".project-item");
    if (!target) {
      els.projectList.append(dragging);
      return;
    }
    if (target === dragging) return;
    const rect = target.getBoundingClientRect();
    const placeAfter = event.clientY > rect.top + rect.height / 2;
    els.projectList.insertBefore(dragging, placeAfter ? target.nextSibling : target);
  });
  els.projectList.addEventListener("drop", (event) => {
    event.preventDefault();
    saveProjectOrder().catch(async (error) => {
      els.refreshStatus.textContent = `顺序保存失败：${error.message}`;
      await loadProjects();
    });
  });
}

const sidebarLayoutStorageKey = "asset-browser.sidebar-layout.v1";

function readSidebarLayout() {
  try {
    return JSON.parse(window.localStorage.getItem(sidebarLayoutStorageKey) || "{}") || {};
  } catch {
    return {};
  }
}

function saveSidebarLayout() {
  if (!els.sidebarLayout) return;
  const modules = [...els.sidebarLayout.querySelectorAll(".sidebar-module")];
  const payload = {
    order: modules.map((module) => module.dataset.sectionId).filter(Boolean),
    open: Object.fromEntries(modules.map((module) => [module.dataset.sectionId, module.open]))
  };
  try {
    window.localStorage.setItem(sidebarLayoutStorageKey, JSON.stringify(payload));
  } catch {
    // The layout still works for the current page even when local storage is unavailable.
  }
}

function wireSidebarLayout() {
  if (!els.sidebar || !els.sidebarLayout) return;
  const saved = readSidebarLayout();
  const modules = [...els.sidebarLayout.querySelectorAll(".sidebar-module")];
  const byId = new Map(modules.map((module) => [module.dataset.sectionId, module]));
  for (const id of saved.order || []) {
    const module = byId.get(id);
    if (!module) continue;
    els.sidebarLayout.append(module);
    byId.delete(id);
  }
  for (const module of modules) {
    if (byId.has(module.dataset.sectionId)) els.sidebarLayout.append(module);
  }

  for (const module of modules) {
    const id = module.dataset.sectionId;
    if (saved.open && Object.prototype.hasOwnProperty.call(saved.open, id)) {
      module.open = Boolean(saved.open[id]);
    }
    module.addEventListener("toggle", saveSidebarLayout);
    const handle = module.querySelector(":scope > .section-summary .sidebar-module-grip");
    if (!handle) continue;
    handle.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
    });
    handle.addEventListener("dragstart", (event) => {
      module.classList.add("dragging");
      if (event.dataTransfer) {
        event.dataTransfer.effectAllowed = "move";
        event.dataTransfer.setData("text/plain", id);
      }
    });
    handle.addEventListener("dragend", () => {
      module.classList.remove("dragging");
      saveSidebarLayout();
    });
  }

  els.sidebarLayout.addEventListener("dragover", (event) => {
    const dragging = els.sidebarLayout.querySelector(".sidebar-module.dragging");
    if (!dragging) return;
    event.preventDefault();
    if (event.dataTransfer) event.dataTransfer.dropEffect = "move";
    const eventElement = event.target instanceof Element ? event.target : null;
    const target = eventElement?.closest(".sidebar-module");
    if (!target) {
      els.sidebarLayout.append(dragging);
      return;
    }
    if (target === dragging) return;
    const rect = target.getBoundingClientRect();
    const placeAfter = event.clientY > rect.top + rect.height / 2;
    els.sidebarLayout.insertBefore(dragging, placeAfter ? target.nextSibling : target);
  });
  els.sidebarLayout.addEventListener("drop", (event) => {
    const dragging = els.sidebarLayout.querySelector(".sidebar-module.dragging");
    if (!dragging) return;
    event.preventDefault();
    saveSidebarLayout();
    els.refreshStatus.textContent = "左栏布局已保存";
  });

  els.sidebar.addEventListener("wheel", (event) => {
    if (event.ctrlKey || Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;
    const scale = event.deltaMode === 1 ? 24 : event.deltaMode === 2 ? els.sidebar.clientHeight : 1;
    const previous = els.sidebar.scrollTop;
    els.sidebar.scrollTop += event.deltaY * scale;
    if (els.sidebar.scrollTop !== previous) event.preventDefault();
  }, { passive: false });
}

function pathParts(value) {
  return String(value || "").split(/[\\/]+/).filter(Boolean).filter((part) => part !== ".");
}

function episodeRank(name) {
  const ranks = ["第一集", "第二集", "第三集", "第四集", "第五集", "第六集"];
  const rank = ranks.findIndex((label) => String(name || "").startsWith(label));
  return rank === -1 ? 999 : rank;
}

function caseRank(name) {
  const order = new Map([["参考", 0], ["生成视频", 1], ["成片", 2]]);
  return order.has(name) ? order.get(name) : 100;
}

function makeCaseButton(item, label) {
  const button = document.createElement("button");
  button.className = `tree-item${item.id === state.selectedCase ? " active" : ""}`;
  if (item.id === state.selectedCase) button.setAttribute("aria-current", "page");
  const name = document.createElement("span");
  name.className = "tree-item-name";
  name.textContent = label;
  const count = document.createElement("span");
  count.className = "tree-item-count";
  count.textContent = String(item.mediaCount ?? 0);
  button.append(name, count);
  button.title = item.relPath || item.id;
  button.addEventListener("click", async () => {
    state.selectedCase = item.id;
    state.selectedAsset = null;
    setCategoryFilter("");
    renderCases();
    await loadAssets();
  });
  return button;
}

function configureCaseGroup(group, key, defaultOpen = false) {
  const hasSavedState = Object.prototype.hasOwnProperty.call(state.caseGroupOpen, key);
  group.open = hasSavedState ? state.caseGroupOpen[key] : defaultOpen;
  group.addEventListener("toggle", () => {
    state.caseGroupOpen[key] = group.open;
  });
}

function renderGroupedCases() {
  const grouped = new Map();
  for (const item of state.cases) {
    const parts = pathParts(item.relPath || item.id);
    if (parts.length < 2) continue;
    const episode = parts[0];
    if (!grouped.has(episode)) grouped.set(episode, []);
    grouped.get(episode).push({ item, parts });
  }
  const episodes = [...grouped.entries()].sort((a, b) => episodeRank(a[0]) - episodeRank(b[0]) || a[0].localeCompare(b[0], "zh-CN"));
  for (const [episode, entries] of episodes) {
    entries.sort((a, b) => caseRank(a.parts[1]) - caseRank(b.parts[1]) || a.parts.slice(1).join("/").localeCompare(b.parts.slice(1).join("/"), "zh-CN"));
    const hasActive = entries.some(({ item }) => item.id === state.selectedCase);
    const group = document.createElement("details");
    group.className = `case-group${hasActive ? " has-active" : ""}`;
    configureCaseGroup(group, `${state.selectedProject}:${episode}`, hasActive);
    const head = document.createElement("summary");
    head.className = "case-group-head";
    const title = document.createElement("strong");
    title.textContent = episode;
    const total = document.createElement("span");
    total.textContent = `${entries.reduce((sum, { item }) => sum + Number(item.mediaCount || 0), 0)} 个素材`;
    head.append(title, total);
    const children = document.createElement("div");
    children.className = "case-group-children";
    for (const { item, parts } of entries) children.append(makeCaseButton(item, parts.slice(1).join(" / ")));
    group.append(head, children);
    els.caseList.append(group);
  }
}

function renderDailyCases() {
  const group = document.createElement("details");
  group.className = "case-group daily-group";
  configureCaseGroup(group, `${state.selectedProject}:dates`, true);
  const head = document.createElement("summary");
  head.className = "case-group-head";
  const title = document.createElement("strong");
  title.textContent = "按日期";
  const total = document.createElement("span");
  total.textContent = `${state.cases.length} 天`;
  head.append(title, total);
  const children = document.createElement("div");
  children.className = "case-group-children";
  for (const item of [...state.cases].sort((a, b) => String(b.relPath).localeCompare(String(a.relPath)))) {
    children.append(makeCaseButton(item, pathParts(item.relPath || item.id).join(" / ") || item.name));
  }
  group.append(head, children);
  els.caseList.append(group);
}

function renderHierarchicalCases() {
  const entries = state.cases.map((item) => ({ item, parts: pathParts(item.relPath || item.id) }));
  const roots = entries.filter(({ parts }) => parts.length === 1);
  for (const root of roots) {
    const descendants = entries
      .filter(({ parts }) => parts.length > 1 && parts[0] === root.parts[0])
      .sort((a, b) => a.parts.length - b.parts.length || a.parts.slice(1).join("/").localeCompare(b.parts.slice(1).join("/"), "zh-CN"));
    if (!descendants.length) {
      els.caseList.append(makeCaseButton(root.item, root.item.name));
      continue;
    }
    const hasActive = state.selectedCase === root.item.id || descendants.some(({ item }) => item.id === state.selectedCase);
    const group = document.createElement("details");
    group.className = `case-group${hasActive ? " has-active" : ""}`;
    configureCaseGroup(group, `${state.selectedProject}:${root.item.id}`, true);
    const head = document.createElement("summary");
    head.className = "case-group-head";
    const title = document.createElement("strong");
    title.textContent = root.item.name;
    const total = document.createElement("span");
    total.textContent = `${root.item.mediaCount || 0} 个素材`;
    head.append(title, total);
    const children = document.createElement("div");
    children.className = "case-group-children";
    children.append(makeCaseButton(root.item, "全部"));
    for (const { item, parts } of descendants) {
      children.append(makeCaseButton(item, parts.slice(1).join(" / ")));
    }
    group.append(head, children);
    els.caseList.append(group);
  }
}

function folderOverviewContext() {
  const root = state.cases.find((item) => item.id === state.selectedCase);
  if (!root) return null;
  const rootParts = pathParts(root.relPath || root.id);
  const children = state.cases
    .map((item) => ({ item, parts: pathParts(item.relPath || item.id) }))
    .filter(({ parts }) => parts.length === rootParts.length + 1 && rootParts.every((part, index) => parts[index] === part))
    .sort((a, b) => a.parts.at(-1).localeCompare(b.parts.at(-1), "zh-CN"));
  return children.length ? { root, rootParts, children } : null;
}

function pickFolderPreviewAssets(assets, limit = 4) {
  const sorted = [...assets].sort((a, b) => b.mtimeMs - a.mtimeMs || a.name.localeCompare(b.name, "zh-CN"));
  if (sorted.length <= limit) return sorted;
  const indexes = new Set();
  for (let index = 0; index < limit; index += 1) {
    indexes.add(Math.round(index * (sorted.length - 1) / (limit - 1)));
  }
  return [...indexes].map((index) => sorted[index]);
}

function renderFolderPreviewCard(entry, assets) {
  const card = document.createElement("button");
  card.type = "button";
  card.className = "style-folder-card";
  const previewAssets = pickFolderPreviewAssets(assets);
  const preview = document.createElement("div");
  preview.className = `folder-preview-grid folder-preview-count-${previewAssets.length}`;
  if (previewAssets.length) {
    preview.innerHTML = previewAssets.map((asset) => mediaPreview(asset)).join("");
  } else {
    preview.innerHTML = '<div class="folder-preview-empty">暂无预览</div>';
  }
  const body = document.createElement("div");
  body.className = "folder-card-body";
  const heading = document.createElement("div");
  heading.className = "folder-card-heading";
  const title = document.createElement("strong");
  title.textContent = entry.parts.at(-1) || entry.item.name;
  const openLabel = document.createElement("span");
  openLabel.textContent = "打开";
  heading.append(title, openLabel);
  const meta = document.createElement("p");
  meta.textContent = `${entry.item.mediaCount ?? assets.length} 个素材`;
  body.append(heading, meta);
  card.append(preview, body);
  card.title = `打开 ${title.textContent}`;
  card.addEventListener("click", async () => {
    state.selectedCase = entry.item.id;
    state.selectedAsset = null;
    setCategoryFilter("");
    renderCases();
    await loadAssets();
  });
  return card;
}

function renderFolderOverview(context) {
  const query = state.query.trim().toLowerCase();
  const folders = context.children.map((entry) => {
    const childName = entry.parts[context.rootParts.length];
    const assets = state.assets.filter((asset) => pathParts(asset.caseRelPath)[0] === childName);
    return { entry, assets };
  }).filter(({ entry, assets }) => {
    if (!query) return true;
    const haystack = [entry.parts.at(-1), ...assets.map((asset) => asset.name)].join(" ").toLowerCase();
    return haystack.includes(query);
  });

  renderCategoryCounts();
  els.assetCount.textContent = `文件夹：${folders.length} / ${context.children.length} 个，共 ${state.assets.length} 个素材`;
  els.assetGrid.classList.add("folder-overview-grid");
  els.assetGrid.innerHTML = "";
  if (!folders.length) {
    els.assetGrid.innerHTML = `
      <div class="empty-state">
        <h3>没有匹配的风格文件夹</h3>
        <p>清空搜索词后可查看全部风格目录。</p>
      </div>
    `;
  } else {
    for (const folder of folders) els.assetGrid.append(renderFolderPreviewCard(folder.entry, folder.assets));
  }
  renderDetail();
}

function renderCases() {
  els.caseList.innerHTML = "";
  const paths = state.cases.map((item) => pathParts(item.relPath || item.id));
  if (paths.length && paths.every((parts) => /^\d{4}-\d{2}-\d{2}$/.test(parts[0] || ""))) return renderDailyCases();
  if (paths.some((parts) => parts.length >= 2)) return renderHierarchicalCases();
  for (const item of state.cases) {
    const label = pathParts(item.relPath || item.id).join(" / ") || item.name;
    els.caseList.append(makeCaseButton(item, label));
  }
}

function renderCategoryCounts() {
  const counts = { videoResult: 0, generatedAsset: 0, reference: 0, reverse: 0, audio: 0, "": state.assets.length };
  for (const asset of state.assets.map(enrichAsset)) {
    counts[asset.category] = (counts[asset.category] || 0) + 1;
  }
  els.categoryFilters.querySelectorAll("[data-category]").forEach((button) => {
    const category = button.dataset.category;
    const label = categoryLabels[category] || "全部资产";
    button.innerHTML = `<span>${label}</span><small>${counts[category] || 0}</small>`;
  });
}

function setCategoryFilter(category) {
  state.categoryFilter = category;
  els.categoryFilters.querySelectorAll("[data-category]").forEach((button) => {
    button.classList.toggle("active", button.dataset.category === category);
  });
}

function filteredAssets() {
  const q = state.query.trim().toLowerCase();
  const enriched = state.assets.map(enrichAsset);
  let assets = enriched.filter((asset) => {
    const status = displayStatus(asset);
    if (state.categoryFilter && asset.category !== state.categoryFilter) return false;
    if (state.typeFilter && asset.kind !== state.typeFilter) return false;
    if (state.statusFilter) {
      if (state.statusFilter === "待用户判断") {
        if (asset.userStatus) return false;
      } else if (status !== state.statusFilter) {
        return false;
      }
    }
    if (!q) return true;
    const haystack = [
      asset.name,
      asset.version,
      asset.relPath,
      asset.notes,
      asset.initialStatus,
      asset.userStatus,
      asset.kind
    ].join(" ").toLowerCase();
    return haystack.includes(q);
  });

  if (state.compactReverse && state.categoryFilter === "reverse" && !state.typeFilter) {
    assets = compactReverseAssets(assets);
  }

  assets = [...assets].sort((a, b) => {
    if (state.sort === "oldest") return a.mtimeMs - b.mtimeMs;
    if (state.sort === "name") return a.name.localeCompare(b.name);
    if (state.sort === "size") return b.size - a.size;
    return b.mtimeMs - a.mtimeMs;
  });
  return assets;
}

function compactReverseAssets(assets) {
  const standalone = [];
  const groups = new Map();

  for (const asset of assets) {
    if (!["frame", "contact", "image"].includes(asset.kind)) {
      standalone.push(asset);
      continue;
    }
    const key = `${asset.caseId}/${asset.dir}`;
    const group = groups.get(key) || {
      key,
      assets: [],
      latest: asset
    };
    group.assets.push(asset);
    if (asset.mtimeMs > group.latest.mtimeMs) group.latest = asset;
    groups.set(key, group);
  }

  const reverseGroups = [...groups.values()].map((group) => {
    if (group.assets.length === 1) return group.assets[0];
    const sorted = [...group.assets].sort((a, b) => {
      const byName = a.name.localeCompare(b.name, undefined, { numeric: true });
      if (byName) return byName;
      return a.mtimeMs - b.mtimeMs;
    });
    const contact = sorted.find((asset) => asset.kind === "contact");
    const frame = sorted.find((asset) => asset.kind === "frame");
    const representative = contact || frame || sorted[Math.floor((sorted.length - 1) / 2)] || group.latest;
    return {
      ...representative,
      id: `group:${group.key}`,
      isGroup: true,
      kind: "frame-group",
      category: "reverse",
      categoryLabel: "视频反推/抽帧",
      groupDir: representative.dir,
      groupCount: group.assets.length,
      groupFirst: sorted[0],
      groupLast: sorted[sorted.length - 1],
      name: `${representative.dir.split("/").pop()}（${group.assets.length} 项）`,
      size: group.assets.reduce((sum, item) => sum + item.size, 0),
      mtimeMs: group.latest.mtimeMs,
      notes: representative.notes || "",
      initialStatus: "抽帧文件夹",
      userStatus: ""
    };
  });

  return [...standalone, ...reverseGroups];
}

function mediaPreview(asset, controls = false) {
  if (asset.kind === "video") {
    return `<video ${controls ? "controls" : ""} preload="metadata" src="${asset.mediaUrl}"></video>`;
  }
  if (asset.kind === "audio") {
    return `
      <div class="audio-preview">
        <div class="audio-mark">AUDIO</div>
        <audio ${controls ? "controls" : ""} preload="metadata" src="${asset.mediaUrl}"></audio>
      </div>
    `;
  }
  return `<img src="${asset.mediaUrl}" alt="">`;
}

function configureDetailPreviewFit() {
  const preview = els.detailPreview;
  const media = preview.querySelector("img, video");
  preview.classList.remove("is-portrait", "is-square", "is-landscape");
  if (!media) return;

  const applyDimensions = (width, height) => {
    if (!width || !height) return;
    const ratio = width / height;
    preview.classList.toggle("is-portrait", ratio < 0.9);
    preview.classList.toggle("is-square", ratio >= 0.9 && ratio <= 1.1);
    preview.classList.toggle("is-landscape", ratio > 1.1);
  };

  if (media instanceof HTMLVideoElement) {
    if (media.videoWidth && media.videoHeight) applyDimensions(media.videoWidth, media.videoHeight);
    else media.addEventListener("loadedmetadata", () => applyDimensions(media.videoWidth, media.videoHeight), { once: true });
    return;
  }

  if (media.complete && media.naturalWidth && media.naturalHeight) {
    applyDimensions(media.naturalWidth, media.naturalHeight);
  } else {
    media.addEventListener("load", () => applyDimensions(media.naturalWidth, media.naturalHeight), { once: true });
  }
}

function renderAssetCard(asset) {
  const card = document.createElement("article");
  card.className = `asset-card ${asset.isGroup ? "group-card" : ""} ${state.selectedAsset?.id === asset.id ? "selected" : ""}`;
  const status = displayStatus(asset);
  const actionLabel = asset.isGroup ? "展开" : "详情";
  const downloadAction = asset.isGroup
    ? `<button data-action="folder">文件夹</button>`
    : `<a href="${asset.downloadUrl}" download>下载</a>`;
  card.innerHTML = `
    <div class="preview">
      ${mediaPreview(asset)}
      <div class="badge-row">
        <span class="badge">${asset.isGroup ? `${asset.groupCount} 项` : asset.version || asset.kind}</span>
        <span class="badge">${asset.categoryLabel || asset.kind}</span>
      </div>
    </div>
    <div class="card-body">
      <p class="card-title">${asset.name}</p>
      <div class="card-meta">
        <span class="status ${statusClass(status)}">${status}</span>
        <span>${formatSize(asset.size)}</span>
      </div>
      <div class="card-actions">
        <button data-action="select">${actionLabel}</button>
        <button data-action="copy">复制</button>
        <button data-action="reveal">文件夹</button>
        ${downloadAction}
      </div>
    </div>
  `;
  card.addEventListener("click", (event) => {
    const action = event.target.closest("[data-action]")?.dataset.action;
    if (action === "copy") return copyPath(asset);
    if (action === "reveal") return openFolder(asset);
    if (action === "folder") return openFolder(asset);
    selectAsset(asset);
  });
  return card;
}

function render() {
  const currentCase = state.cases.find((item) => item.id === state.selectedCase);
  const currentProject = state.projects.find((item) => item.id === state.selectedProject);
  const breadcrumb = currentCase
    ? [currentProject?.name || "项目", ...pathParts(currentCase.relPath || currentCase.id)].join(" › ")
    : "资产看板";
  els.caseTitle.textContent = breadcrumb;
  els.caseTitle.title = breadcrumb;
  const folderOverview = folderOverviewContext();
  if (folderOverview) {
    renderFolderOverview(folderOverview);
    return;
  }
  els.assetGrid.classList.remove("folder-overview-grid");
  const assets = filteredAssets();
  renderCategoryCounts();
  const categoryName = categoryLabels[state.categoryFilter] || "全部资产";
  const rawCategoryCount = state.categoryFilter
    ? state.assets.map(enrichAsset).filter((asset) => asset.category === state.categoryFilter).length
    : state.assets.length;
  if (state.compactReverse && state.categoryFilter === "reverse" && assets.length < rawCategoryCount) {
    els.assetCount.textContent = `${categoryName}：${assets.length} 组 / 原始 ${rawCategoryCount} 个（全案 ${state.assets.length}）`;
  } else {
    els.assetCount.textContent = `${categoryName}：${assets.length} / ${state.assets.length} 个资产`;
  }
  els.assetGrid.innerHTML = "";
  if (!assets.length) {
    els.assetGrid.innerHTML = `
      <div class="empty-state">
        <h3>${categoryName}暂无资产</h3>
        <p>可以切换其他资产视图，或在生成/整理完成后手动刷新。</p>
      </div>
    `;
  } else {
    for (const asset of assets) els.assetGrid.append(renderAssetCard(asset));
  }
  renderDetail();
}

function selectAsset(asset) {
  state.selectedAsset = asset;
  render();
  if (state.deferredRefresh && !activeDetailMedia()) {
    flushDeferredRefresh().catch((error) => {
      els.refreshStatus.textContent = `刷新失败：${error.message}`;
    });
  }
}

function renderDetail() {
  const asset = state.selectedAsset;
  if (!asset) {
    els.quickMoveAsset.hidden = true;
    els.detailName.textContent = "未选择资产";
    els.detailPreview.innerHTML = "";
    delete els.detailPreview.dataset.assetId;
    els.detailPreview.classList.remove("is-portrait", "is-square", "is-landscape");
    els.detailBody.innerHTML = "选择一个资产查看详情";
    els.detailBody.className = "detail-body muted";
    return;
  }

  els.quickMoveAsset.hidden = Boolean(asset.isGroup);
  const status = displayStatus(asset);
  els.detailName.textContent = asset.name;
  if (els.detailPreview.dataset.assetId !== asset.id) {
    els.detailPreview.innerHTML = mediaPreview(asset, true);
    els.detailPreview.dataset.assetId = asset.id;
  }
  configureDetailPreviewFit();
  els.detailBody.className = "detail-body";
  if (asset.isGroup) {
    els.detailBody.innerHTML = `
      <div class="detail-row">
        <label>抽帧文件夹</label>
        <div class="mono">${absolutePath(asset)}<br>共 ${asset.groupCount} 项<br>代表资产：${asset.caseRelPath}</div>
      </div>
      <div class="detail-row">
        <label>首尾帧</label>
        <div class="mono">第一帧：${asset.groupFirst?.name || "-"}<br>最后帧：${asset.groupLast?.name || "-"}</div>
      </div>
      <div class="detail-actions">
        <button id="copyPath">复制文件夹路径</button>
        <button id="revealAsset">定位代表帧</button>
        <button id="openFolder">打开文件夹</button>
      </div>
    `;
    els.detailBody.querySelector("#copyPath").addEventListener("click", () => copyPath(asset));
    els.detailBody.querySelector("#revealAsset").addEventListener("click", () => reveal(asset));
    els.detailBody.querySelector("#openFolder").addEventListener("click", () => openFolder(asset));
    return;
  }

  els.detailBody.innerHTML = `
    <div class="detail-row">
      <label>完整路径</label>
      <div class="mono">${absolutePath(asset)}</div>
    </div>
    <div class="detail-row">
      <label>信息</label>
      <div class="mono">类型：${asset.kind}<br>版本：${asset.version || "-"}<br>大小：${formatSize(asset.size)}<br>修改：${new Date(asset.mtimeMs).toLocaleString()}<br>主代理初判：${asset.initialStatus}</div>
    </div>
    <div class="detail-row">
      <label class="status-label">用户判断 <span id="statusSaveState">${asset.userStatus ? `已保存：${asset.userStatus}` : "点击即自动保存"}</span></label>
      <div class="status-grid">
        ${userStatuses.map((item) => `<button type="button" class="${asset.userStatus === item ? "active" : ""}" data-asset-status="${item}" aria-pressed="${asset.userStatus === item}">${item}</button>`).join("")}
      </div>
    </div>
    <div class="detail-row">
      <label>备注</label>
      <textarea id="notesInput" placeholder="这里记录你觉得它能怎么用，比如 B-roll、动作局部、封面、参考图...">${asset.notes || ""}</textarea>
    </div>
    <div class="detail-actions">
      <button id="saveMeta">保存标注</button>
      <button id="moveAsset">移动素材</button>
      <button id="copyPath">复制路径</button>
      <button id="revealAsset">打开位置</button>
      <a href="${asset.downloadUrl}" download>下载文件</a>
      <button id="openFolder">打开文件夹</button>
    </div>
  `;

  els.detailBody.querySelectorAll("[data-asset-status]").forEach((button) => {
    button.addEventListener("click", () => {
      saveStatus(asset, button.dataset.assetStatus);
    });
  });
  els.detailBody.querySelector("#saveMeta").addEventListener("click", () => saveMeta(asset));
  els.detailBody.querySelector("#moveAsset").addEventListener("click", () => openMoveAssetDialog(asset));
  els.detailBody.querySelector("#copyPath").addEventListener("click", () => copyPath(asset));
  els.detailBody.querySelector("#revealAsset").addEventListener("click", () => reveal(asset));
  els.detailBody.querySelector("#openFolder").addEventListener("click", () => openFolder(asset));
}

function updateAssetMetaInState(asset) {
  const stored = state.assets.find((item) => item.id === asset.id && item.caseId === asset.caseId);
  if (stored && stored !== asset) {
    stored.userStatus = asset.userStatus;
    stored.notes = asset.notes;
  }
}

async function persistMeta(asset, notes) {
  return await api("/api/mark", {
    method: "POST",
    body: JSON.stringify({
      caseId: asset.caseId,
      projectId: asset.projectId,
      assetId: asset.caseRelPath,
      userStatus: asset.userStatus,
      notes,
      favorite: asset.favorite,
      tags: asset.tags
    })
  });
}

function updateSelectedCardStatus(asset) {
  const badge = els.assetGrid.querySelector(".asset-card.selected .status");
  if (!badge) return;
  badge.textContent = displayStatus(asset);
  badge.className = `status ${statusClass(displayStatus(asset))}`;
}

async function saveStatus(asset, nextStatus) {
  const notes = els.detailBody.querySelector("#notesInput")?.value || "";
  const previousStatus = asset.userStatus || "";
  const buttons = [...els.detailBody.querySelectorAll("[data-asset-status]")];
  const indicator = els.detailBody.querySelector("#statusSaveState");
  asset.userStatus = nextStatus;
  asset.notes = notes;
  for (const item of buttons) {
    const active = item.dataset.assetStatus === nextStatus;
    item.classList.toggle("active", active);
    item.setAttribute("aria-pressed", String(active));
    item.disabled = true;
  }
  if (indicator) indicator.textContent = "保存中…";

  try {
    await persistMeta(asset, notes);
    updateAssetMetaInState(asset);
    updateSelectedCardStatus(asset);
    if (indicator) indicator.textContent = `已保存：${nextStatus}`;
    els.refreshStatus.textContent = `用户判断已保存：${nextStatus}`;
  } catch (error) {
    asset.userStatus = previousStatus;
    for (const item of buttons) {
      const active = item.dataset.assetStatus === previousStatus;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    }
    if (indicator) indicator.textContent = "保存失败，请重试";
    els.refreshStatus.textContent = `判断保存失败：${error.message}`;
  } finally {
    for (const item of buttons) item.disabled = false;
  }
}

function showMoveAssetMessage(message, isError = false) {
  els.moveAssetMessage.textContent = message;
  els.moveAssetMessage.classList.toggle("error", isError);
}

function renderMoveTargetProjects(selectedProjectId) {
  els.moveTargetProject.innerHTML = "";
  for (const project of state.projects.filter((item) => item.exists)) {
    const option = document.createElement("option");
    option.value = project.id;
    option.textContent = project.name;
    option.selected = project.id === selectedProjectId;
    els.moveTargetProject.append(option);
  }
}

async function loadMoveTargetFolders(preferredPath = "") {
  const projectId = els.moveTargetProject.value;
  if (!projectId) return;
  els.moveTargetFolder.disabled = true;
  els.moveTargetFolder.innerHTML = '<option value="">正在读取文件夹…</option>';
  try {
    const data = await api(`/api/folders?project=${encodeURIComponent(projectId)}`);
    els.moveTargetFolder.innerHTML = "";
    for (const folder of data.folders) {
      const option = document.createElement("option");
      option.value = folder.path;
      const indent = folder.depth ? `${"　".repeat(Math.min(folder.depth, 6))}└ ` : "";
      option.textContent = `${indent}${folder.path || "项目根目录"}`;
      els.moveTargetFolder.append(option);
    }
    const available = new Set(data.folders.map((item) => item.path));
    let candidate = preferredPath;
    while (candidate && !available.has(candidate)) {
      const parent = candidate.replace(/[\\/][^\\/]+$/, "");
      if (parent === candidate) break;
      candidate = parent;
    }
    els.moveTargetFolder.value = available.has(candidate) ? candidate : "";
    if (data.truncated) showMoveAssetMessage("文件夹较多，列表只显示前 1500 个；也可以直接填写自定义文件夹。");
  } catch (error) {
    els.moveTargetFolder.innerHTML = '<option value="">读取失败</option>';
    showMoveAssetMessage(`文件夹读取失败：${error.message}`, true);
  } finally {
    els.moveTargetFolder.disabled = false;
  }
}

async function openMoveAssetDialog(asset = state.selectedAsset) {
  if (!asset || asset.isGroup) return;
  state.movingAsset = asset;
  renderMoveTargetProjects(asset.projectId);
  els.moveCustomFolder.value = "";
  els.moveTargetName.value = asset.name;
  els.moveAssetSummary.textContent = `当前：${absolutePath(asset)}`;
  showMoveAssetMessage("选择目标位置后点击“移动到这里”。");
  els.moveAssetDialog.showModal();
  await loadMoveTargetFolders(asset.dir || "");
}

async function confirmMoveAsset() {
  const asset = state.movingAsset;
  if (!asset) return;
  const targetProjectId = els.moveTargetProject.value;
  const targetDirectory = els.moveCustomFolder.value.trim() || els.moveTargetFolder.value;
  const fileName = els.moveTargetName.value.trim() || asset.name;
  if (!targetProjectId) {
    showMoveAssetMessage("请选择目标项目。", true);
    return;
  }
  els.confirmMoveAsset.disabled = true;
  showMoveAssetMessage("正在校验并移动素材…");
  try {
    const data = await api("/api/move-asset", {
      method: "POST",
      body: JSON.stringify({
        sourceProjectId: asset.projectId,
        sourcePath: asset.relPath,
        sourceCaseId: asset.caseId,
        sourceAssetId: asset.caseRelPath,
        targetProjectId,
        targetDirectory,
        fileName
      })
    });
    const destination = data.result.targetRelativePath || data.result.fileName;
    state.selectedAsset = null;
    state.movingAsset = null;
    els.moveAssetDialog.close();
    await loadProjects();
    await loadCases();
    await loadAssets();
    els.refreshStatus.textContent = `已移动到 ${data.result.targetProjectName} › ${destination}`;
  } catch (error) {
    showMoveAssetMessage(`移动失败：${error.message}`, true);
  } finally {
    els.confirmMoveAsset.disabled = false;
  }
}

async function saveMeta(asset) {
  const notes = els.detailBody.querySelector("#notesInput")?.value || "";
  asset.notes = notes;
  try {
    await persistMeta(asset, notes);
    updateAssetMetaInState(asset);
    updateSelectedCardStatus(asset);
    const indicator = els.detailBody.querySelector("#statusSaveState");
    if (indicator) indicator.textContent = asset.userStatus ? `已保存：${asset.userStatus}` : "备注已保存";
    els.refreshStatus.textContent = "标注与备注已保存";
  } catch (error) {
    els.refreshStatus.textContent = `标注保存失败：${error.message}`;
  }
}

async function copyPath(asset) {
  await navigator.clipboard.writeText(absolutePath(asset));
  els.refreshStatus.textContent = "已复制路径";
}

async function reveal(asset) {
  await api("/api/reveal", {
    method: "POST",
    body: JSON.stringify({ projectId: asset.projectId, path: asset.relPath })
  });
  els.refreshStatus.textContent = "已在文件夹中定位该素材";
}

async function openFolder(asset) {
  await api("/api/open-folder", {
    method: "POST",
    body: JSON.stringify({ projectId: asset.projectId, path: asset.relPath })
  });
  els.refreshStatus.textContent = "已打开素材所在文件夹";
}

async function addProject() {
  const name = els.projectNameInput.value.trim();
  const projectPath = els.projectPathInput.value.trim();
  const scanRoots = els.projectScanRootsInput.value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
  if (!projectPath) {
    els.refreshStatus.textContent = "请填写项目文件夹路径";
    return;
  }
  const data = await api("/api/projects", {
    method: "POST",
    body: JSON.stringify({ name, path: projectPath, scanRoots })
  });
  state.selectedProject = data.project.id;
  state.selectedCase = "";
  els.projectNameInput.value = "";
  els.projectPathInput.value = "";
  await loadProjects();
  await loadCases();
  await loadAssets();
  els.refreshStatus.textContent = "项目已添加并开始监听";
}

function wireFilters() {
  els.categoryFilters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) return;
    setCategoryFilter(button.dataset.category);
    render();
  });

  els.statusFilters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-status]");
    if (!button) return;
    state.statusFilter = button.dataset.status;
    els.statusFilters.querySelectorAll("button").forEach((item) => item.classList.toggle("active", item === button));
    render();
  });

  els.typeFilters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-type]");
    if (!button) return;
    state.typeFilter = button.dataset.type;
    els.typeFilters.querySelectorAll("button").forEach((item) => item.classList.toggle("active", item === button));
    render();
  });

  els.searchInput.addEventListener("input", () => {
    state.query = els.searchInput.value;
    render();
  });

  els.sortSelect.addEventListener("change", () => {
    state.sort = els.sortSelect.value;
    render();
  });

  els.refreshButton.addEventListener("click", loadAssets);
  els.addProjectButton.addEventListener("click", addProject);
  els.closeDetail.addEventListener("click", () => {
    state.selectedAsset = null;
    render();
    flushDeferredRefresh().catch((error) => {
      els.refreshStatus.textContent = `刷新失败：${error.message}`;
    });
  });
  els.quickMoveAsset.addEventListener("click", () => openMoveAssetDialog());
  els.moveTargetProject.addEventListener("change", () => {
    els.moveCustomFolder.value = "";
    loadMoveTargetFolders("");
  });
  els.confirmMoveAsset.addEventListener("click", confirmMoveAsset);
  els.cancelMoveAsset.addEventListener("click", () => els.moveAssetDialog.close());
  els.moveAssetDialog.addEventListener("close", () => {
    state.movingAsset = null;
  });
  document.addEventListener("keydown", (event) => {
    const tag = event.target?.tagName?.toLowerCase();
    const typing = ["input", "textarea", "select"].includes(tag) || event.target?.isContentEditable;
    if (event.key.toLowerCase() !== "m" || typing || event.ctrlKey || event.metaKey || event.altKey) return;
    if (!state.selectedAsset || state.selectedAsset.isGroup || els.moveAssetDialog.open) return;
    event.preventDefault();
    openMoveAssetDialog();
  });

  els.autoRefresh.addEventListener("change", configureAutoRefresh);
  els.compactReverse.addEventListener("change", () => {
    state.compactReverse = els.compactReverse.checked;
    render();
  });
  els.workflowEnabled.addEventListener("change", async () => {
    state.configEnabled = els.workflowEnabled.checked;
    await api("/api/toggle-enabled", {
      method: "POST",
      body: JSON.stringify({ enabled: state.configEnabled })
    });
    els.refreshStatus.textContent = state.configEnabled ? "生产任务启用资产工作台" : "简单模式：不强制登记资产";
  });

  els.generationButton.addEventListener("click", () => openGenerationDialog().catch((error) => window.alert(error.message)));
  els.refreshGenerationTickets.addEventListener("click", () => loadGenerationTickets().catch((error) => window.alert(error.message)));
  els.createGenerationTicket.addEventListener("click", () => createGenerationTicket().catch((error) => window.alert(error.message)));
  els.createAndArmGeneration.addEventListener("click", () => createGenerationTicket({ arm: true }).catch((error) => window.alert(error.message)));
  els.generationProfile.addEventListener("change", () => {
    const profile = state.automation?.routing?.profiles?.find((item) => item.id === els.generationProfile.value);
    if (profile) {
      els.generationProject.value = profile.projectId;
    }
  });
  els.generationKind.addEventListener("change", () => {
    els.generationGenerator.value = els.generationKind.value === "video" ? "tapnow" : "codex-image";
  });

  els.automationButton.addEventListener("click", openAutomationDialog);
  els.saveAutomation.addEventListener("click", () => saveAutomationSettings().catch((error) => showAutomationMessage("保存失败", error.message, true)));
  els.previewOrganizer.addEventListener("click", () => runAutomationAction("/api/automation/organizer/preview", "归档预览"));
  els.runOrganizer.addEventListener("click", () => runAutomationAction("/api/automation/organizer/run", "立即归档"));
  els.previewCleanup.addEventListener("click", () => runAutomationAction("/api/automation/cleanup/preview", "清理预览"));
  els.runCleanup.addEventListener("click", () => runAutomationAction("/api/automation/cleanup/run", "本轮清理", {
    saveFirst: true,
    confirmRun: !els.cleanupDryRun.checked
  }));
  els.useCurrentCase.addEventListener("click", () => {
    if (!state.selectedCase) {
      showAutomationMessage("没有当前案例", "请先在左侧选择一个案例。");
      return;
    }
    els.inboxProject.value = state.selectedProject;
    els.inboxBasePath.value = state.selectedCase;
  });
  els.activeProfile.addEventListener("change", async () => {
    if (!els.activeProfile.value) return;
    try {
      const data = await api("/api/automation/active-profile", {
        method: "POST",
        body: JSON.stringify({ profileId: els.activeProfile.value })
      });
      state.automation = data.automation;
      renderAutomationForm();
      showAutomationMessage("当前项目已切换", `后续通用文件将自动进入“${data.profile.name}”。`);
    } catch (error) {
      showAutomationMessage("切换失败", error.message, true);
    }
  });
  els.inboxSourcePath.addEventListener("change", () => {
    if (!els.quarantinePath.value.trim() || els.quarantinePath.value.includes(".asset-browser-quarantine")) {
      const separator = els.inboxSourcePath.value.includes("\\") ? "\\" : "/";
      els.quarantinePath.value = `${els.inboxSourcePath.value.replace(/[\\/]+$/, "")}${separator}.asset-browser-quarantine`;
    }
  });
}

function configureAutoRefresh() {
  if (state.autoRefreshTimer) clearInterval(state.autoRefreshTimer);
  state.autoRefreshTimer = null;
  if (els.autoRefresh.checked) {
    state.autoRefreshTimer = setInterval(() => {
      requestBackgroundRefresh().catch((error) => {
        els.refreshStatus.textContent = `刷新失败：${error.message}`;
      });
    }, 15000);
  }
}

function configureLiveEvents() {
  if (!window.EventSource) return;
  const source = new EventSource("/api/events");
  source.addEventListener("asset-change", async () => {
    await requestBackgroundRefresh({ reloadProjects: true, reloadCases: true });
  });
  source.addEventListener("project-change", async () => {
    await requestBackgroundRefresh({ reloadProjects: true, reloadCases: true });
  });
  source.addEventListener("config-change", async () => {
    await loadConfig();
  });
  source.addEventListener("automation-change", async () => {
    await requestBackgroundRefresh();
    if (els.automationDialog.open) {
      const status = await api("/api/automation/status");
      if (status.organizerPreview) showAutomationResult("当前收件箱", status.organizerPreview);
    }
  });
  source.addEventListener("generation-change", async () => {
    if (els.generationDialog.open) await loadGenerationTickets();
    await requestBackgroundRefresh();
  });
  source.addEventListener("connected", () => {
    els.refreshStatus.textContent = "实时监听已连接";
  });
  source.onerror = () => {
    els.refreshStatus.textContent = "实时监听断开，保留自动刷新";
  };
}

wireSidebarLayout();
wireProjectReorder();
wireFilters();
await loadConfig();
await loadProjects();
await loadCases();
setCategoryFilter(state.categoryFilter);
await loadAssets();
configureAutoRefresh();
configureLiveEvents();
