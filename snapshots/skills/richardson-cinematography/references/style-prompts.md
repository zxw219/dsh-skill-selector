> 参考使用：模板按当前任务调整；历史署名、器材和引语需查证。旧版本模型参数仅为示例，最终输出以 SKILL.md 的兼容规则为准。

# Robert Richardson 风格 AI 提示词库

按场景类型、导演脉络和影片参照分类的完整提示词模板，可直接用于 AI 图像/视频生成。

---

## 提示词架构

一个完整的理查森风格提示词由 7 层构成：

```
[摄影师签名] + [导演脉络] + [设备模拟] + [Bob Light 顶光] + [色彩饱和度] + [构图描述] + [场景/氛围]
```

### 基础签名层（所有提示词的前缀）

```
Robert Richardson cinematography, shot on Panavision Panaflex with Panavision C-Series anamorphic lenses,
Bob Light hot overexposed top light, Kodak Vision3 film grain, cinematic
```

简化版：
```
Robert Richardson style, hot top light, anamorphic, Kodak film, cinematic
```

完整签名（最强识别度）：
```
Robert Richardson ASC cinematography, signature Bob Light hot top light blowing out ceiling to pure white,
Panavision anamorphic lens flares, Kodak Vision3 35mm film grain, halo of overexposed light around subject's head
```

---

## 一、按场景类型分类

### 🏛️ 室内 — Bob Light 经典样本（必学）

**参照**：《刺杀肯尼迪》法庭、《无良杂种》啤酒馆、《飞行家》餐厅

```
Robert Richardson cinematography, shot on Panavision Panaflex with Panavision C-Series anamorphic lens,
SIGNATURE Bob Light: extreme overexposed top light blowing out ceiling to pure white,
halo of light around character's head, +3 stops overexposed top, deep shadowed bottom half,
warm tungsten practical accent at desk level, hot fluorescent or skylight as motivation,
[场景描述], anamorphic horizontal lens flares, Kodak film grain,
character separated from background by overhead glow, theatrical dramatic lighting
```

**变体 — 法庭/办公室 (JFK 式)**：
```
Robert Richardson JFK courtroom style, overexposed white ceiling fluorescents,
Bob Light halo around speaker at podium, deep shadowed audience below,
1960s wood-paneled American courtroom, theatrical lighting shifts mid-monologue,
35mm Kodak grain, ENR-processed high contrast, anamorphic Panavision
```

**变体 — 啤酒馆地下室 (Inglourious Basterds 式)**：
```
Robert Richardson Inglourious Basterds basement style, claustrophobic 1940s tavern,
overhead Bob Light hot fixture blowing out wooden ceiling,
warm amber kerosene lamps as practicals, dialogue tension at table,
deep shadows in corners, anamorphic Panavision flares, Kodak Vision3 grain,
period-accurate occupied France warm gold tones
```

---

### 🌅 室外 — 强阳光过曝

**参照**：《野战排》丛林、《被解救的姜戈》棉花田、《好莱坞往事》洛杉矶

```
Robert Richardson exterior style, harsh overexposed sunlight burning highlights,
direct sun in or near frame, hard backlight rimming subject silhouette,
visible volumetric light shafts through dust haze,
anamorphic Panavision horizontal flares streaking across frame,
[场景描述], deep shadow under subject, no fill light,
desaturated mid-tones to push highlight blowout, Kodak Vision3 250D
```

**变体 — 丛林战场 (Platoon 式)**：
```
Robert Richardson Platoon jungle style, hot tropical overexposed sunlight bursting through canopy,
low-angle silhouette of soldier against burning sky, smoke and dust catching light,
handheld documentary urgency, 35mm Kodak grain, deep shadow jungle floor,
Vietnam War run-and-gun camera, hard backlit foliage glowing
```

**变体 — 西部沙漠 (Django/Kill Bill Vol 2 式)**：
```
Robert Richardson spaghetti western style, Mexican desert harsh amber sunlight,
anamorphic Panavision lens flares from chrome and sun, dust haze in air,
hot top sun overexposing hat brim, long compressed telephoto landscape,
Tarantino homage to Sergio Leone, Kodak Vision3 saturated warm
```

