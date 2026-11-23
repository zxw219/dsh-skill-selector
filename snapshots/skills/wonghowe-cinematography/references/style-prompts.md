> 参考使用：模板按当前任务调整；历史署名、器材和引语需查证。旧版本模型参数仅为示例，最终输出以 SKILL.md 的兼容规则为准。

# James Wong Howe 黄宗霑 风格 AI 提示词库

按场景类型、情绪和影片参照分类的完整提示词模板，可直接用于 AI 图像/视频生成（Midjourney、Stable Diffusion、FLUX、DALL-E、Nano Banana Pro、ZenStudio）。

---

## 提示词架构

一个完整的黄宗霑风格提示词由 6 层构成：

```
[摄影师签名] + [设备/胶片模拟] + [低调打光方案] + [色调/黑白调性] + [低角度/深焦构图] + [场景/氛围]
```

### 基础签名层（所有提示词的前缀）

```
James Wong Howe cinematography, shot on Mitchell BNC with Cooke Speed Panchro lens,
low-key lighting with single hard key source, deep shadows dominating frame,
1950s black and white silver-gray tonal range, classic Hollywood Golden Age aesthetic
```

简化版：
```
James Wong Howe style, Mitchell BNC, low-key lighting, black and white, low angle, 1950s
```

彩色版（用于《血与沙》《飞瀑怒潮》《Funny Lady》风格）：
```
James Wong Howe Technicolor style, three-strip color, oil-painting saturated palette,
1940s-1970s period color, Mitchell BNC + Technicolor camera
```

---

## 一、按场景类型分类

### 🌑 黑白低调打光 — 室内单光源（最经典 Wong Howe）

**参照**：《艾尔及利亚》《光荣》更衣室、《大公无私》21 Club、《原野铁汉》农舍

```
James Wong Howe cinematography, shot on Mitchell BNC with Cooke 35mm lens,
single hard bare bulb hanging overhead as only light source,
60-80% of frame in deep impenetrable shadow, NO fill light,
silver-gray tonal range with living shadow detail,
chiaroscuro on face — half lit half in darkness, top light creating eye-socket shadows,
[场景描述], 1950s black and white film noir aesthetic,
Kodak Plus-X grain, low angle camera position from waist height
```

**变体 — 玫瑰纹身式炽热室内**：
```
James Wong Howe Rose Tattoo style, harsh Mediterranean Sicilian sunlight piercing through windows,
single source dramatic key on Anna Magnani-style passionate face,
deep shadows in modest cluttered interior, religious icon practical light accent,
silver-gray B&W with explosive high contrast, 1955 Tennessee Williams Southern heat aesthetic
```

**变体 — Hud 式干旱农舍**：
```
James Wong Howe Hud style, dry Texas Panhandle interior,
single bare bulb above kitchen table, vast shadow areas,
Paul Newman-style anti-hero face half in darkness, dust motes in light beam,
Panavision widescreen 1.85:1, modern Western moral grit,
1963 black and white drought aesthetic
```

---

### 🥊 拳击场长镜头 / 运动摄影（黄宗霑革命）

**参照**：《光荣》(*Body and Soul*) 拳击高潮、《天罗地网》

```
James Wong Howe Body and Soul boxing style, immersive handheld inside boxing ring,
roller skate mounted Eyemo camera circling fighters at low angle,
single overhead bare bulb above ring as harsh key light,
deep shadows on roaring crowd faces in foreground,
sweat droplets and motion blur on shirtless boxer,
chiaroscuro silver-gray B&W, 1947 film noir boxing classic,
[场景描述], deep focus three-plane staging — crowd / fighters / opponent corner all sharp,
Mitchell BNC + handheld Eyemo, no cuts within ring sequence
```

**变体 — 拳手特写**：
```
James Wong Howe boxer close-up, low angle hero shot from below the ropes,
bare bulb harsh top light on sweat-glistening face,
black background with single rim of light on shoulder,
mouth bleeding swollen eye, deep shadow in eye sockets,
1947 Body and Soul intensity, B&W high contrast
```

