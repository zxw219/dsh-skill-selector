---
name: asset-manager
description: 为图片、视频、音频和文档素材建立项目、日期、类型、标签、命名和元数据规范，便于归档与检索。A foundational asset-organization Skill for classifying images, video, audio, and documents by project, date, type, tags, filenames, and metadata for reliable retrieval.
metadata:
  version: 1.0.0
version: "1.0.0"
---

# 素材整理归档（Asset Manager）

## 功能概述
标准化拍摄素材的分类、标签、存档规范，方便检索和管理。

## 分类体系

### 按项目分类
```
/Projects/
  ├── Project_A/
  ├── Project_B/
  └── Project_C/
```

### 按日期分类
```
/YYYY-MM-DD/
```

### 按类型分类
```
/Video/       # 视频素材
/Image/       # 图片素材
/Audio/       # 音频素材
/Document/    # 文档资料
```

## 标签规范

### 场景标签
- indoor（室内）
- outdoor（室外）
- studio（影棚）
- location（外景）

### 人物标签
- portrait（人像）
- group（群体）
- crowd（人群）
- solo（单人）

### 情感标签
- positive（积极）
- negative（消极）
- neutral（中性）
- emotional（情感强烈）

### 技术参数标签
- 4K、1080P、720P
- raw、log、hlg
- slowmo、timelapse

## 命名规范

### 标准命名格式
```
[日期]_[项目]_[类型]_[场景]_[描述]_[序号].扩展名
```

### 示例
```
2024-01-15_ProjectX_Video_Outdoor_CitySkyline_001.mp4
2024-01-15_ProjectX_Image_Studio_Portrait_001.jpg
```

## 元数据记录

### 素材清单格式
```json
{
  "filename": "xxx.mp4",
  "project": "项目名",
  "date": "YYYY-MM-DD",
  "type": "video",
  "tags": ["indoor", "portrait", "4K"],
  "duration": "00:01:30",
  "resolution": "3840x2160",
  "notes": "备注信息"
}
```

## 使用方法

### 自动归档
系统自动根据素材特征进行分类和标签。

### 手动查询
- `查找[关键词]`：按文件名或描述搜索
- `标签[标签名]`：按标签筛选
- `项目[项目名]`：查看项目素材

## 优势
1. **统一规范**：标准化命名和分类
2. **高效检索**：多维度标签支持快速定位
3. **团队协作**：统一格式便于团队共享
4. **长期保存**：规范的元数据便于归档
