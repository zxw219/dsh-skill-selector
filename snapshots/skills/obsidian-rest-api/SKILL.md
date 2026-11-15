---
name: obsidian-rest-api
description: 使用 Obsidian Local REST API 插件连接、验证和排查本地 Obsidian 库。用于检查插件安装与启用状态、自动读取 HTTPS 或 HTTP 端口、验证 API Key、检测本地 API 是否可访问，以及在用户明确授权后通过 API 读取或修改笔记。只使用 Local REST API，不配置或排查 Codex MCP。
---

# Obsidian Local REST API

## 用途

只通过 Obsidian 的 **Local REST API** 插件连接本地库。不要配置 Codex MCP，不要运行 `codex mcp`，不要修改 `config.toml`。

## 默认安全规则

- 先只读检查；连接检测不修改任何笔记或设置。
- 永远不要输出完整 API Key；日志和错误信息中必须隐藏密钥。
- 不要默认打印笔记正文，只报告状态、数量和路径。
- 只连接 `127.0.0.1`，不要把 API Key 发送给远程地址。
- 忽略自签名证书仅限本机 `https://127.0.0.1`。
- 创建、覆盖、移动、重命名或删除笔记前，先说明具体文件和操作并获得用户确认。
- 修改插件设置、端口或 API Key 前也必须获得用户确认。

## 快速检查流程

1. 确认目标库路径；默认从当前目录向上查找 `.obsidian`。
2. 检查 `.obsidian/plugins/obsidian-local-rest-api/` 是否存在。
3. 检查 `.obsidian/community-plugins.json` 是否启用了 `obsidian-local-rest-api`。
4. 从插件 `data.json` 自动读取协议、端口和 API Key，不假设端口固定为 `27124`。
5. 请求 `/` 检查服务是否运行。
6. 请求 `/commands/` 检查 API Key 认证是否有效。
7. 如果库中有 Markdown 笔记，可只读请求一个具体笔记验证读取能力，但不要输出正文。
8. `/vault/` 返回 404 不能单独证明连接失败；不要把它作为唯一成功标准。

## 运行检测脚本

在库根目录执行：

```powershell
python "C:\Users\Administrator\.codex\skills\obsidian-rest-api\scripts\check_obsidian_rest.py"
```

从其他目录指定库路径：

```powershell
python "C:\Users\Administrator\.codex\skills\obsidian-rest-api\scripts\check_obsidian_rest.py" --vault "C:\路径\到\Obsidian库"
```

如果只想检查连接、不读取任何笔记：

```powershell
python "C:\Users\Administrator\.codex\skills\obsidian-rest-api\scripts\check_obsidian_rest.py" --vault "C:\路径\到\Obsidian库" --skip-note-read
```

机器可读输出：

```powershell
python "C:\Users\Administrator\.codex\skills\obsidian-rest-api\scripts\check_obsidian_rest.py" --json
```

## 结果判断

满足以下条件即可报告“Obsidian 已通过 Local REST API 连接”：

- 插件配置存在；
- API Key 存在但未被打印；
- `/` 返回 HTTP 2xx；
- `/commands/` 返回 HTTP 2xx，证明认证有效。

补充说明：

- 没有 Markdown 笔记时，无法验证具体笔记读取，但不影响基础连接结论。
- `/active/` 在没有打开活动笔记时可能报错，不应判定为连接失败。
- API 可访问时，即使系统端口枚举没有显示监听，也以实际 HTTPS/HTTP 请求结果为准。

## 常见故障

- `data.json` 不存在：插件未安装或目标路径不是正确的库。
- 插件已安装但未启用：检查 `community-plugins.json`，然后让用户在 Obsidian 中启用插件。
- 连接被拒绝或超时：确认 Obsidian 正在运行，并检查插件服务是否启用。
- HTTP 401/403：API Key 无效或插件配置与运行实例不一致；不要输出密钥。
- HTTPS 证书错误：本机检测使用 Python 的本地未验证证书上下文，不要把此做法扩展到远程主机。
- 具体笔记返回 404：检查相对路径和 URL 编码；基础连接与笔记路径问题要分开报告。
- **`/`、`/commands/`、`/vault/` 都 200，但 `/vault/<某笔记.md>` 持续 TimeoutError** —— 这是真实遇到过的情况：库内含超大目录（本例 `Higgsfield离线案例库/` 约 30 万文件、14 万 webp），Obsidian 主线程被文件索引占满，插件的笔记读取请求排在队列里永远拿不到响应。
  - 判定方法：连续拉长超时（30s→60s→90s）仍全部超时，且 `Get-Process Obsidian` 里某个进程 CPU 恒定接近满载、内存 800MB+，即可确认不是路径写错。
  - 此时**只能如实报告「基础连接有效、笔记读取被阻塞」**，不要谎报读取成功。
  - 建议用户：把超大非笔记目录移出库、或在 Obsidian 设置里把它加进「排除的文件」/关闭其文件监听，重启 Obsidian 后恢复。
  - **替代方案（推荐）**：日常读写库内笔记直接用文件系统工具（Read/Write/Edit），它和 REST API 指向同一批文件，且不受插件阻塞影响。只有需要「触发 Obsidian 内部动作」（打开笔记、执行命令、让 Obsidian 感知变更）时才必须走 REST API。
- `python -c` 内联脚本里若在 `try` 中用了 `except ... as e` 之后再 `except Exception as e`，变量 `e` 作用域没问题；但**`urllib.parse.quote` 遇到非 ASCII 路径必须先 quote 再拼 URL**，否则抛 `UnicodeEncodeError`（不是 HTTP 错误，容易误判）。
- 批量端点探测建议写成一个临时 `.py` 文件跑，不要用长 `python -c`——Git Bash + 多层引号 + 中文路径极易出错。

## 写入操作

只有用户明确要求并确认具体变更后，才允许调用写入接口。执行前必须列出：

- 操作类型；
- 目标笔记的库内相对路径；
- 是新建、追加还是覆盖；
- 是否存在覆盖或删除风险。

完成后报告修改了哪些笔记以及如何在 Obsidian 中验证。

## 报告格式

```text
结果：
- Obsidian 库：<路径>
- 插件：已安装/未安装，已启用/未启用
- 本地 API：已连接/未连接
- API 认证：有效/无效/未测试
- 笔记读取：成功/失败/无笔记未测试

说明：
- 本次是否只读
- 是否修改了任何文件或设置
- 需要用户执行的下一步
```