**变体 — 拳击场长镜头连续运动**：
```
James Wong Howe continuous boxing tracking shot, single take following two fighters,
camera circling at floor level as boxers dance,
crowd silhouettes in foreground OOF, ring ropes whipping past frame,
chiaroscuro arena lighting, sweat and motion in B&W,
roller skate gliding camera movement, 1947 immersive ringside POV
```

---

### 🌧️ 雨夜湿街 — film noir 黑色诗篇

**参照**：《大公无私》(*Sweet Smell of Success*) 纽约凌晨、《艾尔及利亚》卡斯巴雨夜、《柏林快车》战后废墟

```
James Wong Howe Sweet Smell of Success style, rain-slicked Manhattan street at 3am,
neon signs reflecting on wet pavement doubling all light sources,
manhole steam rising in cold air, rain particles falling through lamplight,
hidden camera documentary realism Times Square 1957,
deep chiaroscuro B&W, low angle skyscraper canyon perspective,
silver-gray tonal mastery, [场景描述],
Mitchell BNC + Eyemo hidden in cardboard box, real location
```

**变体 — 卡斯巴雨夜迷宫**：
```
James Wong Howe Algiers Casbah style, North African rainy night labyrinth,
oil lamp practical lights in deep alley shadows,
arched stairways and metal gates creating layered framing,
mature 1938 proto-noir chiaroscuro, no fill light,
Mitchell BNC, James Wong Howe pre-noir aesthetic
```

**变体 — 战后柏林废墟**：
```
James Wong Howe Berlin Express style, post-war 1948 ruins documentary realism,
natural overcast light over bombed buildings, atmospheric steam from rubble,
real location shooting in destroyed Berlin, train station harsh lamps,
gritty silver-gray B&W, pre-Italian Neorealism aesthetic
```

---

### 📐 低角度仰拍（"Low Howe" 招牌）

**参照**：《原野铁汉》Hud 仰拍、《大公无私》纽约高楼、《艾比林镇》西部牛仔

```
James Wong Howe "Low Howe" signature low angle,
ground-level camera position with ceiling visible in frame,
wide angle 25mm-35mm lens with perspective distortion,
character towering over camera as anti-hero or threat,
oppressive ceiling pressing down, deep shadows in upper corners,
[场景描述], B&W high contrast, Mitchell BNC, classical Hollywood low angle drama
```

**变体 — 反英雄仰拍特写**：
```
James Wong Howe Hud anti-hero low angle close-up, Paul Newman-style face from below,
hat shadow obscuring eyes, hard sunlight from above,
sweat and dust on weathered face, sky as bright background,
1963 modern Western moral ambiguity, B&W silver-gray, 35mm wide angle distortion
```

**变体 — 城市高楼仰角**：
```
James Wong Howe Sweet Smell skyscraper low angle, looking up at Times Square towers,
neon signs reaching into night sky, vertical lines converging,
people in foreground as silhouettes, oppressive urban scale,
1957 New York B&W noir, Mitchell BNC wide angle perspective
```

---

### 🔍 深焦戏剧调度（Deep Focus Drama）

**参照**：《Transatlantic》《光荣》拳击场、《艾尔及利亚》

```
James Wong Howe deep focus cinematography, foreground middle-ground background ALL sharp,
f/8 to f/16 depth of field with strong key lighting,
wide angle 25mm-35mm lens, characters at multiple depths in single frame,
dramatic staging in depth — action in foreground while reaction in background,
1940s-1950s deep focus aesthetic, pre-Citizen Kane influence,
[场景描述], B&W silver-gray, Mitchell BNC + 5K-10K arc lights
```

**变体 — 三层人群调度**：
```
James Wong Howe deep focus crowd staging, foreground hands and props sharp,
mid-ground main character in dramatic action, background secondary characters reacting,
all planes simultaneously in focus, theatrical multi-action composition,
1947 Body and Soul style depth, low-key lighting, B&W chiaroscuro
```

**变体 — 室内深焦门廊**：
```
James Wong Howe deep focus interior, foreground table with practical lamp,
mid-ground character standing in doorway, distant room visible through corridor,
all sharp from inches to infinity, Mitchell BNC + wide angle Cooke lens,
1940s low-key drama, single source key light
```

---

### 🎭 伪一镜到底 / 长镜头（Pseudo Long Take）

