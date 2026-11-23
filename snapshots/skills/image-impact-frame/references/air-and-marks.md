# 空气与笔触 · Air with Mass, and the Scrape-Brush Module

## 一、笔触模块 v4（硬边 · 不并实 · 不渗混）

**放在提示词的第一段**（权重偏前）。逐字可用：

```text
Everything is cut with a stiff flat brush dragged fast across a rough dry ground, nothing laid in as a coloured area. Each stroke is a bundle of separate parallel streaks with clean hard edges, and the narrow gaps between those strokes stay open all the way through — however densely the strokes crowd, no part of the picture ever closes into a solid mass. Strokes taper to sharp points at both ends and split and fray like a broom head. The brush never bleeds: no wash, no spreading, no softening between marks. Nothing mixes: nothing blends with anything else, and wherever two values meet the boundary is a clean hard edge.
```

### 三类笔：线层 · 碎片层 · 剪影层

同一幅画里有三类东西，**要求各不相同，必须分开写**：

| 层 | 是什么 | 要求 | 一句话 |
|---|---|---|---|
| **线层** | 速度线、集中线、放射芒、拉丝笔触 | 窄缝始终开着，**不许并实** | 有缝 |
| **碎片层** | 飞散的物质、碎屑、碎楔、墨点 | **就是实心块**，两端收尖 | 无缝，有尖 |
| **剪影层** | 主体形本身（人／兽的躯干） | **实心平涂、内部零肌理**；崩解只在边缘 | 实心，边崩 |

上面的模块管的是**线层**。另外两层各写一句即可：

```text
the fragments are solid wedges, sharp-edged and of every size, each one carrying the direction it was thrown
```

```text
the body itself is one solid flat silhouette — no texture, no streaks and no gaps inside it — and it only comes apart along its outline, where the edge frays outward into long strokes
```

**为什么必须分开**：

- 追「炸满画面」时把线层也逼到密实，笔刷感当场消失；
- 碎片层本来就是实心的，用「缝隙」去要求它是无效指令；
- **剪影层本来就是平涂实心**——用「不许成实心块」去要求它，会逼出内部肌理，人物当场变成毛线团。

因此模块里那句 `no part of the picture ever closes into a solid mass` **只对线层生效**。写主体时必须紧跟一句给它解绑（上面的第二句），否则模型会把剪影也一并拆开。

### 崩解三档（同一张画里必须都在）

| 档 | 对象 | 怎么处理 |
|---|---|---|
| **0** | **道具**（伞、兵器、器物） | **完全不崩**——保持完整几何形，边缘干净 |
| **1** | **躯干** | 实心剪影，边缘轻微毛糙，可有短须 |
| **2** | **头发／衣摆／飘带／末端** | **完全化成丝**，数十条长笔触甩出去 |

**三档并存才是对的。** 全画都崩＝糊成一团；全画都不崩＝剪纸贴图。**唯一不崩的那个道具是全画最强的对比物**——一把边缘完美的实心伞，立在一片全在崩解的笔触里。

### 模块里每一句防的是什么

| 句子 | 防的是 |
|---|---|
| `nothing laid in as a coloured area` | 平涂填实（旧措辞 `nothing filled flat` 与后文 `flat black` 一词两义） |
| `the narrow gaps ... stay open all the way through` | 用「极窄」形容缝隙，把画面逼成实体 |
| `however densely the strokes crowd, no part ... closes into a solid mass` | 追"炸满画面"时最容易丢掉的一句。**只对线层生效**——主体剪影本来就是实心平涂，必须另写一句解绑 |
| `The brush never bleeds: no wash, no spreading, no softening` | 被误解成"写意留白"后出现的渗混 |
| `Nothing mixes ... clean hard edge` | 多值互相渗透 |

## 二、密度原理（三件事同源）

- **满 ≠ 实**：满指没有空场，实指并成色块。
- **灰由疏密产生**：黑白两值下"灰"不是颜料，是白笔触铺得疏、把黑放出来。"灰"的三个档位＝疏／中／密。
- **亮不靠并实，靠被撕开**：命中处不是发光球，是**黑形被撕开一个口子**，亮值从口子成扇状长笔触涌出。这样"最亮"与"缝不许闭"同时成立，且比光晕更狠——**是被打穿的，不是自己亮的**。
- **密度即纵深**：越靠近爆心／接触点越密越亮，越远越疏越暗。**跑道是密度，不是留白**——这是本风格与"大片留白"类构图最根本的区别。

**明度 / 明暗全部由笔触密度承担，不用明暗过渡。**

## 三、空气有质量感：不是加雾

「空气有质量」＝**让空气表现出会挡东西、会吃光、会有阻力**。四个装置：

1. **雾会挡东西** —— 雾**吞掉主体远的那一半**。能被挡住的，才有厚度。
2. **光走不远** —— 爆发的光**只能在有限半径内传播**，形成**边界清晰的亮球**，而不是漫射光晕。介质有密度，光才走不动。
3. **空气有阻力** —— 被击飞的碎屑**只拖出很短的尾迹就被吃掉**。短尾迹＝厚空气。
4. **雾有实体** —— 雾**由笔触构成**：长条横向刮痕，密到并实成一片。不是加一层半透明滤镜。

**必须写的一句**：`The air has weight and it is not empty`，并交代**主体背后干脆不画**——空气已经把它吃掉了。

### 变体 A：雾被劈成两半

用于挥砍／劈击类瞬间。雾本来是"裹"在身上的，把它**切开**：

> 刃刚过，**空气被分成两半，沿着刃的两个面被推开**，每一半**立着，有可见的边缘**，不是化进雾里。

厚度因此从"氛围"变成**看得见的实体**。

### 变体 B：用碎晶代替雾

空气里飘的不是雾，是**有实体的碎片**——比雾更重。

- 碎晶填满每一寸空间，每片**拖一条短尾再被吞**
- **光推不远**：从两个光源出发各只推得动一小段就被吃掉 → **于是画面中段成为全画最暗处**

**纵深不靠渐隐，靠一段"黑暗的厚度"。**
