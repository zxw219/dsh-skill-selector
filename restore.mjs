#!/usr/bin/env node
/**
 * One-shot restore for a DSH skill set described by snapshots/environment.json.
 *
 *   node restore.mjs                          # 还原到 ~/.dsh/skills
 *   node restore.mjs --target "D:/skills"     # 还原到指定目录
 *   node restore.mjs --force                  # 覆盖已存在的同名技能
 *   node restore.mjs --dry-run                # 只报告，不写文件
 *   node restore.mjs --only github|bundle     # 只还原某一类来源
 *
 * Skills whose `source.type` is `github` are downloaded from the upstream repo
 * (whole repo archive, then the referenced folder is copied). Skills with
 * `source.type` is `bundle` come from snapshots/skills/<dir> inside this repo.
 */
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';

const run = promisify(execFile);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SNAPSHOT = path.join(HERE, 'snapshots', 'environment.json');
const BUNDLES = path.join(HERE, 'snapshots', 'skills');

const argv = process.argv.slice(2);
const flag = name => argv.includes('--' + name);
const value = name => {
  const i = argv.indexOf('--' + name);
  return i >= 0 ? argv[i + 1] : undefined;
};

const target = value('target') || path.join(os.homedir(), '.dsh', 'skills');
const force = flag('force');
const dryRun = flag('dry-run');
const only = value('only');

function log(...args) { process.stdout.write(args.join(' ') + '\n'); }

async function exists(p) {
  try { await fsp.access(p); return true; } catch { return false; }
}

async function copyDir(from, to) {
  await fsp.mkdir(to, { recursive: true });
  for (const entry of await fsp.readdir(from, { withFileTypes: true })) {
    const src = path.join(from, entry.name);
    const dst = path.join(to, entry.name);
    if (entry.isDirectory()) await copyDir(src, dst);
    else await fsp.copyFile(src, dst);
  }
}

async function downloadArchive(url, destFile, cwd) {
  // curl handles the Windows TLS stack more reliably than Node's fetch here.
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      await run('curl', ['-sSL', '--max-time', '180', '-o', path.basename(destFile), url], { cwd, windowsHide: true });
      const size = (await fsp.stat(destFile)).size;
      if (size < 1024) throw new Error('下载内容过小 (' + size + ' 字节)');
      return;
    } catch (error) {
      if (attempt === 3) throw error;
      log('  下载失败（' + error.message + '），重试 ' + attempt + '/3…');
      await new Promise(r => setTimeout(r, 1500 * attempt));
    }
  }
}

// Git Bash ships GNU tar, which cannot read zip. Windows' own tar.exe is bsdtar and can.
const TAR = process.platform === 'win32' && fs.existsSync('C:/Windows/System32/tar.exe')
  ? 'C:/Windows/System32/tar.exe'
  : 'tar';

async function extractArchive(archiveName, intoName, cwd) {
  await fsp.mkdir(path.join(cwd, intoName), { recursive: true });
  // Relative paths keep Windows tar from reading "C:" as a remote host.
  await run(TAR, ['-xf', archiveName, '-C', intoName], { cwd, windowsHide: true });
}

async function main() {
  const snapshot = JSON.parse(await fsp.readFile(SNAPSHOT, 'utf8'));
  const skills = (snapshot.skills || []).filter(s => !only || s.source?.type === only);

  log('快照：' + snapshot.schema + '  生成于 ' + snapshot.generatedAt);
  log('目标：' + target);
  log('技能：' + skills.length + ' 个（GitHub ' + skills.filter(s => s.source?.type === 'github').length +
      ' / 本地打包 ' + skills.filter(s => s.source?.type === 'bundle').length + '）');
  if (dryRun) log('干跑模式，不写入任何文件。\n');

  if (!dryRun) await fsp.mkdir(target, { recursive: true });

  // --- GitHub 来源：整个仓库下载一次，按 path 复制 ---
  const byRepo = new Map();
  for (const skill of skills.filter(s => s.source?.type === 'github')) {
    const key = skill.source.repo + '@' + (skill.source.ref || 'main');
    if (!byRepo.has(key)) byRepo.set(key, []);
    byRepo.get(key).push(skill);
  }

  const tmpRoot = await fsp.mkdtemp(path.join(os.tmpdir(), 'dsh-restore-'));
  let restored = 0, skipped = 0, failed = 0;

  for (const [key, list] of byRepo) {
    const [repo, ref] = key.split('@');
    const info = snapshot.restore?.sources?.[repo] || {};
    const archive = path.join(tmpRoot, repo.replace('/', '_') + '.zip');
    const unpack = path.join(tmpRoot, repo.replace('/', '_'));
    log('\n[' + repo + '] ' + list.length + ' 个技能，ref=' + ref);
    try {
      if (!dryRun) {
        await downloadArchive('https://codeload.github.com/' + repo + '/zip/' + ref, archive, tmpRoot);
        await extractArchive(path.basename(archive), path.basename(unpack), tmpRoot);
      }
      // 归档解压后多一层 <repo>-<ref> 目录
      const roots = dryRun ? [] : (await fsp.readdir(unpack, { withFileTypes: true }))
        .filter(d => d.isDirectory()).map(d => path.join(unpack, d.name));
      const root = roots[0];
      if (dryRun) { restored += list.length; log('  ✓ 干跑，跳过下载与复制'); continue; }
      for (const skill of list) {
        const from = path.join(root, skill.source.path);
        const to = path.join(target, skill.dir);
        if (!(await exists(from))) {
          log('  ✗ ' + skill.dir + ' —— 仓库里找不到 ' + skill.source.path);
          failed++;
          continue;
        }
        if (await exists(to) && !force) { skipped++; continue; }
        await copyDir(from, to);
        restored++;
      }
      log('  ✓ 完成');
    } catch (error) {
      log('  ✗ 仓库处理失败：' + error.message);
      failed += list.length;
    }
  }

  // --- 本地打包来源 ---
  const bundled = skills.filter(s => s.source?.type === 'bundle');
  if (bundled.length) {
    log('\n[bundle] ' + bundled.length + ' 个技能，来自 snapshots/skills/');
    for (const skill of bundled) {
      const from = path.join(HERE, skill.source.path);
      const to = path.join(target, skill.dir);
      if (!(await exists(from))) { log('  ✗ ' + skill.dir + ' —— 备份里不存在'); failed++; continue; }
      if (await exists(to) && !force) { skipped++; continue; }
      if (!dryRun) await copyDir(from, to);
      restored++;
    }
    log('  ✓ 完成');
  }

  await fsp.rm(tmpRoot, { recursive: true, force: true }).catch(() => {});

  log('\n=== 结果 ===');
  log('还原 ' + restored + ' | 跳过(已存在) ' + skipped + ' | 失败 ' + failed);
  if (skipped && !force) log('需要覆盖已存在的技能时加 --force。');
  log('\n插件侧还需要手动完成：');
  log('  1. 把 snapshots/environment.json 里 plugins.dependencies 合并进');
  log('     ~/.dsh/profiles/desktop/package.json 的 dependencies');
  log('  2. 把 plugins.enabled 写进该文件 dsh.profile.bundles');
  log('  3. 在 profile 目录执行 pnpm install --ignore-scripts');
  log('  4. 重启 DSH');
}

main().catch(error => { console.error(error); process.exit(1); });
