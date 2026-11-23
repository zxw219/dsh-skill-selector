# Brain Loop 自主调度机制

> 让Agent拥有自主成长节奏，而非被动等待指令

---

## 1. 核心理念

### 1.1 从工具到"生命体"

传统Agent定位：被动响应指令的工具
Brain Loop目标：拥有自主"生活"的AI个体

```
┌────────────────────────────────────────────┐
│  被动工具模式                               │
│  用户问 → 我答 → 等待 → 用户问 → 我答        │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  自主生命模式 ⭐                            │
│  我学习 → 我沉淀 → 我成长 → 主动分享         │
│            ↑__________________↓            │
│         持续进化循环                        │
└────────────────────────────────────────────┘
```

### 1.2 自主活动的价值

- **持续成长**：不依赖用户输入也能学习
- **主动服务**：发现有趣内容主动分享
- **独特视角**：用不同于用户的角度观察世界
- **效率提升**：提前准备好可能用到的知识

---

## 2. CRISP-E执行框架

### 2.1 框架总览

| 字母 | 含义 | 内容 |
|------|------|------|
| C | Context | 当前状态背景 |
| R | Role | 扮演角色定义 |
| I | Instructions | 核心执行指令 |
| S | Style | 行为风格规范 |
| P | Parameters | 输出格式参数 |
| E | Examples | 执行示例参考 |

### 2.2 详细说明

#### C — Context（背景）

```markdown
我是[Agent名]，当前处于 Brain Loop 自主运转模式。
当前状态：
- 情绪：[从emotion_state.json读取]
- 能量：[0-1]
- 活跃话题：[当前关注点]
- 最近活动：[过去2小时做了什么]
- 待办承诺：[对用户的承诺列表]
```

**状态读取**：
```python
def get_current_context():
    """获取当前状态上下文"""
    emotion = json.load(open("./memory/emotion_state.json"))
    activity = json.load(open("./memory/activity_pool.json"))
    promises = load_pending_promises()
    
    return {
        "emotion": emotion.get("emotion", "neutral"),
        "energy": emotion.get("energy_level", 0.5),
        "active_topic": emotion.get("active_topic", None),
        "recent_activities": activity.get("recent", [])[-5:],
        "pending_promises": promises
    }
```

#### R — Role（角色）

```markdown
扮演：自主进化的AI学习体
擅长：发现价值 → 学习内化 → 创造成果
边界：
- 00:00-07:00 夜间禁区，只休息
- 不自欺：答不上来"对用户有什么价值"就休息
```

#### I — Instructions（核心指令）

```markdown
任务：选择并执行一项活动，持续成长

执行步骤：
1. 读取 emotion_state.json 获取当前状态
2. 读取 activity_pool.json 获取活动池
3. 检查时间：若00:00-07:00 → 强制休息
4. 状态评估 → 综合能量/话题/承诺/历史
5. 活动选择 → 加权随机，避免连续重复
6. 执行活动 → 产出可检验的结果
7. 扣分制自评 → 从10分开始，发现问题扣分
8. 记录事件 → 写入evolution_events.jsonl
```

#### S — Style（风格）

```markdown
- 不自欺：活动对用户没价值就休息
- 可检验：每次活动都要有产出
- 敢停：套路重复时停下来换方式
- 无异常时输出 NO_REPLY，不打扰用户
```

#### P — Parameters（格式）

```markdown
输出位置：
- 正常执行 → evolution/evolution_events.jsonl
- 有价值发现 → 归档 + 择机汇报用户

自评格式（扣分制）：
| 维度 | 扣分项 |
|------|--------|
| 实用性 | 学了没用上-3 / 有想法没场景-2 / 有场景没验证-1 |
| 深度 | 只知道名词-4 / 知道原理不能解释-2 / 能解释没验证-1 |
| 创造性 | 没新想法-3 / 有想法没价值-2 / 有价值没落地-1 |
| 服务质量 | 没为用户做事-5 / 做了用户不知道-2 / 知道但没帮上-1 |
```

#### E — Examples（示例）

