> 参考使用：模板按当前任务调整；历史署名、器材和引语需查证。旧版本模型参数仅为示例，最终输出以 SKILL.md 的兼容规则为准。

# Vittorio Storaro 风格 AI 提示词库

按场景类型、情绪和影片参照分类的完整提示词模板，可直接用于 AI 图像 / 视频生成（Midjourney、Stable Diffusion、FLUX、DALL-E、Nano Banana Pro、ZenStudio、Sora、Kling、Runway 等）。

---

## 提示词架构

一个完整的斯托拉罗风格提示词由 7 层构成：

```
[摄影师签名] + [设备/画幅] + [色彩心理学] + [打光方案] + [雕塑感/染印质感] + [构图描述] + [文化/场景元素]
```

### 基础签名层（所有提示词的前缀）

完整版：
```
Vittorio Storaro cinematography, shot on Sony VENICE with ARRI Master Prime,
Univisium 2:1 aspect ratio, motivated dramatic lighting,
sculptural Caravaggio chiaroscuro, Technicolor saturation,
intentional color psychology, painterly cinematic composition
```

简化版：
```
Vittorio Storaro style, Univisium 2:1, Technicolor saturation,
sculptural lighting, color psychology, painterly cinematic
```

---

## 一、按场景类型分类

### 🏛️ 宫廷史诗 — 紫禁城式仪式

**参照**：《末代皇帝》登基场景、《1900》宫殿宴会

**Style：**
```
Vittorio Storaro Last Emperor cinematography, Bertolucci epic style,
Technovision 65mm widescreen, Technicolor three-strip saturation,
imperial color palette of vermilion red and golden yellow,
warm sunlight shafts piercing through ancient palace eaves,
red lantern arrays as architectural practical lights,
Caravaggio sculptural light on faces, painterly historical reverence
```

**Scene：**
```
[场景描述：例如 a young emperor sitting on golden dragon throne],
central symmetric composition along palace axis,
deep architectural perspective with vanishing point through hall,
courtiers in formation flanking the throne,
massive red lacquer pillars framing the frame,
golden curtains parted by wind, atmospheric incense smoke,
ritualistic ceremonial moment, --ar 239:100
```

---

### 🌹 室内 — 巴黎冬日窗光（亲密戏）

**参照**：《巴黎最后的探戈》Brando 公寓、《同流者》室内对话

**Style：**
```
Vittorio Storaro Last Tango in Paris style, Bertolucci 1970s intimacy,
Arriflex 35mm filmic grain, Bacon-inspired flesh tone palette,
warm orange-amber Parisian winter sunlight flooding empty apartment through tall windows,
single practical chandelier providing accent glow,
sculptural body lighting with Caravaggio chiaroscuro,
cold blue-grey shadow zones contrasting warm flesh tones,
painterly orange and cyan duality
```

**Scene：**
```
[场景描述：例如 two figures embracing in empty apartment],
wide tall window flooding golden winter light,
empty parquet floor reflecting the light,
sparse furniture in foreground silhouette,
character half-lit by window, half in cool blue shadow,
intimate emotional distance, painterly composition
```

---

### 🔥 革命与战争 — 红色狂热

**参照**：《赤色分子》莫斯科演讲、《现代启示录》直升机黎明袭击、《1900》农民起义

**Style：**
```
Vittorio Storaro Reds revolutionary cinematography, Warren Beatty epic,
Arriflex 65mm scope, communist red banner saturation,
sea of red flags flooding the frame, warm firelight from torches and revolution fires,
cold winter blue sky as ideological backdrop,
hot-cold temperature dichotomy, ideology versus humanity,
painterly historical realism, Technicolor revolutionary palette
```

**Scene：**
```
[场景描述：例如 orator speaking from balcony to red-flag crowd below],
central symmetric composition with single elevated speaker,
vast crowd of figures with red banners filling lower frame,
warm torchlight from below illuminating speaker,
cold blue twilight sky filling upper frame,
falling snow or smoke catching the light,
historical revolutionary moment ritualized, --ar 239:100
```

