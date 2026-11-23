import { createHash, randomBytes } from "node:crypto";
import { createReadStream, promises as fs } from "node:fs";
import path from "node:path";

const IMAGE_EXTS = new Set([".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"]);
const VIDEO_EXTS = new Set([".mp4", ".mov", ".m4v", ".webm", ".mkv"]);
const TEMP_EXTS = new Set([".crdownload", ".part", ".partial", ".tmp", ".download"]);

function pad(value, size = 2) {
  return String(value).padStart(size, "0");
}

function localDateParts(date = new Date()) {
  return {
    date: `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`,
    compactDate: `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}`,
    compactTime: `${pad(date.getHours())}${pad(date.getMinutes())}${pad(date.getSeconds())}`
  };
}

function cleanSegment(value, fallback = "") {
  const text = String(value ?? "")
    .trim()
    .replace(/[<>:"/\\|?*\x00-\x1F]/g, "-")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^[.\s-]+|[.\s-]+$/g, "");
  return text || fallback;
}

function cleanRelative(value, label = "目标目录") {
  const raw = String(value ?? "").trim().replace(/\//g, path.sep);
  if (!raw || raw === ".") return "";
  if (path.isAbsolute(raw)) throw new Error(`${label}必须是项目内的相对路径`);
  const normalized = path.normalize(raw).replace(/^[.][\\/]/, "");
  if (normalized === ".." || normalized.startsWith(`..${path.sep}`)) {
    throw new Error(`${label}不能跳出项目文件夹`);
  }
  return normalized;
}

function isInside(root, target) {
  const relative = path.relative(path.resolve(root), path.resolve(target));
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function assetKind(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (IMAGE_EXTS.has(ext)) return "image";
  if (VIDEO_EXTS.has(ext)) return "video";
  return "other";
}

function isTemporary(filePath) {
  const lower = path.basename(filePath).toLowerCase();
  return [...TEMP_EXTS].some((ext) => lower.endsWith(ext));
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function hashFile(filePath) {
  return await new Promise((resolve, reject) => {
    const hash = createHash("sha256");
    const input = createReadStream(filePath);
    input.on("error", reject);
    input.on("data", (chunk) => hash.update(chunk));
    input.on("end", () => resolve(hash.digest("hex")));
  });
}

async function uniquePath(desiredPath) {
  if (!await exists(desiredPath)) return desiredPath;
  const dir = path.dirname(desiredPath);
  const ext = path.extname(desiredPath);
  const stem = path.basename(desiredPath, ext);
  for (let index = 2; index < 10000; index += 1) {
    const candidate = path.join(dir, `${stem}-${pad(index)}${ext}`);
    if (!await exists(candidate)) return candidate;
  }
  throw new Error("目标目录中同名文件过多，无法生成安全文件名");
}

function projectFor(config, projectId) {
  const project = (config.projects || []).find((item) => item.id === projectId);
  if (!project) throw new Error(`项目不存在：${projectId || "未指定"}`);
  return { ...project, path: path.resolve(project.path) };
}

function profileFor(config, profileId) {
  if (!profileId) return null;
  return (config.automation?.routing?.profiles || []).find((item) => item.id === profileId) || null;
}

function defaultDestination(config, input, project, profile, date) {
  if (input.destinationPath != null && String(input.destinationPath).trim()) {
    return cleanRelative(input.destinationPath, "生成资产目录");
  }

  const basePath = cleanRelative(input.basePath ?? profile?.basePath ?? "", "项目基础目录");
  const kindLabel = input.kind === "video" ? "视频" : "图片";
  let tail;
  if (profile?.id === "daily-practice" || project.id === "daily-practice") {
    tail = path.join(date, kindLabel);
  } else {
    tail = path.join("生成资产", date, kindLabel);
  }
  return cleanRelative(path.join(basePath, tail), "生成资产目录");
}

function buildNameStem(input, now) {
  if (String(input.nameStem || "").trim()) return cleanSegment(input.nameStem, "生成资产");
  const versionNumber = Number.parseInt(input.version, 10);
  const parts = [input.episode, input.scene, input.shot, input.role]
    .map((item) => cleanSegment(item))
    .filter(Boolean);
  if (Number.isFinite(versionNumber) && versionNumber > 0) parts.push(`v${pad(versionNumber, 3)}`);
  if (!parts.length) {
    const stamp = localDateParts(now);
    parts.push(cleanSegment(input.generator, "generation"), input.kind || "asset", `${stamp.compactDate}-${stamp.compactTime}`);
  }
  return cleanSegment(parts.join("_"), "生成资产");
}

function makeTicketId(now = new Date()) {
  const stamp = localDateParts(now);
  return `gen-${stamp.compactDate}-${stamp.compactTime}-${randomBytes(2).toString("hex")}`;
}

function relativeOrAbsolute(projectRoot, filePath) {
  return isInside(projectRoot, filePath) ? path.relative(projectRoot, filePath) : path.resolve(filePath);
}

function promptMarkdown(ticket, output, project) {
  const references = (ticket.references || []).length
    ? ticket.references.map((item) => `- ${item}`).join("\n")
    : "- 无登记参考素材";
  const settings = Object.keys(ticket.settings || {}).length
    ? `\n\n## 生成参数\n\n\`\`\`json\n${JSON.stringify(ticket.settings, null, 2)}\n\`\`\``
    : "";
  return `# 生成提示词与结果记录

- 项目：${project.name || project.id}
- 类型：${ticket.kind === "video" ? "视频" : "图片"}
- 生成工具：${ticket.generator || "未登记"}
- 模型：${ticket.model || "未登记"}
- 集数：${ticket.episode || "-"}
- 场景：${ticket.scene || "-"}
- 镜头：${ticket.shot || "-"}
- 资产角色：${ticket.role || "-"}
- 版本：${ticket.version || "-"}
- 任务创建：${ticket.createdAt}
- 结果归档：${output.archivedAt}
- 结果文件：${output.relativePath}
- SHA-256：${output.sha256}

## 正向提示词

${ticket.prompt || "（未登记）"}

## 负向提示词 / 稳定性约束

${ticket.negativePrompt || "（未登记）"}

## 参考素材

${references}${settings}

## 备注

${ticket.notes || "（无）"}
`;
}

export class GenerationPipeline {
  constructor({ registryPath }) {
    this.registryPath = path.resolve(registryPath);
    this.lockPath = `${this.registryPath}.lock`;
  }

  async withLock(operation) {
    await fs.mkdir(path.dirname(this.registryPath), { recursive: true });
    let handle = null;
    for (let attempt = 0; attempt < 100; attempt += 1) {
      try {
        handle = await fs.open(this.lockPath, "wx");
        break;
      } catch (error) {
        if (error.code !== "EEXIST") throw error;
        await new Promise((resolve) => setTimeout(resolve, 50));
      }
    }
    if (!handle) throw new Error("生成任务正在被另一个操作更新，请稍后再试");
    try {
      return await operation();
    } finally {
      await handle.close().catch(() => {});
      await fs.rm(this.lockPath, { force: true }).catch(() => {});
    }
  }

  async readRegistry() {
    try {
      const data = JSON.parse((await fs.readFile(this.registryPath, "utf8")).replace(/^\uFEFF/, ""));
      return { version: 1, tickets: Array.isArray(data.tickets) ? data.tickets : [] };
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
      return { version: 1, tickets: [] };
    }
  }

  async writeRegistry(registry) {
    const temporaryPath = `${this.registryPath}.tmp`;
    await fs.mkdir(path.dirname(this.registryPath), { recursive: true });
    await fs.writeFile(temporaryPath, JSON.stringify(registry, null, 2) + "\n", "utf8");
    await fs.rename(temporaryPath, this.registryPath);
  }

  async list({ limit = 100, status = "" } = {}) {
    const registry = await this.readRegistry();
    const statuses = String(status || "").split(",").map((item) => item.trim()).filter(Boolean);
    return registry.tickets
      .filter((ticket) => !statuses.length || statuses.includes(ticket.status))
      .sort((a, b) => Date.parse(b.updatedAt || b.createdAt) - Date.parse(a.updatedAt || a.createdAt))
      .slice(0, Math.max(1, Math.min(Number(limit) || 100, 500)));
  }

  async get(ticketId) {
    const registry = await this.readRegistry();
    const ticket = registry.tickets.find((item) => item.id === ticketId);
    if (!ticket) throw new Error(`生成任务不存在：${ticketId}`);
    return ticket;
  }

  async status() {
    const tickets = await this.list({ limit: 500 });
    const counts = {};
    for (const ticket of tickets) counts[ticket.status] = (counts[ticket.status] || 0) + 1;
    return {
      counts,
      active: tickets.filter((ticket) => ["draft", "awaiting_download", "generated"].includes(ticket.status)),
      recent: tickets.slice(0, 30)
    };
  }

  async create(input, config) {
    return await this.withLock(async () => {
      const now = new Date();
      const kind = input.kind === "video" ? "video" : "image";
      const project = projectFor(config, input.projectId);
      const profile = profileFor(config, input.profileId);
      if (profile && profile.projectId !== project.id) throw new Error("生成任务的项目和分流项目不一致");
      const destinationRelativePath = defaultDestination(config, { ...input, kind }, project, profile, localDateParts(now).date);
      const destinationPath = path.resolve(project.path, destinationRelativePath);
      if (!isInside(project.path, destinationPath)) throw new Error("生成资产目录跳出了项目文件夹");
      const versionNumber = Number.parseInt(input.version, 10);
      const ticket = {
        id: makeTicketId(now),
        projectId: project.id,
        projectName: project.name || project.id,
        profileId: profile?.id || "",
        profileName: profile?.name || "",
        kind,
        generator: cleanSegment(input.generator, kind === "video" ? "tapnow" : "codex-image"),
        model: String(input.model || "").trim(),
        episode: String(input.episode || "").trim(),
        scene: String(input.scene || "").trim(),
        shot: String(input.shot || "").trim(),
        role: String(input.role || "").trim(),
        version: Number.isFinite(versionNumber) && versionNumber > 0 ? versionNumber : 1,
        nameStem: buildNameStem({ ...input, kind }, now),
        destinationRelativePath,
        prompt: String(input.prompt || "").trim(),
        negativePrompt: String(input.negativePrompt || "").trim(),
        references: Array.isArray(input.references) ? input.references.map(String).filter(Boolean) : [],
        settings: input.settings && typeof input.settings === "object" && !Array.isArray(input.settings) ? input.settings : {},
        notes: String(input.notes || "").trim(),
        sourceContext: input.sourceContext && typeof input.sourceContext === "object" ? input.sourceContext : {},
        status: "draft",
        outputs: [],
        createdAt: now.toISOString(),
        updatedAt: now.toISOString()
      };
      const registry = await this.readRegistry();
      registry.tickets.push(ticket);
      await this.writeRegistry(registry);
      return { ...ticket, destinationPath, expectedName: ticket.nameStem };
    });
  }

  async arm(ticketId, { sourcePath = "" } = {}) {
    return await this.withLock(async () => {
      const registry = await this.readRegistry();
      const ticket = registry.tickets.find((item) => item.id === ticketId);
      if (!ticket) throw new Error(`生成任务不存在：${ticketId}`);
      const inboxPath = path.resolve(sourcePath);
      if (!sourcePath || !await exists(inboxPath)) throw new Error("下载文件夹不存在，无法等待下一个结果");
      const conflictingTicket = registry.tickets.find((item) => item.id !== ticket.id
        && item.status === "awaiting_download"
        && item.kind === ticket.kind
        && item.inboxPath
        && path.resolve(item.inboxPath).toLowerCase() === inboxPath.toLowerCase());
      if (conflictingTicket) {
        throw new Error(`已有同类型下载任务正在等待：${conflictingTicket.id}。请先完成/取消它，或使用 TapNow 资产 ID 直接绑定。`);
      }
      const baseline = [];
      for (const entry of await fs.readdir(inboxPath, { withFileTypes: true })) {
        if (!entry.isFile() || isTemporary(entry.name)) continue;
        const fullPath = path.join(inboxPath, entry.name);
        const stats = await fs.stat(fullPath);
        baseline.push(`${entry.name}|${stats.size}|${stats.mtimeMs}`);
      }
      ticket.status = "awaiting_download";
      ticket.armedAt = new Date().toISOString();
      ticket.inboxPath = inboxPath;
      ticket.inboxBaseline = baseline;
      ticket.updatedAt = ticket.armedAt;
      await this.writeRegistry(registry);
      return ticket;
    });
  }

  async markGenerated(ticketId, extra = {}) {
    return await this.withLock(async () => {
      const registry = await this.readRegistry();
      const ticket = registry.tickets.find((item) => item.id === ticketId);
      if (!ticket) throw new Error(`生成任务不存在：${ticketId}`);
      ticket.status = "generated";
      ticket.generatorResult = { ...(ticket.generatorResult || {}), ...extra };
      ticket.updatedAt = new Date().toISOString();
      await this.writeRegistry(registry);
      return ticket;
    });
  }

  async cancel(ticketId, reason = "") {
    return await this.withLock(async () => {
      const registry = await this.readRegistry();
      const ticket = registry.tickets.find((item) => item.id === ticketId);
      if (!ticket) throw new Error(`生成任务不存在：${ticketId}`);
      ticket.status = "cancelled";
      ticket.cancelReason = String(reason || "").trim();
      ticket.updatedAt = new Date().toISOString();
      await this.writeRegistry(registry);
      return ticket;
    });
  }

  async attach(ticketId, input, config) {
    return await this.withLock(async () => {
      const registry = await this.readRegistry();
      const ticket = registry.tickets.find((item) => item.id === ticketId);
      if (!ticket) throw new Error(`生成任务不存在：${ticketId}`);
      const project = projectFor(config, ticket.projectId);
      const sourcePath = path.resolve(String(input.sourcePath || ""));
      const sourceStats = await fs.stat(sourcePath);
      if (!sourceStats.isFile()) throw new Error("生成结果不是文件");
      const kind = assetKind(sourcePath);
      if (kind !== ticket.kind) throw new Error(`文件类型与任务不一致：任务是 ${ticket.kind}，文件是 ${kind}`);

      const destinationDir = path.resolve(project.path, cleanRelative(ticket.destinationRelativePath, "生成资产目录"));
      if (!isInside(project.path, destinationDir)) throw new Error("生成资产目录跳出了项目文件夹");
      await fs.mkdir(destinationDir, { recursive: true });
      const ext = path.extname(sourcePath).toLowerCase();
      const baseStem = cleanSegment(input.nameStem || ticket.nameStem, "生成资产");
      const takeSuffix = ticket.outputs.length ? `_take${pad(ticket.outputs.length + 1)}` : "";
      const requestedPath = path.join(destinationDir, `${baseStem}${takeSuffix}${ext}`);
      const sourceHash = await hashFile(sourcePath);
      const duplicateOutput = ticket.outputs.find((item) => item.sha256 === sourceHash && item.path);
      if (duplicateOutput && await exists(duplicateOutput.path) && await hashFile(duplicateOutput.path) === sourceHash) {
        const sourceIsArchivedOutput = path.resolve(sourcePath).toLowerCase() === path.resolve(duplicateOutput.path).toLowerCase();
        if (input.moveSource === true && !sourceIsArchivedOutput) await fs.rm(sourcePath, { force: false });
        ticket.status = "archived";
        ticket.updatedAt = new Date().toISOString();
        ticket.inboxBaseline = undefined;
        await this.writeRegistry(registry);
        return {
          ticket,
          output: duplicateOutput,
          ledgerPath: path.join(project.path, "生成记录", "生成资产台账.jsonl"),
          duplicate: true
        };
      }

      const sourceIsRequestedPath = path.resolve(sourcePath).toLowerCase() === path.resolve(requestedPath).toLowerCase();
      const destinationPath = sourceIsRequestedPath ? requestedPath : await uniquePath(requestedPath);
      const sameFile = path.resolve(sourcePath).toLowerCase() === path.resolve(destinationPath).toLowerCase();
      let sha256 = sourceHash;

      if (!sameFile) {
        const temporaryPath = path.join(destinationDir, `.${path.basename(destinationPath)}.${ticket.id}.partial`);
        await fs.copyFile(sourcePath, temporaryPath);
        const copiedHash = await hashFile(temporaryPath);
        if (sourceHash !== copiedHash) {
          await fs.rm(temporaryPath, { force: true });
          throw new Error("生成结果归档校验失败，源文件保持不动");
        }
        await fs.rename(temporaryPath, destinationPath);
        if (input.moveSource === true) await fs.rm(sourcePath, { force: false });
      }
      const archivedStats = await fs.stat(destinationPath);
      const archivedAt = new Date().toISOString();
      const relativePath = path.relative(project.path, destinationPath);
      const output = {
        id: `${ticket.id}-out-${pad(ticket.outputs.length + 1)}`,
        path: destinationPath,
        relativePath,
        sourcePath: relativeOrAbsolute(project.path, sourcePath),
        fileName: path.basename(destinationPath),
        size: archivedStats.size,
        sha256,
        archivedAt,
        movedSource: input.moveSource === true && !sameFile
      };
      const stemPath = destinationPath.slice(0, -ext.length);
      const promptPath = `${stemPath}.prompt.md`;
      const metaPath = `${stemPath}.meta.json`;
      output.promptPath = promptPath;
      output.metaPath = metaPath;
      await fs.writeFile(promptPath, promptMarkdown(ticket, output, project), "utf8");
      await fs.writeFile(metaPath, JSON.stringify({
        schemaVersion: 1,
        ticket: { ...ticket, outputs: undefined, inboxBaseline: undefined },
        output,
        project: { id: project.id, name: project.name || project.id, path: project.path }
      }, null, 2) + "\n", "utf8");

      const ledgerDir = path.join(project.path, "生成记录");
      await fs.mkdir(ledgerDir, { recursive: true });
      const ledgerPath = path.join(ledgerDir, "生成资产台账.jsonl");
      await fs.appendFile(ledgerPath, JSON.stringify({
        schemaVersion: 1,
        ticketId: ticket.id,
        projectId: ticket.projectId,
        kind: ticket.kind,
        generator: ticket.generator,
        model: ticket.model,
        prompt: ticket.prompt,
        negativePrompt: ticket.negativePrompt,
        references: ticket.references,
        settings: ticket.settings,
        episode: ticket.episode,
        scene: ticket.scene,
        shot: ticket.shot,
        role: ticket.role,
        version: ticket.version,
        output
      }) + "\n", "utf8");

      ticket.outputs.push(output);
      ticket.status = "archived";
      ticket.updatedAt = archivedAt;
      ticket.inboxBaseline = undefined;
      await this.writeRegistry(registry);
      return { ticket, output, ledgerPath };
    });
  }

  async claimArmedDownloads(config, { settleSeconds = 4 } = {}) {
    const tickets = (await this.list({ limit: 100, status: "awaiting_download" }))
      .sort((a, b) => Date.parse(a.armedAt) - Date.parse(b.armedAt));
    const claimed = [];
    const reservedPaths = new Set();
    for (const ticket of tickets) {
      const inboxPath = ticket.inboxPath;
      if (!inboxPath || !await exists(inboxPath)) continue;
      const baseline = new Set(ticket.inboxBaseline || []);
      const candidates = [];
      for (const entry of await fs.readdir(inboxPath, { withFileTypes: true })) {
        if (!entry.isFile() || isTemporary(entry.name)) continue;
        const fullPath = path.join(inboxPath, entry.name);
        if (reservedPaths.has(fullPath.toLowerCase()) || assetKind(fullPath) !== ticket.kind) continue;
        const stats = await fs.stat(fullPath);
        const fingerprint = `${entry.name}|${stats.size}|${stats.mtimeMs}`;
        if (baseline.has(fingerprint)) continue;
        if (stats.mtimeMs < Date.parse(ticket.armedAt) - 2000) continue;
        if (Date.now() - stats.mtimeMs < Math.max(1, settleSeconds) * 1000) continue;
        candidates.push({ fullPath, mtimeMs: stats.mtimeMs });
      }
      candidates.sort((a, b) => a.mtimeMs - b.mtimeMs);
      const candidate = candidates[0];
      if (!candidate) continue;
      reservedPaths.add(candidate.fullPath.toLowerCase());
      claimed.push(await this.attach(ticket.id, { sourcePath: candidate.fullPath, moveSource: true }, config));
    }
    return claimed;
  }
}

export function generationAssetKind(filePath) {
  return assetKind(filePath);
}
