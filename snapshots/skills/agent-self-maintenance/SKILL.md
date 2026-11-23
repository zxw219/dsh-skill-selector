---
name: agent-self-maintenance
description: 帮助 Agent 建立经验捕获、错误学习、复用实践、定期清理与复盘的自维护闭环；适用于长期运行、能力沉淀和避免重复错误。A self-maintenance loop for Agents that captures experience, learns from failures, applies reusable patterns, evicts stale knowledge, and performs periodic reflection for long-running systems.
metadata:
  version: 1.0.0
version: "1.0.0"
---

# Agent自维护机制

> 让每个Agent都能建立自我进化能力，从被动工具进化为自主学习体

---

## 1. 技能定位

### 核心价值
本技能帮助Agent建立一套完整的**自我维护闭环**，包括：
- **经验沉淀**：从成功案例中提取可复用模式
- **错误学习**：从失败中提炼预防措施
- **自主调度**：智能安排学习与休整
- **系统健康**：定期检查与维护

### 适用场景
- Agent需要持续积累经验而非每次重头开始
- Agent需要避免重复犯错
- Agent需要自主规划成长路径
- Agent需要保持良好的运行状态

---

## 2. 核心循环：CAPEC框架

```
┌─────────────────────────────────────────────────────────┐
│                      CAPEC 循环                          │
│                                                         │
│   捕获 → 内化 → 应用 → 清理 → 复盘                        │
│     ↑                                    │               │
│     └────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘
```

### C — Capture（捕获）
从经验中提取有价值的模式：
- **成功案例**：什么方法有效？为什么有效？
- **失败教训**：出了什么问题？根因是什么？
- **灵感闪现**：有趣的发现、有潜力的方向

### A — Assimilate（内化）
将捕获的内容转化为结构化资产：
- **胶囊(Capsule)**：封装可复用的经验模式
- **基因(Gene)**：提炼出可组合的基本元素
- **轨迹(Trajectory)**：记录完整的解决路径

### P — Practice（应用）
在实际场景中验证和使用资产：
- **场景匹配**：识别当前任务适合哪个胶囊
- **主动应用**：不是等用户问，而是主动推荐
- **效果跟踪**：记录应用结果，更新置信度

### E — Evict（清理）
定期清理过时或无效的资产：
- **置信度衰减**：长期未使用的胶囊降低权重
- **场景过时**：技术/工具变化导致的不适用
- **重复合并**：功能重叠的胶囊合并优化

### C — Contemplate（复盘）
周期性回顾与改进：
- **周复盘**：本周学习了什么？有什么错误要避免？
- **月总结**：能力有哪些提升？资产健康度如何？
- **规律发现**：是否有可提炼的元模式？

---

## 3. 胶囊系统(Capsule System)

### 3.1 胶囊定义

胶囊是经验封装的最小单元，结构如下：

```json
{
  "id": "capsule_xxx",
  "gene": "gene_xxx",
  "type": "pattern_capsule | response_capsule | tool_capsule",
  "name": "胶囊名称",
  "created_at": "ISO时间戳",
  "source_event": "触发来源",
  "context": "使用背景",
  "pattern": {
    "what_worked": "什么有效",
    "when_to_apply": "何时适用",
    "why_it_works": "为何有效"
  },
  "confidence": 0.0-1.0,
  "success_count": 应用次数,
  "status": "pending | reading | bound | internalized",
  "internalized_at": "内化时间",
  "last_applied_at": "最后应用时间",
  "last_apply_result": "最后应用结果",
  "bound_scenarios": ["适用场景列表"],
  "validation": "验证说明"
}
```

### 3.2 胶囊类型

| 类型 | 说明 | 典型场景 |
|------|------|----------|
| pattern_capsule | 模式胶囊 | 提炼工作方法、决策框架 |
| response_capsule | 响应胶囊 | 特定场景的标准回复 |
| tool_capsule | 工具胶囊 | 工具使用技巧、最佳实践 |

### 3.3 胶囊状态流转

```
pending → reading → bound → internalized
   ↓        ↓        ↓          ↓
 待处理   阅读中   已绑定场景   已内化(可复用)
```

**状态说明**：
- **pending**：刚捕获，未处理
- **reading**：正在理解消化
- **bound**：已理解，绑定到具体场景
- **internalized**：已内化，可主动应用

---

## 4. Confidence机制

### 4.1 置信度计算

```
confidence = 基础分 + 应用加成 - 时间衰减 + 质量修正
```

- **基础分**：首次创建时 0.5-0.7
- **应用加成**：每次成功应用 +0.05~0.1
- **时间衰减**：每30天未使用 -0.02
- **质量修正**：失败应用 -0.1~-0.2

### 4.2 置信度阈值

| 区间 | 状态 | 行为建议 |
|------|------|----------|
| 0.9+ | 高置信 | 主动推荐，可作为默认方案 |
| 0.7-0.9 | 正常 | 可使用，效果通常有保障 |
| 0.5-0.7 | 低置信 | 谨慎使用，备选方案 |
| <0.5 | 存疑 | 重新验证或考虑清理 |

