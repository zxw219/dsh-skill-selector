# 冲击帧导演 2.0 · image-impact-frame

把一句「这一下要打出狠劲」，编译成**一整段能直接粘进模型**的提示词——图能出、视频能出。默认只出提示词，不调用出图工具。

## 两套东西合成了一套

| | 管什么 | 打个比方 |
|---|---|---|
| **六条硬口径**（原有） | 这张画**成不成立** | 地基：写在那一瞬、炸满但不并实、一个颜色只干一件事、边缘要硬不要晕 |
| **L1–L5 档位**（2.0 并入） | 这一下**狠到什么程度** | 音量旋钮，说「再狠一点」就往上一格 |

**关键关系**：档位只管加多少手段，不管能不能违规。**拧到 L4 也不能「打空了靠特效糊」**——那是第一条死罪。

## 它解决什么

冲击帧的失败几乎不发生在"文笔"，而在这七件事上：

1. 写成了**状态**（"两人对峙"）而不是**瞬间**（"两股力刚碰上"）；
2. 写成了**版式**（"A 占左三分之一"），画面是摆好的而不是撞出来的；
3. 追"炸满"时写出 `almost solid`，**把笔刷感抹平**；
4. 用了 `face` / `eye` / `skin` 这类**解剖词**，主体直接往写实跑；
5. 同一段话里**一句要虚、一句要实**，模型只能二选一；
6. 每一击都上满特效，**档位没有落差**，反而每一下都轻；
7. 视频里写了闪白**没写恢复**，模型把反相拖到片尾。

本技能把这七类坑变成了可逐条执行的清单。

## 什么时候用 / 不用

**用**：`冲击帧` `冲击感` `打击感` `张力` `爆发帧` `命中那一瞬` `关键一击` `对轰` `打爆` `终结技` `炸满画面` `极端透视` `黑红` `空气有质量感` `顿帧` `震屏` `打得没力` `漫剧打斗`，以及英文 `impact frame` `hit frame` `hitstop`。

**不用**（转给对应技能）：

| 需求 | 转给 |
|---|---|
| 整段运镜、转场、镜头语言 | `video-camera-motion-director` |
| 整场分镜表、剪辑节奏 | `professional-storyboard-director`、`high-tension-shot-design` |
| 跨帧／跨集一致性 | `character-continuity-bible`、`entity-continuity-system` |
| 通用电影感场景、参考图角色路由 | `image-cinematic-realism` |
| 海报设计 | `cinematic-poster-designer` |
| 特效构造与生产审计 | `vfx-effect-construction-engine`、`aigc-audit-gate` |

## 你可以直接这样说

- 「中景两人对轰，冲击感、张力、极端透视，空气要有质量感。」
- 「特写拳头一拳打穿，黑红，16:9，给我 Midjourney 提示词。」
- 「这张参考图帮我做成冲击帧，要炸满画面。」
- 「8 秒动漫打斗，挡住连斩后反击，命中一瞬做黑白冲击，用 Seedance。」
- 「5 个镜头的打斗分镜，从普通攻防到终结技，要档位曲线。」
- 「这段视频拳头打中了却没重量，只在 3.4 秒加强。」

嫌不够狠说「升一档」，看不清说「降一档」。

## 档位速记

```
L1 清楚命中 → L2 有分量 → L3 爆发 → L4 炸裂 → L5 极限
```

普通攻防压 **L1–L2**，转折用 **L3–L4**，终结技才上 **L5** 且**一场只准一次**。冲击力来自**落差**，不来自每一下都 L5。

## 怎么工作

1. **判类** —— 是冲击帧/击点吗？不是就转走。
2. **定档** —— L1–L5 选一档（决定用多少手段）。
3. **选帧型** —— 命中／斩击横贯／纯爆发／站场／碎裂。
4. **选力学式** —— 爆点／压伏／贯穿／对撞，只选一个。
5. **放灭点** —— 打击点／兵器内部／脚下／光源，只放一个。
6. **分层写** —— 笔触模块 → 那一瞬 → 空间与透视 → 空气 → 配色。**笔触模块放第一段**。
7. **编译** —— 目标模型原生语法 ＋ 短而具体的 `--no`。
8. **自检后交付** —— 逐条过清单，特别是"同句自相矛盾"。

## 加载什么

