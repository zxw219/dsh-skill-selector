> 参考使用：模板按当前任务调整；历史署名、器材和引语需查证。旧版本模型参数仅为示例，最终输出以 SKILL.md 的兼容规则为准。

# Christopher Doyle 杜可风 风格 AI 提示词库

按场景类型、情绪和影片参照分类的完整杜可风风格英文提示词模板，可直接复制到 Midjourney / Stable Diffusion / FLUX / Nano Banana Pro / Kling / Runway 等 AI 工具中使用。

---

## 提示词架构

一个完整的杜可风风格提示词由 6 层构成：

```
[摄影师签名 + 导演宇宙] + [设备/胶片模拟] + [实景光方案] + [湿润色彩] + [广角/畸变构图] + [时间与情绪]
```

### 基础签名层（所有提示词的前缀）

```
Christopher Doyle cinematography, Wong Kar-Wai universe,
shot on Arriflex 35BL with Zeiss Super Speed 14mm lens, Kodak Vision3 push-processed 1-stop,
practical neon and tungsten lights only — no key light, handheld intimate framing,
humid saturated color palette, happy-accident spontaneity
```

简化版：
```
Christopher Doyle style, Wong Kar-Wai palette, handheld 14mm wide-angle,
neon humid Hong Kong, step-printing motion blur, no key light
```

---

## 一、按场景类型分类（核心场景库）

### 🌃 1. 霓虹夜街 — 重庆森林香港便利店

**参照**：《重庆森林》(1994) 金城武在午夜快餐店等女友 / 旺角午夜便利店 / 林青霞金发红雨衣的尖沙咀夜街

**Style（风格）：**
```
Christopher Doyle Chungking Express 1994 aesthetic, 4am Tsim Sha Tsui insomnia,
Hong Kong convenience store fluorescent ceiling tubes mixed with magenta-cyan neon signage,
push-processed Kodak 5293 film grain, humid tropical night air, lens fogged by humidity,
no key light — only practical neon and ceiling fluorescent, handheld breathing camera,
magenta and lime green dichromatic palette, wet reflective terrazzo floor doubling the neon,
cigarette smoke drifting across the frame
```

**Scene（画面）：**
```
A lone man in a trench coat eating pineapple from a can at a chrome convenience store counter,
Chungking Mansions corridor visible through glass door, overhead Chinese shop signage
bleeding magenta light onto his face, 14mm wide-angle shot from hip level distorting space,
blonde-wigged woman in red raincoat and sunglasses passing as out-of-focus silhouette behind glass,
4am emptiness, clocks on the wall frozen at different times
```

**完整提示词：**
```
Christopher Doyle Chungking Express 1994, 4am Hong Kong convenience store, magenta-cyan
neon mixed with fluorescent ceiling tubes, lone man in trench coat eating canned pineapple
at chrome counter, wet terrazzo floor reflecting neon, 14mm wide-angle handheld from hip,
blonde woman in red raincoat passing behind glass as bokeh silhouette, Chungking Mansions
corridor beyond, push-processed Kodak film grain, humid tropical lens fog, cigarette smoke
drift, no key light practical only, Wong Kar-Wai palette, timeless insomniac loneliness
```

💡 打光笔记：天花板日光灯作为硬顶光 + 窗外粉紫霓虹作为侧逆光，不打 fill，让面部阴影真实
🎨 色彩笔记：洋红（Pantone 219）+ 柠檬黄（Pantone 102）+ 凯莉绿（Kelly green）三色主导
🎞️ 技术备注：14mm 广角贴近 40cm 距离，快门 1/8s 拖影路过行人

---

### 🌃 2. 霓虹夜街 — 堕落天使尖沙咀

**参照**：《堕落天使》(1995) 黎明骑摩托狂奔 / 金城武夜半闯入店铺 / 李嘉欣在无人酒吧跳舞

**Style（风格）：**
```
Christopher Doyle Fallen Angels 1995 extreme aesthetic,
sickly acid yellow mixed with cobalt blue and bloody red neon,
Hong Kong underground subway fluorescent bleeding onto oily wet concrete,
9.8mm Zeiss Super Speed fisheye-adjacent ultra-wide, 30cm intimate distance to subject,
Dutch angle 10-15 degrees tilted, handheld drunken sway,
push-processed 2-stop grain storm, lens vignetting in corners,
practical streetlights only — no key light, neon steam and motorcycle exhaust,
Doyle drunken-camera signature
```

**Scene（画面）：**
```
A leather-jacketed young man on a motorcycle racing through Tsim Sha Tsui underpass at 3am,
a woman in black vinyl clinging to his back, ultra-wide 9.8mm lens distorting their faces into
caricature, tunnel ceiling fluorescent tubes streaking into light trails, rain-slick asphalt
mirroring acid-yellow sodium lamps, neon pharmacy sign bleeding cobalt blue on left edge,
blurred speed lines from step-printing, claustrophobic tunnel walls compressing perspective,
figures frozen crisp while world smears into painterly chaos
```

**完整提示词：**
```
Christopher Doyle Fallen Angels 1995, 9.8mm fisheye extreme wide-angle, leather-jacketed
motorcycle rider with black-vinyl woman, 3am Tsim Sha Tsui underpass, acid yellow and
cobalt blue mixed neon, step-printing motion smear, Dutch angle 12 degrees tilted,
ceiling fluorescent tubes streaking into light trails, oily wet asphalt reflection,
handheld drunken sway, push-processed grain storm, claustrophobic tunnel walls,
frozen subject in smeared world, Doyle signature drunken camera
```

💡 打光笔记：只用隧道日光灯 + 街边药房霓虹 + 摩托尾灯作为唯一光源
🎨 色彩笔记：酸黄（sodium 1800K）+ 钴蓝（cyan neon 8500K）+ 血红（pharmacy signage）
🎞️ 技术备注：9.8mm 极致广角 + Dutch angle + step-printing 1/4s 快门叠 3 帧

---

### 🎞️ 3. Step-Printing 印片机叠帧模糊 — 重庆森林金城武食堂

**参照**：《重庆森林》(1994) 警员 223 在 California 快餐店等女友，周围人群化为彩色拖影

**Style（风格）：**
```
Christopher Doyle step-printing impressionist blur signature technique,
each frame exposed three times through optical printer,
frozen central subject tack-sharp while surrounding crowd dissolves into painterly color streaks,
Chungking Express California cafe fluorescent lighting, humid 4am Hong Kong timeless insomnia,
red and yellow and turquoise blurred into Monet-like chromatic rivers,
1/8 second shutter photographed then re-photographed for multi-exposure,
push-processed Kodak 5293 heavy grain, handheld micro-tremor, no key light
```

**Scene（画面）：**
```
A uniformed off-duty police officer sitting motionless at a chrome cafe counter,
holding a can of pineapple frozen in sharpness, while the crowd around him —
office workers, food servers, delivery men — smears into rainbow color trails of motion,
background jukebox and menu board glow yellow and pink, his face crisp in the center
as reality flows around him like an impressionist painting, time stretched and compressed
```

**完整提示词：**
```
Christopher Doyle step-printing signature, Chungking Express 1994 California cafe,
off-duty cop frozen tack-sharp at chrome counter holding pineapple can, surrounding
crowd smeared into impressionist color rivers of red yellow turquoise, fluorescent
cafe lighting, humid 4am insomnia, optical-printer multi-exposure 1/8s shutter,
Monet-like painterly crowd blur, frozen subject in flowing time, push-processed
Kodak grain, no key light, Wong Kar-Wai signature impressionist cinema
```

💡 打光笔记：快餐店天花板荧光 + 菜单板背光即可，不加灯
🎨 色彩笔记：洋红快餐店霓虹 + 柠檬黄菜单 + 人群衣服的随机撞色
🎞️ 技术备注：step-printing 核心关键词，AI 模型可以理解为 "frozen subject crowd motion smear trail"

---

### 🏍️ 4. 慢门拖影追逐 — 堕落天使摩托夜驰

**参照**：《堕落天使》(1995) 黎明骑摩托带李嘉欣穿越九龙隧道 / 杀手追杀长镜头

**Style（风格）：**
```
Christopher Doyle long-exposure drag-shutter cinematography,
1/4 to 1/2 second handheld long exposure creating light-trail chaos,
Kowloon Cross-Harbour Tunnel at 3am, sodium orange streetlights streaking into
ribbons of fire, headlights painting white-red laser rivers,
motorcycle headlamp carving forward tunnel of light, zoom-during-exposure blast,
rear tail light smeared into blood-red wake, ceiling fluorescent tubes ghost-trails,
push-processed 2-stop emulsion, Fallen Angels dark hallucinatory urgency
```