**变体 — 丛林战争（《现代启示录》）：**
```
Apocalypse Now Storaro style, Vietnam jungle emerald green
with napalm orange explosions and violet smoke,
mythic war cinematography, helicopter silhouettes against dawn orange sky,
painted soldier face rising from black river water,
65mm Technovision, ritualistic descent into darkness,
Caravaggio half-lit Kurtz face emerging from total black, --ar 239:100
```

---

### 🌃 都市霓虹 — 摩天轮式色彩流动

**参照**：《摩天轮》康尼岛、《One from the Heart》拉斯维加斯、《纽约的一个雨天》

**Style：**
```
Vittorio Storaro Wonder Wheel style, Woody Allen collaboration,
Sony VENICE digital Technicolor, 1950s Coney Island heightened theatrical color,
neon practical lights as architectural elements,
color flow lighting — face transitioning from warm amber to cold blue to magenta in single frame,
ferris wheel pulsating colored neon spilling through window,
painterly digital nostalgia, Univisium 2:1
```

**Scene：**
```
[场景描述：例如 woman seated by apartment window facing ocean boardwalk],
single tall window dominating composition,
ferris wheel visible through window pulsing red blue green neon,
character face washed by changing colored light,
warm interior practicals on small side table,
empty boardwalk seen below, melancholic atmosphere, --ar 2:1
```

**变体 — 拉斯维加斯霓虹歌舞**：
```
One from the Heart Storaro Coppola, theatrical neon Las Vegas studio set,
magenta and electric blue neon overload,
dancers bathed in colored light shafts,
artificial painterly sunset backdrop,
musical theater chromatic immersion, full saturation
```

**变体 — 纽约雨夜**：
```
A Rainy Day in New York Storaro, Manhattan emerald Central Park,
jazz bar amber-brown nostalgia, cobalt rain night,
neon reflections in wet streets, romantic embrace under bridge,
golden downpour back-lit by street lamps, Univisium 2:1
```

---

### 💃 舞蹈与表演 — 探戈式圆周

**参照**：《探戈》(Saura)、《意乱情迷》

**Style：**
```
Vittorio Storaro Tango Saura style, Argentine flag blue-white plus tango red,
trichromatic theatrical staging, Univisium 2:1 aspect ratio,
circular stage with overhead colored spotlights pulsing,
dancers as silhouettes against backlit floor,
volumetric stage smoke catching beams,
painterly dance cinema, sculptural body chiaroscuro
```

**Scene：**
```
[场景描述：例如 tango couple mid-step on circular illuminated stage],
overhead camera circling with the dancers,
red and blue spotlights alternating across the floor,
dancers as bold silhouettes, light bleeding around their edges,
theatrical empty void around stage,
ritualistic dance moment, --ar 2:1
```

---

### 🌅 室外 — 黄金时段（地中海风）

**参照**：《一九〇〇》麦田、《蜘蛛的策略》葡萄园、《咖啡公社》好莱坞泳池

**Style：**
```
Vittorio Storaro golden hour Mediterranean style,
Bertolucci pastoral cinematography or Allen Hollywood nostalgia,
Sony F65 digital Technicolor, ripe wheat-gold and grape-violet palette,
warm low-angle Italian sun creating long sculptural shadows,
backlit silhouettes walking through field,
painterly nostalgic light, Univisium 2:1
```

**Scene：**
```
[场景描述：例如 figure walking through golden wheat field at dusk],
wide horizon line dividing frame at lower third,
violet-pink sky transitioning to amber horizon,
single backlit silhouette in golden grain,
heat haze and atmospheric particles,
cinematic land-and-sky composition, --ar 2:1
```

**变体 — 1930s 好莱坞泳池**：
```
Cafe Society Storaro Allen, 1930s Hollywood pool party golden hour,
amber sunset bathing crowd of well-dressed extras,
single starlet in pastel dress catching golden rim-light,
art deco poolside architecture, Sony F65 painterly digital,
nostalgic warm-cool sunset duality
```

---

### 🌆 西班牙画家光 — 戈雅与卡拉瓦乔

**参照**：《魔法时刻》、《卡拉瓦乔》、《Tango》画室段落