| 文件 | 内容 |
|---|---|
| `references/core-doctrine.md` | 六条口径、满≠实、不实≠晕、C1–C6 自毁句、逐句比对法 |
| `references/force-architectures.md` | 五帧型 ＋ 力学四式 ＋ 选式速查 ＋ 英文现成句 |
| `references/perspective-and-scale.md` | 极端透视四招、四种灭点、极端大小对比 |
| `references/air-and-marks.md` | 拉丝笔触模块 v4、线层／碎片层两类笔、空气有质量感 |
| `references/deconstruction-and-palette.md` | 解构七条、形语法、零解剖词表、配色分层、正反相 |
| `references/intensity-ladder.md` | ★ L1–L5 逐档写法、档位曲线、平台现实 |
| `references/video-impact.md` | ★ 逐秒时间轴、三联卡、连招击点表、时间数字、光敏安全 |
| `references/style-packs.md` | ★ 六画风包、三色法、六组配色 |
| `references/model-adapters.md` | ★ MJ／Nano Banana／即梦／Seedance／可灵／Veo 写法 |
| `references/repair-guide.md` | ★ 四层故障树 |
| `references/post-production.md` | ★ framecraft 全参数 |
| `references/case-index.md` | 20 个实际案例与已知失败模式 |
| `scripts/framecraft.py` | 视频后期工具（8 配方 9 图层） |
| `examples/cues-example.json` | 多击点击点表示例 |
| `examples/reference-matrix/` | 九张同风格参考矩阵（对拳 ×4 配色、撑伞 ×3 配色、实拍源 ×2）＋索引 README |

## 后期工具（给现成视频加顿帧/闪白/震屏）

只要机器上有 FFmpeg（**9.x 已验证**），不需要装任何 Python 库。

```bash
python scripts/framecraft.py menu                  # 中文数字菜单，最省事
python scripts/framecraft.py detect --input 打斗.mp4   # 不知道第几秒命中，让它自己找
python scripts/framecraft.py apply --input 打斗.mp4 --at 3.4 --recipe heavy --output 打斗_重击.mp4
```

- **原视频永远不动**，只写新文件；输出名**不能已存在**、不能等于输入（这是保护机制，不是报错）。
- 8 配方：`cinema` `light` `heavy` `manga` `anime` `energy` `blackout` `crit`
- 9 图层：`hitstop` `flash` `invert` `ink` `punch` `rgbsplit` `shake` `zoom` `still`
- 自动拦截每秒超过 3 次的闪烁，输出后再做亮度扫描。

## Troubleshooting

| 症状 | 原因 | 处理 |
|---|---|---|
| 出图没有笔刷感 | 出现"密到近乎实心"类措辞，或笔触句掉到末尾 | 换 `the narrow gaps ... stay open all the way through`，笔触模块提到第一段 |
| 主体很写实 | 用了 `face`／`eye`／`skin` | 换 `deconstruction-and-palette.md` 的零解剖词表 |
| 画面像一层灰膜、边缘糊 | 把"不要实"做成了"写意留白" | 加回 `The brush never bleeds` 与 `The two values never blend` |
| 两股力糊成一片 | 两侧颜色太近，或 `--no` 漏了 `grey` | 拉开明度与温度，补 `grey` |
| 画面像摆好的版式 | 用了区域分配式描述 | 改为单一矢量贯穿＋因小失大＋密度作跑道 |
| 极端透视出不来 | 镜头不够贴、线没收束 | "贴地平放＋向灭点收束"往前挪，**不要**先加 `--raw` |
| 碎片被写成空的 | 线层与碎片层没分开写 | 线层永不闭合；碎片层直接写 `solid wedges` |
| 每一下都一样轻 | 全部上满特效，没有档位落差 | 按 `intensity-ladder.md` 排曲线：普通压低、转折跳两档 |
| 视频反相拖到片尾 | 没写"恢复原画面" | 命中那一句后面补 `then the frame returns to the original picture` |
| 视频换脸／崩形 | 一上来就做 L4–L5 | 先用 L2–L3 生成稳定动作，再用后期工具抬档 |
| 后期工具报"输出已存在" | 保护机制 | 换一个新文件名，工具不会覆盖任何文件 |

## 版本

- **2.1.0**：画面层六条硬口径 ＋ 三类笔分层（线层／碎片层／剪影层）＋ 崩解三档 ＋ 强度层 L1–L5 ＋ 结构层五帧型／力学四式 ＋ 视频击点逐秒时间轴 ＋ 六画风包 ＋ 分平台写法 ＋ 四层故障树 ＋ 九张参考矩阵示例 ＋ framecraft 后期工具。