**参照**：《光荣》拳击连续镜头、《飞瀑怒潮》舞会环绕

```
James Wong Howe pseudo long take cinematography, continuous flowing single shot,
crab dolly omnidirectional smooth movement, camera following multiple characters
through complex blocking, choreographed lighting changes within shot,
no apparent cuts, documentary immersive feel, 1950s technical innovation,
[场景描述], Mitchell BNC + crab dolly + practical lights,
B&W or color depending on era
```

**变体 — Picnic 月夜舞会环绕**：
```
James Wong Howe Picnic dance scene, crab dolly rotating around dancers,
Chinese lantern warm color glow, William Holden Kim Novak romantic embrace,
moonlit Kansas summer night CinemaScope, 1955 Technicolor,
continuous lyrical movement, period romantic atmosphere
```

---

### 📰 伪纪录 / 实景街拍（Hidden Camera Documentary）

**参照**：《大公无私》时代广场、《柏林快车》柏林废墟、《新闻先生》街头新闻

```
James Wong Howe hidden camera documentary realism,
real location street photography 1950s, camera concealed in cardboard box or vehicle,
authentic passersby in frame unaware of filming, natural ambient available light,
gritty newsreel quality, no studio recreation,
[场景描述], pre-Italian Neorealism authenticity, B&W silver-gray,
handheld Eyemo + Mitchell BNC, real urban texture
```

**变体 — 时代广场 1957 凌晨**：
```
James Wong Howe Times Square 1957 hidden camera, real Manhattan dawn,
neon signs flickering, real night workers and revelers walking past,
camera at street level catching authentic urban life,
Sweet Smell of Success documentary aesthetic, B&W with neon highlights
```

---

### 🌫️ 蒸汽与雾氛围（Steam & Fog Atmosphere）

**参照**：《大公无私》纽约街、《柏林快车》废墟、《艾尔及利亚》卡斯巴

```
James Wong Howe atmospheric steam style, manhole steam rising in cold city night,
fog and humidity diffusing all light sources, halos around street lamps,
visible breath in cold air, atmospheric haze creating layered depth,
silver-gray B&W with luminous fog, [场景描述],
1950s urban atmospheric drama, Mitchell BNC + practical lights
```

---

### 🎨 Technicolor 油画饱和（彩色实验）

**参照**：《血与沙》斗牛士、《飞瀑怒潮》、《Funny Lady》

```
James Wong Howe Technicolor three-strip color cinematography,
oil-painting saturated palette inspired by Velazquez, Goya, El Greco,
Spanish bullfighter red yellow and black, dramatic chapel candlelight contrasts,
1941 Blood and Sand color masterpiece, ornate religious iconography,
[场景描述], strong key light to feed Technicolor density,
3-strip Technicolor camera, period saturated reds and golds
```

**变体 — Funny Lady 怀旧歌舞**：
```
James Wong Howe Funny Lady 1975 backstage nostalgia, warm amber 1930s nightclub stage,
sepia-toned period color, Streisand-era glamour close-up with soft diffusion,
period stage lights with halation, supper club elegance,
1930s Art Deco production design, classical Hollywood color palette
```

---

### 🎯 单光源人物特写（Single-Source Portrait）

**参照**：Anna Magnani《玫瑰纹身》、Paul Newman《原野铁汉》、Burt Lancaster《大公无私》

```
James Wong Howe single source star portrait, precisely controlled eye light catchlight,
half-lit face with deep shadow on opposite side,
top light from above creating eye socket shadows,
sculpted facial planes — bones revealed by shadow,
classical Hollywood glamour with hard edge, no soft beauty fill,
[人物描述], B&W silver-gray, Mitchell BNC + 75mm Cooke lens,
1950s star face lighting
```

**变体 — 男星硬朗特写（Burt Lancaster / Paul Newman 式）**：
```
James Wong Howe leading man hard portrait, low angle close-up from below,
single hard key carving cheekbone and jawline,
deep shadow under brow ridge, eyes catching single sharp light,
silver-gray B&W with masculine grit, 1957-1963 era
```

