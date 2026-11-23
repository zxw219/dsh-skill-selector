# 3:4 肖像生成规范 v3 · 从零创造版（正向措辞）

> 建立 2026-10-09。**本版推翻 v2 的两处口径**：① v2 假设"以已定角色参考图为依据重拍"→ 实际是**从零创造**；② v2 大量使用"裁切锁死语义"→ 本版**禁止使用**。
> 本文件为本技能的核心出图规范（v3 口径）。
> 本技能**只产出提示词，不调用任何出图工具**；出图须由用户逐次明确授权。
> 相邻边界：本技能管「从零创造 3:4 肖像的提示词」，不管参考图重拍、不管既有角色的跨镜头锁定。

---

## 一、明确目标：从无到有创造一张 3:4 肖像

**一句话定义**

> **从零创造**一张 **3:4 竖版肖像**：完整呈现头部、发型与头顶以及颈项与双肩，**头部与肩部充满整个画面**；
> **服饰绝对不要**；背景为 **#808080（18% 中性灰）纯净影棚背景板**；
> **光默认「漫射柔光 + 平光铺照」，光线分布均匀柔和**；
> 措辞**正向为主**，**不使用裁切锁死语义**，**负向词非必要不用**；
> **画风**由用户指定，未指定则默认「中式写实」（或先询问）；
> **默认只出提示词，不调用任何出图工具**。

**输入与输出**

| 项 | 内容 |
|---|---|
| 输入 | **角色设定**：可直接用 220 脸型库编号（如 `F021`），或自然语言 brief（性别／年龄／气质方向） |
| 输出 | **3:4 肖像的出图提示词**（中文 + 英文），默认不出图 |
| 产物用途 | 角色定妆底图／面部锚点／课程实操示例 |

**它不是**：以某张参考图重拍；也不是 casting 三视图或全身人物卡。

---

## 二、九项字段在创造模式下的归属

v2 的"锁"是对参考图的锁；本版是从零创造，四项改为**写入即固定的定值**——一经设定，生成与后续复用中都不得漂移。

| 字段 | 归属 | 规则 |
|---|---|---|
| `[骨相]` | **定值 ①** | 从库/设定写入，一经写入即固定，生成中不调不改 |
| `[五官]` | **定值 ②** | 同上 |
| `[识别]` | **定值 ③** | 毫米级写死（痣／疤／不对称的位置与左右） |
| `[气质]` | **定值 ④** | 与原库「半固定」不同——本产物列为定值；**不可为了救构图去改气质词** |
| `[性别]` | **设定 · 必写** | 不写模型自猜，库内骨相词偏中性，极易出成男性 |
| `[妆容]`（男 `[面部]`） | **设定 · 必写** | 唇色必须有具体色相；写成"淡／灰／裸"＝出男人脸 |
| `[发型]` | **设定** | 并按本产物追加「含发际线、额前碎发、发丝走向与体积」 |
| 头饰／发饰／耳饰 | **设定** | 有则写清形制与位置；无则写"无饰品" |
| `[镜头]` | **规格项** | 改为正向的 3:4 肖像构图描述（见第五节） |
| `[姿态]` | **停用** | 肖像构图，手不入画，无需规定双手去向 |
| `[服饰]` | ❌ **绝对不要** | 不设此维度 |
| `[光]` | ⚙️ 风格层 | **默认「漫射柔光 + 平光铺照」** |
| `[画风]` | ⚙️ 风格层 | 用户指定；未指定则默认「中式写实」，或**起手先问** |

**为什么气质列为定值**：气质一动，眼神、眉形走向、唇形松弛度会同步漂移——而这四样正是观众认人的依据。定值化之后，"靠删气质词救构图"这条路关闭，构图问题只能从构图句解决。

---

## 三、措辞纪律（本版核心）

### 3.1 三条硬规矩

1. **正向为主**：把要求写成"画面是什么"，不写成"画面不能是什么"。
2. **禁止裁切锁死语义**：不声明画面边缘、不声明哪些部分不入画、不声明什么不得被切断。
3. **负向词非必要不用**：默认**整份提示词不含负向块**；确有必要时只补极简四项（见第七节）。

### 3.2 禁用措辞 → 替换对照表