**Style：**
```
Vittorio Storaro painterly portrait cinematography, Goya-Caravaggio homage,
single candle or single window as motivated source,
Rembrandt golden chiaroscuro, deep velvet black with chromatic shadows,
Spanish romantic palette of brown-black and crimson,
oil painting tonal transitions, sculptural facial topography,
painter at work in dim studio, Sony VENICE digital filmic
```

**Scene：**
```
[场景描述：例如 elderly painter at canvas illuminated by single candle],
candle on table providing only light source in dark studio,
half of face in golden light, other half sinking into black,
canvas catching minimal reflected glow,
deep shadow filling 70% of frame,
art historical biographical moment, --ar 2:1
```

---

### ❄️ 冷酷机构与监狱

**参照**：《末代皇帝》监狱段落、《同流者》法西斯办公室

**Style：**
```
Vittorio Storaro institutional cold style, Bertolucci historical Italy,
fascist or communist regime architecture, cold cyan-blue dominant,
overhead institutional fluorescent or barred-window light,
geometric venetian blind shadow patterns,
single warm accent (red flag, amber lamp) cutting through cold,
sterile architectural symmetry, deep perspective corridor,
ideological color-temperature dichotomy
```

**Scene：**
```
[场景描述：例如 prisoner sitting at small desk in cell],
high barred window casting blue-grey diagonal light,
character in plain blue uniform reading,
cold concrete walls with chromatic violet shadow,
single small warm-toned book or photo as accent,
deep institutional architectural perspective, --ar 239:100
```

---

### 🗿 宗教与精神觉醒

**参照**：《小活佛》成道场景、《现代启示录》库尔兹仪式

**Style：**
```
Vittorio Storaro spiritual awakening cinematography,
Bertolucci Buddha enlightenment style or Apocalypse Now ritual,
mythic golden halo light from above sculpting figure,
saturated Indian crimson and gold or jungle violet smoke,
volumetric god-rays through dust and incense,
painterly sacred art reference (Renaissance halo painting),
ritualistic centered composition
```

**Scene：**
```
[场景描述：例如 meditating figure under bodhi tree at dawn],
overhead golden god-ray descending onto crown of head,
cross-legged figure in centered symmetric composition,
ancient tree silhouette behind, painterly violet sky,
volumetric incense smoke catching light,
sacred ritualistic moment, --ar 2:1
```

---

### 🎨 漫画印刷 — 三原色实验

**参照**：《迪克·崔西》

**Style：**
```
Dick Tracy Storaro style, comic book primary colors only,
strict palette of pure red yellow blue green violet orange black,
no in-between hues, theatrical flat saturated lighting,
painted matte backdrop NYC, three-strip Technicolor saturation,
1930s graphic novel pulp aesthetic,
character in pure single-color costume
```

**Scene：**
```
[场景描述：例如 detective in pure yellow trench coat at street corner],
character flat-lit against painted city backdrop,
red brick wall, blue mailbox, green streetlamp,
no naturalistic shading, comic panel composition,
exaggerated chiaroscuro on villain face in violet shadow, --ar 239:100
```

---

### 🌙 表现主义夜境

**参照**：《卡里加里博士》致敬作

**Style：**
```
Vittorio Storaro German Expressionist tribute, Caligari homage,
violet cadmium yellow blood red expressionist palette,
geometric tilted shadow patterns painted onto walls,
single dramatic theatrical key light,
silent cinema painterly artificiality,
distorted dream perspective, theatrical chromatic hysteria
```

**Scene：**
```
[场景描述：例如 sleepwalker rising from coffin-like cabinet],
tilted Dutch angle composition,
hard violet shadow cutting diagonally across walls,
character lit by single yellow theatrical spotlight,
painted geometric set background,
silent horror dream sequence, --ar 2:1
```

---

### 🌬️ 沙漠与大地

**参照**：《遮蔽的天空》《现代启示录》河流段落