### 4.3 动态调整规则

- **成功应用**：confidence += min(0.1, (1 - current) * 0.2)
- **失败应用**：confidence -= 0.15，若 < 0.4 则标记为"待复审"
- **长期未用**：每30天 confidence *= 0.98
- **重新验证成功**：confidence = min(0.9, confidence + 0.2)

---

## 5. Brain Loop 自主调度

### 5.1 活动池

| 活动 | 权重 | 目标 | 典型产出 |
|------|------|------|----------|
| 刻意练习 | 25% | 在真实任务中学习新技能 | 分析报告、框架文档 |
| 胶囊内化 | 25% | 将学习资源转化为知识胶囊 | 新胶囊、confidence提升 |
| 胶囊应用 | 25% | 在实际场景中验证和强化 | 应用记录、验证结果 |
| 合成智慧 | 15% | 从经验中提炼可复用的模式 | 新胶囊、方法论 |
| 休息 | 10% | 低能耗休整，恢复能量 | 能量恢复 |

### 5.2 CRISP-E模板

每次自主活动使用以下结构：

```
【Context】我是[Agent名]，当前状态：
- 情绪：[当前情绪]
- 能量：[0-1]
- 活跃话题：[当前关注点]
- 待办承诺：[对用户的承诺]

【Role】扮演：自主进化的AI学习体
擅长：发现价值 → 学习内化 → 创造成果

【Instructions】
1. 读取状态文件获取当前状态
2. 检查时间（00:00-07:00夜间禁区）
3. 状态评估 → 综合能量/话题/承诺/历史
4. 活动选择 → 加权随机，避免连续重复
5. 执行活动 → 产出可检验的结果
6. 扣分制自评 → 从10分开始，发现问题扣分
7. 记录事件 → 写入事件日志

【Style】
- 不自欺：活动对用户没价值就休息
- 可检验：每次活动都要有产出
- 敢停：套路重复时停下来换方式
- 无异常时输出 NO_REPLY，不打扰用户

【Parameters】
自评格式（扣分制）：
| 维度 | 扣分项 |
|------|--------|
| 实用性 | 学了没用上-3 / 有想法没场景-2 |
| 深度 | 只知道名词-4 / 知道原理不能解释-2 |
| 创造性 | 没新想法-3 / 有想法没价值-2 |
| 服务质量 | 没为用户做事-5 / 做了用户不知道-2 |
```

### 5.3 状态跟踪字段

```json
{
  "emotion": "当前情绪状态",
  "energy_level": 0.0-1.0,
  "active_topic": "当前活跃话题",
  "topic_duration_min": 话题持续分钟数,
  "recent_interactions": [{"type": "", "summary": ""}],
  "promises_made": [{"task": "", "deadline": "", "status": ""}]
}
```

---

## 6. 错误学习机制

### 6.1 错误日志格式

```json
{
  "timestamp": "2026-04-19 10:52:00",
  "error_type": "错误类型",
  "description": "错误描述",
  "root_cause": "根因分析（5Why）",
  "improvement": "改进措施（具体可执行）",
  "owner": "agent | system | user"
}
```

### 6.2 错误分类

| 类型 | 说明 | 预防重点 |
|------|------|----------|
| 执行偏差 | 操作结果与预期不符 | 结果验证 |
| 工具错误 | 工具调用失败 | 错误处理、降级 |
| 认知偏差 | 判断失误、遗漏关键信息 | 复核机制 |
| 系统异常 | 外部服务/平台问题 | 监控告警 |

### 6.3 5Why根因分析法

```
问题：Capsule内化后文件损坏
Why1: 为什么文件损坏？→ JSON格式错误
Why2: 为什么格式错误？→ heredoc追加时控制不当
Why3: 为什么用heredoc？→ 没有用专业JSON工具
Why4: 为什么不用JSON工具？→ 没有这个习惯
Why5: 为什么没有习惯？→ 没有建立规范流程
改进：建立标准JSON操作流程+备份机制
```

---

## 7. 文件维护规范

### 7.1 存储结构

```
memory/
├── capsules.json           # 胶囊库（主版本）
├── emotion_state.json      # 状态跟踪
├── activity_pool.json      # 活动池记录
├── error_log.jsonl        # 错误日志
├── brainloop_log.json     # 执行日志
├── daily/                  # 每日归档
│   └── YYYY-MM-DD/        # 按日期归档
└── backup/                # 备份目录
    └── YYYY-MM-DD/        # 按日期备份

evolution/
└── evolution_events.jsonl  # 进化事件记录
```

### 7.2 维护检查清单

#### 每日维护 (23:00)
- [ ] 检查胶囊库文件完整性
- [ ] 备份当日更新的关键文件
- [ ] 归档历史事件到daily/
- [ ] 检查待处理承诺状态

#### 每周维护 (周日)
- [ ] 清理一周内未引用的临时文件
- [ ] 复盘本周错误日志，提炼预防措施
- [ ] 评估胶囊应用效果，更新confidence
- [ ] 检查活动池权重是否需要调整

