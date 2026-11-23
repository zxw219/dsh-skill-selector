> 参考使用：模板按当前任务调整；历史署名、器材和引语需查证。旧版本模型参数仅为示例，最终输出以 SKILL.md 的兼容规则为准。

# Greig Fraser 风格 AI 提示词库

按场景类型、情绪和影片参照分类的完整提示词模板，可直接用于 AI 图像/视频生成。

---

## 提示词架构

一个完整的弗莱瑟风格提示词由 6 层构成：

```
[摄影师签名] + [设备模拟] + [打光方案] + [色彩调性] + [构图描述] + [场景/氛围]
```

### 基础签名层（所有提示词的前缀）

```
Greig Fraser cinematography, shot on ARRI Alexa LF Mini with Panavision Ultra Vista lenses,
IMAX 65mm large format, motivated practical lighting, available light first, cinematic composition
```

简化版：
```
Greig Fraser style, ARRI Alexa LF, IMAX large format, motivated practical lighting, cinematic
```

---

## 一、按场景类型分类

### 🏜️ 沙漠史诗 — 厄拉科斯式

**参照**：《沙丘》《沙丘2》《抹大拉的玛丽亚》

```
Greig Fraser cinematography, shot on ARRI Alexa LF Mini with Panavision Ultra Vista 47mm,
IMAX 65mm large format expanded aspect ratio, real desert sunlight as primary key,
golden hour amber dunes stretching to horizon, atmospheric heat haze shimmer,
desaturated warm earth tones, single dramatic shadow direction,
[场景描述], telephoto compressed sandscape, monumental scale dwarfing human,
no artificial fill light, ARRI Alexa LF Dune Arrakis style
```

**变体 — 正午硬光大漠**：
```
Greig Fraser Dune midday style, white-hot tropical noon sun overhead,
zero shadows under feet, blinding desert glare, bleached amber tones,
heat shimmer mirage in telephoto distance, figures reduced to stark silhouettes,
no mercy in the sunlight, IMAX 65mm large format, available daylight only
```

**变体 — 黎明蓝紫沙漠**：
```
Greig Fraser Dune dawn style, cool pre-sunrise blue-violet light on dunes,
purple-pink horizon glow, low ambient illumination,
prophetic dreamlike atmosphere, single figure cresting dune ridge,
muted desaturated cool palette, IMAX 65mm contemplative quietude
```

**变体 — 沙暴遮蔽**：
```
Greig Fraser sandstorm style, diffused gray particulate haze obscuring vision,
flat omnidirectional ambient, monochromatic desaturated brown-gray,
figures emerging from sand wall, atmospheric obliteration,
real wind and dust on lens, ARRI Alexa LF environmental immersion
```

---

### ⚫ 红外黑白 — 吉迪主竞技场

**参照**：《沙丘2》Giedi Prime 段落

```
Greig Fraser infrared cinematography, shot on ARRI Alexa Mini LF infrared-modified,
black sun in white sky, ghostly porcelain skin tones, inverted tonality monochrome,
white foliage against black landscape, alien planet greyscale palette,
[场景描述], stark high-contrast black and white,
surreal otherworldly atmosphere, Giedi Prime arena style,
fireworks bursting as luminous white orbs, no green or color, pure infrared
```

**变体 — 红外肖像**：
```
Greig Fraser infrared portrait, ghostly porcelain bloodless skin,
eyes appearing as deep dark voids, hair dark or silver depending on chemistry,
black lips against white skin, surreal vampire-like presence,
infrared modified ARRI Alexa Mini LF, monochrome inverted tonality
```

**变体 — 红外景观**：
```
Greig Fraser infrared landscape, white grass against black sky,
white trees with black trunks, water as obsidian black,
clouds as pure white solid masses, alien Earth visualization,
high-contrast infrared monochrome, Giedi Prime planetary aesthetic
```

---

### 🌃 低光黑色城市 — 哥谭式

**参照**：《新蝙蝠侠》《真理之眼》

```
Greig Fraser noir cinematography, shot on ARRI Alexa Mini LF in extreme low-light,
sodium vapor amber street lamps as dominant light source,
deep underexposed shadows with preserved detail, wet asphalt orange reflections,
atmospheric rain or fog catching light, [场景描述],
red brake lights piercing through amber haze, blue police strobe lights,
embracing darkness as narrative element, The Batman Gotham noir style,
ARRI Signature Prime lens character flares
```