| 禁用（裁切锁死语义） | 替换（正向描述） |
|---|---|
| 画面下缘止于锁骨线与肩线 | 肖像构图取景至肩部 |
| 锁骨以下不出现身体／胸／手臂 | 画面主体为人物头部、颈项与双肩 |
| 画面下缘切在××位置 | （删除，不做边缘声明） |
| 任何一缕发丝不得被画面边缘切断 | 完整呈现整个头部与全部发型，发型轮廓完整 |
| 裁切／裁切出画／不入画／出画 | （一律删除） |
| 锁定边界／锁死构图范围 | （一律删除）。「锁定」只允许用于**比例**：锁定 3:4 比例 |
| 不得超出／不得越出 | （删除，改正向陈述） |
| 保持…不变（对参考图而言） | 改为设定陈述句：「…是…」 |

---

## 四、起手流程（四步）

1. **先定画风**：用户已给画风则直接用；未给则**询问是否已有指定画风**，无则默认「中式写实」。
2. **取角色设定**：从 220 脸型库按「性别＋年龄＋气质」选型（或直接用用户的自然语言 brief）。
3. **生成提示词**：按第五节模板正向撰写；默认不写负向块，确需时按第七节补极简四项。
4. **交付**：只交付提示词，**不调用任何出图工具**；出图须逐次明确授权。

---

## 五、提示词模板 v3（可直接整段复制）

### 5.1 中文版

```
【肖像设定】一位［性别］，［年龄］，［地域与气质方向］。东方［性别］面孔。

[骨相] ［脸型、颧骨、下颌角、下巴、面部轮廓与骨点结构］
[五官] ［眼型与眼裂、双眼皮形态、眉形与眉峰、鼻梁鼻头、唇形与唇峰］
[识别] ［痣／疤／不对称，位置与左右写死到毫米］
[气质] ［神态、目光温度、眼神状态、面部张力与情绪压强］
[妆容] ［妆面名称 + 具体色相，如"极简冷妆，唇色豆沙"］
[发型] 含发际线、额前碎发、发丝走向与体积的［发型描述］
[饰品] ［头饰／发饰／耳饰的形制、材质、位置；无则写"无饰品"］

【构图与比例】竖版 3:4 比例。肖像构图取景至肩部：完整呈现整个头部与全部发型，包括头顶
与发际线；并呈现颈项与双肩。头部与肩部充满整个画面，面部中轴居中，双眼位于画面上三分之一，
平视视角，面部正面朝向镜头，目光平视镜头。

【着装】画面主体为人物头部、颈项与双肩的皮肤，肩颈自然裸露；除头饰与耳饰外，
画面中不出现任何其他物件，不出现衣物、衣领、领口、肩带、布料或披风。

【光】漫射柔光，平光铺照：光线从正面均匀铺照面部，光比极小，明暗过渡柔和，
无硬阴影方向，面部受光均匀通透，肤色还原自然，皮肤纹理清晰可见。

【背景】标准 18% 中性灰专业影棚背景板，色值 #808080，纯净无瑕疵：
均匀单一色值，无纹理、无褶皱、无渐变、无污渍、无道具、无文字。

【画风】中式写实，保留皮肤纹理与毛孔，影棚自然光质感，不磨皮。

【质感】真实皮肤质感：可见毛孔、细纹与自然色差，半哑光；
中性白平衡，面部高光克制；真实商业妆容质感，非美颜滤镜效果。
```

**填空来源**：`[骨相]`~`[气质]` 从 220 脸型库条目**整段复制**（四行一字不改）；`[性别]`／`[妆容]` 行必须带上；`[发型]` 行在库文本后追加"含发际线、额前碎发、发丝走向与体积"；库中的 `[镜头]`／`[姿态]` 两行**不复制**，由上面「构图与比例」段替换。

### 5.2 英文版（GPT Image / 通用）

