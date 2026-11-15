# Midjourney 用法与资料

本参考提供操作区别和内置资料入口，不把某个版本、账号设置或按钮布局固定为所有宿主的默认值。编写依据包括 2026-11-05 阅读的官方文档。Midjourney 用法与规则查询只读本技能内的资料；信息缺失、功能或界面变化、资料冲突时先报告，不自动联网，也不自行更新技能文件。

## 获取资料

完整资料包位于本文件同级的 [midjourney-official/index.md](midjourney-official/index.md)，包含源文件夹的全部文档、图片、视频、文字稿和抓取原始资料。使用此技能副本，不依赖原来的项目绝对路径。

从索引定位本轮专题，再读正文和关联截图，不要求每次加载全包。原文中的外部链接保留用于标明来源，不应自动打开。离线资料可能省略表格或把操作步骤留在图片中，须查看配图；本地未收录的专题或无法核实的细节应明确说明，不自行搜索网络。仅宿主另行明确要求联网核验时，才查询对应官方页面。

| 本轮需要 | 技能内的官方资料 |
| --- | --- |
| 入门与生成完成 | [官方入门指南](<midjourney-official/Midjourney 官方入门指南.md>)、[入门视频文字稿](<midjourney-official/Midjourney 入门视频文字稿.md>) |
| Discord 账号关联 | [Using Midjourney in Discord](midjourney-official/docs/32_Using-Midjourney-in-Discord.md)、[登录和关联账号](midjourney-official/docs/03_Logging-In-Connecting-Accounts.md) |
| 提示词基础 | [Prompt Basics](midjourney-official/docs/04_Prompt-Basics.md)、[Art of Prompting](midjourney-official/docs/05_Art-of-Prompting.md) |
| 模型及功能兼容 | [Version](midjourney-official/docs/12_Version.md) |
| 比例和 Raw | [Aspect Ratio](midjourney-official/docs/10_Aspect-Ratio.md)、[Raw](midjourney-official/docs/11_Raw.md) |
| 风格化、怪异度和变化度 | [Stylize](midjourney-official/docs/14_Stylize.md)、[Weird](midjourney-official/docs/15_Weird.md)、[Chaos / Variety](midjourney-official/docs/16_Chaos-Variety.md) |
| 速度及全局影响 | [GPU Speed](midjourney-official/docs/17_GPU-Speed-Fast-Relax-Turbo.md) |
| 图像参考 | [Image Prompts](midjourney-official/docs/19_Image-Prompts.md) |
| 风格参考 | [Style Reference](midjourney-official/docs/20_Style-Reference.md) |
| 编辑与角色参考 | [Edit Model](midjourney-official/docs/21_Edit-Model.md) |
| 官网生成和结果信息 | [Creating on Web](midjourney-official/docs/22_Creating-on-Web.md) |
| 后续图片操作 | [Modifying Your Creations](midjourney-official/docs/08_Modifying-Your-Creations.md) |
| 归档和下载 | [Organizing Your Creations](midjourney-official/docs/23_Organizing-Your-Creations.md) |
| 个性化和情绪板 | [Personalization](midjourney-official/docs/07_Personalization.md)、[Moodboards](midjourney-official/docs/06_Moodboards.md) |
| Draft 和对话模式 | [Draft & Conversational Modes](midjourney-official/docs/13_Draft-Conversational-Modes.md) |
| 视频 | [Video](midjourney-official/docs/09_Video.md) |
| 隐私设置 | [Stealth Mode](midjourney-official/docs/18_Stealth-Mode.md) |
| 平台规则 | [Community Guidelines](midjourney-official/docs/24_Community-Guidelines.md) |
| 订阅与账单 | 从[资料索引](midjourney-official/index.md)选择对应专题；阅读和教学不授权操作账号账单 |

此包完整复制了宿主提供的文件夹，但不代表收录了官网全部专题。Discord Quick Start、完整命令/参数总表、文字生成和 Discord 图片托管等独立专题未在此包单独收录；不要把原文中的外部链接视为本地已有文档。所需细节不足时如实说明。

## Discord 与官网