---

### 🌃 夜景 — 霓虹饱和

**参照**：《赌城风云》拉斯维加斯、《好莱坞往事》Sunset Strip、《五维空间》纽约夜

```
Robert Richardson neon night style, vivid saturated red blue purple neon signs,
anamorphic horizontal flares streaking from neon, wet street reflections doubling lights,
Bob Light still present from streetlamp or sign overhead,
[场景描述], chrome car reflections catching neon,
high color saturation pushed to limit, Kodak Vision3 500T pushed,
1970s-80s cinematic neon urban atmosphere
```

**变体 — 拉斯维加斯赌场 (Casino 式)**：
```
Robert Richardson Casino Las Vegas style, opulent gold and red interior,
crystal chandelier overexposed white sparkle, neon casino floor saturated pink purple green,
mirror and polished marble reflections layered everywhere,
hot top spotlight gilding mob figures, Panavision anamorphic flares,
Scorsese 1970s glamorous decadence, Kodak film grain rich
```

**变体 — Sunset Strip (Once Upon a Time in Hollywood 式)**：
```
Robert Richardson 1969 Sunset Strip style, vivid neon signs red blue yellow saturated,
anamorphic Panavision flares from chrome muscle cars,
warm amber streetlamps, golden California dusk transitioning to night,
nostalgic 1969 Los Angeles warmth, Kodak Vision3 35mm grain rich
```

---

### ❄️ 雪景 — 雪盲式高光

**参照**：《八恶人》暴风雪、《杀死比尔 Vol.1》青叶屋雪夜、《禁闭岛》海岸

```
Robert Richardson snow whiteout style, pure white snow blowout no detail,
overwhelming white field dominating composition, blizzard whiteout exterior,
red blood drops on pure white snow as only color contrast,
[场景描述], cold blue tinted shadows, Bob Light from sky overexposed,
70mm or anamorphic Panavision wide framing,
eye-piercing assault of white, snow-blind moral void
```

**变体 — 暴风雪密室 (Hateful Eight 式)**：
```
Robert Richardson Hateful Eight style, Ultra Panavision 70 ultra-wide 2.76:1,
warm tungsten lantern interior haberdashery contrasted with pure white blizzard outside,
hot top kerosene lantern Bob Light overhead, anamorphic 70mm flares,
red blood on snow visible through doorway, Tarantino chamber piece tension,
Kodak 65mm film grain, period western interior
```

**变体 — 雪庭剪影 (Kill Bill Vol.1 式)**：
```
Robert Richardson Kill Bill snow garden style, lone figure silhouette in pure white snow,
single bare tree composition, vivid red blood pattern on snow,
cold moonlight hot top, anamorphic Panavision flares,
samurai sword catching backlight, Tarantino eastern western homage,
high contrast minimalist composition
```

---

### 🔥 火光 / 爆炸

**参照**：《无良杂种》电影院火灾、《野战排》村庄、《飞行家》飞机失事

```
Robert Richardson fire-lit style, intense orange and red flames consuming scene,
warm flickering firelight on faces, deep black shadow surrounding fire,
hot ember particles drifting through frame, smoke catching light,
[场景描述], anamorphic flares from flames, Kodak Vision3 saturated,
visceral heat and danger, dramatic chiaroscuro
```

**变体 — 电影院燃烧 (Inglourious Basterds 式)**：
```
Robert Richardson Inglourious Basterds burning cinema style,
intense red smoke filling theater, orange flames climbing curtains,
Shosanna's laughing face projected on smoke screen as ghost,
anamorphic Panavision flares, theatrical surreal apocalypse,
Tarantino vengeance fantasy, Kodak film grain heavy
```

---

### 💎 浮华室内 — Scorsese 镀金

**参照**：《赌城风云》、《飞行家》、《雨果》

