---
name: local-asset-workbench
description: 本地资产工作台工具：在Windows上安装、配置和操作图片、视频、音频资产浏览与整理工作台，支持项目分类、案例管理、拖拽排序、预览和故障排查。用于本地创作资产管理。
version: 1.0.0
---

# 本地资产工作台

使用本 Skill 内的通用应用副本部署资产工作台。不要带入创建者的项目名、用户名、磁盘路径或历史台账。

## 安装流程

1. 确认操作系统、Node.js 与目标目录。Windows 为完整支持环境。
2. 用户未指定路径时，使用：
   - 程序：`%LOCALAPPDATA%\LocalAssetWorkbench`
   - 数据：`%USERPROFILE%\Documents\AssetWorkbenchData`
3. 运行安装脚本：

```powershell
powershell -ExecutionPolicy Bypass -File "<skill目录>\scripts\install_asset_workbench.ps1"
```

常用参数：

```powershell
-InstallDir "D:\Apps\LocalAssetWorkbench"
-WorkspaceRoot "D:\资产工作台"
-PrimaryProjectPath "D:\项目"
-DailyPracticePath "D:\每日练习"
-NodePath "C:\Program Files\nodejs\node.exe"
-Port 5177
```

4. 默认保留已有 `asset-browser.config.json`。只有全新部署或用户明确要求重置时才使用 `-ResetConfig`。
5. 默认创建桌面快捷方式并启动工作台。批量部署或测试时使用 `-NoShortcut -SkipStart`。

Node.js 不在 PATH 时，先调用工作区依赖定位工具寻找可用 Node，再把绝对路径传给 `-NodePath`。不要修改系统 PATH 作为首选方案。

## 接入用户项目

- 已有项目优先直接注册原文件夹，不复制全库。
- 默认 `scanRoots: ["."]`；只有用户目录有明确扫描入口时才缩小范围。
- 项目 ID 使用小写字母、数字和连字符。
- 保持项目路径绝对化，并确认目录存在。
- 需要配置下载分流、清理或生成任务时，读取 [references/configuration.md](references/configuration.md)。

## 默认交互规则

保留并验证以下行为：

- 左栏统一滚动，不在项目与目录中嵌套独立滚动区。
- 项目顺序可拖动并写入配置。
- 左栏模块可折叠、可拖动，布局保存在浏览器本地。
- 参考库项目递归读取多级目录；顶层目录以可折叠分组显示，点击“全部”先呈现子目录拼图封面，进入子目录后再浏览具体素材。
- 横屏、方形与竖屏素材使用不同的详情预览高度，始终 `object-fit: contain`。
- 素材卡的“文件夹”直接打开所在目录；详情“打开位置”在资源管理器中选中文件。
- 详情中存在视频或音频时，自动刷新延后；关闭预览后补刷。
- 生成结果旁保存 `.prompt.md`、`.meta.json` 与项目级 JSONL 台账。
- 新写入的图片按文件内容计算 SHA-256；同一目录中内容完全相同的副本只保留一张。
- 带生成提示词或元数据边车的已登记图片优先保留；只隔离与它内容完全相同的未登记副本。
- “用户判断”按钮点击后立即保存，刷新页面后仍保留，不要求再点一次“保存标注”。
- 选中素材后，允许通过详情顶部“移动”、详情操作区“移动素材”或快捷键 `M` 打开移动窗口。
- 移动时可选择其他项目、已有文件夹、手填项目内相对目录并修改文件名；素材的 `.prompt.md`、`.meta.json` 与“用户判断”标注必须一起迁移。
- 移动目标存在同名素材时自动生成 `-02`、`-03` 后缀，禁止覆盖；完成复制与 SHA-256 校验后才删除源文件。

## 重复图片处理

- 默认开启，只处理字节完全一致的图片，不按文件名、尺寸或视觉相似度猜测。
- 新图片稳定写入 5 秒后检查；启动时补扫最近 7 天的图片。
- 优先保留原始命名、较早创建的文件，把其余副本移入安装目录的 `duplicate-quarantine`。
- 如果重复组中存在带 `.prompt.md` 或 `.meta.json` 的已登记资产，优先保留已登记版本；多个已登记生成尝试不会互相删除。
- 隔离副本保留 14 天后自动清除，并在 `.duplicate-cleanup-ledger.json` 中记录原路径、保留文件、哈希和隔离位置。
- 同一生成任务重复绑定同一内容时复用已有输出，不再创建 `_take02` 或 `-02` 副本。

## 下载整理安全

- 首次启用使用复制模式。
- 清理默认 dry-run。
- 永久清理前必须获得用户明确确认。
- 只处理已稳定完成的下载；忽略临时扩展名与仍在写入的文件。
- 目标路径必须留在已配置项目根目录内。
- 未经确认不删除原文件、不清空隔离区、不覆盖现有同名资产。

## 更新与修复

- 应用源码位于 `assets/app/`。
- 更新安装时重新运行安装脚本；配置与运行台账默认保留。
- 修改脚本后运行：

```powershell
node --check "<安装目录>\server.js"
node --check "<安装目录>\duplicate-cleaner.js"
node --check "<安装目录>\public\app.js"
Invoke-RestMethod http://localhost:5177/api/projects
```

- 修改项目配置后验证所有项目 `exists: true`。
- 修改 Explorer 打开逻辑后实际点击一次“文件夹”，确认出现可见的文件资源管理器窗口。
- 修改播放或刷新逻辑后用一个超过自动刷新周期的视频完整播放验证。

## 交付

向用户报告程序目录、数据目录、桌面快捷方式、访问地址与配置文件位置。不要暴露测试临时目录、个人目录或内部调试日志。
