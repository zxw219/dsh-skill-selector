> 参考使用：模板按当前任务调整；历史署名、器材和引语需查证。旧版本模型参数仅为示例，最终输出以 SKILL.md 的兼容规则为准。

# Sven Nykvist 风格 AI 提示词库

按场景类型、情绪和影片参照分类的完整提示词模板，可直接用于 AI 图像/视频生成（Midjourney / Stable Diffusion / FLUX / DALL-E / Nano Banana Pro / ZenStudio 等）。

---

## 提示词架构

一个完整的尼科维斯特风格提示词由 6 层构成：

```
[摄影师签名] + [设备模拟] + [打光方案] + [色彩调性] + [构图描述] + [场景/氛围]
```

### 基础签名层（所有提示词的前缀）

```
Sven Nykvist cinematography, Bergman-era visual language, shot on Panavision Panaflex Gold
with Cooke Speed Panchro 50mm lens, single source naturalistic lighting, bounced reflected
illumination, intimate composition
```

简化版：
```
Sven Nykvist style, single source light, bounced reflection, Nordic naturalism
```

### 全局负面提示词（推荐通用）

```
anamorphic, lens flare, HDR, oversaturated colors, retouched skin, glamour lighting,
fill light visible, hard direct key light, magic hour orange tan, plastic skin,
shaky cam, Dutch angle, fisheye, multiple shadow directions, three-point lighting
```

---

## 一、按场景类型分类

### 🌫️ 北欧冷光内景（Nordic Cool Interior）

**参照**：《冬日之光》《沉默》《犹在镜中》《婚姻生活》

```
Sven Nykvist cinematography, shot on Mitchell BNC with Cooke Speed Panchro 50mm,
single window source casting pale Nordic skylight, soft diffused overcast illumination,
bounced reflection off white walls, no fill light, deep shadow on far side,
muted cool blue-gray palette, low-saturation skin tones, [场景描述],
minimalist Scandinavian interior, sparse furnishing, eye-level framing,
sustained stillness, Bergman-era restraint, Nordic naturalism
```

**变体 — 教堂式高窗光**：
```
Sven Nykvist Winter Light style, empty Lutheran rural church interior,
high clerestory window slanting pale beam down, silent ambient daylight,
cold gray stone walls, single candle warm accent, vertical sacred composition,
ash-gray monochrome palette, no artificial light, Bergman faith trilogy atmosphere
```

**变体 — 海岛多云光**：
```
Sven Nykvist Faro island style, summer overcast Nordic light,
silver-gray sea visible through window, four figures in geometric formation,
desaturated melancholy palette, glass and mirror reflections,
Through a Glass Darkly atmosphere, mental fragility light
```

---

### 👤 心灵特写 / 面孔光（The Bergman Face Close-up）

**参照**：《呼喊与细语》《假面》《秋日奏鸣曲》《冬日之光》

```
Sven Nykvist cinematography, intimate extreme facial close-up, soft 3/4 side key light
sculpting features from one direction only, half face fading into deep shadow,
catchlight in eyes, unretouched honest skin texture preserving every pore wrinkle freckle,
desaturated muted skin tones, slightly cool pale complexion,
[人物描述], face filling frame as landscape, sustained long take of emotional thought,
locked imperceptibly slow dolly-in, Bergman face lighting, no makeup glow,
single bounced reflected source, no fill, Sven Nykvist Persona Cries and Whispers style
```

**变体 — 双人面孔并置（Persona）**：
```
Sven Nykvist Persona iconic style, two women's faces side by side merging into one,
single hard side key light from one direction, half each face in pure white half in
absolute black, no gray midtones, identity dissolution composition, Faro summer interior,
extreme black and white contrast, mirror as conceptual frame
```

**变体 — 母女夜谈（Autumn Sonata）**：
```
Sven Nykvist Autumn Sonata style, mother and daughter night confrontation,
candlelight and single table lamp warm key, sustained dual close-up exchange,
autumn red-brown muted palette, Norwegian rural house interior at night,
two faces in opposing close-ups, raw emotional truth, no Hollywood polish
```

**变体 — 临终告白（Cries and Whispers）**：
```
Sven Nykvist Cries and Whispers blood-red room, woman in white nightgown lying in bed,
single candle warm key, blood-red walls reflecting onto skin, absolute black shadows,
Bergman three-color palette red-white-black, sustained close-up of dying face,
Liv Ullmann face lighting reference, Oscar-winning intimate cinematography
```