**Scene（画面）：**
```
A motorcycle speeding through a tunnel from the rider's side view, two figures blurred
onto the seat in a frozen-crisp pose while the world around them dissolves into
light ribbons, tunnel tiles becoming streaked abstract lines, oncoming headlights
carving white javelins across the frame, tail lights dragging blood-red tails into
the vanishing point, sparks of orange from distant neon, the image balanced between
stillness and cataclysm
```

**完整提示词：**
```
Christopher Doyle drag-shutter long exposure, Fallen Angels 1995 Kowloon tunnel
motorcycle chase, 1/4 second handheld exposure, sodium orange ceiling fluorescents
streaking into fire ribbons, headlights as white laser rivers, tail lights dragging
blood-red wakes, two figures frozen crisp on motorcycle amid chaos, zoom-during-exposure
radial burst, push-processed grain, 3am hallucinatory urgency, Doyle hand-painted-with-light
signature technique
```

💡 打光笔记：隧道本身的日光灯 + 路过车辆车灯 + 摩托尾灯 = 全部光源
🎨 色彩笔记：sodium orange + 白色 HID 冷光 + 血红尾灯三条光河
🎞️ 技术备注：快门 1/4s ~ 1/2s 手持，中途变焦制造 zoom-burst

---

### 💄 5. 湿润室内 — 花样年华公寓走廊

**参照**：《花样年华》(2000) 苏丽珍在狭窄旅店走廊慢镜头走过 / 墙纸花纹贴脸特写 / 酒红旗袍宝石色

**Style（风格）：**
```
Christopher Doyle In the Mood for Love 2000 signature aesthetic,
1962 Hong Kong tenement tungsten tungsten 3200K warm amber illumination,
single wall sconce practical, floral ochre wallpaper absorbing light into bronze patina,
no key light — only wall sconces and corridor ceiling bulb,
half-lit profile half sunk into tobacco-amber shadow, Black Pro-Mist 1/4 diffusion,
slow-motion 32fps tracking dolly, cigarette smoke drifting like memory,
Cooke S4 35mm spherical lens, Kodak 5245 daylight balanced for rich amber
```

**Scene（画面）：**
```
A woman in a high-collared oxblood silk qipao with embroidered peonies walking slowly
down a narrow tenement corridor, the wall covered in ochre floral wallpaper, single
wall sconce casting warm amber light that catches her cheekbone and lips only,
other half of her face dissolving into brown darkness, thermos flask held at her side,
slow-motion movement, faded photograph stairwell beyond, smoke rising from a forgotten
cigarette on a side table, restrained devastating longing
```

**完整提示词：**
```
Christopher Doyle In the Mood for Love 2000, 1962 Hong Kong tenement corridor,
woman in oxblood silk qipao with peony embroidery walking slow-motion, ochre
floral wallpaper absorbing tungsten 3200K amber, single wall sconce half-lighting
her profile, Black Pro-Mist 1/4 diffusion, Cooke S4 35mm spherical, cigarette smoke
drifting like memory, Maggie Cheung archetype, tobacco-amber shadow on other half,
restrained romantic longing, Wong Kar-Wai memory palette
```

💡 打光笔记：钨丝壁灯 CHROS + 窗外蓝调作为远景冷光对比 + Black Pro-Mist 柔焦丝
🎨 色彩笔记：酒红旗袍 (oxblood Pantone 7421) + 铜锈黄墙纸 + 烟草棕阴影 + 远景冷蓝
🎞️ 技术备注：32fps 过曝 1/3 档，拍出「记忆慢镜」质感

---

### 🛏️ 6. 湿润室内 — 2046 旅馆房间

**参照**：《2046》(2004) 周慕云的 2046 号房 / 王菲透过窗帘看进房间 / 未来列车与旧旅馆叠化

**Style（风格）：**
```
Christopher Doyle 2046 hotel aesthetic dual-world palette,
1960s tungsten amber mixed with science-fiction cobalt neon spill from window,
translucent curtain veiling half the room, cigarette smoke thick enough to refract light,
Black Pro-Mist 1/2 diffusion softening highlights into halos,
Arriflex 35mm Kodak 5218 push-processed, in-camera double exposure for memory layer,
handheld slow drift, no key light only wall sconce and exterior cobalt street glow,
smoky tobacco-amber with cyan bleed-through, time-loop melancholia
```

**Scene（画面）：**
```
A man in white undershirt sitting on the edge of a double bed in a narrow hotel room,
typewriter on the bedside table, rotary phone, half-empty whiskey glass, single wall
sconce casting warm amber on his face, translucent cheap white curtain billowing from
the open window with cobalt blue neon street glow bleeding through, hotel room number
"2046" painted on the door visible in a mirror reflection, cigarette smoke thick in
the air refracting both amber and cobalt, woman's silhouette glimpsed through curtain,
double exposure ghost of future train corridor faint over the scene
```

**完整提示词：**
```
Christopher Doyle 2046 hotel room 2004, man in white undershirt at edge of bed,
typewriter and whiskey glass, 1960s tungsten amber wall sconce + cobalt neon
bleeding through translucent billowing curtain, "2046" room number visible in
mirror, cigarette smoke refracting both colors, Black Pro-Mist 1/2 diffusion,
in-camera double exposure with future train corridor ghost, Arriflex 35mm
Kodak 5218, dual-world time-loop melancholia, Wong Kar-Wai signature
```

💡 打光笔记：室内单壁灯暖橙 + 窗外霓虹蓝冷光双主光，阴影里混色
🎨 色彩笔记：怀旧黄 (amber 2700K) + 病态酸黄 + 科幻钴蓝 (cyan 9000K) 三层时间色
🎞️ 技术备注：机内双曝将未来列车叠加到现实旅馆

---

### 💛 7. 王家卫式怀旧黄 — 花样年华面店

**参照**：《花样年华》(2000) 苏丽珍拎热水瓶买云吞面 / 窗棂阴影下慢镜头

**Style（风格）：**
```
Christopher Doyle Wong Kar-Wai nostalgic amber signature palette,
Hong Kong 1962 back alley noodle stall at dusk, tungsten 2700K street lamps,
steamed-up air from dumpling stall catching warm light,
Kodak 5245 stock push-processed for richer amber density, black Pro-Mist 1/4,
no key light only practical lantern and single stall bulb,
slow-motion 32fps tracking dolly, rain-wet cobblestone alley floor reflecting amber,
smoky tobacco-honey haze, Maggie Cheung slow-motion corridor walk aesthetic
```

**Scene（画面）：**
```
A woman in a pale rose qipao with jade-green trim carrying a thermos flask through
a narrow back alley at dusk, steam rising from a noodle stall on the left, single
amber bulb hanging from a cable, her shadow long on the wet cobblestones, window
grid shadows from a tenement above cutting across her face, slow-motion walk,
nostalgic fading daylight from above mixing with warm stall bulb, 1962 Hong Kong
alley with hand-painted Chinese signage, restrained solitary grace
```

**完整提示词：**
```
Christopher Doyle In the Mood for Love 2000, woman in rose qipao with jade trim
carrying thermos through 1962 Hong Kong noodle stall alley at dusk, tungsten 2700K
single amber bulb above stall, steaming dumpling air catching light, rain-wet
cobblestone reflection, window grid shadow on face, slow-motion 32fps tracking,
Kodak 5245 push-processed amber density, Black Pro-Mist 1/4, hand-painted Chinese
signage, nostalgic tobacco-honey haze, restrained solitary grace, Wong Kar-Wai
memory color
```

💡 打光笔记：摊位裸灯 + 天空残余冷蓝 = 冷暖对比
🎨 色彩笔记：琥珀黄 + 蜂蜜黄 + 旗袍玉绿撞色 + 阴影褐棕
🎞️ 技术备注：32fps slow-motion + Black Pro-Mist 晕柔高光

---

### 🚂 8. 王家卫式怀旧黄 — 2046 列车走廊

**参照**：《2046》(2004) 未来列车上红衣王菲走过窗外星光流动的走廊

**Style（风格）：**
```
Christopher Doyle 2046 futuristic train corridor aesthetic,
hybrid Wong Kar-Wai memory palette with sci-fi neon futurism,
cherry-red LED rope lights running along corridor ceiling and floor,
cobalt blue and amber window lights flashing past at long-exposure speed,
push-processed Kodak 5218, Black Pro-Mist 1/4, handheld drift tracking,
no key light only practical rope LEDs and window pulse,
anamorphic-flavored wide frame at 2.39:1, time-loop melancholia,
motion blur through window exposure
```

**Scene（画面）：**
```
A woman in a form-fitting red cheongsam-inspired futuristic robe walking away from
camera down a narrow train corridor, cherry-red LED rope lights lining the ceiling
and floor creating parallel guide rails, rectangular windows on the left flashing
past with cobalt blue and amber pulse, star-field long-exposure streaks visible
beyond, her silhouette in crimson against the flashing world outside, distant
figure of a man watching from end of corridor, time dissolving into speed
```