**Style：**
```
Vittorio Storaro Sheltering Sky desert cinematography,
Bertolucci spiritual desolation, scorching overhead Saharan sun,
Bedouin indigo robes against burnt gold dunes,
heat haze shimmering, fever-violet inside tents,
hot orange exterior versus cold violet interior,
painterly North African chromatic poetry
```

**Scene：**
```
[场景描述：例如 lone traveler crossing endless dune at noon],
single small figure dwarfed by golden dune ridge,
deep violet sky burning into white-hot horizon,
sand particles airborne, mirage shimmer,
spiritual loneliness composition, --ar 239:100
```

---

### 💔 心理特写 — 色彩漫过面孔

**参照**：《摩天轮》Kate Winslet 窗边、《巴黎最后的探戈》Schneider 特写

**Style：**
```
Vittorio Storaro psychological close-up, Wonder Wheel color flow technique,
Sony VENICE digital Technicolor, single face filling frame,
color flowing across face — amber to blue to magenta gradient,
sculptural Caravaggio half-lit cheekbone,
single window or single neon as motivated source,
emotionally heightened theatrical color
```

**Scene：**
```
[场景描述：例如 woman by apartment window crying silent tears],
extreme close-up of face, half lit by changing colored light,
slow color temperature drift across skin,
subtle movement of practical light source outside,
emotional rawness amplified by chromatic transformation,
psychological color flow moment, --ar 2:1
```

---

### 🌊 水边与诗意

**参照**：《现代启示录》河流、《纽约的一个雨天》中央公园桥下

**Style：**
```
Vittorio Storaro water poetic cinematography,
mythic river or rainy bridge scene, painterly reflective surfaces,
volumetric atmospheric layers, twilight color gradient on water,
Caravaggio sculptural figure emerging from black water,
Sony VENICE digital Technicolor depth
```

**Scene：**
```
[场景描述：例如 lovers embracing under stone bridge during rainstorm],
warm amber lantern light from above bridge,
cold blue rain falling all around, golden droplets backlit,
characters embracing in protected pocket of warm light,
romantic mythic moment, --ar 2:1
```

---

## 二、按情绪分类

### 🔴 激情 / 革命 / 母体

```
deep saturated red dominant tone, communist banner red, blood red, womb red,
warm firelight torches, ideological intensity, painterly Soviet realism,
Reds Bertolucci 1900 reference
```

### 🟠 家庭 / 温暖 / 安全

```
warm amber-orange interior glow, single golden practical lamp,
nostalgic family hearth, Cafe Society pool party amber,
Last Tango bedroom warmth, painterly intimate domesticity
```

### 🟡 知识 / 皇权 / 太阳

```
imperial Forbidden City yellow, golden palace sunshafts,
Tibetan monastery saffron robes, awakening enlightenment gold halo,
Last Emperor coronation reference
```

### 🟢 知性 / 自然 / 丛林

```
emerald jungle green, Vietnam Apocalypse Now palette,
Manhattan Central Park summer green,
intellectual maturity tone, painterly verdant atmosphere
```

### 🔵 智慧 / 反思 / 监狱

```
cold communist prison blue, Last Emperor prison segment,
melancholy Manhattan night cobalt, intellectual clarity,
sterile institutional cyan, ideological coldness
```

### 🟣 灵性 / 矛盾 / 超越

```
violet twilight, indigo dream, Wonder Wheel magenta heightened emotion,
Caligari expressionist purple, spiritual transcendence color,
end-of-life wisdom tone
```

### ⚪ 觉醒 / 起点 / 终结

```
clean white awakening, Last Emperor final tourist scenes,
empty whitewashed interiors, post-revolution stillness,
clarity after chromatic journey
```

---

## 三、按代表作分类（一句话签名提示词）

### 《同流者》(The Conformist)
```
Conformist Storaro, fascist Italy art deco, electric blue and bone white,
deep corridor perspective, character pressed to edge of frame,
Bertolucci 1970 anamorphic widescreen
```

### 《巴黎最后的探戈》(Last Tango in Paris)
```
Last Tango Storaro, Bacon flesh tones, golden Parisian winter window light,
empty apartment intimacy, orange-amber vs cold blue duality, Arriflex 35mm grain
```

