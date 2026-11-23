# 安装：独立版

版本：2026-11-13-v25

1. 校对随包 `.sha256` 后解压，得到完整的 `director-seedance-prompt/` 文件夹。
2. 放入当前宿主技能目录。Claude Code 的目录为 `~/.claude/skills/`，其他宿主按其说明。
3. 更新或切换版本前，将旧文件夹备份到技能目录之外，再放入完整新文件夹，不采用覆盖合并安装。
4. 刷新技能或重新打开会话，用 `$director-seedance-prompt` 调用。

直接在本地项目文件夹工作。沿用用户已有目录，维护总索引、剧本修订、资产图、生图提示词、视频段落提示词和制作台账；先查看已有资产再补缺。编剧交接沿用同一本地项目与明确采用的稿件修订，用户视频保留原位。本版无需设置远程资产工作区，首次使用直接进入当前任务。

作者：MARIOZHAOFAN｜微信：MARIOZHAOFAN｜抖音：晚上睡不赵

角色、场景和道具资产方法及视频规则反推功能已经内置。实际生图仍使用宿主工具或用户授权接口；缺少工具时按 [能力降级](knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md)执行。用户确认无生图后交付所需资产的生图提示词并继续文生，不虚构已生成图片。

通用提示词检查需要 Python 3.10+，只使用标准库；媒体取证需要实际可访问的视频、音轨和相应环境，具体见 [媒体运行说明](capabilities/reference-rule-extraction/RUNTIME.md)。安装包不带外部程序、模型或私密凭据。

可在安装目录运行：

```text
python -B -m unittest discover -s scripts -p "test_*.py"
```

运行测试不等于实际生图、生成视频或取得用户验收。完整能力索引见 [README.md](README.md)，文件完整性见 `package-manifest.json`，版权与使用限制见 [LICENSE](LICENSE)。