- Discord 使用 `https://discord.com/` 中宿主指定的服务器/文字频道或 Midjourney Bot 私聊。完整频道 URL 比只凭“常规”等名称更可靠。核对实际频道及 Bot 身份，不在同名错误频道生成。
- `/imagine` 是 Bot 的应用命令，需要在命令菜单中选择并进入实际 prompt 参数槽。按已有资料与实际页面操作；遇到不一致时报告，不自动联网补查，不能假设向普通消息框粘贴斜杠文本就一定调用成功。
- 官网生成页为 `https://www.midjourney.com/imagine`。检查当前是静态图片生成，避免因残留参考图或模式误触视频任务。宿主要求生成且必要信息齐备后，按主技能直接提交，不追加最终确认。
- 某些设置在 Discord 与官网之间同步。切换入口不意味着模型、速度、个性化或隐私设置已经恢复，确认实际生效值。

## 提示词与参考图检查

- 每个对话首次生图时，集中补齐未指定的模型、比例、速度、分辨率及任务数量等参数；可让宿主一次采用列出的当前值。之后沿用本对话约定，直到宿主明确修改，不重复询问，也不把官网默认值或界面漂移当作修改指令。
- 比例不是像素尺寸。只在取得实际文件/元数据后记录真实尺寸，不能根据 `--ar` 推算为已知尺寸。
- 核对 Bot 回显时先把比例约成最简整数比。例如 `21:9` 约分为 `7:3`，两者宽高比相同。归档保留实际提交的写法，必要时单独记录回显的等价写法。官方比例文档列出的是常见例子，所需比例的支持范围按模型及分辨率模式核验。只有回显比例确实不同、需要核实输出规格或宿主要求时，再按指令检查实际图片尺寸。
- 图像参考用于影响内容、构图、颜色等；风格参考用于视觉风格，不保证复制人物身份；编辑参考及其他角色参考功能按对应模型核验。不要跨版本机械复用参数。
- Discord 图片参考通常需要实际在线图片 URL；宿主给本地文件时，通过授权的上传流程获得实际可用链接，不能虚构链接。参考图上传至 Discord 也可能产生可见消息，确认上传位置和图像用途后再做。
- 对普通图像参考，官方建议描述目标画面；编辑模型可以有指令式描述。把这种建议作为提示而非统一禁令。格式差异先提醒；不改变语义或参数值的明确语法修正可直接采用，涉及内容或参数选择时说明阻塞，不擅自改写，也不追加无关的提交确认。
- 参数应使用当前官方支持的写法、位置、范围和组合。缺失、重复冲突或不支持时说明问题；不静默删除、换值或改版本。
- 有画面文字要求时，检查官方要求的双引号等写法，说明字符和语言的实际支持限制；不能把“最佳效果建议”说成必然无法生成，也不擅自翻译画面文字。
- 对自己的任务输入，可清理与宿主本次要求不符的残留引用图或模式，使其符合已有指令；若不确定是否属于宿主正在准备的其他任务，先报告阻塞，不擅自改动。

## 结果与后续动作

默认在发送键执行成功后告知宿主，由宿主查看 Bot 回执和结果。宿主要求查看时，用消息、Job ID、提交记录和提示词定位对应任务。要求等待完成时再跟踪生成。一条任务可能产生一组图片，输出数量以实际结果为准。

Discord 的 U 按钮在某些版本中仅分离网格图片，较早版本可能实际放大；V、重抽、实际 Upscale、编辑等可能生成新结果或消耗 GPU 时间。根据实际版本和操作说明判断，不把所有 U 操作一概称为放大。所有后续动作等宿主明确指示，收到具体指令且信息齐备后直接执行，沿用本对话参数，不追加二次确认。

按项目要求记录实际发送文本、模型设置、参考图来源和可取得的任务链接。只有按键成功时标为「已按发送键，回执未核验」。核对 Bot 接收后标为「已提交，结果未检查」。按宿主指令查看并确实取得结果后，再记录生成成功和归档状态。

## 已核实的平台风险

2026-11-05 核对的官方社区规则明确禁止未经特别授权的自动化交互，并说明账号可能被封禁；相关规则也适用于 Bot 私聊、私有服务器和官网。BrowserSkill 能操作页面不等于平台许可，本技能不提供免除该风险的保证。首次使用时向宿主简短告知；规则核验不授予绕过验证码、限制或更换账号的权限。