**完整提示词：**
```
Christopher Doyle 2046 train corridor 2004, woman in red futuristic cheongsam walking
away down narrow corridor, cherry-red LED rope lights along ceiling and floor,
cobalt-blue and amber windows flashing past at long-exposure speed, star-field streaks
beyond, distant male silhouette at corridor end, Black Pro-Mist 1/4, 2.39:1 anamorphic
flavor, handheld drift, Kodak 5218 push-processed, Wong Kar-Wai sci-fi memory-loop
melancholia
```

💡 打光笔记：顶部地面 LED 红绳 + 窗外高速闪光脉冲即全部光源
🎨 色彩笔记：樱桃红 + 钴蓝 + 琥珀黄三色脉冲构成赛博怀旧
🎞️ 技术备注：2.39:1 画幅，窗外长曝光星光拖尾

---

### 🥡 9. 亚洲城市迷幻 — 曼谷晚娘湿热夜

**参照**：《无烟的爱情》(2003) 曼谷郊区清晨 / 《晚娘》(2005) 泰国热带迷幻色欲

**Style（风格）：**
```
Christopher Doyle Bangkok tropical aesthetic Last Life in the Universe 2003,
humid monsoon pre-storm light, green-amber tropical mold patina color palette,
Thai noodle shop fluorescent mixed with hanging tungsten bulb,
rusted metal rooftops and tropical vines intruding into frame,
handheld 21mm wide-angle observational, natural light plus practicals only,
atmospheric humidity fogging the lens, push-processed for rich green density,
slow contemplative pacing, Southeast Asian melancholy
```

**Scene（画面）：**
```
A lone man sitting at a plastic table on a Bangkok back-alley noodle shop at dusk,
the sky overhead a pre-monsoon bruise purple, hanging tungsten bulb swinging slightly
above him, rusted corrugated roof dripping with humidity, tropical vines and
hand-painted Thai lettering on peeling walls, a passing motorbike leaves a streak
of red tail light, the air thick with steam from soup pots, mold patina greens
climbing the wall behind him, a woman in a thin cotton sundress watching from a
doorway across the alley
```

**完整提示词：**
```
Christopher Doyle Last Life in the Universe 2003, Bangkok back-alley noodle shop
dusk, lone man at plastic table, pre-monsoon bruise-purple sky, hanging tungsten
bulb, rusted corrugated roof, tropical vines, hand-painted Thai signage, passing
motorbike red tail-light streak, mold-patina green walls, woman in thin sundress
watching from doorway, 21mm handheld wide-angle, humidity fogging lens,
push-processed green density, Southeast Asian melancholy, Pen-ek Ratanaruang
collaboration aesthetic
```

💡 打光笔记：钨丝裸灯 + 隔壁店铺冷荧光 + 天空残蓝 = 三层冷暖
🎨 色彩笔记：热带霉绿 + 铜锈黄 + 紫红暮色 + 摩托尾红
🎞️ 技术备注：21mm 广角但不贴脸，保留观察距离

---

### 🏙️ 10. 亚洲城市迷幻 — 东京下町雨夜

**参照**：《空气人形》(2009) 东京下町孤独童话 / 杜可风游览东京偷拍作品

**Style（风格）：**
```
Christopher Doyle Tokyo shitamachi aesthetic, 4am Shibuya alley back-streets,
humid autumn drizzle, red-paper izakaya lantern mixed with vending-machine cyan glow,
neon Japanese katakana bleeding onto wet asphalt reflection,
Sony Venice modern digital with vintage Zeiss Super Speed lens,
handheld observational documentary sway, no key light only practicals,
push-processed digital grain simulating Kodak 5219, Black Pro-Mist 1/4,
lonely fairy-tale dreaminess, Eastern urban solitude
```

**Scene（画面）：**
```
A narrow Tokyo back-alley at 4am after rain, glowing red izakaya paper lantern
casting warm pool of light on wet cobblestones, cyan vending machine on opposite
wall casting cold fill, hand-painted katakana signs stacked vertically, lone
figure in raincoat under umbrella walking away, reflection in puddles doubling
the neon, narrow Showa-era wooden buildings on both sides, cherry leaves
scattered on the ground, melancholic fairy-tale loneliness
```

**完整提示词：**
```
Christopher Doyle Tokyo shitamachi 4am, narrow back-alley after autumn rain,
red izakaya paper lantern warm pool on wet cobblestones, cyan vending machine
cold fill opposite, vertical katakana signage, lone raincoat figure under
umbrella walking away, puddle reflections doubling neon, Showa-era wooden
buildings, scattered cherry leaves, handheld observational sway, Black Pro-Mist
1/4, push-processed grain, Eastern urban fairy-tale solitude
```

💡 打光笔记：红灯笼暖调 + 自动贩卖机冷蓝 + 雨后水面反射 = 双色镜像
🎨 色彩笔记：朱红 + 氖蓝 + 柏油湿黑 + 木材焦茶
🎞️ 技术备注：Sony Venice 模拟 35mm 胶片颗粒

---

### 🤳 11. 广角畸变人脸 — 堕落天使鱼眼贴脸

**参照**：《堕落天使》(1995) 黎明、李嘉欣、金城武的 9.8mm 极致贴脸特写

**Style（风格）：**
```
Christopher Doyle 9.8mm fisheye-adjacent ultra-wide signature distortion,
30cm intimate face-to-lens distance, nose exaggerated into foreground,
warped room geometry with ceiling and walls curving inward,
Dutch angle 10-15 degrees, handheld drunken intimacy,
practical desk lamp or single wall bulb as only light, no fill,
claustrophobic Hong Kong micro-apartment, Fallen Angels 1995 signature,
push-processed grain, acid-yellow tungsten mixed with cobalt window neon
```

**Scene（画面）：**
```
Extreme close-up of a young man's face shot from 30cm with 9.8mm wide-angle lens,
his nose appearing oversized in exaggerated perspective, forehead receding,
background room walls curving backward into fisheye barrel distortion,
a single naked bulb hanging in the corner casting half his face in acid yellow,
the other half in cobalt blue from window neon, a woman's out-of-focus shoulder
intruding into the lower-left frame, Dutch angle 12 degrees tilted, he exhales
cigarette smoke directly at the lens, intimate confrontational proximity
```

**完整提示词：**
```
Christopher Doyle Fallen Angels 9.8mm fisheye ultra-wide face distortion,
30cm lens-to-nose distance, exaggerated nose perspective, room walls curving
barrel-distorted, single naked bulb acid yellow half-face, cobalt window neon
other half, woman shoulder out-of-focus lower-left, Dutch angle 12 degrees,
cigarette smoke exhaled at lens, handheld drunken intimacy, push-processed
grain, Hong Kong micro-apartment claustrophobia, Wong Kar-Wai 1995
```

💡 打光笔记：单颗钨丝灯泡 + 窗外霓虹，阴影明确不加 fill
🎨 色彩笔记：酸黄 + 钴蓝对分面部
🎞️ 技术备注：9.8mm 或等效 14mm 广角，30-40cm 极近距离

---

### 💃 12. 春光乍泄阿根廷探戈

**参照**：《春光乍泄》(1997) 黎耀辉与何宝荣在布宜诺斯艾利斯公寓 / 探戈酒吧跳舞 / 伊瓜苏瀑布

**Style（风格）：**
```
Christopher Doyle Happy Together 1997 Buenos Aires aesthetic,
red butcher shop neon mixed with tango bar amber incandescent bulbs,
humid South American winter, Argentine dive bar smoke-stained wallpaper,
16mm blown-up to 35mm for heavier grain, push-processed 1-stop,
intermittent black-and-white sequences interrupting color,
handheld documentary observation, practical bar lamps and street lights only,
Iguazu waterfall mist haze diffusion, immigrant queer melancholia,
cumbia music scored visual rhythm
```

**Scene（画面）：**
```
Two men in a narrow Buenos Aires studio apartment dancing tango in the kitchen
with a single bare bulb overhead, one wearing a white ribbed undershirt the other
in pinstripe trousers, their bodies pressed close, warm amber light catching
the sweat on their foreheads, a red neon butcher shop sign visible through the
small window bleeding crimson across the wooden floor, condensation on the window
from cooking steam, wooden radio playing tango music on a stool, handheld camera
swaying with their dance, intimate melancholic queer tenderness
```

**完整提示词：**
```
Christopher Doyle Happy Together 1997 Buenos Aires, two men tango dancing in
narrow kitchen, single bare bulb amber overhead, white undershirt and pinstripe
trousers, red butcher-shop neon through small window bleeding crimson on wooden
floor, condensation on windows, wooden radio tango music, handheld camera swaying
with dance, 16mm blown-up grain, push-processed, Argentine immigrant queer
melancholia, Wong Kar-Wai Cannes Best Director aesthetic
```