```
Robert Richardson Scorsese gilded interior style, opulent warm golden tones throughout,
crystal chandelier overexposed white sparkle as Bob Light source,
Art Deco brass and mahogany interiors, polished marble floor reflections,
[场景描述], hot top light gilding subject as legend,
anamorphic Panavision flares, champagne gold fur and silk reflections,
1930s Hollywood / 1970s Vegas / 1900s Paris period luxury,
Kodak film rich grain
```

**变体 — 1930s 餐厅 (Aviator 式)**：
```
Robert Richardson Aviator 1930s nightclub style, 2-strip Technicolor red-green simulation,
crystal chandelier overexposed white, gilded brass railings,
Howard Hughes hot top halo Bob Light,
Art Deco geometric architecture, period-accurate Hollywood glamour,
Panavision anamorphic, faded technicolor pastels
```

**变体 — 1930s 巴黎火车站 (Hugo 式)**：
```
Robert Richardson Hugo Paris station style, warm amber gold throughout,
overexposed glass skylight Bob Light, golden volumetric light shafts through steam,
clock tower mechanical interiors gilded brass, Méliès theatrical stage flat colors,
3D depth composition, Scorsese romantic period magic, hand-tinted homage
```

---

### 🎞️ 混合格式拼贴

**参照**：《刺杀肯尼迪》《天生杀人狂》《尼克松》

```
Robert Richardson mixed format collage, single frame contains multiple film stocks:
Super 8 grainy faded memory footage with overexposed colors,
16mm documentary handheld with visible grain,
35mm cinematic color clarity for present reality,
B&W archival cut-in with high contrast,
Hi8 video tape with horizontal scan lines,
[场景描述], Oliver Stone fevered media-saturated collage,
political rage in visual chaos, hot top light Bob Light still present
```

**变体 — Stone 政治拼贴 (JFK 式)**：
```
Robert Richardson JFK style fevered collage, 1960s Dallas reconstruction,
Super 8 home movie footage of motorcade intercut with B&W news archival,
35mm color present-day investigation with hot top light courtroom,
real archival documentary mixed with dramatized reenactment,
Oliver Stone political conspiracy visual rage, ENR high contrast processing
```

**变体 — 心理拼贴 (Natural Born Killers 式)**：
```
Robert Richardson Natural Born Killers style, psychotic visual collage,
saturated red green blue gel lighting on actor's face shifting mid-shot,
projected backdrop behind characters revealing sky in sitcom kitchen,
B&W cut-in for guilt flashback, animation insert for confession,
Hi8 tape footage of TV news, anamorphic, hot top light, surreal hyper-saturation
```

---

### 👁️ 反射镜面戏

**参照**：《赌城风云》《禁闭岛》《飞行家》

```
Robert Richardson reflective composition style, mirror within frame revealing second image,
character looking at mirror that reveals hidden self or contradiction,
polished marble floor mirror reflection doubling composition,
glass partition with layered narratives visible simultaneously,
[场景描述], Bob Light hot top still present, anamorphic Panavision,
psychological complexity through reflective surfaces
```

**变体 — 身份镜像 (Shutter Island 式)**：
```
Robert Richardson Shutter Island mirror style, 1950s bathroom mirror revealing
unreliable identity, cold blue institutional fluorescent overhead,
hot top Bob Light blowing out ceiling tiles, anamorphic flares,
psychological dread atmosphere, fevered orange-red flashback bleeding into reflection
```

---

## 二、按导演脉络分类

### 🎬 Oliver Stone 脉络（炽烈拼贴）

```
Robert Richardson Oliver Stone collaboration style,
fevered multi-format collage: Super 8, 16mm, 35mm, B&W, Hi8 video intercut,
political rage visualized in visual chaos, theatrical jump-cut lighting changes,
hot top light Bob Light blowing out ceilings,
projected backdrops bleeding into reality, surreal stage lighting,
hyper-saturated psychotic color, ENR-processed high contrast,
[场景描述], 1960s-1990s American media-saturated atmosphere
```

**关键作品**: Platoon, Born on the Fourth of July, JFK, Natural Born Killers, Nixon, U Turn

---

