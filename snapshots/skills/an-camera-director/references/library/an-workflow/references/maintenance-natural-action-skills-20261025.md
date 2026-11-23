# 2026-10-25 自然动作、技能与震撼效果维护

用户要求维护 `An工作流.zip` 对应的工作流源文件。实际诊断、来源阅读和负责层修改见[学习与反思](learning-full-body-skills-20261025.md)；用户没有要求在本轮创作战斗提示词或生成视频。

## 附件与修改

修改前ZIP、已安装来源和D盘分发的520个来源文件哈希全部一致，ZIP有5298项，路径、CRC及载荷清单核查无错误。完整旧ZIP和来源快照保留在本轮工作区 `战斗工作流优化_20261025/before/`；[附件审计](../assets/validation/natural-action-skills-20261025/attachment-audit.json)保留旧包SHA-256。

实际写回主入口、设计系统、默认契约、战斗体验、能力画面、特效语法、密度与镜头语法、采用路由、终检和功能映射；同步修改动作专项的入口/翻腾/模块库，以及特效、场面专项入口。保留动作库、原题材/模板与职责边界。早轮计数及船战固定案例保留在历史记录中，不再作为现行采用规则。

## 实际独立文本验证

[试用任务与维度](../assets/validation/natural-action-skills-20261025/evaluation-plan.md)在主代理读取任何试用正文前冻结。创作者各自只得到原始新任务、相应技能与按需参考，不得知诊断、修改方案、其他稿或预期优胜者。旧版使用修改前ZIP内来源；新版使用本轮已安装来源。没有用回信教会同一案例再称自主采用。

- 同题30秒水车栈道：[旧版原稿](../assets/validation/natural-action-skills-20261025/baseline.md)、[新版原稿](../assets/validation/natural-action-skills-20261025/revised.md)，原始哈希见[冻结记录](../assets/validation/natural-action-skills-20261025/trial-original-hashes.json)。两稿匿名为[P](../assets/validation/natural-action-skills-20261025/P.md)/[Q](../assets/validation/natural-action-skills-20261025/Q.md)，[映射](../assets/validation/natural-action-skills-20261025/anonymization-map.json)未交给审阅者；完整结论见[匿名审阅](../assets/validation/natural-action-skills-20261025/pair-review.md)。
- 新任务迁移：[18秒塔楼单股持续风](../assets/validation/natural-action-skills-20261025/transfer.md)，术者最终仍受压，非能力者靠身体/双刃介入，不毁塔。审阅确认内容基本满足，完整身体/持械、持续风改变局面及主峰有证据；北侧石墩止滑前的侧向位置交代仍有可读性风险，未认定为必然空间矛盾。
- 相邻边界：[12秒固定机位一镜到底、只改摄影](../assets/validation/natural-action-skills-20261025/boundary.md)。独立审阅判满足，未擅加招式、能力、胜负或换镜，保留剑上角力。
- 后两项[原始审阅全文](../assets/validation/natural-action-skills-20261025/transfer-review.md)保留。审阅者未读An模板，提出“若分栏指左右表格则缺项”的条件式意见；主代理回核现行模板本就使用画面/S/fx-env/sound/transition分项，因此未把“无左右表格”认作已证格式错，也未为该意见改用户格式。

匿名对照的两稿都具备实质身体链、能力改局和带负载的主峰；不能由这一对样本宣称新版全面胜出或旧版必然失败。新版原稿可定位侧翻、滚出、低扫、旋身回切、跃隙及霜脉/风压的多次用途，证明该次文本出现了所需内容；不等于稳定采用率或成片质量。审阅记录中的局部路径/站位风险保留，不把可推定关系包装成全部已验证。

另外进行[来源语义独立复查](../assets/validation/natural-action-skills-20261025/source-review.md)：原先四类根因已实质修正，未见新职责扩张；仍发现瞬发承接和默认事件流的S栏目两处口径问题，主代理已定向回修。此两项记为独立发现、作者修复，没有冒称另一次独立全审。创作者读取与末次来源整理处于同轮，不能把未单独试用的小修登记为独立行为通过。

## 文件验证与交付依据

隔离分发首次构建通过：11个来源技能、12个功能技能、23个入口，20170个功能包内部链接、21819个总链接及章节锚点，13个独立ZIP内容核验。末次证据和来源整理后，正式分发仍须由同步脚本重建并复核；最终文件数/哈希以D盘 `package-manifest.json`、`sync-state.json`、`validation.json` 与工作区 `release-verification.json` 为准，不把本段旧统计当最终清单。

标准 `quick_validate.py` 已尝试，但当前Python缺PyYAML而未能启动；未声称该脚本成功，未为此安装依赖。实际使用本项目标准库打包器完成入口/frontmatter、闭包、链接锚点、ZIP及发布哈希检查。

文件结构、作者语义复核、独立文本与真实视频四层分开。本轮未生成视频，未正常速度观看/试听新成片；没有逐帧原样本，不虚报消除实际动画脚滑、运动歧义或特效执行失败。后续成片反馈仍应定位最早偏离的动作/技能/空间相位，不能把本轮文件发布或一次原稿当成免检依据。