**变体 — 女星雕刻特写（Anna Magnani / Lana Turner 式）**：
```
James Wong Howe female star portrait, single key from camera-front 3/4,
fill bounce barely lifting shadow side, eye catchlight precisely placed,
slight diffusion through black net or stocking softening texture but preserving structure,
1940s-1950s glamour with edge, B&W Hollywood Golden Age
```

---

### 🏛️ 监狱 / 机构 / 压迫空间

**参照**：《艾尔及利亚》卡斯巴、《飞越疯人院》(顾问)、《光辉时刻》煤矿

```
James Wong Howe institutional oppression style, harsh overhead bare bulbs,
geometric architectural shadows from bars/grates/blinds,
cold cell or mineshaft interior, single hanging light swinging,
deep shadows engulfing peripheral space, only central area lit,
[场景描述], B&W chiaroscuro 1940s-1950s, Mitchell BNC,
dehumanizing institutional perspective
```

**变体 — 煤矿黑暗（Molly Maguires 式）**：
```
James Wong Howe Molly Maguires mine style, pitch dark mine shaft,
single helmet headlamp as only light, coal dust in beam,
1970 desaturated color shot like B&W, gray-blue-green palette,
Pennsylvania mining tragedy, claustrophobic underground horror
```

---

### 🌅 西部荒野 / 露天日光

**参照**：《艾比林镇》《原野铁汉》《风流绅士》《血与沙》

```
James Wong Howe Western frontier style, harsh overhead high-noon sunlight,
strong directional shadows, dust kicking up, sweat and parched earth,
low angle hero cowboy framing, sky as overexposed white background,
deep shadows under hat brims, [场景描述],
B&W silver-gray with explosive contrast, Mitchell BNC + 25mm wide angle,
1940s-1960s Western iconography
```

**变体 — Hud 干旱平原**：
```
James Wong Howe Hud Texas plains, infinite flat horizon,
bleached white sky, low angle of cattle and weathered ranchers,
1963 modern Western moral grit, Panavision widescreen B&W,
wind-blown dust in foreground
```

---

### 🎬 极广角主观噩梦（Seconds 式实验）

**参照**：《Seconds》(1966) 身份噩梦

```
James Wong Howe Seconds extreme wide angle nightmare,
9.8mm Kinoptik fisheye subjective POV, distorted curved horizons,
head-mounted camera disorienting movement, paranoid perspective,
harsh high-contrast B&W with overexposed clinical whites,
surgical operating room horror, identity dissolution,
1966 Frankenheimer experimental cinema, surreal disorientation
```

---

## 二、按情绪分类

### 😰 紧张 / 悬疑（Suspense）

```
James Wong Howe suspense style, single bare bulb swinging slightly creating moving shadows,
60% of frame in impenetrable darkness, character partly hidden in shadow,
silence visualized through stillness — locked-off Mitchell BNC,
predatory low angle from waist height, B&W high contrast,
no music — only shadow does the talking,
1940s-1950s film noir tension
```

### 💔 绝望 / 沉重（Despair）

```
James Wong Howe despair style, lone figure dwarfed by deep shadows,
single dim practical light far in background, character moving away from camera,
silver-gray B&W with crushed lower mid-tones, oppressive ceiling visible,
1947 Body and Soul morning-after defeat aesthetic, low angle from floor
```

### 🌟 救赎 / 微光（Redemption）

```
James Wong Howe redemption style, single shaft of warm light breaking deep darkness,
character stepping from shadow into circle of light,
B&W with luminous highlights in otherwise dark frame,
single source key as moral spotlight, 1955 Rose Tattoo emotional release
```

### 😡 暴力 / 对峙（Violence）

```
James Wong Howe violence style, harsh unflinching low angle from below,
single hard key carving aggressor's face, victim in shadow foreground,
documentary brutality without stylization, no slow motion,
1947 Body and Soul ringside punishment, B&W chiaroscuro
```

### 🕊️ 怀旧 / 时代消逝（Nostalgia）

```
James Wong Howe nostalgia style, soft amber period light,
1930s-1940s era recreation, Streisand-era glamour diffusion,
Funny Lady backstage warmth, period-accurate practical lights,
warm color or silver B&W with halation,
classical Hollywood Golden Age elegance fading
```