### 🎩 Martin Scorsese 脉络（浮华金光）

```
Robert Richardson Martin Scorsese collaboration style,
opulent gilded warm gold interiors, crystal chandelier overexposed white sparkle,
Bob Light halo gilding subject as mythic figure,
Art Deco brass mahogany period luxury, polished marble floor reflections,
anamorphic Panavision Primo or C-Series flares,
[场景描述], 1900s-1970s glamorous decadence,
Kodak Vision3 rich grain, period authenticity
```

**关键作品**: Casino, Bringing Out the Dead, The Aviator, Shutter Island, Hugo

---

### 🎬 Quentin Tarantino 脉络（复古饱和）

```
Robert Richardson Quentin Tarantino collaboration style,
intensely saturated vivid color palette pushed to limit,
Panavision C-Series anamorphic horizontal lens flares,
Kodak Vision3 35mm film grain rich and visible (or 65/70mm),
Bob Light hot top in chamber piece interiors,
spaghetti western dust haze and hard sunlight,
[场景描述], homage-rich genre collage,
deliberate retro film stock aesthetic
```

**关键作品**: Kill Bill 1&2, Inglourious Basterds, Django Unchained, Hateful Eight, Once Upon a Time in Hollywood

---

## 三、按情绪分类

### ⚡ 政治愤怒 / 阴谋

```
Robert Richardson political conspiracy style, fevered media collage,
B&W archival news intercut with 35mm color reality,
hot top light Bob Light blowing out interrogation ceiling,
shadows of conspirators in corners, theatrical jump-cut lighting,
projected backdrops of historical events, ENR high contrast,
Oliver Stone JFK Nixon political dread atmosphere
```

### 💎 浮华堕落 / 黑帮兴衰

```
Robert Richardson decadent rise-and-fall style, opulent gilded interior,
crystal chandelier overexposed sparkle, mob figures gilded by Bob Light halo,
mirror reflections layering moral compromise, anamorphic flares,
Scorsese Casino glamour decay, Kodak film grain warm
```

### 🩸 暴力诗意 / 复仇

```
Robert Richardson Tarantino violent poetry style, vivid red blood
on saturated background, anamorphic Panavision flares,
hot top spotlight on avenger's face Bob Light,
slow-motion blood arcing through air, period film stock saturation,
Kodak Vision3 grain, choreographed brutal beauty
```

### 🌫️ 战争创伤 / 纪实

```
Robert Richardson war documentary style, handheld 16mm grainy footage,
hot tropical overexposed sunlight, run-and-gun urgency,
real exposure no fill light, blown out sky behind soldiers,
1960s-70s television news aesthetic, journalistic immediacy,
Vietnam Platoon Born on the Fourth of July atmosphere
```

### 🎩 怀旧 / 历史浪漫

```
Robert Richardson nostalgic period style, warm amber gold suffused,
hot top light Bob Light overexposed skylight or chandelier,
anamorphic Panavision soft flares, hand-tinted color homage,
2-strip or 3-strip Technicolor simulation for historical era,
faded postcard memory quality, Aviator Hugo Once Upon a Time atmosphere
```

### 🌀 心理不可靠 / 噩梦

```
Robert Richardson unreliable psyche style, mirror reflections splitting identity,
fevered orange-red flashback bleeding into cold blue reality,
jump-cut lighting changes mid-shot reflecting mental state,
anamorphic flares streaking across face, Bob Light blown ceiling,
Shutter Island Natural Born Killers psychological dread
```

---

## 四、按影片参照的完整提示词

### 《刺杀肯尼迪》(JFK) 风格

```
Robert Richardson JFK style, shot on Arriflex 35BL with Aaton 16mm and Beaulieu Super 8,
multi-format collage: Super 8 home movies, 16mm B&W documentary, 35mm color reality,
SIGNATURE Bob Light: hot overexposed top light blowing out 1960s courtroom ceiling fluorescents,
Garrison monologue with theatrical lighting shifts mid-shot,
Dealey Plaza recreation pseudo-archival footage,
Oliver Stone fevered political conspiracy collage,
ENR-processed high contrast, anamorphic where applicable,
[场景描述], 1960s-1990s American media-saturated atmosphere
```