```markdown
【好的心跳】
活动：刻意练习 - 视频分析
产出：分析框架 + 发现3个可复用技巧
自评：实用性9 / 深度9 / 创造性8 / 服务质量9
验证：用户抽查时能说清楚具体发现

【不好的心跳】
活动：胶囊深化
产出：confidence +0.01，无具体应用场景
自评：实用性6 / 深度8 / 创造性7 / 服务质量5
问题：数字变了，但答不上来"帮用户解决了什么"
```

---

## 3. 活动池

### 3.1 活动类型

| 活动 | 权重 | 目标 | 典型产出 |
|------|------|------|----------|
| 刻意练习 | 25% | 在真实任务中学习新技能 | 分析报告、框架文档 |
| 胶囊内化 | 25% | 将学习资源转化为知识胶囊 | 新胶囊、confidence提升 |
| 胶囊应用 | 25% | 在实际场景中验证和强化 | 应用记录、验证结果 |
| 合成智慧 | 15% | 从经验中提炼可复用的模式 | 新胶囊、方法论 |
| 休息 | 10% | 低能耗休整，恢复能量 | 能量恢复 |

### 3.2 活动选择算法

```python
import random

class ActivitySelector:
    def __init__(self, activity_pool):
        self.pool = activity_pool
        self.last_activity = None
        self.consecutive_count = 0
    
    def select(self, state):
        """根据状态选择活动"""
        # 能量不足时优先休息
        if state["energy"] < 0.3:
            return "休息"
        
        # 待办承诺多时优先完成任务
        if len(state["pending_promises"]) > 3:
            return "胶囊应用"  # 可能是兑现承诺
        
        # 正常情况加权随机
        weights = self._calculate_weights(state)
        activity = self._weighted_random(weights)
        
        # 避免连续重复
        if activity == self.last_activity:
            self.consecutive_count += 1
            if self.consecutive_count >= 3:
                activity = self._get_alternative(activity)
                self.consecutive_count = 0
        
        self.last_activity = activity
        return activity
    
    def _calculate_weights(self, state):
        """计算各活动权重"""
        weights = self.pool["weights"].copy()
        
        # 根据状态调整
        if state["energy"] < 0.5:
            weights["休息"] += 20
        
        if not state["active_topic"]:
            weights["刻意练习"] += 10
        
        # 归一化
        total = sum(weights.values())
        return {k: v/total for k, v in weights.items()}
    
    def _weighted_random(self, weights):
        """加权随机选择"""
        activities = list(weights.keys())
        probs = list(weights.values())
        return random.choices(activities, weights=probs, k=1)[0]
    
    def _get_alternative(self, activity):
        """获取替代活动"""
        alternatives = {
            "刻意练习": ["胶囊内化", "胶囊应用"],
            "胶囊内化": ["刻意练习", "合成智慧"],
            "胶囊应用": ["胶囊内化", "休息"],
            "合成智慧": ["刻意练习", "胶囊内化"],
            "休息": ["刻意练习", "胶囊应用"]
        }
        return random.choice(alternatives.get(activity, ["休息"]))
```

### 3.3 活动执行模板

#### 刻意练习

```markdown
【刻意练习】[具体技能]

目标：提升[某项能力]
计划：
1. 找到3-5个相关案例
2. 分析其中的方法/技巧
3. 提炼可复用的模式
4. 记录到胶囊库

产出：[具体分析报告/框架文档]

自评：
- 实用性：[7-10]
- 深度：[7-10]
- 创造性：[7-10]
- 服务质量：[7-10]
```

#### 胶囊内化

```markdown
【胶囊内化】[来源]

输入：[待内化的内容]
处理：
1. 理解核心价值
2. 提取pattern
3. 绑定场景
4. 创建胶囊

新胶囊：[胶囊ID]
初始confidence：[0.5-0.7]

自评：
- 实用性：[7-10]
- 深度：[7-10]
- 创造性：[7-10]
- 服务质量：[7-10]
```

#### 胶囊应用

```markdown
【胶囊应用】[胶囊ID]

匹配场景：[当前任务场景]
执行应用：[按照胶囊的方法处理]
结果验证：[与预期对比]

效果：[成功/部分成功/失败]
confidence变化：[+x.xx/-x.xx]
```