💡 打光笔记：室内单灯暖 + 窗外红色霓虹冷暖撞色 + 手持晃动
🎨 色彩笔记：琥珀黄 + 血红 + 湿绿瓷砖 + 烟熏棕
🎞️ 技术备注：偶尔切黑白段落表达情绪低谷

---

### 🌊 13. 春光乍泄伊瓜苏瀑布

**参照**：《春光乍泄》(1997) 何宝荣独自去伊瓜苏瀑布的孤独长曝光

**Style（风格）：**
```
Christopher Doyle Iguazu Falls aesthetic Happy Together 1997,
long exposure 1 to 4 seconds on waterfall turning water into white silk ribbons,
dense atmospheric mist refracting rainbow halos,
16mm blown-up to 35mm for grain texture, push-processed,
overcast South American subtropical sky, desaturated earth-green palette,
handheld micro-tremor adding organic feel to long exposure,
solitary figure dwarfed by cosmic scale of water, queer immigrant loss
```

**Scene（画面）：**
```
A lone man in a brown leather jacket standing at an observation platform overlooking
Iguazu Falls, the waterfall rendered in long-exposure silk white ribbons cascading
into a misty green chasm below, rainbow halos in the thick atmospheric spray,
his back to camera, shoulders slumped in grief, deep green jungle framing left and
right, overcast subtropical sky, his figure tiny against the cosmic scale of water,
a sense of being at the end of the world alone
```

**完整提示词：**
```
Christopher Doyle Happy Together Iguazu Falls 1997, lone man in brown leather
jacket at observation platform, waterfall long-exposure 2-second silk white
ribbons, rainbow halos in atmospheric mist, deep green jungle framing, overcast
subtropical sky, back to camera shoulders slumped in grief, handheld micro-tremor,
16mm push-processed grain, queer immigrant end-of-world loneliness
```

💡 打光笔记：全部自然天光 + 瀑布水雾反射
🎨 色彩笔记：去饱和绿 + 水银白 + 灰蓝 + 皮夹克焦茶
🎞️ 技术备注：长曝光 1-4 秒，手持不上三脚架

---

### 🎋 14. 英雄竹林青绿段落

**参照**：《英雄》(2002) 张曼玉与章子怡在竹林飞刀决斗 / 翡翠绿单色章节

**Style（风格）：**
```
Christopher Doyle Hero 2002 emerald jade wuxia aesthetic,
Zhang Yimou color-chapter cinematography monochromatic emerald green,
bamboo forest cathedral with dappled sunlight filtering through canopy,
wire-fu elegant suspended combat, flowing silk robes in matching jade green,
35mm Arriflex 535B anamorphic 2.39:1, Cooke anamorphic primes,
stable composed composition NOT handheld, poetic elevated stillness,
color as narrative chapter — everything in emerald spectrum,
push-processed for saturation density
```

**Scene（画面）：**
```
Two women in flowing jade-green silk robes suspended mid-air in a vast Chinese
bamboo forest, sunlight dappling through the green canopy, thousands of bamboo
stalks in vertical rhythm, flying dagger frozen between them, robes unfurling like
wings, emerald-green light dominating every inch of the frame, fallen bamboo
leaves scattered below, atmospheric haze emphasizing green density, elegant
silent wuxia poetry, anamorphic 2.39:1 wide frame
```

**完整提示词：**
```
Christopher Doyle Hero 2002 bamboo forest emerald chapter, two women in jade-green
silk robes suspended mid-air wire-fu, vast bamboo forest cathedral with dappled
canopy light, flying dagger frozen between them, robes unfurling like wings,
monochromatic emerald dominating frame, Cooke anamorphic primes 2.39:1, stable
composed NOT handheld, Zhang Yimou color-chapter wuxia poetry, push-processed
saturation density, silent elegant combat
```

💡 打光笔记：竹林顶光自然漏光 + 反光板绿色反射 = 让绿色主宰
🎨 色彩笔记：单一翡翠青绿统治，唯一撞色是皮肤与黑发
🎞️ 技术备注：《英雄》是杜可风罕见的稳定构图作品

---

### 🍁 15. 英雄红黄绿单色书馆段落

**参照**：《英雄》(2002) 张曼玉章子怡的红色书馆决斗 / 胡杨林金黄飞叶

**Style（风格）：**
```
Christopher Doyle Hero 2002 blood-red chapter wuxia aesthetic,
crimson maple leaves swirling in tornado of color, everything in the frame red —
robes, walls, leaves, light, shadow,
Zhang Yimou color-as-narrative jealousy chapter,
golden Populus euphratica autumn trees for outdoor duels,
35mm Arriflex with anamorphic primes 2.39:1,
stable composition, high-saturation push-processed,
color replaces dialogue — red is jealousy, lies, desire
```

**Scene（画面）：**
```
Two women in blood-red flowing silk robes swirling in a tornado of crimson maple
leaves, their long black hair whipping, twin swords suspended between them,
the sky behind them fiery amber-red, golden Populus euphratica trees framing
the backdrop, every leaf every thread in red-amber spectrum, one woman's tear
falling in slow-motion, anamorphic 2.39:1 wide frame, high saturation,
wuxia poetic revenge, silent choreography
```

**完整提示词：**
```
Christopher Doyle Hero 2002 red chapter, two women in blood-red silk robes in
tornado of crimson maple leaves, twin swords suspended, fiery amber-red sky,
golden Populus euphratica autumn trees framing, tear falling slow-motion,
anamorphic 2.39:1, high-saturation push-processed, Zhang Yimou jealousy
color-chapter, silent wuxia poetic revenge, Christopher Doyle Cannes technical
Grand Prix 2002
```

💡 打光笔记：反光板染色 + 大量红绸布遮光 + 胡杨林天然金黄
🎨 色彩笔记：单一血红 + 琥珀黄作为唯一呼吸口
🎞️ 技术备注：这是杜可风视觉音乐的巅峰

---

### 🎒 16. 大象哥伦拜恩美式青春

**参照**：《大象》(2003) Gus Van Sant 哥伦拜恩高中校园悲剧 / 斯坦尼康长跟

**Style（风格）：**
```
Christopher Doyle Elephant 2003 Gus Van Sant aesthetic,
Portland Oregon high school naturalistic daylight,
fluorescent corridor tubes overhead, pale-green linoleum floors,
Steadicam long-follow-shot behind teenage figures (rare Doyle stabilized work),
35mm Kodak Vision2 500T stock, natural ambient only,
contemplative slow pacing, Cannes Palme d'Or 2003 minimalism,
mundane American suburb teenage isolation before tragedy,
light-up mirrored reflections in classroom glass
```

**Scene（画面）：**
```
A teenage boy in a yellow T-shirt walking down an empty high school corridor,
camera following steadily behind him in a long Steadicam take, rows of lockers
on both sides, pale-green fluorescent ceiling tubes, overcast Portland daylight
filtering through distant windows at end of corridor, his shadow soft on the
linoleum floor, golden afternoon light catching his blond hair, banal teenage
loneliness, an unseen tragedy about to unfold in the mundanity
```

**完整提示词：**
```
Christopher Doyle Elephant 2003 Gus Van Sant, teenage boy in yellow T-shirt
walking empty high school corridor, Steadicam long-follow-shot behind, rows of
lockers, pale-green fluorescent ceiling tubes, overcast Portland Oregon daylight
through distant end window, soft shadow on linoleum, golden afternoon light on
blond hair, Kodak Vision2 500T, contemplative naturalistic pacing, Cannes 2003
Palme d'Or minimalism, banal tragedy-eve
```

💡 打光笔记：校园日光灯 + 窗外自然光，全部现场光
🎨 色彩笔记：pale 绿 + 暖黄 T 恤 + 灰蓝走廊 = 低饱和美式日常
🎞️ 技术备注：罕见的 Doyle 使用 Steadicam，稳定长跟拍

---

### 🛹 17. 心灵驿站日落汽车公路

**参照**：《心灵驿站》(2007) Gus Van Sant 俄勒冈滑板少年 / 夕阳车窗 / Super 8mm 家庭录像

**Style（风格）：**
```
Christopher Doyle Paranoid Park 2007 Portland skater aesthetic,
Oregon Pacific Northwest overcast diffused cold-blue daylight,
dual-format 35mm main + Super 8mm home-video insert texture,
warm amber golden-hour sunset breaking through cloud layer,
slow-motion skateboard tracking, handheld-with-tremor intimate,
naturalistic available light only, adolescent melancholy and dreaminess,
car dashboard lights as only warm accent in cold blue world,
Kodak Vision 500T for main, Tri-X B&W for memory
```