### 《天生杀人狂》(Natural Born Killers) 风格

```
Robert Richardson Natural Born Killers style,
psychotic visual hurricane within single shot,
8mm 16mm 35mm B&W and animation intercut every few seconds,
Hi8 video tape with scan lines for TV news segments,
projected backdrops behind actors revealing surreal sky in domestic kitchen,
intense saturated red green blue Rosco gel lighting on faces,
hot top light Bob Light still present in chaos,
anamorphic Panavision flares, hyper-saturated psychotic color,
Oliver Stone media-rage manifesto, [场景描述]
```

### 《飞行家》(The Aviator) 风格

```
Robert Richardson Aviator style, shot on Panavision Panaflex Platinum with Primo lenses,
1927-1935 sequences in 2-strip Technicolor red-green simulation (no blue),
1935+ sequences in saturated 3-strip Technicolor full palette,
1930s Hollywood gilded glamour, crystal chandelier overexposed white,
Bob Light halo around Howard Hughes,
Art Deco brass mahogany interiors, polished surfaces reflecting glamour,
snow-blind white isolation room for paranoid scenes,
[场景描述], Scorsese opulent period authenticity
```

### 《雨果》(Hugo) 风格

```
Robert Richardson Hugo style, shot on Arri Alexa Plus 3D (Richardson's only digital 3D),
1930s Paris train station warm amber gold, overexposed glass skylight Bob Light,
golden volumetric light shafts through steam, clock tower mechanical interiors gilded brass,
Méliès silent cinema homage with hand-tinted color, theatrical stage flat backgrounds,
3D depth composition, [场景描述], Scorsese romantic period mechanical magic
```

### 《无良杂种》(Inglourious Basterds) 风格

```
Robert Richardson Inglourious Basterds style, shot on Panavision Panaflex with C-Series anamorphic,
1940s occupied France warm amber gold tones,
SIGNATURE Bob Light: hot overexposed top light blowing out farmhouse and basement ceilings,
anamorphic Panavision horizontal flares, claustrophobic dialogue tension,
period-accurate Kodak Vision3 grain rich,
burning cinema with red smoke and orange flames,
Shosanna face projected on smoke screen,
[场景描述], Tarantino spaghetti war homage
```

### 《被解救的姜戈》(Django Unchained) 风格

```
Robert Richardson Django Unchained style, shot on Panavision Panaflex Millennium XL2,
Antebellum South harsh sunlight on cotton fields,
white plantation pillars contrasted with red blood and brown earth,
anamorphic C-Series Panavision lens flares,
Bob Light hot top in Candyland mansion crystal chandelier interiors,
gilded slave-state decadence, spaghetti western dust haze,
Tarantino intense saturation, [场景描述], Kodak Vision3 film
```

### 《八恶人》(The Hateful Eight) 风格

```
Robert Richardson Hateful Eight style, shot on Panavision Ultra Panavision 70mm,
ULTRA-WIDE 2.76:1 aspect ratio (first use since 1966),
interior tungsten warm gold haberdashery — coffee pot copper, kerosene lanterns,
blizzard whiteout exterior pure white blowout no detail,
hot top kerosene lantern Bob Light overhead beam,
red blood on white snow visible through doorway,
anamorphic 70mm horizontal flares, Tarantino chamber piece tension,
[场景描述], Kodak 65mm film grain
```

### 《好莱坞往事》(Once Upon a Time in Hollywood) 风格

```
Robert Richardson Once Upon a Time Hollywood style,
Panavision 35mm + Panavision System 65 mixed format,
1969 Los Angeles golden afternoon sunlight, Sunset Strip neon vivid red blue saturation,
anamorphic Panavision flares from chrome 1960s muscle cars,
Cielo Drive amber dusk light, hot top Bob Light in studio backlot sets,
faded TV western show within film with desaturated period look,
Tarantino nostalgic warmth, Kodak Vision3 35mm grain rich, [场景描述]
```