**变体 — 雨夜追逐**：
```
Greig Fraser Batman chase style, rain-soaked Gotham streets at night,
sodium vapor amber haze blanketing scene, red brake lights as only color accent,
extreme telephoto compression of taillights, motion blur and water spray,
deep blacks with sodium yellow highlights, urban gothic kinetic energy
```

**变体 — 单灯泡审讯**：
```
Greig Fraser interrogation style, single hanging tungsten bulb harsh top light,
half-lit face deep shadow opposite side, no fill light whatsoever,
warm amber pool of light surrounded by impenetrable black,
oppressive intimacy, single source minimalism, ARRI Alexa Mini LF noise grain
```

**变体 — 霓虹反射**：
```
Greig Fraser neon noir style, multicolored neon signs reflected in wet pavement,
character walking through pools of color, magenta and cyan accents,
amber dominance with neon punctuation, Blade Runner-adjacent but warmer,
practical neon lights all visible in frame, embracing chromatic complexity
```

---

### 🚀 虚拟制片 LED Volume — 曼达洛人式

**参照**：《曼达洛人》

```
Greig Fraser StageCraft LED Volume style, in-camera VFX virtual production,
real-time environment lighting from 270-degree LED wall, practical reflections on costume,
[场景描述], no green screen no compositing, immersive Star Wars universe atmosphere,
ARRI Alexa LF cinematic streaming framing, ARRI DNA LF Prime lenses,
seamless background-foreground integration, Mandalorian episode aesthetic
```

**变体 — 塔图因落日**：
```
Greig Fraser Mandalorian Tatooine style, double-sun golden hour sky,
warm amber sunset reflections on Beskar helmet, dust haze in low atmosphere,
silhouette against twin sun horizon, LED Volume practical lighting,
Western space frontier aesthetic, sodium-amber dominance
```

**变体 — 太空船舱**：
```
Greig Fraser Mandalorian cockpit style, cool blue starfield through windshield,
warm interior console glow on face, dual temperature contrast,
practical screen reflections in helmet visor, LED Volume star projection,
no compositing seam, ARRI Alexa LF immersive intimacy
```

**变体 — 火山熔岩**：
```
Greig Fraser Mandalorian volcanic style, glowing red lava as bottom-up key light,
warm orange-red illumination from below, deep shadows above eye line,
heat-distortion atmospheric haze, LED Volume real-time fire reflection,
infernal hell-planet aesthetic, dramatic underlighting
```

---

### 🎬 IMAX 大画幅人像 — 沙丘式

**参照**：《沙丘》《沙丘2》《新蝙蝠侠》（Selina Kyle 屋顶戏）

```
Greig Fraser IMAX 65mm portrait style, shot on ARRI Alexa LF + IMAX-certified Alexa 65,
1.43:1 expanded aspect ratio, monumental face composition,
extreme detail resolution showing skin pores and fabric texture,
[场景描述], large format shallow depth of field isolating subject,
Panavision Ultra Vista lenses with subtle character rendering,
contemplative still long take, IMAX cathedral-scale intimacy
```

**变体 — 仪式肖像**：
```
Greig Fraser Dune ceremonial portrait, 1.43:1 IMAX full frame,
character framed dead center monumentally, single dramatic key light,
ritualistic stillness, costume textile detail at maximum resolution,
Panavision Ultra Vista 65mm, large format spiritual gravitas
```

---

### 🌌 太空科幻 — 侠盗一号 + 曼达洛人

**参照**：《侠盗一号》《曼达洛人》

```
Greig Fraser Star Wars cinematography, ARRI Alexa LF/65 large format,
Panavision T-Series anamorphic lens flares horizontal blue streaks,
documentary-realist war-film handheld follow shots, gritty practical lighting,
[场景描述], multi-planet color palette diversity,
Star Wars universe authentic textures, Rogue One war epic style
```

**变体 — Scarif 热带海滩战**：
```
Greig Fraser Rogue One Scarif style, tropical paradise beach harsh sunlight,
turquoise lagoon water, palm tree shadows, AT-ACT walker silhouettes,
saturated tropical color contrasting with imperial white, anamorphic blue flares,
documentary handheld following soldiers in surf, war-film realism
```