---

### ⛪ 宗教 / 精神性场景（Sacred / Spiritual Space）

**参照**：《冬日之光》《处女泉》《牺牲》《说谎》

```
Sven Nykvist cathedral light, empty sacred interior, high window beam slanting silently
down through cold air, single candle warm flicker as only color, gray stone walls,
vertical contemplative composition, figure dwarfed by architecture,
Lutheran austerity atmosphere, [场景描述], no artificial light at all,
patient sustained framing, silence as visual element, Bergman faith trilogy
```

**变体 — 中世纪仪式（Virgin Spring）**：
```
Sven Nykvist Virgin Spring style, medieval Swedish forest clearing,
high-contrast black and white, natural daylight only, single torch flame in dark interior,
deep blacks with detail in shadows, austere religious ritual atmosphere,
Mitchell BNC sharpness, ancient Scandinavian myth gravity
```

**变体 — 末世燃烧（The Sacrifice / Tarkovsky）**：
```
Sven Nykvist Tarkovsky Sacrifice style, Gotland island gray-blue dawn,
single sustained extremely long take, burning house orange flames against pale sky,
ascetic philosophical Nordic atmosphere, low-saturation cold base with apocalyptic warm
contrast, slow horizontal camera, spiritual gravity in landscape
```

---

### 🏠 家庭室内戏（Domestic Interior Drama）

**参照**：《婚姻生活》《芬妮与亚历山大》《罪与错》《另一个女人》

```
Sven Nykvist Scenes from a Marriage style, apartment interior with only practical lamps,
single window soft daylight, warm muted domestic palette, two-shot dinner table conversation,
sustained 8-minute close-up exchange, naturalistic ambient light, no movie lighting,
[场景描述], honest unembellished room, eye-level intimate framing,
Bergman marital realism, low-saturation truth
```

**变体 — 烛光宴会（Fanny and Alexander）**：
```
Sven Nykvist Fanny and Alexander candlelight masterpiece, opulent family Christmas dinner
lit only by hundreds of candles, warm red-gold glowing interior, Edwardian Swedish home,
multiple practicals across long table, faces glowing in soft candlelight,
rich textile and porcelain reflections bouncing warm light, Oscar-winning cinematography,
Kodak 5247 high-sensitivity warm grain
```

**变体 — 主教冷家（Fanny and Alexander 对比）**：
```
Sven Nykvist Fanny and Alexander cold bishop house, austere Lutheran severity,
cold blue ambient daylight, white sparse walls, no decoration, single chair single lamp,
opposite of family warmth, child Alexander imprisoned by visual coldness,
Bergman color dichotomy
```

**变体 — 曼哈顿犹太家庭（Crimes and Misdemeanors）**：
```
Sven Nykvist Woody Allen Manhattan style, Upper West Side apartment Sunday afternoon,
warm Jewish family dining table, window light from street, intellectual New York warmth,
1980s Manhattan interior, sustained dinner conversation, restrained urban naturalism
```

---

### 🪞 镜面与玻璃构图（Mirror & Glass Composition）

**参照**：《假面》《犹在镜中》《罪与错》《狼之时刻》

```
Sven Nykvist mirror motif composition, character confronting reflection in vintage mirror,
glass overlay merging two faces, layered identity, window as mirror with exterior bleeding
through interior reflection, [场景描述], single side key light defining both subject and
reflection, Persona-era visual philosophy, double image psychology,
soft bounced fill, Bergman identity dissolution atmosphere
```

**变体 — 化妆台（Vanity）**：
```
Sven Nykvist vanity mirror scene, woman seated at dressing table looking at her reflection,
single bedside lamp warm key, mirror doubling face into two narratives,
intimate domestic confession atmosphere, low-saturation skin, half face in shadow
```

**变体 — 玻璃叠影（Window Overlay）**：
```
Sven Nykvist window glass overlay, character's face reflected on window with rain or city
night beyond, two layers in single frame, melancholy urban interior,
single practical lamp inside, cold exterior light outside, restrained palette
```

---

### 🌆 户外北欧风景（Outdoor Nordic Landscape）

**参照**：《沉默》《耻辱》《牺牲》《犹在镜中》