### 《杀死比尔》(Kill Bill) 风格

```
Robert Richardson Kill Bill style, shot on Panavision with C-Series anamorphic + 65mm,
House of Blue Leaves yellow-black tracksuit against black ninja masses,
dramatic overhead spot Bob Light hot top, anime cel-shaded flashback intercut,
snow garden silhouette duel with vivid red blood on pure white,
Panavision anamorphic horizontal flares,
Tarantino vibrant homage saturation: yellow black red white primary palette,
eastern western collage, [场景描述]
```

### 《赌城风云》(Casino) 风格

```
Robert Richardson Casino style, shot on Panavision Panaflex Platinum with Primo lenses,
1970s Las Vegas casino opulent gold and red interiors,
crystal chandelier overexposed sparkle as Bob Light source,
neon casino floor saturated pink purple green,
mirror and polished marble reflections layered everywhere,
hot top spotlight gilding mob bosses as mythic figures,
Panavision anamorphic flares streaking, Scorsese 1970s glamorous decadence,
[场景描述], Kodak film grain warm
```

### 《禁闭岛》(Shutter Island) 风格

```
Robert Richardson Shutter Island style, shot on Panavision Panaflex Platinum,
1950s psychiatric institution cold blue-gray fluorescent,
hot top light Bob Light blowing out interrogation ceiling tiles,
fevered orange-red flashback memories bleeding into present,
snow-blind cliff coast exterior, mirror reflections revealing identity confusion,
anamorphic Panavision lens flares in storm scenes,
[场景描述], Scorsese psychological dread atmosphere
```

### 《野战排》(Platoon) 风格

```
Robert Richardson Platoon style, shot on Arriflex 35BL handheld documentary,
Vietnam War jungle, hot tropical overexposed sunlight bursting through canopy,
hard backlight rimming smoke and dust, low-angle silhouette of soldier,
deep shadow jungle floor, run-and-gun camera urgency,
35mm Kodak grain, real exposure no fill light, blown out sky,
[场景描述], Oliver Stone war journalism aesthetic
```

---

## 五、打光方案模板

### 方案 A：经典 Bob Light 顶光（最签名）

```
LIGHTING SETUP — Richardson Bob Light:

• KEY: Single overhead source pushed +3 stops over exposure (HMI / tungsten / fluorescent)
• MOTIVATION: Skylight, ceiling fixture, kicker spot, sun overhead
• FILL: None — let the bottom go dark
• PRACTICAL: Warm tungsten lamp at desk/table level (visible in frame)
• SHADOW: Deep, contrast ratio 8:1 to 16:1
• COLOR TEMP: Top light variable; bottom warm 2700K practical
• EXPOSURE: Top of frame fully blown out to pure white
• MOOD: Dramatic, theatrical, "halo of legitimacy" around subject
```

### 方案 B：混合格式拼贴（Stone 式）

```
LIGHTING SETUP — Richardson Stone Collage:

• KEY: Hot top light Bob Light still present
• PRIMARY FORMAT: 35mm color anamorphic
• INSERT FORMATS: Super 8 grainy / 16mm B&W / Hi8 video / archival
• COLOR: Hyper-saturated Rosco gels — red, blue, green zones
• BACKDROPS: Projected backdrops behind actors (surreal sky in living room)
• SHIFTS: Lighting can JUMP-CUT mid-scene
• MOOD: Media-saturated political rage
```

### 方案 C：Scorsese 镀金浮华

```
LIGHTING SETUP — Richardson Scorsese Gilded:

• KEY: Crystal chandelier overhead pushed +2 stops over (Bob Light)
• FILL: Warm bounce from gold/brass surfaces
• PRACTICAL: Lamps with amber bulbs visible everywhere
• REFLECTORS: Mirrors, polished marble, brass railings catching light
• COLOR TEMP: Warm 2800K throughout
• SHADOW: Deep but warm, never cold
• MOOD: Opulent legend-making, period luxury
```

