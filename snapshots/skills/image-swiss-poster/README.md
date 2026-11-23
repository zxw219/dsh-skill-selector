# image-swiss-poster · 使用说明

## 这是什么

把任意角色改写成**现代瑞士主义（国际主义平面设计）风格竖版角色海报**的提示词工具。

产出物是**一条完整、可直接复制粘贴的生图提示词**——不是图片，不是要点清单。

风格特征：超大无衬线标题被画面边缘裁切、非对称网格、大面积留白、**只有一种**强调色、坐标与编号做次级信息层、半写实肖像。

**覆盖模型**：GPT Image 2 · GPT Image 2.5（Flare / Sunburst）

## 文件

```
SKILL.md                              入口：触发、边界、工作流、输出契约
agents/interface.yaml                 接口契约
references/01-prompt-template.md      完整提示词模板 ＋ 九层拆解 ＋ 填空指引
references/02-model-adaptation.md     两个模型的参数建议与换模型退化预期
references/03-visual-anatomy.md       从 4 张示例成片反推的版式规律
references/04-failure-modes.md        10 类常见失败与修法补句
examples/original-posters/            示例成片 A 批 · 日漫 4 张
examples/china-myth-series/           示例成片 B 批 · 中国神话 9 张
examples/visual-check.md              两批共 13 张的核对台账与结论
manifest.json                         元数据
```

## 安装

纯文档包，无脚本、无依赖、无构建步骤：

```bash
# 本地包直接复制目录即可：
SKILLS="<技能目录>"
cp -r "<本目录>" "$SKILLS/image-swiss-poster"
```

装入后需在宿主中**重新加载技能列表**才会生效。

## 你可以直接这样说

以下说法**会**触发：

- 「用瑞士风格给我做一张 XX 的角色海报」
- 「国际主义风格 / Swiss style 的角色海报提示词」
- 「要那种超大标题字、带坐标编号的杂志封面感海报」
- 「把这张角色图改成 Editorial 大字海报，竖版」

**不会**触发（转给别的技能）：

- 「做一张电影感海报」→ `cinematic-poster-designer`
- 「帮我设计这个角色的三视图」→ `character-casting-studio`
- 「出一套品牌视觉规范」→ `brandkit`
- 「画一张日漫手绘人设」→ `wild-handdrawn-anime-image`
- 「做条海报动效视频」→ 视频类技能

## 怎么用

**单张**：给出角色 → 技能输出完整提示词 → 你复制到生图工具执行。

**最小例子**：

> 输入：`用瑞士风格做一张夜巡人的角色海报，男性，黑长发高马尾，深灰立领长风衣，佩无鞘直刀，沉静寡言`
>
> 输出：一条完整提示词，含 `【角色】` 三处已替换、强调色锁定为深灰蓝、画面文字列全、并附「GPT Image 2.5 · Flare · 2K · Medium · 9:16」的参数建议。

## 参数速查

| 用途 | 变体 | 分辨率 | 质量档 |
|---|---|---|---|
| 试稿 | Flare | 1K | Low / Medium |
| **正式交付（默认）** | Flare | 2K | Medium |
| 印刷 / 大屏 | **Sunburst** | 4K | High+ |

画幅：**9:16 或 3:4，都是竖版**——A 批 4 张实测 577×1024（9:16），B 批 9 张实测 1440×1920（3:4）。两者均成立，按用途选。

## 三条硬约束（别碰）

1. **强调色只有一个**——多给一个，设计秩序立刻垮
2. **禁止居中构图**——人物必须占一侧或从边缘切入
3. **标题字必须被裁切或被遮挡**——字体是图形，不是标题栏

## 自检命令

```bash
PKG="<技能目录>/image-swiss-poster"
PYW="C:/Users/EDY/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
QMS="C:/Users/EDY/.workbuddy/skills/qiaomu-meta-skill/scripts"

# 结构校验
"$PYW" "$QMS/validate_skill.py" "$PKG"

# 触发边界评测
"$PYW" "$QMS/trigger_eval.py" "$PKG" --cases "$PKG/evals/trigger_cases.json"

```

## 故障排查（Troubleshooting）

| 症状 | 原因 | 处理 |
|---|---|---|
| 人物居中，像证件照 | 模型按默认中心构图 | 追加「偏左/右三分之一，画面中不存在垂直对称轴」——见 `04-failure-modes.md` F1 |
| 标题字出现拼写错误 | 依赖模型自由生成文案 | **显式列出全部文字**，不要让它自己编——F2 |
| 画面出现两种以上鲜艳色 | 「高饱和强调色」被放宽理解 | 追加「除指定强调色外不得出现任何其他高饱和色彩」——F3 |
| 标题规规矩矩排在顶部 | 被当成排版标题而非图形 | 追加「字高不小于画面高度 1/4，必须被边缘裁切」——F4 |
| 认不出是哪个角色 | 风格权重压过身份 | 角色描述加长到 50 字以上，并追加身份保真句——F5 |
| 画面太满、没留白 | 「极少量」被忽略 | 追加「留白不小于 35%」——F6 |
| 出成横版 / 多人 | 末句权重不足 | 把「竖版、单人」提到前面并重复——F8 |
| 人物变扁平矢量插画 | 「插画」压过「半写实」 | 追加「保留体积、材质、摄影级光影」——F10 |
