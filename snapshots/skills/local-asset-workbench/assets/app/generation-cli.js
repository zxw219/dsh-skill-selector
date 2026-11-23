import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { GenerationPipeline } from "./generation-pipeline.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const configPath = path.resolve(process.env.ASSET_BROWSER_CONFIG || path.join(__dirname, "asset-browser.config.json"));
const registryPath = path.resolve(process.env.GENERATION_TICKETS || path.join(__dirname, ".generation-tickets.json"));
const pipeline = new GenerationPipeline({ registryPath });

function parseArgs(argv) {
  const args = { _: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith("--")) {
      args._.push(item);
      continue;
    }
    const key = item.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      index += 1;
    }
  }
  return args;
}

async function loadJson(filePath) {
  return JSON.parse((await fs.readFile(path.resolve(filePath), "utf8")).replace(/^\uFEFF/, ""));
}

async function loadJsonInput(value) {
  const text = String(value || "").trim();
  if (text.startsWith("{") || text.startsWith("[")) return JSON.parse(text);
  return loadJson(text);
}

async function loadConfig() {
  const config = await loadJson(configPath);
  config.projects = (config.projects || []).map((project) => ({ ...project, path: path.resolve(project.path) }));
  return config;
}

function print(value) {
  process.stdout.write(JSON.stringify(value, null, 2) + "\n");
}

const args = parseArgs(process.argv.slice(2));
const command = args._[0] || "status";

try {
  if (command === "status") {
    print(await pipeline.status());
  } else if (command === "list") {
    print({ tickets: await pipeline.list({ limit: args.limit, status: args.status }) });
  } else if (command === "create") {
    if (!args.payload) throw new Error("create 需要 --payload <任务JSON>");
    const payload = await loadJsonInput(args.payload);
    print(await pipeline.create(payload, await loadConfig()));
  } else if (command === "arm") {
    const config = await loadConfig();
    const sourcePath = args.source || config.automation?.inbox?.sourcePath;
    print(await pipeline.arm(args.ticket, { sourcePath }));
  } else if (command === "generated") {
    const extra = args.payload ? await loadJsonInput(args.payload) : {};
    print(await pipeline.markGenerated(args.ticket, extra));
  } else if (command === "attach") {
    if (!args.ticket || !args.source) throw new Error("attach 需要 --ticket 和 --source");
    print(await pipeline.attach(args.ticket, {
      sourcePath: args.source,
      moveSource: args.move === true || args.move === "true",
      nameStem: args.name || ""
    }, await loadConfig()));
  } else if (command === "cancel") {
    print(await pipeline.cancel(args.ticket, args.reason || ""));
  } else {
    throw new Error(`未知命令：${command}`);
  }
} catch (error) {
  process.stderr.write(`${error.message || error}\n`);
  process.exitCode = 1;
}
