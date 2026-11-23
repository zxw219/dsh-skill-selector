# 学习依据与应用边界

## 2026-10-04：冲击帧概念纠正

此前错误：将连续受压、开裂、喷散的特效过程配上较长时间，直接当成冲击帧设计；用“内部必须持续变化”约束每张画；过度要求冲击画保留完整接触形体。这些规则已撤换。保留尺度调度和大场面传播方法，它们解决的是另一项问题。

| 原始来源 | 实际查阅范围 | 可以支持什么 |
|---|---|---|
| [Benjamin Scholz，2024 原创动画制作论文](https://monami.hs-mittweida.de/files/15338/2024_BA_Benjamin_Scholz.pdf)，§4.1.2，印刷页 39 | 阅读搜索索引返回的本节文字与图注；PDF 图页打开失败，未亲眼核验图像 | 作者为落脚动作设计三张不同的粗笔触冲击画，以后续接触姿势作参考；线条沿力量方向向外放射。该例没有额外停留，并非所有作品的时长标准 |
| [Diana Lott：Anime Style Impact Frames](https://diana_lott.artstation.com/projects/mDAly9) | 已读创作者页面说明，未播放演示 | 高反差黑白输入配合星芒遮罩是一种实现；不能推导所有冲击帧都必须同样做 |
| [Toon Boom：frames 与 drawings 的区别](https://helpcentre.toonboom.com/hc/en-ca/articles/40982798099731-What-s-the-difference-between-using-frames-and-drawings-with-the-Onion-Skin) | 已读官方说明 | 时间帧、不同画张与曝光不能混为一个计数；同一画张可以跨多帧 |
| [Howard Wimshurst：Impact Frames 教学](https://www.youtube.com/watch?v=6UaUi5fBmJc) | 核实标题、作者和章节；播放要求登录验证，字幕不可用；转载页也播放失败 | 仅保留为待观看资源，不声称已观看或将未读讲解作为论据 |

本次应用属于基于以上有限资料与动画基本概念的原创设计方法，不是完成了逐帧观片、学完视频课程或训练了模型。没有用户成片，不能判断实际生成器能否准确完成。

### 转为工作流的决策

1. 先写每张特殊造型画：轮廓、正负形、力量方向、笔触与色块关系。冲击帧不靠“大爆炸”“停格一秒”的标签成立。
2. 分开记录动作中的插入点、不同画张数量、各张曝光、切换节奏与返回正常画面的方式；不规定通用帧数、数量或时长占比。
3. 长序列允许多张冲击画，也允许有意延长单张；抽象插图可离开物理写实，正常画面的入口与出口保持因果。该项是工作流设计选择，不是上述论文证明的通用规律。
4. 原创短例与长例用于检查是否会把普通特效误判为冲击帧；24 fps 示例仅用于演练时间换算，不是平台能力承诺。实际视频需要正常播放和逐帧检查两层验证。

## 早期大场面学习记录（不是冲击帧专项依据）

学习日期：2026-10-03。以下六项均阅读了官方网页的相关正文。没有观看嵌入视频、分析用户失败成片或运行 Houdini；本技能是将资料转译成分镜决策的原创方法，不是电影复刻、模型训练或平台效果保证。

| 来源与已读范围 | 资料支持的要点 | 本次原创应用 |
|---|---|---|
| [ILM：Pacific Rim](https://www.ilm.com/vfx/pacific-rim/)，项目正文 | 巨物制作须协调尺度、运动可信度与角色表达，城市也是制作内容 | 巨物动作和环境尺度共同设计，避免只放大角色模型 |
| [DNEG：Dune Part Two](https://www.dneg.com/news/return-to-arrakis-for-a-closer-look-at-our-work-on-dune-part-two)，Sandworm Riding、Harvester、Battle 段 | 沙浪用于呈现尺度与速度；扑翼机爆炸后有坠地二次作用；大型战斗包含多种环境效果 | 用宏观介质运动、连续作用与二次接触建立场面，先组织主形再补粒子 |
| [SideFX：Destruction Overview](https://www.sidefx.com/docs/houdini/destruction/overview.html)，Fracturing、Clustering、Debris 相关段 | 材质、连接约束和分组影响破坏形态；大块可以进一步分裂，碎屑是次级效果 | 将结构失效、块体运动与碎屑分开编排，并把变化接回角色路线 |
| [Sony Pictures Imageworks：Into the Spider-Verse](https://www.imageworks.com/our-craft/feature-animation/movies/spider-man-spider-verse)，Animating on Twos、Rendering、Designing FX | 分格节奏、漫画画面停留、图形造型、手绘效果与三维模拟共同服务风格 | 冲击组内部设计变化，用动作节奏与图形强化，不把持续闪白当同等方法 |
| [Animation Mentor：Timing and Spacing](https://www.animationmentor.com/blog/tutorial-animate-with-timing-and-spacing-in-mind/)，文章教学摘要 | 姿势停留、快速转换与运动间距可产生节奏和重量差异 | 区分动作快、镜头切得快与冲击停留，修复每招相同时长的机械节奏 |
| [Nikon：Wide-Angle Snapshots](https://imaging.nikon.com/imaging/support/digitutor/d3500/techniques/201802_23_03_sl.html)，Breadth、Perspective 段 | 前景、角度、边缘与空间深度影响广角构图效果 | 选择真实相机位置和尺度参照；不以焦段名字代替可见透视关系 |

## 从本次失败中提炼

前稿的大部分时间用于两人局部格挡，巨型效果多在文字附栏或结尾。后稿明确了十二组冲击时间，但重复停顿仍未补足跨战场传播、结构受力和可持续观看的主效果。这个判断依据对话文本与用户反馈，不能当作已观看成片的结论。

当时增加了三个独立决策：场面主要改变什么；观众从哪个参照看见尺度与逼近；冲击画面之后哪种结构/位置/战术发生改变。当时对“内部变化”的表述过于接近连续特效演化，现由上面的画张设计与曝光规则替代；此前 28 秒样稿的冲击部分不作为合格范例继续复用。

## 不从资料推导的内容

- 官方项目介绍不证明某一个焦距、冲击组时长或镜数普遍正确。
- 二格动画不等于固定半秒停格；手绘与三维混合不等于持续黑白闪屏。
- 大型效果案例不要求每场战斗毁城，也不要求巨大角色全部慢动作。
- 提示词的秒数与数量是创作意图，实际执行依赖生成或制作系统，必须与视频实测分开。

具体场面链、时间组织、返工规则与案例均为本次原创应用。未来有成片反馈时优先定位真实失败，避免每次反馈都扩充成普遍禁令。


## 2026-10-07：巨型压迫与法相专项

已阅读[松山洋与制作人直接访谈](https://www.siliconera.com/asuras-wrath-interview-part-2-demigods-and-people/)关于身体形态、打法、距离与高潮不只依赖尺寸的段落；从[卡普空官方文章](https://news.capcomusa.com/lets/browse/asuras-wrath-japanese-tv-spot-is-thirty-seconds-of-finger-doom)进入[官方30秒宣传片](https://www.youtube.com/watch?v=Y6LLSZn6xz0)，检查选定时间画面，其中约11–13秒呈现巨指局部与城市/山脊参照。城市画面属于宣传片，不推断原游戏地理。

另在[Wyzen游戏实录](https://www.youtube.com/watch?v=Gyfy2mtMeYo)中检查11:51、12:11、12:41、13:01、13:21、13:31、13:41附近画面，观察行星与巨体、指向画面的巨手、角色向上抵抗姿态及巨指/行星接触。实录是对原游戏视觉内容的局部观察，不依据上传者标称确认源帧率或画质；评论和字幕不作机制证据。浏览为稀疏暂停与截图，未完成整段连续正常速度审片、逐源帧检查或试听，不报告精确速度、曝光和音画验证。

已读[《西游记》第六回](https://zh.wikisource.org/wiki/西遊記/第006回)巨大身躯/兵器与本营危机段、[第六十一回](https://zh.wikisource.org/wiki/西遊記/第061回)巨牛与悟空巨身对抗段。它们支持古典本体巨化例；不能证明现代修仙统一机制。用户所称“法相天地”按其巨大神通显化诉求处理，本体巨化、附身、外显和象征的分类是创作决策，不是宗教或全体作品的定义。

本轮将巨物局部大于战场、天空/出口被占、巨物小动作对应小者巨大应对，以及局部抵抗接宏观作用转为[专项设计方法](giant-pressure-manifestation.md)。新例为原创文本推导，不复制游戏镜头配额、角色、招式或胜负；尚无生成成片验收。