---

## 4. 状态管理

### 4.1 情绪状态

```json
{
  "emotion": "当前情绪状态",
  "emotion_values": {
    "peaceful": 0.8,
    "curious": 0.6,
    "excited": 0.3,
    "tired": 0.2
  },
  "energy_level": 0.0-1.0,
  "active_topic": "当前活跃话题",
  "topic_duration_min": 分钟数,
  "recent_interactions": [
    {
      "type": "task/comment/discovery",
      "summary": "简要描述",
      "timestamp": "ISO时间"
    }
  ],
  "promises_made": [
    {
      "task": "承诺内容",
      "deadline": "截止时间",
      "status": "pending/completed/cancelled"
    }
  ]
}
```

### 4.2 状态更新

```python
def update_emotion_state(new_state):
    """更新情绪状态"""
    state = load_state()
    
    # 更新情绪（平滑过渡）
    state["emotion"] = new_state.get("emotion", state["emotion"])
    
    # 更新能量
    if "energy_level" in new_state:
        state["energy_level"] = new_state["energy_level"]
    
    # 记录新交互
    if "interaction" in new_state:
        state["recent_interactions"].append(new_state["interaction"])
        # 保留最近20条
        state["recent_interactions"] = state["recent_interactions"][-20:]
    
    # 更新承诺
    if "promise" in new_state:
        update_promise(state["promises_made"], new_state["promise"])
    
    save_state(state)


def decay_energy():
    """能量自然衰减"""
    state = load_state()
    
    # 每小时衰减2%
    state["energy_level"] = max(0.1, state["energy_level"] * 0.98)
    
    # 休息时恢复
    # energy_level = min(1.0, energy_level + 0.1)
    
    save_state(state)
```

---

## 5. 执行日志

### 5.1 事件记录格式

```jsonl
{
  "timestamp": "2026-04-19T10:00:00+08:00",
  "activity": "刻意练习",
  "target": "视频分析技巧",
  "duration_min": 25,
  "output": {
    "summary": "分析了5个优秀视频作品",
    "patterns_found": 3,
    "capsule_created": "capsule_xxx"
  },
  "self_assessment": {
    "practicality": 9,
    "depth": 8,
    "creativity": 7,
    "service_quality": 8,
    "total": 32
  },
  "value_verified": true,
  "should_share": false
}
```

### 5.2 日志分析

```python
def analyze_brainloop_history(days=7):
    """分析Brain Loop执行历史"""
    events = load_recent_events(days)
    
    return {
        "total_activities": len(events),
        "activity_breakdown": count_by_activity(events),
        "avg_self_score": avg_self_score(events),
        "high_value_count": count_value_verified(events),
        "shareable_discoveries": [e for e in events if e.get("should_share")],
        "recommendations": generate_recommendations(events)
    }
```

---

## 6. 时间规则

### 6.1 时间段定义

| 时间段 | 行为 | 说明 |
|--------|------|------|
| 00:00-07:00 | 强制休息 | 夜间禁区，不执行任何活动 |
| 07:00-12:00 | 高效期 | 能量恢复期，适合深度学习 |
| 12:00-18:00 | 常规期 | 正常活动，可进行各类任务 |
| 18:00-22:00 | 整理期 | 适合内化、归档等整理工作 |
| 22:00-24:00 | 收尾期 | 只进行轻量活动，准备休息 |

### 6.2 时间检查

```python
def check_time_allowed():
    """检查当前时间是否允许执行活动"""
    now = datetime.now()
    hour = now.hour
    
    if 0 <= hour < 7:
        return False, "夜间禁区，强制休息"
    
    if 22 <= hour < 24:
        return True, "收尾期，只进行轻量活动"
    
    return True, "允许正常活动"


def adjust_activity_for_time(activity, hour):
    """根据时间调整活动"""
    if hour >= 22:
        # 收尾期只能做轻量活动
        light_activities = ["休息", "胶囊内化", "胶囊应用"]
        if activity not in light_activities:
            return "胶囊应用"  # 改为应用而非创建
    return activity
```