**变体 — Jedha 沙漠尘暴**：
```
Greig Fraser Rogue One Jedha style, holy desert city sandstorm,
pale dusty amber haze, ancient stone architecture, Imperial occupation tension,
anamorphic horizontal frame, religious tension atmosphere,
ARRI Alexa 65 large format gritty texture
```

---

### 🌊 自然光室内 — 生命之钻 + 抹大拉的玛丽亚

**参照**：《生命之钻》《抹大拉的玛丽亚》

```
Greig Fraser available light interior, soft window light as only key,
no artificial fill, painterly Vermeer-like illumination on face,
period-accurate luminance, candlelight or oil lamp warm accents,
[场景描述], natural shadow gradients, contemplative stillness,
35mm or large format film aesthetic, Bright Star romantic naturalism
```

**变体 — 19 世纪英国春日**：
```
Greig Fraser Bright Star style, pale spring English meadow light,
soft overcast diffused daylight, lace curtain filtered window glow,
Romantic poet 19th century atmosphere, watercolor pale palette,
no artificial light, available natural illumination only
```

**变体 — 圣经沙漠**：
```
Greig Fraser Mary Magdalene style, Jordan valley golden hour,
robed figures in warm amber light, cyan empty desert sky,
ARRI Alexa 65 large format, Biblical poetic realism,
available sunlight only, ancient timeless atmosphere
```

---

### ❄️ 冰封肖像 — 狐狸猎手式

**参照**：《狐狸猎手》

```
Greig Fraser Foxcatcher cold style, Pennsylvania winter overcast pale gray-blue,
isolated mansion estate emotional distance, single tungsten study lamp warm pool,
fluorescent gymnasium clinical white, telephoto compressed isolation,
[场景描述], melancholy stillness, dual temperature contrast,
ARRI Alexa Plus + Cooke S4 Prime, psychological cinematography
```

---

## 二、按情绪分类

### 🏛️ 史诗 / 神话感

```
Greig Fraser epic cinematography, IMAX 65mm large format scale,
monumental composition with single human figure dwarfed by environment,
real natural light as primary key, golden hour or dramatic atmospheric conditions,
Panavision Ultra Vista anamorphic widescreen, slow contemplative camera movement,
mythic timeless atmosphere, Dune-scale grandeur
```

### 😈 黑色 / 罪恶

```
Greig Fraser noir style, sodium vapor amber dominance with deep underexposed shadows,
single motivated practical light source, wet streets reflecting orange,
embracing extreme low light, ARRI Alexa Mini LF push to ISO limits,
red and blue color punctuation through amber haze,
The Batman Gotham gothic atmosphere
```

### 👽 异星 / 超现实

```
Greig Fraser infrared surreal style, inverted tonality monochrome,
black sun white sky, ghostly porcelain skin, white foliage,
Giedi Prime alien planet aesthetic, infrared modified ARRI Alexa Mini LF,
high-contrast greyscale, no Earth-color reference
```

### 🕯️ 诗意 / 亲密

```
Greig Fraser intimate cinematography, single window light or candle,
available natural light only, soft directional shadow on face,
period-accurate luminance, painterly Vermeer-influenced lighting,
35mm film or large format aesthetic, contemplative stillness,
Bright Star romantic naturalism style
```

### 🔫 战争 / 现实

```
Greig Fraser war-film realism, documentary handheld follow shots,
natural daylight only, dust and smoke atmospheric haze,
gritty practical lighting, no glamour or beauty light,
infrared night-vision green for nighttime sequences,
Zero Dark Thirty / Rogue One war-realism aesthetic
```

### 🌌 沉思 / 预言

```
Greig Fraser prophetic vision style, cool blue-violet pre-dawn light,
soft diffused atmospheric haze, monumental quietude,
single contemplative figure on horizon, IMAX 65mm contemplative scale,
desaturated cool palette, dreamlike Dune prophetic atmosphere
```

---

## 三、按影片参照的完整提示词

### 《沙丘》风格

```
Greig Fraser Dune style, shot on ARRI Alexa LF Mini + IMAX-certified Alexa 65,
Panavision Ultra Vista lenses, IMAX 65mm 1.43:1 expanded aspect ratio,
real desert sunlight as primary key, golden Arrakis amber dunes,
cool Caladan ocean blue-green stone halls contrast,
single overhead practical chandelier in Atreides council,
atmospheric heat haze shimmer, telephoto sandworm distance compression,
[场景描述], no artificial fill light, monumental scale, contemplative pace
```