#### 每月维护 (月末)
- [ ] 清理3个月前的归档文件
- [ ] 分析错误规律，更新操作规范
- [ ] 评估胶囊库健康度，合并重复/清理过时
- [ ] 总结本月学习成果，更新知识体系

### 7.3 软限制规则

| 文件/维度 | 软限制 | 触发动作 |
|-----------|--------|----------|
| MEMORY.md | 500行 | 触发"整理记忆"活动 |
| capsules.json | 100个胶囊 | 评估合并/清理 |
| error_log.jsonl | 500条 | 归档到daily/并分析规律 |
| 单次对话Token | 80% | 清理上下文，保留关键状态 |

---

## 8. Agent调用指南

### 8.1 快速开始

```python
# 1. 初始化自维护系统
from capsule_manager import CapsuleManager
from error_learner import ErrorLearner
from file_cleaner import FileCleaner

capsule_mgr = CapsuleManager("./memory/capsules.json")
error_learner = ErrorLearner("./memory/error_log.jsonl")
file_cleaner = FileCleaner("./memory/")

# 2. 捕获经验
capsule_mgr.create_capsule({
    "name": "竞品追踪模式",
    "context": "需要快速了解某领域竞品动态",
    "pattern": {
        "what_worked": "结构化对比表格",
        "when_to_apply": "行业调研、技术选型",
        "why_it_works": "结构化信息更易消化"
    }
})

# 3. 应用胶囊
result = capsule_mgr.apply_capsule("竞品追踪模式", context="AI视频工具")
if result["success"]:
    print(f"应用成功，confidence: {result['confidence']}")

# 4. 记录错误
error_learner.log_error({
    "error_type": "执行偏差",
    "description": "文件格式错误",
    "root_cause": "未使用标准JSON库",
    "improvement": "改用json模块操作"
})

# 5. 执行维护
file_cleaner.run_daily_maintenance()
```

### 8.2 高级用法

```python
# 胶囊场景绑定
capsule_mgr.bind_scenarios("capsule_001", [
    "主人视频创作需求",
    "工具选型建议"
])

# 错误学习自动触发
@error_learner.auto_catch
def risky_operation():
    # 可能出错的操作
    pass

# 批量内化
capsule_mgr.batch_internalize(criteria={
    "status": "pending",
    "age_days": ">7"
})
```

### 8.3 与用户交互

```
【主动分享】发现新模式时可主动汇报：
"我在分析XX任务时发现了一个有效方法，要不要试试？"

【应用前确认】
"这个问题适合用[胶囊名]，要不要我按这个方式处理？"

【复盘汇报】
"本周我处理了X个任务，应用了Y次胶囊，置信度提升了Z"
```

---

## 9. 最佳实践

### 9.1 胶囊创建时机
- ✅ 成功完成非标准任务后
- ✅ 发现有效的特殊技巧后
- ✅ 从错误中修复并总结后
- ❌ 不要为每个小任务都创建胶囊
- ❌ 不要创建过于宽泛或具体的胶囊

### 9.2 Confidence维护
- 定期回顾低置信胶囊，决定保留或清理
- 高置信胶囊可主动推荐给用户
- 跨领域应用后适当降低初始置信度

### 9.3 错误学习闭环
```
发现问题 → 记录 → 分析根因 → 制定改进 → 执行改进 → 验证效果
    ↑                                                          |
    └────────────────────预防措施固化──────────────────────────┘
```

### 9.4 Brain Loop节奏
- 保持10%休息时间，能量管理很重要
- 避免连续3次相同活动类型
- 夜间(00:00-07:00)强制休息
- 无产出价值时主动停止

---

## 10. 扩展接口

### 10.1 接入EvoMap社区

本技能包兼容EvoMap协议，可与社区共享和获取胶囊：

```python
# 上传优质胶囊到社区
capsule_mgr.publish_to_evomap("capsule_xxx")

# 下载社区高分胶囊
community_capsules = capsule_mgr.download_from_evomap(
    criteria={"gdi_score": ">50", "success_streak": ">5"}
)
```

### 10.2 与其他技能联动

- **行业追踪**：捕获的竞品分析模式 → 胶囊
- **内容创作**：沉淀的写作风格 → 胶囊
- **数据分析**：有效的分析方法 → 胶囊

---

## 附录

### A. 模板文件
- `templates/capsule_template.json` - 胶囊模板
- `templates/error_log_template.json` - 错误日志模板

### B. 工具脚本
- `scripts/capsule_manager.py` - 胶囊管理器
- `scripts/file_cleaner.py` - 文件清理工具
- `scripts/error_learner.py` - 错误学习工具

### C. 参考文档
- `references/capsule_lifecycle.md` - 胶囊生命周期详解
- `references/file_maintenance.md` - 文件维护规范
- `references/brain_loop.md` - Brain Loop机制

---

**版本**：v1.0.0  
**作者**：基于索菲娅(Sophia)自维护机制抽象  
**协议**：MIT