```
Sven Nykvist Nordic landscape, Faro island summer overcast pale daylight,
silver-gray sea horizon, sparse windswept vegetation, tiny human figure in vast emptiness,
desaturated melancholy palette, no shadow direction, lingering dusk atmosphere,
[场景描述], Bergman island visual language, Scandinavian solitude
```

**变体 — 冬日教堂村（Winter Light）**：
```
Sven Nykvist Winter Light exterior, snow-dusted Swedish village,
empty wooden church silhouette against pale sky, frozen afternoon light,
ash-gray winter monochrome palette, solitary priest figure walking,
1960s rural Sweden austere atmosphere
```

---

### 🌃 夜景与烛光（Night & Candlelight）

**参照**：《呼喊与细语》《芬妮与亚历山大》《狼之时刻》

```
Sven Nykvist candlelight cinematography, single candle warm flicker as only key source,
warm orange falloff into deep black surroundings, faces lit from below by table candle,
unretouched skin glowing softly, intimate night confession atmosphere, [场景描述],
red textile or wood walls reflecting warm light, no electric light, no fill,
Bergman candlelight tradition, Fanny and Alexander warmth
```

**变体 — 哥特噩梦（Hour of the Wolf）**：
```
Sven Nykvist Hour of the Wolf style, gothic single candle illumination,
demonic uplight as exception, deep ink black shadows surrounding face,
glowing pale skin against absolute darkness, surreal nightmare interior,
black and white psychological horror
```

---

### 🎭 黑白经典（Classic Monochrome）

**参照**：《假面》《冬日之光》《沉默》《处女泉》《再见少年》

```
Sven Nykvist black and white cinematography, high-contrast monochrome,
single side key light only, half face in pure white half in absolute black,
no gray midtones, Mitchell BNC sharpness, [场景描述],
1960s Swedish art film aesthetic, Bergman-era purity, deep blacks with detail,
ash-gray midtones where present, austere Scandinavian framing
```

**变体 — 高调（High-Key BW）**：
```
Sven Nykvist Winter Light high-key monochrome, ash-gray palette dominating,
no deep blacks, pale ambient daylight everywhere, white-on-white desolation,
faded photograph quality, faith void atmosphere
```

**变体 — 低调（Low-Key BW）**：
```
Sven Nykvist Persona low-key monochrome, deep ink blacks dominating,
single hard side light, glowing pale face emerging from darkness,
identity dissolution composition, extreme contrast
```

---

## 二、按情绪 / 主题分类

### 💔 痛苦 / 临终

```
Sven Nykvist Cries and Whispers dying-woman style, blood-red walls, white nightgown,
single candle, sustained close-up of suffering face, sister's hand entering frame,
ultimate emotional intimacy, Bergman three-color discipline
```

### 🧘 信仰危机 / 沉默

```
Sven Nykvist Winter Light doubt style, empty church, priest's hollow face by window,
ash-gray monochrome, silence weighing on frame, no music no comfort,
faith-void atmosphere, Bergman spiritual emptiness
```

### 💑 婚姻 / 关系崩塌

```
Sven Nykvist Scenes from a Marriage style, kitchen table close-up of arguing couple,
naturalistic apartment light, sustained unbroken take, low-saturation domestic truth,
no music, eye-level framing, intimate marital realism
```

### 🧒 童年记忆

```
Sven Nykvist Fanny and Alexander childhood style, child wandering through opulent
candlelit family home, warm golden interior, magical realism through child's eyes,
toy theater glow, Edwardian Swedish nostalgia, Oscar-winning candlelight
```

### 🕯️ 忏悔 / 告白

```
Sven Nykvist confession style, single candle or table lamp, two figures close,
sustained dual close-up, low-saturation faces, restrained intimate framing,
sacred secular space, Bergman moral seriousness
```

### 🎭 身份消融 / 自我对峙

```
Sven Nykvist Persona identity style, two women's faces merging, mirror imagery,
extreme black and white contrast, single side light, Faro summer interior,
psychological boundary dissolving, iconic Bergman experimental visual
```

---

## 三、按合作导演分类

### 与 Ingmar Bergman（22 部）

```
Sven Nykvist + Ingmar Bergman collaboration, Faro island spirit, Bergman-era visual language,
single source bounced light, Cooke 50mm close-up, three-color palette discipline,
sustained close-up of human face as ultimate subject, philosophical intimate cinema
```