### 🌃 都市孤独（Urban Loneliness）

```
James Wong Howe urban loneliness style, lone figure on rain-slicked Manhattan street,
neon signs reflected in puddles, vast empty pavement,
1957 Sweet Smell of Success 3am desolation, hidden camera distance,
B&W with luminous wet reflections, single trench coat silhouette
```

### 🥊 体力与汗水（Physical Exertion）

```
James Wong Howe physicality style, sweat glistening under harsh single overhead bulb,
muscle definition revealed by side rim light, breath visible in cold gym air,
1947 Body and Soul boxing intensity, low angle from floor,
chiaroscuro B&W, motion blur on swinging fists
```

---

## 三、按影片参照的完整提示词

### 《艾尔及利亚》(*Algiers*, 1938) 风格

```
James Wong Howe Algiers style, shot on Mitchell BNC,
North African Casbah labyrinth low-key lighting,
arched stairways and metal gates creating layered architectural framing,
oil lamp practical lights in deep alley shadows,
mature 1938 proto-noir chiaroscuro silver-gray, NO fill light,
Hedy Lamarr-style luminous portrait against dark background,
[场景描述], pre-noir aesthetic foundation
```

### 《光荣》(*Body and Soul*, 1947) 风格

```
James Wong Howe Body and Soul style, shot on Mitchell BNC + handheld Eyemo,
revolutionary 1947 boxing cinematography, roller skate mounted camera circling fighters,
single overhead bare bulb above ring as harsh key, deep shadows on crowd,
low angle hero fighter shot, sweat and motion blur in chiaroscuro,
locker room single bulb between rounds, John Garfield era boxing tragedy,
[场景描述], B&W film noir boxing classic, deep focus three-plane staging
```

### 《玫瑰纹身》(*The Rose Tattoo*, 1955) 风格 ★ 首座奥斯卡

```
James Wong Howe Rose Tattoo Oscar-winning style, shot on Mitchell BNC 1.85:1,
Sicilian-American passionate B&W, harsh Mediterranean sunlight in modest interiors,
single source bare bulb portrait of Anna Magnani-style woman,
low angle dramatic close-ups, religious icon practical light accents,
silver-gray tonal mastery, 1955 Tennessee Williams Southern heat,
[场景描述], explosive emotional B&W with mature low-key
```

### 《大公无私》(*Sweet Smell of Success*, 1957) 风格

```
James Wong Howe Sweet Smell of Success legendary style, shot on Mitchell BNC + hidden Eyemo,
rain-slicked Manhattan 3am, neon reflections doubling on wet pavement,
hidden camera Times Square documentary realism,
low angle skyscraper canyon shots, deep shadows in 21 Club booths,
Burt Lancaster-style cold portrait single source key, Tony Curtis-style desperate close-up,
manhole steam rising, 1957 NYC noir B&W silver-gray pinnacle,
[场景描述], hidden cardboard box camera real street life
```

### 《飞瀑怒潮》(*Picnic*, 1955) 风格

```
James Wong Howe Picnic style, shot on Mitchell BNC + CinemaScope + crab dolly,
1955 Kansas summer night Technicolor, Chinese lantern warm dance lighting,
purple moonlit river romance, crab dolly rotating tracking around dancers,
William Holden Kim Novak picnic dance, period romantic atmosphere,
[场景描述], CinemaScope 2.39:1 widescreen color period
```

### 《原野铁汉》(*Hud*, 1963) 风格 ★ 二度奥斯卡

```
James Wong Howe Hud second Oscar-winning style, shot on Mitchell BNC + Panavision 1.85:1,
1963 Texas Panhandle drought B&W, harsh blinding plains sunlight,
single bare bulb ranch interior, low angle Paul Newman anti-hero "Low Howe" portrait,
dust and sweat textures in silver-gray, modern Western moral grit,
Patricia Neal weary woman portrait, [场景描述],
B&W when color was mainstream — pure aesthetic conviction
```

### 《Seconds》(1966) 风格

```
James Wong Howe Seconds experimental style, shot on Mitchell BNC + 9.8mm Kinoptik,
extreme wide angle subjective POV, fisheye distortion psychological horror,
head-mounted camera disorienting paranoid movement,
harsh high-contrast B&W, surgical operating room nightmare,
1966 Frankenheimer identity anxiety, [场景描述],
existential dread visualized through optical distortion
```