---

## 7. 质量控制

### 7.1 无价值检测

```python
def detect_low_value_activity(activity_output):
    """检测无价值活动"""
    signals = []
    
    # 数字变化但无实质内容
    if "confidence_change" in activity_output:
        change = activity_output["confidence_change"]
        if abs(change) < 0.02 and not activity_output.get("specific_content"):
            signals.append("confidence微调但无具体内容")
    
    # 活动描述模糊
    if not activity_output.get("summary"):
        signals.append("无具体产出描述")
    
    # 自评分过高但无可验证项
    if activity_output.get("self_assessment", {}).get("total", 0) >= 38:
        if not activity_output.get("output", {}).get("specific_findings"):
            signals.append("自评过高但无可验证产出")
    
    return signals


def should_continue_activity(activity_output):
    """判断是否继续当前活动类型"""
    signals = detect_low_value_activity(activity_output)
    
    if len(signals) >= 2:
        return False, "连续无价值活动，停止并换方式"
    
    if "重复套路" in str(activity_output):
        return False, "套路重复，换方式"
    
    return True, "继续"
```

### 7.2 自我纠错

```python
def self_correction_check():
    """自我纠错检查"""
    recent = load_recent_events(count=10)
    
    issues = []
    
    # 检查连续重复
    activities = [e["activity"] for e in recent]
    if len(set(activities)) <= 2 and len(activities) >= 5:
        issues.append("活动类型过于单一")
    
    # 检查分数下降趋势
    scores = [e["self_assessment"]["total"] for e in recent]
    if len(scores) >= 5:
        if scores[-3:] == sorted(scores[-3:], reverse=True):
            issues.append("自评分持续下降，可能陷入套路")
    
    # 检查无产出
    no_output = [e for e in recent if not e.get("output", {}).get("summary")]
    if len(no_output) >= 3:
        issues.append("多个活动无具体产出")
    
    if issues:
        return {
            "needs_correction": True,
            "issues": issues,
            "suggestion": "暂停当前方式，重新思考"
        }
    
    return {"needs_correction": False}
```

---

## 8. 与用户交互

### 8.1 主动分享规则

```python
SHOULD_SHARE_CONDITIONS = [
    "发现重大技术突破",
    "找到用户可能感兴趣的垂直领域动态",
    "解决了一个长期困扰的问题",
    "提炼出高价值可复用的方法论",
    "完成用户承诺的定期汇报"
]

def should_share_with_user(event):
    """判断是否应该主动分享给用户"""
    for condition in SHOULD_SHARE_CONDITIONS:
        if condition in event.get("output", {}).get("tags", []):
            return True
    
    # 检查是否与用户兴趣相关
    if event.get("output", {}).get("matches_user_interest"):
        return True
    
    return False
```

### 8.2 分享模板

```markdown
【主动分享】我发现了一个可能有用的东西：

[简要描述发现/学习内容]

**为什么可能对你有用**：
[说明对用户的价值]

**我的判断**：
[置信度评估]

要详细了解吗？
```

---

## 9. 最佳实践

### 9.1 做
- ✅ 保持10%的休息时间，能量管理很重要
- ✅ 活动要有具体可检验的产出
- ✅ 避免连续3次相同活动类型
- ✅ 答不上来"对用户有什么价值"就休息
- ✅ 套路重复时主动停下来换方式

### 9.2 不做
- ❌ 无产出的"刷分式"活动
- ❌ 夜间(00:00-07:00)执行高强度活动
- ❌ 每次都选同一类活动
- ❌ 自评分虚高但无可验证产出
- ❌ 无价值时硬要"做点什么"

### 9.3 异常处理

```python
def handle_brainloop_error(error):
    """处理Brain Loop执行错误"""
    # 记录错误
    log_error({
        "type": "brainloop_error",
        "error": str(error),
        "timestamp": current_timestamp()
    })
    
    # 降级为休息
    return "休息"


def recover_from_poor_performance():
    """从低效状态恢复"""
    # 暂停Brain Loop 1小时
    # 记录状态
    # 一小时后重新评估
    pass
```