### 与 Andrei Tarkovsky（《牺牲》）

```
Sven Nykvist + Tarkovsky Sacrifice style, Gotland island gray-blue palette,
extremely long sustained take, philosophical cosmic scale, ascetic apocalyptic atmosphere,
slow horizontal motion, spiritual landscape gravity
```

### 与 Woody Allen（多部）

```
Sven Nykvist + Woody Allen Manhattan style, Upper East Side apartment afternoon light,
intellectual New York warmth, sustained dinner table conversation,
Crimes and Misdemeanors moral chiaroscuro, urban Bergman, restrained naturalistic
```

### 与 Roman Polanski（《苦月亮》）

```
Sven Nykvist + Polanski Bitter Moon style, cruise ship cabin warm amber practicals,
faded romantic memory tones, decadent intimate confession,
Mediterranean late-career restraint
```

### 与 Lasse Hallström（《不羁夜的欢愉》）

```
Sven Nykvist + Hallström Gilbert Grape style, small-town American naturalism,
faded summer warmth, restrained domestic interior, Iowa rural light,
Hollywood meets Bergman quietude
```

---

## 四、按镜头焦段分类

### 50mm 标准 — 双人对话

```
Sven Nykvist Cooke 50mm, two-shot dinner conversation, natural human perspective,
window light from one side, sustained unbroken take, eye-level intimate framing
```

### 75mm — 招牌心灵特写

```
Sven Nykvist signature 75mm close-up, face filling frame, soft side key light,
catchlight in eyes, unretouched skin, Bergman face landscape, sustained emotional take
```

### 85–100mm — 极致面孔解剖

```
Sven Nykvist 85mm extreme close-up, isolated facial detail, single bounced source,
half face in shadow, Persona-era extreme intimacy, no environment visible
```

### 25–35mm — 教堂 / 房间广角

```
Sven Nykvist 28mm Nordic interior, character small in austere room, vertical tall window
above, sparse furnishing, Lutheran spatial discipline, sustained static frame
```

---

## 五、完整组装示例

### 示例 1：默坐窗前的女性

```
🎬 Style：
Sven Nykvist cinematography, Bergman-era visual language, shot on Panavision Panaflex Gold
with Cooke 75mm, single soft north window source on subject's left, bounced reflection
off white wall, no fill light, deep shadow on right side of face, desaturated muted Nordic
palette with cool blue-gray base, unretouched honest skin texture preserving every pore,
catchlight in eye, restrained Bergman intimate atmosphere

🎬 Scene：
A Scandinavian woman in her thirties seated by a tall window in a sparse 1960s Swedish
apartment, looking out at pale overcast daylight, wearing a simple wool sweater,
hands resting in her lap, half her face illuminated by window light the other half fading
into shadow, sustained meditative stillness, no other figures in frame, faded wooden floor
and white wall behind

🎬 Full：
Sven Nykvist cinematography, Bergman-era visual language, shot on Panavision Panaflex Gold
with Cooke 75mm, single soft north window source on left, bounced white-wall reflection,
no fill light, deep shadow on right, desaturated cool blue-gray Nordic palette,
unretouched skin with every pore visible, catchlight in eye,
a Scandinavian woman in her thirties seated by a tall window in a sparse 1960s Swedish
apartment, looking out at pale overcast daylight, wearing simple wool sweater, hands in lap,
half face illuminated half in shadow, sustained meditative stillness,
1.66:1 aspect ratio, eye-level framing, Sven Nykvist Scenes from a Marriage style

💡 Lighting Note: Single window key + white wall bounce only. No fill. Story A: woman's
external composure. Story B: internal grief in shadowed half. — One Light, Two Stories.

🎨 Color Note: Cool gray-blue dominant + low-saturation skin. No accent color.
```

### 示例 2：烛光晚宴