### 《沙丘2》红外段落风格

```
Greig Fraser Dune Part Two infrared style, shot on infrared-modified ARRI Alexa Mini LF,
Giedi Prime black sun in white sky, ghostly porcelain skin on Harkonnen warriors,
inverted tonality black and white, white foliage and black landscape,
fireworks bursting as luminous white orbs, alien planet greyscale,
[场景描述], surreal otherworldly atmosphere, no color whatsoever
```

### 《新蝙蝠侠》风格

```
Greig Fraser The Batman style, shot on ARRI Alexa Mini LF pushed to ISO 1280+,
Panavision Panaspeed + ARRI Signature Prime lenses,
sodium vapor amber Gotham street lighting, deep underexposed shadows preserved detail,
rain-soaked wet asphalt orange reflections, blue police strobe punctuating amber haze,
red brake lights piercing fog, single bulb interrogation harsh top light,
[场景描述], embracing darkness as style, urban gothic noir, telephoto compression
```

### 《曼达洛人》风格

```
Greig Fraser Mandalorian style, shot on ARRI Alexa LF + ARRI DNA LF Prime,
StageCraft LED Volume in-camera VFX, real-time environment lighting,
practical reflections on Beskar helmet, no green screen no compositing,
[场景描述], Star Wars universe authentic atmosphere, dual sun Tatooine golden hour,
warm amber sunset on chrome armor, immersive virtual production aesthetic
```

### 《侠盗一号》风格

```
Greig Fraser Rogue One style, shot on ARRI Alexa 65 + Panavision T-Series Anamorphic,
documentary-realist war-film handheld, anamorphic horizontal blue lens flares,
multi-planet color diversity (Scarif blue-green / Jedha amber / Eadu rainy gray),
gritty practical Star Wars lighting, low-angle epic figure framing,
[场景描述], real war-film texture, no traditional space-fantasy gloss
```

### 《猎杀本拉登》风格

```
Greig Fraser Zero Dark Thirty style, shot on ARRI Alexa Plus,
covert CIA black site harsh tungsten interrogation, monitor screen blue glow on face,
dusty Pakistani daylight amber sun, infrared night-vision green helicopter raid,
documentary-realist framing, available light commitment, no glamour,
[场景描述], procedural war-thriller authenticity
```

### 《狐狸猎手》风格

```
Greig Fraser Foxcatcher style, shot on ARRI Alexa Plus + Cooke S4 Prime,
Pennsylvania winter overcast pale gray-blue exterior,
isolated mansion estate emotional distance, single tungsten study lamp warm pool,
fluorescent gymnasium clinical white, telephoto compressed isolation,
[场景描述], psychological coldness, dual temperature contrast, melancholy stillness
```

### 《抹大拉的玛丽亚》风格

```
Greig Fraser Mary Magdalene style, shot on ARRI Alexa 65 large format,
Jordan valley golden hour amber, cyan empty desert sky, robed figures in warm light,
available natural sunlight only, painterly Biblical realism,
[场景描述], ancient timeless poetic atmosphere, monumental quietude
```

### 《生命之钻》风格

```
Greig Fraser Bright Star style, 35mm film aesthetic, available natural light,
soft window light filtered through lace curtain, candlelit interior amber accents,
pale spring English meadow daylight, watercolor pale palette,
[场景描述], 19th century Romantic poet atmosphere, Vermeer-like painterly stillness
```

---

## 四、打光方案模板

### 方案 A：单窗光（《生命之钻》《沙丘》卡乐丹）

```
LIGHTING SETUP — Fraser Single Window:

• KEY: Large soft window light (camera-left or camera-right), diffused naturally
• FILL: None — let opposite side fall into shadow
• PRACTICAL: Optional candle or oil lamp for warm accent (must be visible in frame)
• AMBIENT: Low — room naturally dark except window area
• SHADOW: Deep but with preserved detail in darkest areas
• COLOR TEMP: Window = cool daylight (5600K), Practical = warm tungsten (1800-2700K)
• MOOD: Contemplative, period-accurate, painterly
```

### 方案 B：单灯泡审讯（《新蝙蝠侠》Riddler 戏）