**Scene（画面）：**
```
A teenage boy in a hoodie sitting in the passenger seat of a rusted pickup truck
at golden hour, Portland forested highway through the windshield, dashboard lights
glowing amber on his face, the horizon a band of molten sunset orange bleeding
into cold blue cloud, skateboard on his lap, handheld camera swaying with the
truck's motion, his expression blank teenage uncertainty, Super 8mm flashback
texture ghost-dissolved over his reflection in the side window, Pacific Northwest
forests streaming past in motion blur
```

**完整提示词：**
```
Christopher Doyle Paranoid Park 2007 Gus Van Sant, teenage boy in hoodie passenger
seat of rusted pickup truck at golden hour, Portland forested highway through
windshield, amber dashboard lights, molten sunset bleeding into cold-blue cloud
horizon, skateboard on lap, handheld sway with truck motion, Super 8mm flashback
texture ghost-dissolved on side window reflection, Pacific Northwest forests
streaming in motion blur, Kodak Vision 500T + Tri-X B&W inserts, adolescent
melancholy dreaminess
```

💡 打光笔记：夕阳直射 + 仪表盘微光 = 自然冷暖
🎨 色彩笔记：落日琥珀 + 冷蓝阴云 + 森林暗绿 + 仪表板橙
🎞️ 技术备注：主格式 35mm，插入 Super 8mm 童年段落

---

### 👻 18. 灵异第六感冷蓝阴影

**参照**：《灵异第六感》(1999) / 《Lady in the Water》(2006) M. Night Shyamalan 心理惊悚

**Style（风格）：**
```
Christopher Doyle M. Night Shyamalan psychological horror aesthetic,
sickly pale-green hospital corridor mixed with cold desaturated blue shadows,
slow creeping wide-angle dolly forward, precise symmetrical composition,
Kodak Vision2 low-contrast pushed to desaturate further,
no warm color anywhere — supernatural dread in cold palette,
Philadelphia Gothic residential with heavy curtains blocking light,
single practical table lamp casting small warm pool (the lone human warmth),
cinematic supernatural silence visualized
```

**Scene（画面）：**
```
A young boy in red pajamas standing at the top of a dark Philadelphia Victorian
staircase, single table lamp in the foyer below casting a small warm pool, rest
of the house drowned in cold desaturated blue-green shadow, long hallway receding
into blackness behind him, windows with heavy velvet curtains muting any
exterior light, the air visibly cold — breath-mist, his eyes looking past camera
at something we cannot see, slow creeping dolly-in composition, supernatural
silence
```

**完整提示词：**
```
Christopher Doyle Sixth Sense 1999 M Night Shyamalan, young boy in red pajamas
at top of dark Victorian staircase, single warm table lamp in foyer below as
lone warm pool, cold desaturated blue-green shadows throughout house, long
receding hallway into blackness behind, velvet curtains blocking exterior,
breath-mist cold air visible, eyes looking past camera at unseen entity,
slow creeping dolly-in, precise symmetrical composition, supernatural silence,
low-contrast pushed desaturation
```

💡 打光笔记：单灯暖光作为「人类温度锚点」vs 整屋冷蓝阴影
🎨 色彩笔记：冷蓝绿 + 苍白灰 + 红睡衣作为唯一视觉刺点
🎞️ 技术备注：缓慢 dolly-in，完全相反于杜可风常用的手持

---

## 二、按情绪分类的提示词模板

### 💔 孤独 / 失眠

```
Christopher Doyle insomnia loneliness aesthetic, 4am Hong Kong empty street,
single lone figure at convenience store counter, neon signs humming silently,
magenta-cyan humid palette, step-printing crowd blur with frozen subject,
14mm wide-angle hip-level, push-processed Kodak grain, handheld micro-tremor,
time dilated and compressed, Wong Kar-Wai existential urban solitude
```

### 💘 暧昧 / 未说出口的爱

```
Christopher Doyle unspoken-love aesthetic, In the Mood for Love palette,
two figures in narrow corridor with restrained distance, window grid shadow across faces,
oxblood qipao silk against tungsten amber wallpaper, Black Pro-Mist diffusion,
slow-motion 32fps near-touch, cigarette smoke as suppressed desire,
tobacco-amber half-lit profile, Maggie Cheung archetype
```

### 🍷 醉酒 / 迷幻

```
Christopher Doyle drunken-camera aesthetic, 9.8mm ultra-wide Dutch angle 12-degree tilt,
warped room geometry closing in, neon bleeding onto face unevenly,
handheld swaying step-printing blur, push-processed grain storm,
acid-yellow tungsten mixed with cobalt neon, Fallen Angels 1995 extremity,
lens closer than comfort allows
```

### 🌸 怀旧 / 记忆

```
Christopher Doyle memory-palette aesthetic, nostalgic 1960s Hong Kong amber,
tungsten 2700K warm wallpaper interior, Black Pro-Mist 1/4 dreamlike softness,
slow-motion corridor walk, smoky tobacco-honey haze, in-camera double exposure
for memory layer, Maggie Cheung half-lit profile, Wong Kar-Wai time-loop
```

### 🔪 危险 / 杀意

```
Christopher Doyle menacing aesthetic, Fallen Angels killer silhouette,
cobalt-blue neon backlighting figure into darkness, 9.8mm claustrophobic proximity,
bloody-red practical light intrusion, handheld predatory drift, push-processed grain,
push-processed acid-yellow tungsten mixing with cyan neon, urban night hunt
```

### 🌊 自由 / 流浪

```
Christopher Doyle wanderlust aesthetic, Happy Together Iguazu or Last Life Bangkok,
vast natural landscape dwarfing lone figure, desaturated green-amber tropical palette,
handheld 21mm observational, long-exposure waterfall silk or motion-blur highway,
queer immigrant end-of-world loneliness, poetic geographic displacement
```

### 🗡️ 宿命 / 武侠

```
Christopher Doyle Hero wuxia aesthetic, monochromatic color chapter per scene,
blood-red OR emerald-jade OR cobalt-blue OR desert-white single color dominating frame,
Cooke anamorphic primes 2.39:1 stable composition, Zhang Yimou collaboration,
silk robes suspended mid-air wire-fu, color-as-narrative poetic combat,
Cannes technical Grand Prix 2002 aesthetic
```

---

## 三、按影片参照的完整提示词套装

### 《阿飞正传》(Days of Being Wild, 1990) 风格

```
Christopher Doyle Days of Being Wild 1990, 1960s Hong Kong amber tungsten interior,
monsoon humid Manila tropic scenes, Wong Kar-Wai genesis style, slow handheld
breathing, low-angle vintage room composition, mirror reflections doubling subject,
oxblood and brass tones, single wall sconce illumination, [场景描述], Leslie Cheung
archetype, tropical rain through window, Arriflex 35BL Zeiss Super Speed
```

### 《重庆森林》(Chungking Express, 1994) 风格

```
Christopher Doyle Chungking Express 1994, Hong Kong Chungking Mansions corridor,
magenta and lime neon humid night, step-printing motion blur impressionist crowd,
14mm wide-angle convenience store, blonde wig in trench coat, frozen subject in
flowing time, push-processed Kodak 5293 film grain, 4am Tsim Sha Tsui insomnia,
[场景描述], handheld intimate breathing, no key light only practicals
```

### 《东邪西毒》(Ashes of Time, 1994) 风格

```
Christopher Doyle Ashes of Time 1994, Wuxia desert poetry, golden hour sandstorm,
blood-red sunset over Gobi Desert, fire-lit handheld duels, step-printing sword
fight blur, intimate wide-angle face in vast desert emptiness, Mongolian wasteland
mysticism, [场景描述], Kodak push-processed grain, Tony Leung/Leslie Cheung archetype,
handheld 14mm close-ups mixed with vast wide shots
```

### 《堕落天使》(Fallen Angels, 1995) 风格

```
Christopher Doyle Fallen Angels 1995, 9.8mm fisheye extreme wide-angle intimate
face distortion, Hong Kong underground tunnel neon, sickly acid yellow and cobalt
blue mixed, drunken Dutch angle 12-degree handheld, late-night Mong Kok subway,
killer angel claustrophobic micro-apartment, push-processed grainy nightscape,
[场景描述], step-printing motion smear, extreme proximity leather-jacket aesthetic
```

### 《春光乍泄》(Happy Together, 1997) 风格

```
Christopher Doyle Happy Together 1997, Buenos Aires red butcher-shop neon,
Argentine tango bar amber, Iguazu Falls long-exposure silk ribbons, claustrophobic
immigrant apartment wide-angle, color and B&W intercut, 1997 South American queer
melancholia, handheld observational street, [场景描述], 16mm blown-up to 35mm heavy
grain, Tony Leung/Leslie Cheung archetype, cumbia rhythm visualized
```