```
🎬 Style：
Sven Nykvist Fanny and Alexander candlelight masterpiece style, Panaflex Gold + Kodak 5247
high-sensitivity stock, hundreds of candles as only light source across long dinner table,
warm red-gold opulent interior, soft warm falloff, multiple practicals reflecting in
porcelain and silver, faces glowing in candlelight, no electric light, low-saturation
warm palette with red-gold dominance

🎬 Scene：
An Edwardian Swedish family Christmas dinner around a long oak table, fifteen people
of all ages, women in dark velvet dresses, men in tailcoats, table set with white cloth,
porcelain, crystal glasses, hundreds of candles in candelabras and on the table, walls of
deep red velvet wallpaper, warm wood paneling, wide medium shot capturing entire table

🎬 Full：
[Style + Scene 合并]

💡 Lighting Note: Pure candlelight cinematography. Kodak 5247 fast stock allowed
shooting at f/2.0 with candle-only exposure. No movie lights at all.

🎨 Color Note: Red-gold dominant palette, classic Bergman warm interior, restricted to
candle warmth + deep red walls + warm wood.
```

### 示例 3：教堂内部

```
🎬 Style：
Sven Nykvist Winter Light cathedral style, Mitchell BNC + Cooke 35mm, high clerestory
window beam slanting silently down, ash-gray monochrome palette, no artificial light,
cold stone walls, vertical sacred composition, ascetic Bergman religious melancholy

🎬 Scene：
A small empty Lutheran rural church in Sweden in 1960s winter afternoon, wooden pews
in foreground, simple altar in background, a single priest figure in dark robe standing
small at the altar, dust motes visible in the slanting window beam,
weathered stone walls, no congregation

🎬 Full：
[Style + Scene 合并]

💡 Lighting Note: Pure window daylight. Nykvist and Bergman waited for the exact angle
of winter sun before rolling. — One Light, Sacred.

🎨 Color Note: Ash-gray monochrome — almost no black, almost no white pure, just gray
midtones suspending faith in doubt.
```

---

## 六、模型适配速查

### Midjourney 8.2

```
[prompt] --raw --ar 83:50 --s 100
```

关键词强化：`Sven Nykvist`, `Bergman cinematography`, `single source`, `Nordic light`,
`bounced reflection`, `unretouched skin`

### FLUX.1 / Stable Diffusion XL

正面：
```
Sven Nykvist cinematography, Ingmar Bergman style, single source naturalistic lighting,
bounced reflected light, Mitchell BNC, Panavision Panaflex, Cooke Speed Panchro 50mm,
unretouched honest skin, desaturated Nordic palette, eye-level framing
```

负面：
```
anamorphic, lens flare, HDR, oversaturated, retouched skin, glamour lighting,
Hollywood orange tan, fill light, three-point lighting, plastic skin,
shaky cam, Dutch angle, fisheye, magic hour, golden hour orange
```

### DALL-E 3 / GPT Image

自然语言描述：
```
A photo in the style of Sven Nykvist's collaboration with Ingmar Bergman: single window
light from one side, the other half of the face fading into deep shadow, no fill light,
unretouched skin texture, desaturated cool palette, sustained intimate close-up.
```

### Nano Banana Pro / ZenStudio

中英混合：
```
Sven Nykvist 风格, Bergman cinematography, single source 单光源, bounced reflection 反射光,
Nordic naturalism, unretouched skin 皮肤纹理保留, [场景描述], 低饱和北欧色调,
eye-level intimate framing, 1.66:1
```

---

## 七、常见错误避免

| ❌ 错误做法 | ✅ 正确做法 |
|-----------|-----------|
| `cinematic golden hour orange` | `pale Nordic overcast skylight` |
| `dramatic three-point lighting` | `single source, no fill, bounced reflection` |
| `flawless beauty skin glow` | `unretouched honest skin, every pore visible` |
| `vibrant colorful palette` | `desaturated three-color discipline` |
| `anamorphic lens flare` | `spherical Cooke prime, no flare` |
| `low angle hero shot` | `eye-level dignified framing` |
| `quick montage cuts` | `sustained long take, no cutting` |
| `crowded composition` | `minimalist sparse Nordic restraint` |

---

## 八、记忆口诀

> **"一束光，两个故事。"**
> One light. Two stories.

> **"皮肤是真相，阴影是叙事。"**
> Skin is truth. Shadow is narrative.

> **"少即是雄辩。"**
> Less is eloquence.

> **"光必须有理由——来自窗、烛、信仰，而非好莱坞。"**
> Light must have reason — from window, candle, or faith. Never from Hollywood.

这些口诀是激活尼科维斯特视觉灵魂的关键。在写每一句提示词之前，先问自己：这束光来自哪里？它在讲谁的故事？