```text
Character: a [gender], [age], [regional and temperament direction]. East Asian [gender] face.

Bone structure: [face shape, cheekbones, gonial angle, chin, facial contour and bone landmarks]
Features: [eye shape and aperture, eyelid form, brow shape and peak, nose bridge and tip, lip shape]
Identifying anchors: [moles / scars / asymmetry, with exact position and side]
Temperament: [expression, gaze warmth, eye state, facial tension, emotional pressure]
Makeup: [makeup style with a specific visible hue, e.g. minimal cool makeup, dusty rose lips]
Hair: [hairstyle description] including hairline, baby hairs, strand direction and hair volume
Accessories: [form, material and position of hair ornament, headpiece or earrings; or "no accessories"]

Composition and aspect ratio: vertical 3:4 portrait. The portrait is framed to the shoulders:
the whole head and the entire hairstyle are fully shown, including the top of the head and the hairline,
together with the neck and both shoulders. Head and shoulders fill the whole frame,
facial axis centered, eyes near the upper third, eye-level view,
face facing the camera directly, gaze level at the lens.

Attire: the subject is the head, neck and shoulders rendered as skin, with shoulders and neck naturally bare;
apart from the hair ornament and earrings no other object appears in the frame - no garment,
collar, neckline, strap, fabric or cape.

Light: diffuse soft light, flat even wash. Light is spread evenly across the face from the front,
extremely low contrast ratio, soft tonal transitions, no hard shadow direction,
evenly lit and luminous skin, natural color rendering, skin texture clearly visible.

Background: standard 18% neutral gray professional studio backdrop, hex #808080, pure and flawless:
one uniform value, no texture, no wrinkle, no gradient, no stain, no prop, no text.

Style: Chinese photorealistic, visible skin texture and pores, studio natural-light quality, no retouching.

Texture: real skin - visible pores, fine lines and natural tonal variation, semi-matte;
neutral white balance with restrained highlights; real commercial makeup finish, not a beauty-filter look.
```

---

## 六、按需补极简负向块（默认不用）

**默认整份提示词不含负向块。** 仅当出现下表现象时，**只补对应一行**，用完即撤：

| 触发现象 | 只补这一行 |
|---|---|
| 出现衣物、领口、肩带 | 任何衣物、领口、肩带、布料 |
| 皮肤蜡像感／磨皮／油光 | 蜡像皮肤、塑料皮肤、油光、磨皮、美颜滤镜 |
| 出现第二个人物或倒影 | 第二个人物、重复人物、镜中倒影 |
| 出现文字、水印、道具 | 文字、水印、logo、道具 |

> 这四项之所以罕见地必要，是因为它们**无法用正向句排除**（"画面里没有衣服"本身仍会唤出衣物概念）。除此之外一律改写成正向句。

---

## 七、QA 质量门（9 条，正向核验口径）

1. **比例**：确为竖版 3:4。
2. **完整**：整个头部、全部发型与头顶、发际线完整呈现；发型轮廓完整。
3. **取景**：画面呈现头部、颈项与双肩，头部与肩部充满画面；面部中轴居中，双眼约在画面上三分之一。
4. **着装**：画面中除头饰与耳饰外无其他物件，无衣物、衣领、领口、肩带、布料、披风。
5. **背景**：#808080 单一色值，无纹理／褶皱／渐变／污渍／道具／文字。
6. **四定值一致**：骨相、五官、识别锚点、气质四项与设定值一致，无漂移。
7. **妆容与发型**：妆容与唇色有色相；发色、发际线、头顶轮廓与设定一致。
8. **饰品**：头饰／发饰／耳饰按设定呈现，形制、位置、材质一致。
9. **光与质感**：光线分布均匀柔和、光比极小、无硬阴影；皮肤半哑光可见毛孔，中性白平衡，面部高光克制。

---

## 八、常见现象的修法（全部走正向句）

| 现象 | 修法 |
|---|---|
| 构图偏紧，头顶被切 | 正向加「完整呈现头顶与全部发型」，并把该句**提到提示词最前**；或改为先出 4:5 再自行裁到 3:4 |
| 出成侧脸、半张脸 | 正向写「面部正面朝向镜头，目光平视镜头」，并**前置**该句（**不可改气质词**——气质是定值） |
| 画面偏暗、阴影硬 | 强化「漫射柔光、平光铺照、光比极小、明暗过渡柔和、无硬阴影方向」 |
| 背景发灰不均匀／有渐变 | 正向写「均匀单一色值、无渐变、无褶皱」；必要时后期替换背景（#808080 无纹理，替换极干净） |
| 皮肤蜡像感／磨皮 | 正向写「可见毛孔、细纹与自然色差，半哑光」，并补第六节第 2 行负向 |
| 性别漂移（女脸出成男） | 补上 `[性别]` 与 `[妆容]` 两行；唇色写具体色相，不写"淡／灰／裸" |

---