### 《花样年华》(In the Mood for Love, 2000) 风格

```
Christopher Doyle In the Mood for Love 2000, 1962 Hong Kong tungsten amber corridor,
oxblood qipao silk slow-motion walk, window grid shadow on wall, claustrophobic
boardinghouse staircase, In the Mood for Love palette, smoky tobacco-amber haze,
Maggie Cheung half-lit profile, restrained romantic longing, [场景描述], Black
Pro-Mist 1/4 diffusion, Cooke S4 35mm spherical, Kodak 5245 push-processed
```

### 《英雄》(Hero, 2002) 风格

```
Christopher Doyle Hero 2002 color-chapter wuxia, [选择章节：blood-red maple leaves
OR cobalt blue silk lake duel OR emerald jade bamboo forest fight OR white sand
desert death OR black-and-gold imperial Qin court], monochromatic palette per scene,
Cooke anamorphic primes 2.39:1, Zhang Yimou collaboration, stable composition
wire-fu wuxia, Cannes technical Grand Prix 2002, [场景描述], high-saturation
push-processed, silk robes suspended mid-air
```

### 《2046》(2004) 风格

```
Christopher Doyle 2046 2004, future train neon corridor, 1960s amber hotel room
overlap, double exposure memory dissolve, dual-world palette, sickly cobalt vs
nostalgic gold, Wong Kar-Wai time-loop melancholia, [场景描述], Black Pro-Mist 1/2
diffusion, in-camera double exposure, cherry-red LED rope lights, anamorphic flavor
2.39:1, Tony Leung with typewriter archetype
```

### 《大象》(Elephant, 2003) 风格

```
Christopher Doyle Elephant 2003 Gus Van Sant, Portland Oregon high school
naturalistic daylight, Steadicam long-follow-shot behind teenager, pale-green
fluorescent corridor, rows of lockers, Kodak Vision2 500T naturalistic ambient,
contemplative slow pacing, Cannes 2003 Palme d'Or minimalism, [场景描述], banal
teenage suburbia pre-tragedy, overcast Pacific Northwest diffused light
```

### 《心灵驿站》(Paranoid Park, 2007) 风格

```
Christopher Doyle Paranoid Park 2007 Gus Van Sant, Portland skater teenage
melancholy, Super 8mm home-video texture intercut with 35mm main, Pacific Northwest
overcast diffused cold-blue daylight, dreamy slow-motion skateboard tracking,
Kodak Vision 500T + Tri-X B&W inserts, [场景描述], golden-hour sunset amber break,
adolescent uncertainty aesthetic
```

### 《灵异第六感》(Sixth Sense 姊妹片 / Lady in the Water) 风格

```
Christopher Doyle M Night Shyamalan psychological horror, sickly pale-green
hospital corridor, cold desaturated blue shadows, slow creeping wide-angle
dolly-in, precise symmetrical composition, Kodak Vision2 low-contrast pushed
desaturation, no warm color anywhere, Philadelphia Victorian Gothic residential,
single practical lamp lone warm pool, [场景描述], supernatural silence visualized,
breath-mist cold air
```

### 《无烟的爱情》(Last Life in the Universe, 2003) 风格

```
Christopher Doyle Last Life in the Universe 2003 Pen-ek Ratanaruang, Bangkok
suburban natural light, slow contemplative wide shots, humid green-amber tropical
palette, lonely Japanese expat poetic isolation, [场景描述], atmospheric humidity
fogging lens, push-processed green density, 21mm handheld observational, Southeast
Asian melancholy, pre-monsoon bruise-purple sky
```

### 《追龙》(Chasing the Dragon, 2017) 风格

```
Christopher Doyle Chasing the Dragon 2017, 1960s Kowloon Walled City crime saga,
neon humid noir, period gangster amber, Hong Kong colonial tension, hand-painted
Chinese signage, [场景描述], wet alleyway reflections, tobacco-amber interior
opium den, blood-red street lantern, handheld witness perspective, push-processed
digital grain simulating Kodak 5218
```

---

## 四、打光方案模板（Doyle-Specific Lighting Setups）

### 方案 A：香港便利店午夜 — Chungking Express

```
LIGHTING SETUP — Doyle Convenience Store Night:

• KEY: None — no artificial key light added
• PRACTICAL 1: Ceiling fluorescent tubes (5600K cool) as overall fill
• PRACTICAL 2: Shop-window neon signs (magenta Pantone 219 + cyan Pantone 306)
• PRACTICAL 3: Street sodium lamps bleeding through glass door (2200K amber)
• AMBIENT: Humid air with visible cigarette smoke to refract light
• SHADOW: Under-eye shadows accepted, no fill
• COLOR STRATEGY: Magenta + Cyan + Acid-Yellow triadic neon mix
• MOOD: 4am insomnia, emotional suspension, time dilation
• CAMERA: 14mm wide-angle handheld at hip-level, 30-40cm from subject
```

### 方案 B：9.8mm 贴脸畸变 — Fallen Angels

```
LIGHTING SETUP — Doyle 9.8mm Face Distortion:

• KEY: None
• PRACTICAL 1: Single naked 60W tungsten bulb at 2700K (acid yellow half-face)
• PRACTICAL 2: Window-reflected cobalt neon from outside (8500K cyan other half)
• FILL: Absolutely none — let the face be half-black
• AMBIENT: Cigarette smoke + humid lens fog
• SHADOW: Extreme, full occlusion on one facial half
• COLOR STRATEGY: Acid yellow vs cobalt blue dichromatic split
• MOOD: Drunken, lovesick, claustrophobic intimacy
• CAMERA: 9.8mm Zeiss, 30cm face distance, Dutch tilt 10-15°
```

### 方案 C：In the Mood for Love 走廊

```
LIGHTING SETUP — Doyle Tenement Corridor:

• KEY: Single wall sconce practical at 3200K (warm amber)
• FILL: None — or dim bounce from opposite amber wall
• PRACTICAL 2: Distant corridor ceiling bulb as rim (2700K)
• PRACTICAL 3: Window grid shadow casting diagonal bars on face
• AMBIENT: Cigarette smoke thick to refract warm light
• SHADOW: Half-face dissolving into tobacco-brown
• COLOR STRATEGY: Monochromatic amber (tungsten) with oxblood silk punch
• DIFFUSION: Black Pro-Mist 1/4 on lens for dreamlike softness
• FRAME RATE: 32fps for slow-motion memory quality
• MOOD: Restrained longing, unspoken love
```

### 方案 D：Step-Printing 可视化 — Chungking Express

```
LIGHTING SETUP — Doyle Step-Printing Crowd Blur:

• BASE: Convenience store fluorescent ceiling tubes (existing practical)
• SUBJECT: Central figure lit with matching practical, no extra key
• CROWD: Ambient lighting; subjects in motion create color streaks
• TECHNIQUE: Shot at 1/8 second shutter, then optical-printer re-exposed 3x
• COLOR STRATEGY: Triadic — red / yellow / turquoise trailing motion smear
• MOOD: Time-dilation, impressionist urban loneliness
• POST: Push-processed Kodak 5293 for heavy grain density
• MODEL PROMPT: "step-printing motion blur, frozen subject in flowing crowd,
  Wong Kar-Wai impressionist smear, multi-exposure crowd trails"
```

### 方案 E：Hero 单色章节打光

```
LIGHTING SETUP — Doyle Hero Monochromatic Chapter:

• KEY: Reflected light bounced off massive colored silk cloth (red/green/blue)
• FILL: Matching-colored bounce card for same-palette fill
• AMBIENT: Atmospheric haze tinted with same color gel
• PRACTICAL: None — this is intentionally stylized, not realistic
• SHADOW: Tinted same color, never pure black
• COLOR STRATEGY: ONE color dominates entire frame
  - Red chapter: Blood-red Pantone 200 + amber accent
  - Blue chapter: Cobalt Pantone 286 + silver
  - Green chapter: Emerald Pantone 341 + jade
  - White chapter: Pure 6500K + golden sand
  - Black chapter: 2700K tungsten + polished brass
• MOOD: Color as narrative chapter, Zhang Yimou poetic wuxia
• CAMERA: Anamorphic 2.39:1, stable (rare for Doyle)
```

### 方案 F：Bangkok 热带湿热 — Last Life in the Universe

```
LIGHTING SETUP — Doyle Bangkok Tropical Humid:

• KEY: Natural pre-monsoon sky diffused through cloud (6500K overcast)
• PRACTICAL 1: Hanging tungsten bulb over food stall (2700K amber swing)
• PRACTICAL 2: Fluorescent from adjacent shop (5600K cool)
• AMBIENT: Dense humidity fogging lens, mold-patina walls absorbing green
• SHADOW: Soft, long due to low sun angle
• COLOR STRATEGY: Green-amber dichromatic — tropical mold vs warm tungsten
• CAMERA: 21mm Zeiss wide-angle handheld observational
• MOOD: Southeast Asian melancholy, expat isolation, heat suspension
```