```
LIGHTING SETUP — Fraser Bulb Interrogation:

• KEY: Single hanging tungsten bulb directly overhead (visible in frame)
• FILL: None — embrace black
• PRACTICAL: Just the bulb itself
• AMBIENT: Near-zero — surrounded by impenetrable darkness
• SHADOW: Deep undereye shadows, half face in shadow
• COLOR TEMP: Warm tungsten (2700K) drowning in cool darkness
• MOOD: Oppressive intimacy, single source minimalism
```

### 方案 C：钠灯街景（《新蝙蝠侠》哥谭夜雨）

```
LIGHTING SETUP — Fraser Sodium Noir:

• KEY: Sodium vapor street lamps (visible in frame), characteristic amber-orange
• FILL: Reflected from wet asphalt, slight bounce
• PRACTICAL: All street lights, neon signs, car lights visible
• AMBIENT: Dense atmospheric rain or fog catching light
• ACCENT: Red brake/tail lights, blue police strobe
• SHADOW: Deep, but never solid black — sodium glow penetrates
• COLOR TEMP: Sodium 2200K dominant + cool 5600K + 8000K accents
• MOOD: Urban gothic, embraced underexposure
```

### 方案 D：太阳如灯（《沙丘》全片）

```
LIGHTING SETUP — Fraser Sun-as-Key:

• KEY: Real sun as massive HMI (no replacing with artificial)
• FILL: Sky bounce, sand reflection, no artificial fill
• PRACTICAL: None in exterior
• AMBIENT: Determined entirely by time of day and weather
• SHADOW: Determined by sun angle — accept hard noon shadows
• COLOR TEMP: Varies through day (3000K dawn → 5600K noon → 2500K sunset)
• MOOD: Cosmic indifference, planetary scale
```

### 方案 E：LED Volume 虚拟制片（《曼达洛人》）

```
LIGHTING SETUP — Fraser StageCraft Volume:

• KEY: 270° LED wall projecting environment as primary illumination
• FILL: Color-accurate ambient from LED panels
• PRACTICAL: All set-piece practicals also used
• AMBIENT: Volume-driven — entire space color-saturated
• SHADOW: Determined by virtual environment angle/intensity
• COLOR TEMP: Variable per environment (Tatooine 2500K / space 8000K / lava 1800K)
• MOOD: In-camera VFX immersion, no post compositing seam
```

### 方案 F：红外改装（《沙丘2》吉迪主竞技场）

```
LIGHTING SETUP — Fraser Infrared:

• CAMERA: ARRI Alexa Mini LF with IR filter modification
• KEY: Same physical lighting, but recorded in 720nm+ infrared spectrum
• RESULT: Sun/sky → black, skin → white, foliage → white, water → black
• FILL: None — high contrast preferred
• MOOD: Alien, vampiric, ritualistic, otherworldly
```

---

## 五、负面提示词（Negative Prompts）

以下元素与弗莱瑟风格矛盾，应在 SD/FLUX 的负面提示词中排除：

```
NEGATIVE (anti-Fraser):
flat HDR over-correction, neutralized white balance, fake daylight on sets,
green screen edges, obvious compositing seams, glossy beauty lighting,
soft glamour focus, evenly lit talking-heads television look,
cartoon shading, anime gradients, flat ambient occlusion,
washed-out cinematic LUT overuse, teal-and-orange Hollywood preset,
RGB gaming neon outline, drone aerial extreme angle, GoPro fisheye,
shaky handheld for no reason, action-cam over-stabilization,
plastic skin, smoothed-out detail, low-resolution upscale artifacts
```

---

## 六、画幅比例推荐

| 比例 | 用途 | 弗莱瑟实例 |
|------|------|-----------|
| **1.43:1** | IMAX 全画幅——史诗/仪式/亲密肖像 | 《沙丘》《沙丘2》IMAX 段落 |
| **2.39:1** | 宽银幕——史诗/壁画感 | 《沙丘》《新蝙蝠侠》《曼达洛人》主比例 |
| **1.78:1** | 流媒体标准 | 《曼达洛人》Disney+ 默认 |
| **1.85:1** | 标准院线——人物叙事 | 《狐狸猎手》《猎杀本拉登》 |
| **2.20:1** | Panavision Ultra Vista 原生 | 《沙丘》某些段落 |

**Midjourney 适配**：
- `--ar 143:100` 或 `--ar 143:100` → IMAX 全画幅
- `--ar 12:5` 或 `--ar 239:100` → 2.39:1 宽银幕
- `--ar 16:9` → 流媒体标准