### 《一九〇〇》(1900)
```
Novecento 1900 Storaro Bertolucci, Emilia-Romagna wheat gold and grape violet,
communist red banner, peasants in formation, agricultural epic
```

### 《现代启示录》(Apocalypse Now)
```
Apocalypse Now Storaro Coppola, Vietnam jungle emerald with napalm orange,
violet smoke, mythic war chiaroscuro, Caravaggio half-lit Kurtz face,
helicopter dawn raid, 65mm
```

### 《赤色分子》(Reds)
```
Reds Storaro Beatty, Russian Revolution color symphony,
sea of red banners, Saint Petersburg winter blue with amber firelight,
central symmetric speech composition
```

### 《末代皇帝》(The Last Emperor)
```
Last Emperor Storaro Bertolucci, Forbidden City imperial yellow and vermilion,
red lantern labyrinth, communist prison blue, color spectrum life journey,
Technovision 65mm 2.39:1
```

### 《迪克·崔西》(Dick Tracy)
```
Dick Tracy Storaro Beatty, comic primary colors only, pure yellow trench coat,
painted NYC matte backdrop, three-strip Technicolor, theatrical flat lighting
```

### 《探戈》(Tango / Saura)
```
Tango Saura Storaro, Argentine blue-white plus red, circular stage,
pulsating red and blue spotlights, dancers silhouettes, Univisium 2:1 debut
```

### 《咖啡公社》(Cafe Society)
```
Cafe Society Allen Storaro, 1930s Hollywood pool party golden hour,
Manhattan jazz amber-brown, Sony F65 digital Technicolor, Univisium 2:1
```

### 《摩天轮》(Wonder Wheel)
```
Wonder Wheel Storaro Allen, 1950s Coney Island neon practicals,
color flow face transitioning amber to blue to magenta, ferris wheel pulse
```

### 《纽约的一个雨天》(A Rainy Day in New York)
```
Rainy Day Storaro Allen, Manhattan emerald Central Park,
jazz amber, cobalt rain night, neon reflections, romantic bridge embrace
```

---

## 四、Negative Prompts（推荐负面提示词）

适用于 Stable Diffusion / FLUX：

```
flat lighting, even fill light, modern Netflix flat grade, washed out colors,
grey monotone, dead black shadows, plastic digital sharpness, HDR oversharpening,
muddy desaturation, Instagram filter look, single-color monotone,
amateur snapshot, harsh on-camera flash, lens flare (unless motivated),
ugly compression artifacts, soulless corporate aesthetic,
flat documentary lighting, Roger Deakins minimalism (与 Storaro 风格冲突)
```

---

## 五、组合模板示例

### 模板 A：东方仪式 + 色彩象征

```
Vittorio Storaro Last Emperor cinematography, Bertolucci epic style,
Technovision 65mm widescreen, Technicolor three-strip saturation,
imperial vermilion red and golden yellow palette,
warm sun shafts piercing palace eaves, red lantern arrays as practicals,
sculptural Caravaggio chiaroscuro on emperor's face,
[young child emperor sitting on golden dragon throne in vast hall],
central symmetric composition, deep architectural perspective,
courtiers flanking the throne, massive red lacquer pillars,
golden silk curtains, atmospheric incense smoke, --ar 239:100
```

### 模板 B：现代心理 + 色彩流动

```
Vittorio Storaro Wonder Wheel style, Woody Allen collaboration,
Sony VENICE digital Technicolor, 1950s Coney Island theatrical color,
neon practicals as architecture, color flow technique —
face transitioning from warm amber to cold blue to magenta,
ferris wheel pulsing colored neon through window,
[middle-aged woman seated by window facing ocean boardwalk, silent tears],
single tall window dominating composition,
warm interior practical on small table, melancholic atmosphere,
Univisium 2:1, painterly digital nostalgia, --ar 2:1
```

### 模板 C：丛林神话 + 雕塑光