### 《光辉时刻》(*The Molly Maguires*, 1970) 风格

```
James Wong Howe Molly Maguires style, shot on Mitchell BNC + Panavision color,
1970 Pennsylvania coal miners gray history, kerosene lamp dim cottage interiors,
mine shaft pitch darkness with single helmet headlamp,
rainy mining town desaturated blue-green palette,
color shot like B&W — almost monochrome restraint,
Sean Connery weathered union leader portrait, [场景描述]
```

### 《Funny Lady》(1975) 风格 ★ 第十次奥斯卡提名 / 最后作品

```
James Wong Howe Funny Lady final swan song style,
1975 backstage musical 1930s nostalgia, warm amber nightclub stage lighting,
Barbra Streisand glamour close-up, sepia-toned period color,
soft glamour diffusion, classical Hollywood farewell aesthetic,
[场景描述], James Wong Howe's tenth and final Oscar-nominated work
```

---

## 四、打光方案模板

### 方案 A：单裸灯泡（Wong Howe 招牌）

```
LIGHTING SETUP — Wong Howe Single Bare Bulb:

• KEY: Single naked bulb hanging overhead (visible in frame), tungsten 2700K, hard direct light
• FILL: NONE (or minimal bounce — ratio 8:1 to 16:1)
• PRACTICAL: The bulb itself IS the practical
• AMBIENT: Extreme low — darkness surrounds pool of light
• SHADOW: Deep with retained detail (silver-gray, NOT crushed black)
• COLOR TEMP: Warm tungsten (2700K) on B&W → silver-gray rendering
• MOOD: Lonely, threatening, fate approaching
• REFERENCE: Body and Soul locker room / Hud kitchen / Sweet Smell back office
```

### 方案 B：拳击场顶光 + 滑冰手持

```
LIGHTING SETUP — Wong Howe Boxing Ring:

• KEY: 4-6 harsh overhead spots above ring (theatrical lighting)
• FILL: NONE inside ring; crowd in shadow
• PRACTICAL: Ring corner lights, matchbook flashes
• AMBIENT: Dark crowd, only ring is illuminated
• SHADOW: Deep on crowd faces, sweat-glistening on fighters
• CAMERA: Roller skate mounted Eyemo handheld INSIDE ring,
          assistant pushing camera operator on skates,
          OR ringside crab dolly low angle
• MOOD: Brutal, immersive, ringside POV
• REFERENCE: Body and Soul (1947) — the original
```

### 方案 C：film noir 雨夜街景

```
LIGHTING SETUP — Wong Howe Wet Street Noir:

• KEY: Practical street lamps (sodium tungsten warm) + neon signs
• FILL: Reflections from wet pavement (lamps doubled)
• PRACTICAL: Storefront windows, neon, manhole steam
• AMBIENT: Dark wet streets, low ambient
• EFFECTS: Rain machine + steam machine on manholes
• SHADOW: Deep with luminous wet reflections
• CAMERA: Hidden in cardboard box for real-pedestrian shots, OR low angle Mitchell BNC
• COLOR TEMP: Mixed — neon (5000-9000K) + tungsten lamps (2700K), B&W neutralizes
• MOOD: Urban loneliness, moral decay, hidden glamour
• REFERENCE: Sweet Smell of Success (1957)
```

### 方案 D：低角度西部荒野

```
LIGHTING SETUP — Wong Howe "Low Howe" Western:

• KEY: Natural high-noon overhead sunlight (5600K daylight)
• FILL: Earth and dust bounce — minimal natural fill
• PRACTICAL: None outdoor; bare bulbs in interiors
• AMBIENT: Sky as overexposed white "ceiling"
• CAMERA: Ground-level Mitchell BNC, lens 25-35mm wide angle
          OR camera in dug pit for extreme low angle
• SHADOW: Hard directional shadows under hat brims
• COLOR: B&W silver-gray (Hud), or desaturated earth color (Hombre)
• MOOD: Hero/anti-hero majesty, oppressive sky
• REFERENCE: Hud (1963), The Westerner (1940)
```