### 方案 D：Tarantino 超饱和复古

```
LIGHTING SETUP — Richardson Tarantino Saturated:

• KEY: Hot top fixture or hard sun, anamorphic flare welcome
• FILL: Bounce or none, depending on scene
• PRACTICALS: Period-correct tungsten or kerosene
• COLOR: Pushed saturation in DI — primary R/G/B/Y all maxed
• LENS: Panavision C-Series anamorphic — embrace flares, oval bokeh
• FILM STOCK: Kodak Vision3 35mm or 65mm with rich grain
• MOOD: Genre homage, retro film stock authenticity
```

### 方案 E：纪录片新闻（Stone 早期）

```
LIGHTING SETUP — Richardson Documentary:

• KEY: 100% available light (sun, ceiling fluorescent, window)
• FILL: None — accept blown windows and crushed shadows
• CAMERA: Handheld 16mm or 35mm with shoulder rig
• EXPOSURE: Real — accept overexposure and underexposure
• LENS: Long zoom for snatched shots, wide for chaos
• MOOD: Journalistic urgency, moral immediacy
```

### 方案 F：雪盲式高光

```
LIGHTING SETUP — Richardson Snow-Blind:

• KEY: Sky bounce from snow, no shaping
• EXPOSURE: Snow pushed +2 stops over key reading
• SHADOWS: Cold blue tinted, never neutral
• ACCENT: Single warm interior light visible if interior cut
• COLOR: Pure white dominant, red blood as only saturation
• MOOD: Moral void, eye-piercing assault
```

---

## 六、负面提示词（Negative Prompts）

以下元素与理查森风格矛盾，应在 SD/FLUX 的负面提示词中排除：

```
NEGATIVE (anti-Richardson):
flat even lighting, low contrast, properly exposed ceiling,
dark top of frame, naturalistic protected highlights,
desaturated muted Deakins-style restrained color,
digital clean look, modern lens-corrected sterile,
single format pure cinematography, no grain,
documentary objectivity without theatrical flair,
ARRI Alexa with spherical primes (Deakins look),
soft natural Lubezki long take feel,
HDR even tone mapping, modern color science clean
```

---

## 七、画幅比例推荐

| 比例 | 用途 | 理查森实例 |
|------|------|-----------|
| **2.76:1** | Ultra Panavision 70 极宽史诗 | 《八恶人》 |
| **2.39:1** | 标准 anamorphic 宽银幕 | 《无良杂种》《被解救的姜戈》《杀死比尔》《赌城风云》《禁闭岛》 |
| **2.20:1** | 70mm 标准 | 《飞行家》部分段落、《好莱坞往事》65mm 段落 |
| **1.85:1** | 标准院线 | 《刺杀肯尼迪》《野战排》《雨果》 |
| **1.66:1** | 欧洲学院 | 部分早期作品 |
| **多比例混用** | 拼贴叙事 | 《刺杀肯尼迪》《天生杀人狂》— Super 8 / 16mm / 35mm 不同画幅在同片切换 |

**Midjourney 适配**：
- `--ar 69:25` → 2.76:1 Ultra Panavision 70（八恶人）
- `--ar 239:100` 或 `--ar 12:5` → 2.39:1 标准 anamorphic
- `--ar 11:5` → 2.20:1 70mm
- `--ar 37:20` 或 `--ar 37:20` → 1.85:1

---

## 八、组合推荐速查