---

## 七、组合推荐速查

| 场景 | 推荐影片参照 | 关键技法 | 主色调 |
|------|------------|---------|--------|
| 沙漠史诗 | 《沙丘》《沙丘2》《抹大拉的玛丽亚》 | 太阳如灯 + IMAX 65mm + 长焦压缩 | 金黄琥珀 |
| 红外异星 | 《沙丘2》吉迪主竞技场 | 红外改装 + 单光源 | 黑白反相 |
| 哥谭夜雨 | 《新蝙蝠侠》 | 钠灯 + 极低光 + 长焦 | 琥珀橙 + 红 + 蓝 |
| 太空船舱 | 《曼达洛人》《侠盗一号》 | LED Volume + 双色温 | 冷蓝 + 暖橙 |
| 圣经史诗 | 《抹大拉的玛丽亚》 | 自然光 + 大画幅 | 金黄 + 苍青 |
| 心理冷峻 | 《狐狸猎手》 | 长焦隔离 + 双色温 | 冷蓝 + 暖钨 |
| 战争纪录 | 《猎杀本拉登》《侠盗一号》 | 手持 + 自然光 + 夜视绿 | 沙黄 + 夜视绿 |
| 19 世纪诗意 | 《生命之钻》 | 单窗光 + 烛光 + 35mm | 苍白 + 烛黄 |
| 单灯审讯 | 《新蝙蝠侠》《老式黑色》 | 单灯泡 + 顶光 | 暖钨 + 深黑 |
| 火山熔岩 | 《曼达洛人》 | LED Volume 底光 | 红橙 + 黑 |
| 雪景冷调 | 《狐狸猎手》 | 平光 + 冷蓝 | 青灰 |
| 黎明预言 | 《沙丘2》保罗骑沙 | 蓝紫低光 + 大画幅 | 冷紫 + 粉橙 |
| 黄昏血战 | 《沙丘2》圣战 | 暖红低位太阳 | 血红 + 黑 |

---

## 八、跨场景过渡提示词（适合视频生成）

### 黎明 → 正午（沙漠时段过渡）

```
Greig Fraser desert time-lapse style, dawn cool blue-violet horizon
transitioning through golden hour amber to white-hot tropical noon,
shadow direction rotating, color temperature shifting from 3000K to 5600K,
heat haze intensifying, IMAX 65mm contemplative, Dune Arrakis day cycle
```

### 室内 → 室外（双色温走出）

```
Greig Fraser threshold transition style, warm tungsten interior to cool daylight exterior,
character walking from amber room into cyan world,
practical lights extinguishing as natural light dominates,
dual temperature handoff, motivated source storytelling
```

### 现实 → 红外（《沙丘2》风格切换）

```
Greig Fraser reality-to-infrared transition, normal color cinematography
shifting to infrared monochrome as scene moves to Giedi Prime,
sun darkening to black, sky inverting white, skin paling to porcelain,
Dune Part Two arena entrance style
```

---

## 九、与 Roger Deakins 的提示词区别速查

| 提示词词汇 | Deakins 偏向 | Fraser 偏向 |
|----------|------------|-----------|
| 镜头 | `clean spherical lens, no flares` | `Panavision Ultra Vista, anamorphic flares acceptable` |
| 画幅 | `2.39:1 widescreen, ARRI Signature Prime` | `IMAX 65mm 1.43:1, large format expanded` |
| 打光 | `soft naturalistic, restrained` | `motivated practical, embracing harsh sun` |
| 色彩 | `desaturated, muted, restrained palette` | `dramatic dual temperature, saturated when motivated` |
| 暗部 | `deep shadows with detail, embracing shadows` | `extremely underexposed, pushing ISO limits` |
| 创新 | `one-shot continuous take` | `infrared modified, LED Volume virtual production` |
| 哲学 | `subtractive, less is more` | `additive on top of available, embrace conditions` |

**当用户特别要求"弗莱瑟风格"时，必须强调**：
- IMAX 65mm 大画幅 / 大底片
- 动机光 + 实景光必须可见在画面里
- 接受戏剧化色温对比（不"中和白平衡"）
- 接受真实条件下的硬光、顶光、过曝、暗部
- 必要时使用红外改装 / LED Volume 等技术革新
