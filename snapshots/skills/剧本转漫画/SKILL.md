---
name: 剧本转漫画
description: 将小说、剧本、分集大纲或 Obsidian 项目改编为漫画/国漫分镜与成稿流程。适用于“剧本转漫画”“小说转漫画”“国漫漫画版”“继续漫画生成”“按本地图片方法出图”等任务。使用时必须先查询本机可用的图片生成方法，再询问用户选择哪套出图方式，以及是否提供新的 API key、Base URL、模型名称。
---

# 剧本转漫画

## 用途

把小说、剧本或章节大纲转成可持续推进的漫画项目：拆集、拆页、写分镜、写生图提示词、调用本地图片生成方案出图、写回 Obsidian，并记录进度。

## 启动规则

当用户要求“剧本转漫画”“小说转漫画”“生成国漫漫画版”“继续漫画生成”“监督漫画任务”时，使用本技能。

开始前必须先做两件事：

1. 查询本地可用图片生成方法。
2. 问用户本次使用哪套方式生成图片，是否要提供新的 `API key`、`Base URL`、`模型名称`。

不要在未确认前更换、展示或复述用户的密钥。

## 优先查询本地出图方案

先检查这些本地技能和脚本是否存在，并读取必要说明：

- `C:\Users\Administrator\.codex\skills\cdn-gpt-image\SKILL.md`
- `C:\Users\Administrator\Documents\Codex驯化过程\.agents\skills\gemini-image-gen\SKILL.md`
- `C:\Users\Administrator\.codex\skills\koda-storyboard-image-skill-20260608-021514\SKILL.md`
- `C:\Users\Administrator\Documents\Codex驯化过程\tools\gemini_image_gen.py`

如果存在多套方案，简短列给用户：

- `12AI画图-gpt-image`：OpenAI-compatible Images 接口，常用于 `gpt-image-2`。
- `gemini-image-gen`：Gemini native `generateContent`，常用于 `gemini-2.5-flash-image`。
- `koda-storyboard-image`：偏分镜、镜头控制、连续性，不一定负责真正出图。

然后询问：

```text
这次用哪套出图？
1. 沿用本地已配置的 12AI/gpt-image
2. 沿用本地已配置的 Gemini image
3. 你提供新的 API key / Base URL / 模型名，我重新配置
4. 先只做分镜和提示词，不出图
```

## 推荐工作流

1. 确认输入来源：
   - 小说正文
   - 剧本
   - 分集大纲
   - Obsidian 文件夹
   - 旧项目断点

2. 建立或读取项目目录：
   - `00_script`：原文/剧本
   - `01_comic_bible`：漫画改编总方案、角色、场景、画风连续性
   - `02_episode_pages`：分集分页
   - `03_koda_storyboards`：镜头/分镜控制
   - `04_comic_generation`：每页生图提示词
   - `outputs/comic_pages`：最终图片

3. 先读本地文件确认真实进度：
   - 不要依赖旧对话记忆判断进度。
   - 不要读取已经卡死的长线程全文。
   - 统计每集图片数量、样章文件、总览文件和进度记录。

4. 改编顺序：
   - 全书/全季总方向
   - 分集目标
   - 每集 8-12 页
   - 每页画面、对白、镜头、情绪、连续性
   - 生图提示词
   - 出图
   - 检查
   - 写回样章/总览/进度

5. 出图时控制上下文：
   - 不要把大图或 base64 嵌入对话。
   - 只输出图片路径和一句检查结果。
   - 每完成几页就落盘。
   - 长任务建议每 1-3 集开新线程，并把进度写入本地文件。

## 断点续做规则

续做旧项目时，先检查本地文件：

```powershell
Get-ChildItem -Directory "项目路径\outputs\comic_pages" |
  ForEach-Object {
    [PSCustomObject]@{
      Episode = $_.Name
      PngCount = (Get-ChildItem $_.FullName -Filter *.png -File).Count
    }
  }
```

从第一个未完成页继续。不要口头宣称完成，必须以本地文件数量和总览记录为准。

## 长线程防卡死规则

旧线程如果出现 `systemError`、`notLoaded`、长时间空转，优先判断为线程状态损坏。

处理方式：

- 新开接管线程。
- 不引用旧对话全文。
- 只读取本地项目文件。
- 每次只处理小批量页数。
- 不在对话中展示图片本体，只用绝对路径。

## 完成标准

完成后必须说明：

- 完成到第几集、第几页。
- 图片输出目录在哪里。
- 样章/总览/进度文件在哪里。
- 是否做过连续性检查。
- 哪些只是“已配置”，哪些是“已验证成功”。

## 默认回复风格

用户是编程新手，解释时先讲用途，再讲步骤。回答简洁，先结论后细节。