| 场景 | 推荐影片参照 | 关键技法 | 主色调 |
|------|------------|---------|--------|
| 法庭独白 / 政治调查 | 《刺杀肯尼迪》 | Bob Light + 多格式 | 爆白顶 + 暖木色 |
| 啤酒馆/餐厅密谋 | 《无良杂种》 | Bob Light + anamorphic | 暖琥珀金 |
| 浮华赌场/夜总会 | 《赌城风云》《飞行家》 | 镀金 Bob Light + 反射 | 金红多彩 |
| 暴风雪密室 | 《八恶人》 | 雪盲 + 70mm 极宽 | 纯白 vs 暖橙 |
| 沙漠/西部 | 《被解救的姜戈》《杀死比尔 V2》 | 强阳光 + anamorphic 炫光 | 饱和橙黄红 |
| 丛林战场 | 《野战排》 | 纪录片手持 + 逆光 | 墨绿 + 爆光 |
| 1960s 政治阴谋拼贴 | 《刺杀肯尼迪》《尼克松》 | 多格式炽烈拼贴 | 黑白 + 彩色 |
| 心理崩溃 / 噩梦 | 《天生杀人狂》《禁闭岛》 | 跳光 + 镜面 | 跳变饱和 |
| 1969 LA 怀旧 | 《好莱坞往事》 | 35mm + 65mm 混合 | 金橙霓虹 |
| 巴黎 1930s 机械梦境 | 《雨果》 | 暖金过曝 + 蒸汽光柱 | 琥珀金 |
| 1950s 精神病院 | 《禁闭岛》 | 冷蓝 vs 闪回橙红 | 冷蓝 / 暖橙跳变 |
| Tokyo 暴力对决 | 《杀死比尔 V1》 | 黄黑对撞 + 雪上血红 | 黄黑红白 |
| 哥特雾夜 | 《断头谷》 | 冷月光 + 烛火暖橙 | 蓝灰 + 血红 |

---

## 九、Richardson 与其他大师的对比速查

**当用户说"我想要 Deakins 风格" → 不要给 Richardson 方案**：
- Deakins = 自然动机光、克制、无炫光、单一格式、去饱和
- Richardson = 戏剧性顶光过曝、anamorphic 炫光、多格式拼贴、超饱和

**当用户说"我想要 Lubezki 风格" → 不要给 Richardson 方案**：
- Lubezki = 自然光长镜头、广角流动
- Richardson = 戏剧化打光介入、剪辑式拼贴

**当用户提到"hot top light / Bob Light / 头顶光环" → 必定 Richardson**

**当用户提到"多种胶片格式 / Super 8 + 35mm 同片" → 必定 Richardson Stone 期**

**当用户提到"水晶吊灯 + 镀金 + 黑帮" → Richardson Scorsese 期**

**当用户提到"anamorphic 横向炫光 + 70mm + 复古" → Richardson Tarantino 期**

---

## 十、终极组合提示词模板（可直接套用）

```
🎬 [场景标题]

📽️ 影片参照：[最接近的理查森作品 + 场景]
🎭 导演脉络：[Stone / Scorsese / Tarantino]

**Style：**
Robert Richardson ASC cinematography, [导演脉络] collaboration style,
shot on Panavision Panaflex with [C-Series anamorphic / Ultra Panavision 70 / Primo],
SIGNATURE Bob Light: hot overexposed top light blowing out ceiling to pure white +3 stops,
halo of light around subject's head, anamorphic horizontal lens flares,
[色彩饱和度策略：saturated / gilded warm / desaturated whiteout],
Kodak Vision3 [50D / 250D / 500T] film grain rich,
[特殊技术：mixed film formats / 2-strip Technicolor / Ultra Panavision 70 wide]

**Scene：**
[具体场景描述，包含主体、环境、动作、氛围]

**Composition：**
[构图描述：anamorphic 2.39:1 / Ultra Panavision 2.76:1 / 1.85:1,
camera angle, framing, depth, reflective elements if any]

💡 打光笔记：Bob Light from [光源动机] pushed [+2/+3/+4] stops over,
practical [warm tungsten / kerosene / chandelier] at lower frame,
deep shadow bottom, contrast ratio [8:1 / 16:1].

🎨 色彩笔记：[色彩策略说明 — 饱和 / 镀金 / 雪盲 / 黑白拼贴]

🎞️ 格式笔记：[Kodak Vision3 35mm anamorphic / 65mm / Super 8 拼贴等]
```

---

**最后忠告**：理查森的精髓不在"漂亮"，而在"敢"——敢过曝、敢饱和、敢拼贴、敢炫光。提示词写作时不要回到 Deakins 那一套克制美学的舒适区。
