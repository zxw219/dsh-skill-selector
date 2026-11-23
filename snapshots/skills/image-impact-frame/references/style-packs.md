# 画风包与配色

**用户素材的画风永远优先。** 有参考图或已有角色，就沿用它的画风，只从下面借冲击手段；画风包只在用户没定画风、或明确点名时整体套用。

每个包给出：适合场合、关键写法、适合档位、要避开的坑。

---

## 1. 赛璐璐漫剧（动漫默认）

- **适合**：国漫、日系动画、AI 漫剧的大多数打斗。
- **关键写法**：清晰粗描边，平涂两层阴影，高光是硬边色块；冲击瞬间背景化为集中线或纯色；可以一帧反相或黑白剪影；受击部位有夸张形变（拳头压进脸颊的凹陷、身体对折）。
- **中文句**：赛璐璐动画风格，干净粗描边，平涂双色阴影，冲击瞬间背景变为放射集中线，接触点一团硬边白光。
- **English**：cel-shaded anime, clean bold outlines, flat two-tone shading, hard-edged highlight shapes, the background collapses into radial speed lines at the moment of impact.
- **档位**：L1–L5 全可用。
- **避开**：只写"anime style"会被视频模型拉向写实；写实皮肤毛孔、真实布料褶皱会冲淡赛璐璐感。

## 2. 写实电影

- **适合**：真人感短剧、电影预告、写实动作。
- **关键写法**：真实镜头语言（焦段、景深、快门）；冲击靠重心转移、道具惯性、布料与碎屑反馈；局部瞬时高光、粉尘体积光、慢动作中的水珠和汗珠。
- **中文句**：电影级实拍质感，35mm 镜头，浅景深，命中瞬间接触点局部被照亮，粉尘在逆光里成团散开。
- **English**：photoreal live-action, 35mm lens, shallow depth of field, a brief local burst of light at the point of contact, dust blooming through the backlight.
- **档位**：L1–L4；L5 的画风断裂只在用户明确要时用。
- **避开**：漫画放射线、全屏黑白；过度震屏。

## 3. 刮痕干笔（高风格化）

- **适合**：概念感强的冲击帧、海报式战斗、抽象对决。
- **特征清单**（写提示词时逐项落到画面上）：
  1. **画法先行**：第一句交代"干笔刮痕画"，再写人物和动作。
  2. **笔触质感**：每一笔都带干刷的毛糙纹理，笔尾分叉。
  3. **高反差**：通常只用两到三种颜色，没有中间过渡色。
  4. **人物简化**：姿态靠大笔势表达，五官省略，眼睛只留一点高光。
  5. **兵器最亮**：武器或能量是全画最亮的笔画。
  6. **碎块硬朗**：飞出的碎块边缘有棱角。
- **English**：dry-brush scratch painting, rough bristle texture inside every stroke, split stroke tails, two or three flat colours with no gradients, figures reduced to a few bold gestural strokes with a single glint for the eye, the weapon as the brightest stroke in the image, angular flying chips.
- **档位**：L3–L5。
- **常见跑偏与修正**：
  - 出来像普通插画 → 把画法描述移到第一句，Midjourney 加 `--raw`。
  - 人物变写实 → 删掉描写五官和皮肤的词，只留姿态和轮廓。
  - 笔触被抹平成色块 → 补"每一笔都看得见干刷纹理"。

## 4. 美漫硬阴影

- **适合**：超英、机甲、街头格斗。
- **关键写法**：大块纯黑阴影，网点，粗犷描线，强烈明暗切分；可加拟声字（用户要才加，字放进双引号）。
- **English**：American comic style, heavy spot blacks, halftone dots, thick confident inks, a hard split between light and shadow.
- **档位**：L2–L5。
- **避开**：细碎写实纹理；渐变柔光。

## 5. 3D 游戏 CG

- **适合**：游戏宣传、3D 动画、机甲与魔法特效。
- **关键写法**：PBR 材质，武器拖尾，方向性粒子，命中火花从金属相交处喷出，局部辉光；镜头保持稳定空间轴线。
- **English**：stylized 3D game cinematic, PBR materials, weapon trail ribbons, directional spark particles from the point of contact, localized bloom.
- **档位**：L2–L5。
- **避开**：全屏辉光盖住接触点；粒子方向随机。

## 6. 水墨武侠

- **适合**：古风、仙侠、武侠。
- **关键写法**：墨色浓淡分层，飞白，墨溅从接触点甩出，大面积留白衬托一点重墨。这个包以留白取胜，和其他包"画面要满"的倾向相反，二者不要混用。
- **English**：Chinese ink-wash painting, layered ink tones, dry-brush streaks, ink splatter flung from the point of the strike, wide empty paper around one heavy accent.
- **档位**：L2–L4。
- **避开**：霓虹色；3D 光泽。

---

## 配色：三色法

L4–L5 的冲击帧把颜色收到三种，每种负责一件事：

| 颜色 | 负责 | 写法提示 |
|---|---|---|
| **底色** | 画面大部分面积：背景、暗部、大体积 | 深而统一 |
| **亮核** | 全画最亮的一小块：接触点、刃口、能量源 | 面积越小越刺眼；速度线可以用亮核的较暗一档 |
| **强调色** | 飞出的东西：碎块、火星、血、能量碎屑 | 只给会飞的东西，不给背景 |

自查：如果强调色出现在背景里，或亮核铺满了半个画面，就是颜色在抢工作，收回去。

### 六组配色

| 名称 | 底色 | 亮核 | 强调色 | 适合 |
|---|---|---|---|---|
| 炭火 | 炭黑 `#17130F` | 暖白 `#FFF6E5` | 炉火橙 `#FF6A13` | 拳脚、巨兽、熔岩 |
| 深海 | 深海蓝 `#071A2B` | 冰白 `#EAF8FF` | 青绿 `#19D3B5` | 水系、冰系、夜战 |
| 血月 | 墨紫 `#1B0F1F` | 月白 `#F7F1FF` | 绯红 `#D7193F` | 刀剑、暗黑系 |
| 雷暴 | 铅灰蓝 `#1C2230` | 电白 `#F2F6FF` | 闪电黄 `#F5E625` | 雷电、能量 |
| 青铜 | 古铜褐 `#2A1E12` | 象牙 `#FFF8E7` | 铜绿 `#3FA58A` | 古风、仙侠 |
| 纸本 | 米白纸 `#F3EEE4`（浅底） | 纸色本身 | 朱砂 `#B8322B` ＋ 墨线 | 浅底反相、水墨 |

**浅底画面**：浅色底上，最亮处靠周围的深色衬出来；给冲击点四周留足深色，它才跳得出来。

### 对冲专用：双力配色

对冲画面是三色法的例外：底色＋左力色＋右力色＋亮核，共四色。亮核只留给相撞处：

| 左力 | 右力 | 亮核 |
|---|---|---|
| 电紫 `#8A3CFF` | 酸绿 `#B8FF3A` | 白 |
| 熔橙 `#FF6A13` | 冰青 `#4FD8FF` | 白 |
| 绯红 `#D7193F` | 金 `#F2C14E` | 暖白 |

用户坚持两股力同一色系时，先说明会难以区分，再把两股力的亮度差拉开到最大。

单色或黑白画面，不想要中间灰时，Midjourney 可在 `--no` 里放 `grey`。