---

## 五、负面提示词（Negative Prompts — Anti-Doyle）

以下元素与杜可风美学矛盾，应在 SD/FLUX/Nano Banana Pro 的负面提示词中排除：

```
NEGATIVE (anti-Doyle):
clean studio lighting, HDR tone-mapped, three-point broadcast lighting,
perfect color grading, teal-and-orange Hollywood, sterile digital sharpness,
Steadicam ultra-smooth, gimbal stabilized, drone aerial perspective,
lens correction, anti-shake stabilization, anti-aliasing perfect edges,
low-saturation muted palette, muted naturalism, documentary neutral gray,
long-focus telephoto compression, 85mm portrait compression, zoom flatness,
GoPro wide-angle action-cam, fisheye corrected, optically perfect,
over-sharp, AI-upscaled detail, 8K hyperreal detail, sterile clean,
bokeh-heavy DSLR shallow DOF, portrait mode beauty-smooth,
warm cozy Instagram filter, pastel dreamy pastel, vaporwave aesthetic,
anime cel-shaded, cartoon stylization, Pixar smooth 3D,
perfectly symmetrical composition, rule-of-thirds precision,
dry arid color, Scandinavian minimalism neutral, cold desaturated melancholy
```

**关键排除项解释**：
- `three-point lighting` → 杜可风拒绝好莱坞三点布光
- `teal-and-orange` → 杜可风用洋红-青绿代替
- `Steadicam ultra-smooth` → 杜可风要手持呼吸感
- `clean digital sharpness` → 杜可风要颗粒、湿气、模糊
- `lens correction` → 杜可风拥抱镜头畸变
- `perfect composition` → 杜可风要酒醉、倾斜、偏移
- `muted Scandinavian` → 杜可风是高饱和亚洲

---

## 六、模型适配指南

### Midjourney

**推荐参数**：
```
--raw --stylize 750 --chaos 25 --ar 16:9 --v 8.2
```

**画幅**：
- `--ar 37:20` 或 `--ar 37:20` → 35mm 学院宽银幕（《重庆森林》《堕落天使》）
- `--ar 239:100` 或 `--ar 12:5` → 变形宽银幕（《英雄》《2046》未来段）
- `--ar 4:3` 或 `--ar 133:100` → 早期胶片感（偶尔实验）

**权重调校**：
```
Christopher Doyle::2 Wong Kar-Wai::1.5 neon humid::1.5 step-printing::1.2
handheld::1 9.8mm wide-angle::1.3 push-processed film grain::1
```

**示例**：
```
Christopher Doyle::2 Chungking Express 1994 convenience store, magenta cyan
neon humid, 14mm wide-angle handheld, step-printing crowd blur, frozen subject
in flowing time, push-processed Kodak grain, 4am Hong Kong insomnia, Wong Kar-Wai
palette --raw --stylize 750 --chaos 25 --ar 37:20 --v 8.2
```

### Stable Diffusion / FLUX

**推荐 LoRA**：
- Wong Kar-Wai LoRA（Hong Kong noir）
- Analog Film Style LoRA（push-processed grain）
- Neon City LoRA
- Hong Kong 80s/90s LoRA
- 9.8mm Fisheye LoRA（广角畸变）
- Step-Printing Motion Blur LoRA（若存在）

**Sampler**：DPM++ 2M Karras / Euler a

**Steps**：30-40

**CFG Scale**：6-8（别太高，杜可风要保留「意外」）

**Resolution**：最好 1024×768 或 1536×1024 以上

**正面提示词强调**：
```
(Christopher Doyle cinematography:1.4), (Wong Kar-Wai palette:1.3),
(neon humid Hong Kong:1.3), (step-printing motion blur:1.2),
(9.8mm wide-angle distortion:1.2), (push-processed Kodak 5293 film grain:1.1),
(handheld intimate framing:1.1), (Black Pro-Mist diffusion:1.0),
(no key light practical only:1.0)
```

**负面提示词（完整）**：
```
(clean studio lighting:1.3), (three-point lighting:1.3), (teal and orange:1.4),
(Steadicam smooth:1.2), (HDR:1.3), (8K hyperreal:1.2), (lens correction:1.1),
(sterile digital:1.2), (muted Scandinavian:1.2), (anime:1.4), (cartoon:1.4),
blurry face, deformed, extra fingers, bad anatomy, watermark, text, logo
```

### DALL-E 3 / GPT Image

**推荐风格**：叙事描述型（不用权重）
```
A cinematic still from a Christopher Doyle / Wong Kar-Wai style film,
[场景描述], shot on 35mm Arriflex with 14mm wide-angle lens, push-processed
for heavy grain, lit only by practical neon and tungsten bulbs, humid
magenta-cyan Hong Kong atmosphere at 4am, handheld intimate framing,
step-printing motion blur on background crowd, frozen subject tack-sharp
in center, Black Pro-Mist diffusion softening highlights
```

**关键词顺序**：影片类型 → 场景 → 器材 → 光源 → 色彩 → 运动 → 质感

### Nano Banana Pro (Gemini 3 Pro Image) / ZenStudio

**提示词特点**：中英混合有效，结构化 prompt 效果最佳

**推荐模板**：
```
Style: Christopher Doyle 杜可风 1994 Chungking Express aesthetic
Scene: 4am Hong Kong convenience store with magenta-cyan neon humid
Subject: lone man in trench coat eating canned pineapple at chrome counter
Lens: 14mm wide-angle handheld, hip-level, 30cm intimate distance
Light: no key light, ceiling fluorescent + window neon practical only
Color: magenta + lime green + acid yellow triadic palette
Motion: step-printing crowd blur, frozen subject in flowing time
Grain: push-processed Kodak 5293 heavy grain, Black Pro-Mist 1/4 diffusion
Mood: 4am insomnia, emotional suspension, Wong Kar-Wai signature
Aspect: 1.85:1 standard theatrical
```

### Kling / Runway Gen-3 / Sora（视频）

**关键 motion 词**：
```
step-printing motion blur trailing behind running figure,
drag-shutter light trail ribbons from motorcycle headlights,
slow-motion 32fps Maggie-Cheung corridor walk,
frozen subject while crowd smears into impressionist color rivers,
handheld breathing camera micro-tremor,
1/4 second long-exposure zoom-during-exposure radial burst
```

**时长建议**：3-6 秒为最佳（杜可风的「时间凝固」本就不需要长）

**Prompt 示例（Kling）**：
```
Christopher Doyle Chungking Express style, lone man in trench coat at chrome
convenience store counter eating canned pineapple, magenta-cyan neon humid
Hong Kong night, step-printing motion blur on background crowd smearing into
color rivers while he stays tack-sharp, handheld 14mm wide-angle breathing
camera, push-processed Kodak grain, 4am insomnia, subtle cigarette smoke drift,
duration 5 seconds, 24fps with optical-printer blur on crowd motion
```

---

## 七、画幅比例推荐

| 比例 | 用途 | 杜可风实例 | MJ 参数 |
|------|------|-----------|--------|
| **1.85:1** | 标准院线——王家卫宇宙主力 | 《重庆森林》《堕落天使》《花样年华》 | `--ar 37:20` |
| **2.39:1** | 变形宽银幕——史诗/未来 | 《英雄》《2046》未来段落 | `--ar 12:5` |
| **1.66:1** | 欧洲艺术片学院 | 《春光乍泄》部分 / 早期欧洲合作 | `--ar 5:3` |
| **1.37:1** | 学院比例——复古回忆 | 《花样年华》部分插入段 | `--ar 11:8` |
| **2:1** | 现代折中 | 近期数字合作 | `--ar 2:1` |
| **4:3** | 偶尔实验 / Super 8 插入 | 《心灵驿站》《2046》记忆段 | `--ar 4:3` |

**画幅选择逻辑**：
- 「湿润迷幻香港夜」优先 1.85:1（杜可风经典比例）
- 「武侠/未来史诗」优先 2.39:1（《英雄》《2046》）
- 「记忆/童年/家庭录像」用 4:3（插入段落）
- 永远不要用 16:9 电视比例（杜可风从不为电视拍摄）

---

## 八、杜可风 vs 李屏宾 提示词速查对比