### 方案 E：Technicolor 油画饱和

```
LIGHTING SETUP — Wong Howe Technicolor (1941-1955):

• KEY: 5K-10K arc lights for Technicolor density (heavy lights required by 3-strip)
• FILL: Bounce and floods — Technicolor needs lots of light
• PRACTICAL: Period candles, lanterns, gas lamps
• AMBIENT: Bright enough for f/8 minimum
• COLOR DESIGN: Velazquez/Goya inspired — saturated reds, deep golds, pure blacks
• CAMERA: Technicolor 3-strip camera (1941) or Eastmancolor (later)
• SHADOW: Less than B&W — Technicolor needs exposure, but still dramatic
• MOOD: Operatic, painterly, mythic
• REFERENCE: Blood and Sand (1941)
```

### 方案 F：深焦多平面调度

```
LIGHTING SETUP — Wong Howe Deep Focus:

• KEY: 5K-10K arc to enable f/8-f/16 small aperture
• FILL: Multiple lower-intensity sources to lift mid-grounds
• PRACTICAL: Multiple practicals at different depths (lamp foreground / sconce middle / window background)
• AMBIENT: Higher than low-key normal — but still chiaroscuro
• LENS: 25mm-35mm wide angle for depth
• CAMERA: Locked Mitchell BNC for stability
• SHADOW: Selective — each plane has its own light logic
• MOOD: Theatrical multi-action, complex blocking
• REFERENCE: Transatlantic (1931), The Power and the Glory (1933)
```

---

## 五、负面提示词（Negative Prompts）

以下元素与黄宗霑风格矛盾，应在 SD/FLUX 的负面提示词中排除：

```
NEGATIVE (anti-Wong Howe):
soft beauty fill light, even lighting, flat lighting, high-key bright lighting,
HDR, modern digital look, sharp digital edges, oversaturated colors,
lens flare from anamorphic, fisheye distortion (except Seconds),
chromatic aberration, film grain overlay (real grain only),
shaky modern handheld, drone aerial extreme angle, GoPro wide,
teal and orange color grading, Instagram filter, beauty diffusion,
RGB gaming neon outline, multiple colored rim lights,
crushed pure black shadow detail loss, blown white highlight,
soft glamour overall (only on female stars selectively)
```

---

## 六、画幅比例推荐

| 比例 | 用途 | Wong Howe 实例 |
|------|------|---------------|
| **1.37:1** 学院 | 1930s-1953 黑白经典 | 《艾尔及利亚》《光荣》《血与沙》 |
| **1.85:1** 平宽 | 1953 后 B&W / 现代 | 《玫瑰纹身》《原野铁汉》 |
| **2.39:1** CinemaScope | 1955 后宽银幕 | 《飞瀑怒潮》《大公无私》 |
| **2.20:1** Todd-AO | 70mm 史诗 | 《伊甸园之子》风格 |

**Midjourney 适配**：
- `--ar 137:100` → 1.37:1 学院（推荐用于经典 1930s-40s 黑白）
- `--ar 37:20` → 1.85:1 平宽（推荐用于 1955+ 黑白 / 现代）
- `--ar 239:100` 或 `--ar 12:5` → 2.39:1 CinemaScope（推荐用于宽银幕史诗）

---

## 七、组合推荐速查

