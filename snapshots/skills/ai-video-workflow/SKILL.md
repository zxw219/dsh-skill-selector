---
name: ai-video-workflow
description: 把文案、氛围底图、改图和视频生成串成可检查的 AI 视频生产流程，并提供阶段模板和质量检查点。A staged AI-video production workflow connecting script development, look frames, image revision, and video generation with prompt templates and quality gates.
metadata:
  version: 1.0.0
version: "1.0.0"
---

# AI视频生产流程（AI Video Workflow）

## 功能概述
标准化AI视频生产流程，整合多个AI工具完成从文案到视频的完整制作。

## 核心流程

### 标准生产链路
```
文案策划(Gemini) → 氛围底图(Midjourney) → 图像改图(FLUX/ComfyUI) → 视频生成
```

### 工具链说明

| 环节 | 工具 | 用途 |
|------|------|------|
| 1. 文案 | Gemini | 生成视频脚本和文案 |
| 2. 底图 | Midjourney | 生成氛围底图 |
| 3. 改图 | FLUX/ComfyUI | 根据需求改图 |
| 4. 视频 | 可灵/海螺/Runway | 生成视频 |

## 各环节指南

### 1. 文案策划（Gemini）
- 输入：视频主题、风格、时长要求
- 输出：完整分镜脚本、画面描述、配音稿
- 质量要点：画面感强、节奏感好、情感丰富

### 2. 氛围底图（Midjourney）
- 输入：分镜画面的文字描述
- 输出：高清氛围底图
- 质量要点：风格统一、光影到位、构图讲究

### 3. 图像改图（FLUX/ComfyUI）
- 输入：底图 + 改图需求
- 输出：符合视频要求的最终图
- 质量要点：主体清晰、细节完整、风格一致

### 4. 视频生成
- 输入：最终图像
- 输出：视频片段
- 质量要点：动作自然、时长合适、连贯流畅

## 提示词模板

### Gemini文案提示词
```
请为[主题]类型的视频创作脚本，要求：
1. 时长：[X]秒
2. 风格：[风格描述]
3. 目标受众：[受众描述]
4. 需要包含[数量]个分镜
```

### Midjourney绘图提示词
```
[画面描述], cinematic, high detail, 4K, professional lighting, 
[风格描述], --ar 16:9 --s 750 --q 2
```

### 视频生成提示词
```
[动作描述], smooth motion, cinematic, high quality
```

## 注意事项
- 不使用tapnow（竞品）
- 每个环节需质量检查通过后再进入下一环节
- 保留原始素材和中间文件
- 记录每环节使用的提示词
