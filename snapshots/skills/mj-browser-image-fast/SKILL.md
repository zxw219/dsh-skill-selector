---
name: mj-browser-image-fast
description: MJ 快速提交版。一次调用把整串 /imagine 粘进 Discord 空输入框并回车，不做候选菜单、不做二次确认、不查结果，只回一行结论。用于已知频道和参数的高频重复提交；首次配置、需要参考图、需要离线教学或需要看结果时用完整版 mj-browser-image。
---

# MJ 快速提交

完整版 `mj-browser-image` 的加速分支。差别只有三条：

1. **不选命令菜单**——把整串 `/imagine prompt: …` 一次粘进空输入框，Discord 自己解析成命令表单。
2. **不做事后核查**——脚本内部判定完就返回一行，不再额外查 Bot 回执、不截图。
3. **不解释**——拿到提示词直接执行，只回一行结论。

参数约定、频道、账号、离线资料全部沿用 `mj-browser-image`，本技能不重复维护。两者可以并存，互不影响。

**完整版资料在磁盘上的位置**（需要查官方文档、截图或手动操作教学时直接读，不要联网搜索）：

```
C:\Users\Administrator\.dsh\skills\mj-browser-image\
├─ references\offline-help.md                     问题路由入口
├─ references\midjourney-official\index.md        官方资料索引
├─ references\midjourney-official\docs\           46 篇官方文档（01_… 到 46_…）
├─ references\midjourney-official\assets\         各篇配套截图
└─ references\midjourney-official\assets\videos\  11 个官方视频
```

只读，不要修改完整版目录下的任何文件。

## 何时用

- 已在同一对话确认过频道、账号、模型参数，只是继续出图。
- 重复提交、批量提交、需要压到 3 秒内。

## 何时不要用

- 需要参考图 / 垫图 / `--sref` / 局部重绘 —— 用完整版。
- 需要改动频道或账号 —— 先确认再执行。
- 首次连接、扩展掉线、需要排查 —— 用完整版。

## 调用

```powershell
# PowerShell 7
pwsh -NoProfile -STA -File 'C:\Users\Administrator\.dsh\skills\mj-browser-image-fast\scripts\submit-fast.ps1' `
  -Prompt '<完整提示词含参数>' `
  -ChannelUrl 'https://discord.com/channels/<guild>/<channel>' `
  -BrowserInstance '<bsk browsers 里的 instance_id>' `
  -AccountLabel '<用户状态区账号按钮标签>'
```

可用 `-SessionId <已有会话>` 复用同一窗口（更快，省掉新建+导航）；会话已失效时脚本会自动新建，不会报错停在半路。

加 `-NoSubmit` 只走到「命令表单已成型且内容校验通过」就停，不按 Enter——用于干跑。

## 返回

脚本只输出一行：

```
SUBMITTED 16:47:05 elapsed=2.55s session=rhat tab=337889505
```

或失败：

```
FAILED stage=paste reason="..." elapsed=1.2s  sent=false
```

- `SUBMITTED` 表示**已按 Enter 且输入框已清空**。按约定这就算完成，不再查 Bot 回执、不等待出图、不下载。
- `FAILED` 里带 `sent=true` 表示不确定是否已发出，此时不要重试，先让宿主看一眼频道。
- 提示词里没有 `--ar` / `--aspect` 时，脚本**照常提交**，但在第二行追加 `WARN: no --ar in prompt, Midjourney will use its 1:1 default`。看到这行要把它原样转给宿主——出图比例会和预期不符。本脚本只警告这一项，不补参数、不拦其他参数缺失。

## 硬规则

- 提示词按宿主原文执行，不翻译、不精简、不补参数。
- 输入框非空时**不覆盖**，直接失败报出——里面可能是宿主的草稿。
- 失败不自动重试、不换账号、不切官网。
- 不修改完整版技能、不改 BrowserSkill 或扩展。