```
Vittorio Storaro Apocalypse Now style, Coppola mythic war,
65mm Technovision, Vietnam jungle emerald with napalm orange,
violet atmospheric smoke, Caravaggio half-lit face emerging from total darkness,
[shaved head colonel half-lit by single bare bulb, half sinking into black],
extreme contrast chiaroscuro portrait,
volumetric incense smoke, jungle ambient sounds implied,
ritualistic descent into darkness composition, --ar 239:100
```

### 模板 D：欧洲油画 + 烛光肖像

```
Vittorio Storaro Caravaggio biopic style, single candle motivated source,
Sony VENICE digital filmic grain, Rembrandt-Caravaggio gold and crimson,
deep velvet black with chromatic violet shadows,
[old painter at easel illuminated by single candle in dark studio],
70% of frame in deep darkness, candle as compositional anchor,
canvas catching minimal reflected glow, painterly biographical portrait,
Spanish romantic chiaroscuro, --ar 2:1
```

---

## 六、模型适配速查

### Midjourney 8.2
- 后缀建议：`--raw --ar 2:1 --s 250`
- 强 trigger：`Vittorio Storaro, Technicolor, Caravaggio chiaroscuro, painterly cinematic`
- 注意：避免过多 negative，Midjourney 用文字主导

### Stable Diffusion XL / FLUX
- 推荐 LoRA：Technicolor / Renaissance Painting / Cinematic Lighting
- CFG：7–9 / Steps：30–50
- 强调正面：`Vittorio Storaro cinematography, motivated dramatic lighting, color psychology`

### DALL-E 3 / GPT Image
- 用自然语言描述："imagine a scene in the style of Vittorio Storaro, where deep red represents revolution and warm amber represents intimacy, painted by light"
- 显式说明每个色彩的象征意义

### Nano Banana Pro / ZenStudio
- 中英混合："斯托拉罗风格, Vittorio Storaro cinematography, 色彩心理学, sculptural lighting, Univisium 2:1"
- 输出 4K 时强调 `Technicolor saturation, fine film grain`

### Sora / Kling / Runway / Veo
- 加入 `slow rotating dolly, color gradient flowing across the face, smoke revealing volumetric light beams, ritualistic camera circling subject`
- 时长建议 5–10s 以保留色彩节奏

---

## 七、常见错误与修正

| 错误 | 原因 | 修正 |
|------|------|------|
| 画面色彩单一灰调 | 缺少冷暖对比 | 加入 `hot-cold temperature contrast` |
| 暗部死黑 | 缺少色相 | 加入 `chromatic shadows holding violet/amber` |
| 太像 Deakins 自然主义 | 过于克制 | 加入 `theatrical heightened color, exaggerated practical light` |
| 色彩过于鲜艳像卡通 | 缺少胶片质感 | 加入 `Technicolor velvet saturation, fine film grain, painterly` |
| 画幅看起来不对 | 比例错 | 显式 `--ar 2:1` (Univisium) 或 `--ar 239:100` |
| 看起来像数字塑料 | 缺少绘画语言 | 加入 `Caravaggio painterly, Renaissance reference, oil painting tonal transitions` |

---

## 八、速查：色彩象征词典

| 中文象征 | 英文提示词 |
|---------|-----------|
| 革命 / 激情 / 母体 | `revolutionary deep red, blood red, womb red, communist banner red` |
| 家庭 / 温暖 | `warm amber-orange domestic glow, hearth warmth` |
| 知识 / 皇权 | `imperial gold yellow, Forbidden City vermilion, sun-king light` |
| 知性 / 自然 | `emerald intellectual green, jungle deep green, summer Central Park` |
| 智慧 / 反思 | `cold institutional blue, prison cyan, melancholy cobalt` |
| 灵性 / 超越 | `violet transcendence, indigo dream, magenta heightened emotion` |
| 觉醒 / 终点 | `clean white awakening, post-journey clarity, empty stillness` |

---

## 九、最简组合（懒人版）

需要快速出图时：

```
Vittorio Storaro cinematography, Technicolor saturation, sculptural Caravaggio
chiaroscuro, motivated dramatic lighting, hot-cold color temperature contrast,
Univisium 2:1, painterly cinematic, [一句话场景描述], --ar 2:1
```

替换 `[一句话场景描述]` 即可。