| 场景 | 推荐影片参照 | 关键技法 | 主光 |
|------|------------|---------|------|
| 单裸灯泡室内 | 《光荣》更衣室 / 《Hud》农舍 | 低调 + 单光源 | 顶光裸灯泡 |
| 拳击场长镜头 | 《光荣》(1947) | 滑冰手持 + 顶光 | 4-6 顶光 |
| 雨夜湿街 | 《大公无私》(1957) | 实景隐藏机 + 反射 | 街灯 + 霓虹 |
| 城市仰拍 | 《大公无私》《艾比林镇》 | "Low Howe" 仰角 | 自然天光 |
| 西部荒野 | 《Hud》《Hombre》《血与沙》 | 低角度 + 强日光 | 高位日光 |
| Casbah/迷宫 | 《艾尔及利亚》(1938) | 多层框架 + 油灯 | 油灯实景 |
| Technicolor 史诗 | 《血与沙》《飞瀑怒潮》 | 油画色彩 + 强光 | 5K 弧光 |
| 深焦多平面 | 《Transatlantic》《光荣》 | 小光圈 + 强光 | 多源 5K-10K |
| 极广角噩梦 | 《Seconds》(1966) | 9.8mm 主观 | 高对比硬光 |
| 煤矿/封闭空间 | 《光辉时刻》(1970) | 单头灯 + 黑暗 | 矿工头灯 |
| 怀旧歌舞 | 《Funny Lady》(1975) | 暖色 + 柔光 | 舞台彩光 |
| 单星特写 | 《玫瑰纹身》Magnani / 《Hud》Newman | 单源雕刻 | 75mm + 硬光 |
| 战后废墟实景 | 《柏林快车》(1948) | 实景纪实 + 蒸汽 | 自然 + 蒸汽 |
| 法庭/审讯 | 《青春之歌》《艾尔及利亚》 | 顶光逼问 | 顶光硬灯 |

---

## 八、模型适配速查

### Midjourney
```
[场景] in the style of James Wong Howe cinematography, 1957 black and white film noir,
low-key lighting, single bare bulb, Mitchell BNC, deep shadows,
Sweet Smell of Success aesthetic --raw --ar 37:20
```

### Stable Diffusion / FLUX
```
PROMPT: James Wong Howe black and white cinematography, low-key lighting,
single hard key light, deep shadows 60% of frame, silver-gray tonal range,
Mitchell BNC 1950s film, low angle "Low Howe", chiaroscuro, [场景]

NEGATIVE: color, soft fill, even lighting, HDR, lens flare, modern digital,
oversaturation, fisheye, crushed blacks, blown highlights, beauty diffusion
```

### DALL-E / GPT Image
```
A scene shot by James Wong Howe in 1957, single bare bulb hanging from ceiling
above a wooden table, deep shadows everywhere except the man's sweating face,
silver-gray black and white film noir, low angle from waist height,
classic Hollywood Golden Age cinematography
```

### Nano Banana Pro / ZenStudio
```
James Wong Howe 黄宗霑风格, 1955 black and white, low-key lighting 低调打光,
single hard key 单光源, deep shadows 大面积阴影, low angle "Low Howe",
chiaroscuro silver-gray, Mitchell BNC, film noir aesthetic, [场景]
```

---

## 九、术语速查（中英对照）

| 中文 | English |
|------|---------|
| 低调打光 | Low-key lighting |
| 单光源 | Single key / single source |
| 深焦摄影 | Deep focus |
| 低角度仰拍 | Low angle shot ("Low Howe") |
| 蟹型移动车 | Crab dolly |
| 滑冰手持 | Roller skate handheld |
| 银灰色调 | Silver-gray tonal range |
| 黑色不死 | Living shadows / shadow detail |
| 顶光眼窝 | Top-light eye-socket shadow |
| 半面阴影 | Half-lit face |
| 雨中湿街 | Rain-slicked wet street |
| 蒸汽井盖 | Manhole steam |
| 隐藏摄影机 | Hidden camera |
| 实景拍摄 | Location shooting |
| 拳击场顶光 | Boxing ring overhead light |
| 三色 Technicolor | Three-strip Technicolor |
| 油画式饱和 | Oil-painting saturation |
| Mitchell BNC 摄影机 | Mitchell BNC camera |
| 改装 Eyemo 手持 | Modified handheld Eyemo |
| 9.8mm 极广角 | 9.8mm extreme wide angle |
| 学院画幅 | Academy ratio (1.37:1) |
| 平宽画幅 | Flat widescreen (1.85:1) |
| 宽银幕 | CinemaScope (2.39:1) |

---

**最后提示**：

黄宗霑（James Wong Howe）的核心永远是 — **"不照亮一切，让阴影承担叙事重量"**。
当你写提示词时，先想 *什么不被照亮*，再想 *单一光源在哪里*，最后才想其余画面。
这是从 1899 年广东台山到好莱坞奥斯卡领奖台的视觉哲学。

> "Light tells the story. The shadow tells the truth."
> — James Wong Howe (attributed)