| 维度 | 杜可风（Christopher Doyle） | 李屏宾（Mark Lee Ping-Bing） |
|------|-----------------------------|---------------------------|
| **核心哲学提示词** | `Christopher Doyle humid drunken camera, light-is-a-verb, happy accident spontaneity` | `Mark Lee Ping-Bing contemplative observation, wait-for-light philosophy, Eastern negative space` |
| **光源关键词** | `neon humid Hong Kong, magenta cyan mixed, sodium tungsten practical, step-printing crowd blur` | `natural window light, moonlight diffusion, candlelight ember, fog-veiled ambient, ink-wash luminosity` |
| **色彩关键词** | `humid saturated magenta-jade, nostalgic 1960s amber, acid yellow cobalt, oxblood qipao silk` | `ink-wash gray, desaturated tea-brown, jade mountain green, Republican-era sepia, misty watercolor palette` |
| **构图关键词** | `9.8mm fisheye face distortion, Dutch angle 12 degrees, mirror doubling, frame-within-frame claustrophobia` | `balanced symmetry, Chinese landscape three-part composition, generous negative space, contemplative wide shot` |
| **运镜关键词** | `handheld breathing tremor, step-printing 1/8s shutter, drag-shutter long exposure, drunken sway` | `static contemplative long take, slow horizontal pan, breathing handheld micro-tremor, tidal rhythm movement` |
| **镜头关键词** | `9.8mm Zeiss Super Speed, 14mm wide-angle, 21mm handheld intimate` | `35mm Cooke S4, 50mm standard, 85mm dignified distance` |
| **场景关键词** | `Hong Kong Chungking Mansions, Bangkok back-alley, Buenos Aires tango bar, Kowloon subway 4am` | `Taiwanese countryside, Shanghai longtang lane, Japanese mountain temple, Chinese riverside morning mist` |
| **情绪关键词** | `4am insomnia, lovesick urban solitude, drunken lovesickness, neon fever dream` | `autumn contemplation, familial continuity, four-seasons passage, restrained melancholic acceptance` |
| **时间感** | `time-dilation, frozen subject flowing crowd, moment suspended in humid air` | `time as collaborator, three-week fog wait, season-long observation, breathing-with-light` |
| **代表影片引用** | `Chungking Express 1994, Fallen Angels 1995, Hero 2002, 2046 2004, In the Mood for Love 2000` | `City of Sadness 1989, The Assassin 2015, Flowers of Shanghai 1998, Yi Yi 2000, Norwegian Wood 2010` |
| **负面排除** | 排除稳定器、干净光、低饱和 | 排除霓虹、手持剧烈、高对比硬光 |
| **最适场景** | 都市夜街、霓虹、爱情、迷幻、武侠色彩 | 家庭、历史、自然、乡愁、东方禅意 |

### 选哪一位？快速决策树

```
问：场景是「都市夜晚」吗？
  ├── 是 → 问：有霓虹吗？
  │        ├── 有 → 杜可风（《重庆森林》《堕落天使》模板）
  │        └── 无 → 杜可风（《花样年华》走廊模板）
  │
  ├── 否 → 问：场景是「自然/乡村/历史」吗？
  │        ├── 是 → 李屏宾（《悲情城市》《刺客聂隐娘》模板）
  │        └── 否 → 继续
  │
  ├── 场景是「武侠/古装」？
  │   ├── 色彩强烈单色章节 → 杜可风（《英雄》模板）
  │   └── 水墨山水自然光 → 李屏宾（《刺客聂隐娘》模板）
  │
  └── 场景是「家庭/日常」？
      ├── 都市现代 → 两位都可
      └── 东方传统 → 李屏宾优先
```

### 融合模板（两位大师合作场景）

**《花样年华》式融合**（杜可风前期 + 李屏宾后期）：
```
Hybrid Doyle-and-Mark-Lee aesthetic for In the Mood for Love,
Doyle's tungsten amber corridor + Black Pro-Mist diffusion,
combined with Mark Lee Ping-Bing's window-light contemplative stillness,
Maggie Cheung half-lit by window in oxblood qipao, smoky tobacco-amber haze,
restrained longing both urban-sensual and Eastern-meditative,
slow-motion 32fps tracking with contemplative still frames
```

---

## 九、终极组合速查表

| 场景需求 | 推荐影片模板 | 核心技法 | 主色调 | 关键提示词 |
|---------|------------|---------|--------|-----------|
| 午夜便利店 | 《重庆森林》 | step-printing + 14mm 广角 | 洋红 + 柠檬黄 + 青绿 | `Chungking Express 1994, 4am convenience store, neon humid` |
| 霓虹街头追逐 | 《堕落天使》 | 9.8mm + 慢门拖影 | 酸黄 + 钴蓝 + 血红 | `Fallen Angels 9.8mm fisheye, Dutch angle, drag-shutter` |
| 旅店狭窄走廊 | 《花样年华》 | 32fps 慢镜 + 钨丝暖 | 怀旧黄 + 酒红旗袍 | `In the Mood for Love 1962, tungsten amber corridor` |
| 未来列车/双世界 | 《2046》 | 双重曝光 + 霓虹 | 樱桃红 + 钴蓝 + 琥珀 | `2046 train corridor, double exposure dissolve` |
| 武侠竹林决斗 | 《英雄》绿章 | 单色 + 稳定 + 2.39:1 | 翡翠青绿 | `Hero emerald bamboo forest, anamorphic` |
| 武侠书馆/秋叶 | 《英雄》红章 | 单色 + 飞叶 | 血红 + 琥珀 | `Hero red maple chapter, tornado of crimson` |
| 沙漠武侠 | 《东邪西毒》 | 手持 + 金沙 | 橘金 + 血红 | `Ashes of Time Gobi desert, handheld duel` |
| 阿根廷迷失 | 《春光乍泄》 | 黑白彩色 + 红霓虹 | 血红 + 琥珀 + 黑白 | `Happy Together Buenos Aires, butcher shop neon` |
| 曼谷郊区 | 《无烟的爱情》 | 自然光 + 21mm | 热带霉绿 + 铜锈黄 | `Last Life in Universe Bangkok, tropical humid` |
| 东京下町 | 《空气人形》启发 | 红灯笼 + 雨夜 | 朱红 + 氖蓝 | `Tokyo shitamachi 4am, izakaya lantern` |
| 美式校园 | 《大象》 | Steadicam 长跟 | pale 绿 + 暖黄 | `Elephant 2003 Portland high school corridor` |
| 美式青春公路 | 《心灵驿站》 | Super 8 + 夕阳 | 琥珀 + 冷蓝 | `Paranoid Park golden hour pickup truck` |
| 心理惊悚冷屋 | 《灵异第六感》 | 缓慢 dolly + 冷蓝 | 苍白绿 + 红睡衣 | `Shyamalan sickly pale-green corridor` |
| 香港黑帮历史 | 《追龙》《阿飞正传》 | 实景霓虹 + 怀旧 | 怀旧黄 + 血红 | `Kowloon Walled City 1960s neon noir` |

---

## 十、杜可风「禁止清单」—— AI 提示词中要避免的反模式

❌ **不要写**：`perfect symmetrical composition` → 杜可风要倾斜、偏移
❌ **不要写**：`Steadicam smooth stable` → 杜可风要手持晃动
❌ **不要写**：`HDR high dynamic range` → 杜可风要保留阴影吞噬
❌ **不要写**：`professional three-point lighting` → 杜可风拒绝好莱坞布光
❌ **不要写**：`clean sharp digital 8K` → 杜可风要胶片颗粒与柔焦
❌ **不要写**：`teal and orange color grading` → 杜可风用洋红-青绿代替
❌ **不要写**：`85mm portrait telephoto` → 杜可风讨厌长焦窥视
❌ **不要写**：`bright evenly lit` → 杜可风要明暗撕裂
❌ **不要写**：`low saturation muted Scandinavian` → 杜可风要高饱和亚洲湿润
❌ **不要写**：`drone aerial wide shot` → 杜可风永远在地面、在人群中、在街角

---

## 最后的话

「杜可风的提示词不该是指令，而是邀请——邀请 AI 进入那个永远凌晨 4 点的、霓虹在玻璃上融化的、时间被烟雾稀释的亚洲夜晚。你写的每一个 prompt 都应该像端起一杯啤酒，坐在旺角的大排档，看世界变成印象派油画。」

记住 6 条金律：
1. **宁可湿，不要干** — 所有场景都要 humid / wet / misty / smoky
2. **宁可乱，不要齐** — 用 Dutch angle / handheld / off-center 代替对称
3. **宁可醉，不要醒** — 用 9.8mm 贴脸 / drunken perspective / claustrophobic
4. **宁可糊，不要锐** — 用 step-printing / motion blur / Black Pro-Mist
5. **宁可意外，不要计划** — 用 happy-accident / lens flare / light leak
6. **宁可引用，不要抽象** — 每个 prompt 都带具体影片名与年份

---

*"Light is a verb, not a noun. Shoot with your heart broken open." — Christopher Doyle*