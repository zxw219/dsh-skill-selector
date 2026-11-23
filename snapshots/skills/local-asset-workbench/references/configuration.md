# 配置与维护参考

## 目录

1. 项目配置
2. 下载归档
3. 清理安全
4. 重复图片去重
5. 生成任务
6. 运行与验证
7. 素材纠错移动

## 项目配置

配置文件位于安装目录的 `asset-browser.config.json`。

每个项目包含：

```json
{
  "id": "project-id",
  "name": "项目显示名",
  "path": "D:\\项目\\示例",
  "scanRoots": ["."]
}
```

- `id`：只使用小写字母、数字和连字符，并保持唯一。
- `path`：项目绝对路径。
- `scanRoots`：相对项目根目录的扫描入口；`.` 表示项目根目录。
- 项目数组顺序就是首次显示顺序，用户也可在界面中拖动保存。
- 不要把提示词、缓存、临时下载目录伪装成项目根目录。
- 默认参考库项目 ID `reference-library` 支持最多五级目录扫描，并在左栏以顶层分组和子目录条目展示；顶层“全部”视图使用子目录拼图封面而非混排所有素材。普通项目仍保持单层案例扫描，避免大型制作项目被过度展开。

运行中新增项目优先调用：

```http
POST /api/projects
Content-Type: application/json

{"name":"项目名","path":"D:\\项目","scanRoots":["."]}
```

## 下载归档

默认关闭自动归档。首次启用时：

1. 确认下载目录。
2. 先使用 `copy` 模式。
3. 为图片、视频、音频设置项目内相对路径。
4. 先执行预览，确认目标路径。
5. 确认无误后再运行归档。

路由模板支持 `{date}`、`{month}`、`{year}`。所有目标必须位于项目根目录内。

## 清理安全

- 默认 `dryRun: true`。
- 默认只处理已有导入台账的文件。
- 先进入隔离区，不直接永久删除。
- 未完成下载、临时文件和仍在写入的文件不得移动。
- 只有用户明确确认时才关闭 dry-run 或开启隔离区永久清空。

## 重复图片去重

默认配置：

```json
{
  "deduplication": {
    "enabled": true,
    "exactContentOnly": true,
    "sameDirectoryOnly": true,
    "settleSeconds": 5,
    "recentSweepHours": 168,
    "retentionDays": 14,
    "quarantinePath": "<安装目录>\\duplicate-quarantine"
  }
}
```

- 只比较图片的文件大小和 SHA-256，哈希完全相同才处理。
- 只在同一目录内去重，不跨项目或跨目录删除相同参考图。
- 带相邻 `.prompt.md` 或 `.meta.json` 的图片视为已登记生成尝试并优先保留；与其哈希相同的未登记副本进入隔离区。
- 如果同一重复组内存在多个已登记生成尝试，全部保留，不互相删除。
- 被移出的副本先进入隔离区，保留期到期后才永久清除。
- 去重记录位于安装目录的 `.duplicate-cleanup-ledger.json`。

## 生成任务

生成任务会保存：

- 最终文件；
- 同名 `.prompt.md`；
- 同名 `.meta.json`；
- 项目级 JSONL 台账。

默认目标为 `生成资产/<日期>/<图片|视频>`。每日练习项目默认按 `<日期>/<图片|视频>` 归档。用户提供目标目录时，以项目内安全相对路径为准。

## 素材纠错移动

选中一项素材后，可点“移动”或按 `M`。界面先读取目标项目中的文件夹：

```http
GET /api/folders?project=<project-id>
```

确认后调用：

```http
POST /api/move-asset
Content-Type: application/json

{
  "sourceProjectId": "source-project",
  "sourceCaseId": "case-folder",
  "sourceAssetId": "image.png",
  "sourcePath": "case-folder\\image.png",
  "targetProjectId": "target-project",
  "targetDirectory": "target-folder",
  "fileName": "image.png"
}
```

- `targetDirectory` 必须是目标项目内的安全相对路径，也可以为空表示项目根目录。
- 媒体文件及同名 `.prompt.md`、`.meta.json` 一起移动；人工判断与备注转入目标案例的 `.asset-review-meta.json`。
- 先复制到临时文件并校验 SHA-256，再提交目标文件和删除源文件。
- 禁止覆盖同名媒体或边车文件，冲突时自动追加数字后缀。

## 运行与验证

默认地址为 `http://localhost:5177/`。

验证：

```powershell
Invoke-RestMethod http://localhost:5177/api/projects
```

至少检查：

- 项目均显示 `exists: true`；
- 首页可打开；
- 图片和视频可预览；
- “文件夹”可打开素材所在目录；
- 播放预览期间不会被自动刷新中断。
