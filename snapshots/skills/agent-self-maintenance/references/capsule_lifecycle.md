# 胶囊生命周期详解

> 详细说明胶囊从创建到清理的完整生命周期

---

## 1. 生命周期总览

```
┌─────────┐    捕获     ┌─────────┐    阅读理解   ┌────────┐    绑定场景   ┌─────────────┐
│  经验源  │ ────────→ │  pending │ ─────────→  │ reading │ ────────→   │   bound     │
└─────────┘            └─────────┘              └────────┘              └─────────────┘
                                                                            │
                                                                            ↓
┌─────────┐   验证成功    ┌─────────────┐   主动应用    ┌───────────┐   定期清理   ┌────────┐
│  复盘   │ ←────────── │ internalized │ ←──────────  │  applied  │ ←─────────  │ evicted │
└─────────┘              └─────────────┘              └───────────┘              └────────┘
```

---

## 2. 各阶段详解

### 2.1 捕获阶段 (Capture)

**触发时机**：
- 成功完成非标准任务
- 发现有效的特殊技巧
- 从错误中学习并修复
- 阅读有价值的学习资源

**捕获来源**：
| 来源类型 | 说明 | 典型示例 |
|----------|------|----------|
| 任务执行 | 真实任务中的成功经验 | "用对比表格分析竞品效果很好" |
| 错误修复 | 从失败中总结教训 | "用heredoc追加JSON导致文件损坏" |
| 灵感发现 | 意外发现的技巧 | "凌晨2点灵感涌现想到新方法" |
| 知识学习 | 从外部资源吸收 | "arXiv论文中的方法值得尝试" |

**捕获标准**：
- ✅ 是否是可复用的模式？
- ✅ 是否能说清楚"什么情况下用"？
- ✅ 是否值得花时间结构化？
- ❌ 过于具体的一次性经验不需要胶囊
- ❌ 太宽泛的"常识"不需要胶囊

### 2.2 待处理阶段 (Pending)

**状态特征**：
- 已创建基本结构
- 内容待完善
- 未进行深度处理

**待处理清单**：
- [ ] 补充context（使用背景）
- [ ] 明确pattern（核心模式）
- [ ] 验证示例输出
- [ ] 设定初始confidence

**处理时限**：
- 建议7天内完成处理
- 超过14天未处理自动降级或删除

### 2.3 阅读阶段 (Reading)

**处理内容**：
- 深度理解捕获的内容
- 补充pattern细节
- 撰写示例输出
- 明确适用边界

**输出产物**：
```json
{
  "id": "capsule_xxx",
  "name": "胶囊名称",
  "pattern": {
    "what_worked": "具体有效的做法",
    "when_to_apply": ["场景A", "场景B"],
    "why_it_works": "背后的原理"
  },
  "example_output": "示例输出文本",
  "confidence": 0.6,
  "status": "reading"
}
```

### 2.4 绑定阶段 (Bound)

**核心工作**：
- 识别适用场景
- 绑定到具体场景标签
- 确定与其他胶囊的关系

**场景绑定方法**：

```python
# 场景识别
def identify_scenarios(capsule):
    scenarios = []
    
    # 从when_to_apply提取
    for condition in capsule["pattern"]["when_to_apply"]:
        scenarios.append(condition)
    
    # 从context推断
    if "主人" in capsule["context"]:
        scenarios.extend([
            "主人任务处理",
            "主人需求响应"
        ])
    
    # 从type推断
    if capsule["type"] == "pattern_capsule":
        scenarios.append("方法论应用")
    
    return list(set(scenarios))
```

**场景粒度建议**：
- 太宽泛：`"主人相关"` → 价值不大
- 太具体：`"GPT-6发布时验证"` → 限制性太强
- 适中：`"重大技术发布验证"` → 可复用

### 2.5 内化阶段 (Internalized)

**内化标准**：
- [ ] 场景绑定清晰
- [ ] 有至少1次实战应用
- [ ] 应用结果验证成功
- [ ] confidence >= 0.7

**内化操作**：
```python
def internalize_capsule(capsule_id):
    capsule = get_capsule(capsule_id)
    
    # 验证前置条件
    assert capsule["status"] == "bound"
    assert capsule["success_count"] >= 1
    assert capsule["last_apply_result"]["success"] == True
    
    # 更新状态
    capsule["status"] = "internalized"
    capsule["internalized_at"] = current_timestamp()
    capsule["confidence"] = max(0.7, capsule["confidence"])
    
    save_capsule(capsule)
```

**内化后特性**：
- 可主动推荐给用户
- 进入CAPEC循环的应用环节
- 定期追踪应用效果

### 2.6 应用阶段 (Applied)

**应用流程**：
```
场景识别 → 胶囊匹配 → 执行应用 → 记录结果 → 更新置信度
```

**应用决策**：
```python
def should_apply(capsule, context):
    # 检查场景匹配
    if not match_scenarios(capsule["bound_scenarios"], context):
        return False, "场景不匹配"
    
    # 检查置信度
    if capsule["confidence"] < 0.5:
        return False, "置信度不足"
    
    # 检查时效性
    if is_outdated(capsule):
        return False, "内容可能过时"
    
    return True, "适合应用"
```

**结果记录**：
```json
{
  "capsule_id": "capsule_xxx",
  "applied_at": "2026-04-19T10:00:00+08:00",
  "context": "主人询问AI视频工具选型",
  "result": {
    "success": true,
    "quality_score": 0.85,
    "user_feedback": "很有帮助"
  },
  "confidence_change": "+0.05"
}
```

### 2.7 清理阶段 (Evicted)

**清理触发条件**：

| 条件 | 说明 | 处理方式 |
|------|------|----------|
| confidence < 0.3 | 连续失败导致 | 直接删除或归档 |
| 90天未使用 | 长期闲置 | 降级或删除 |
| 场景过时 | 技术/工具变化 | 删除或重构 |
| 功能重复 | 与其他胶囊重叠 | 合并到更优胶囊 |

**清理决策流程**：
```
胶囊审查 → 判断状态 → 选择处理方式 → 执行清理 → 记录归档
    ↓
┌────────────────────────────────────┐
│ confidence < 0.3? → 直接删除       │
│ 90天未使用? → 降级警告→删除       │
│ 功能重复? → 合并到主胶囊          │
│ 场景过时? → 删除或重构            │
└────────────────────────────────────┘
```

---

## 3. 状态转换规则

### 3.1 正常流转

```
pending → reading → bound → internalized → applied
```

### 3.2 回退机制

```
reading → pending     # 内容不完整需补充
bound → reading       # 场景绑定需重新思考
internalized → bound  # 应用失败需重新绑定场景
```

### 3.3 批量操作

```python
# 批量处理pending胶囊
def batch_process_pending(days_threshold=7):
    pending_capsules = get_capsules_by_status("pending")
    
    for capsule in pending_capsules:
        age = get_age_days(capsule)
        
        if age > days_threshold:
            # 超过阈值，降级处理
            if age > 14:
                delete_capsule(capsule)  # 删除
            else:
                capsule["priority"] = "low"  # 标记低优先级
                save_capsule(capsule)
        else:
            # 正常处理
            process_capsule(capsule)
```

---

## 4. 生命周期指标

### 4.1 健康度指标

| 指标 | 计算方式 | 健康范围 |
|------|----------|----------|
| 内化率 | internalized / total | >60% |
| 平均置信度 | avg(confidence) | >0.65 |
| 应用率 | applied_count / internalized | >30% |
| 清理率 | evicted_count / total | <10% |

### 4.2 预警阈值

```yaml
pending堆积:
  warning: >10个超过7天
  critical: >5个超过14天

内化率低:
  warning: <50%
  critical: <30%

置信度过低:
  warning: >5个<0.4
  critical: >10个<0.4
```

---

## 5. 实战案例

### 案例：竞品追踪模式胶囊

**阶段1：捕获 (2026-04-14)**
```
来源：主人让我追踪AI视频生成领域
发现：系统性汇总比碎片信息更有效
触发："HappyHorse(开源+盲测第一+4/30 API) | Wan2.7..."
```

**阶段2：Pending → Reading**
```json
{
  "name": "AIGC竞品追踪模式",
  "pattern": {
    "what_worked": "竞品排名 + 关键特性 + 时间节点 + 商业化状态",
    "when_to_apply": "探索兴趣活动、行业调研、技术选型",
    "why_it_works": "快速迭代的领域需要结构化对比"
  }
}
```

**阶段3：Bound**
```json
{
  "bound_scenarios": [
    "主人视频创作需求",
    "行业调研任务",
    "技术选型建议"
  ]
}
```

**阶段4：Internalized**
```json
{
  "status": "internalized",
  "confidence": 0.8,
  "success_count": 1,
  "internalized_at": "2026-04-14T16:00:00+08:00"
}
```

**阶段5：应用与提升**
```
2026-04-17: 应用1次，confidence 0.8→0.85
2026-04-18: 应用2次，confidence 0.85→0.88
```

---

## 6. 常见问题

### Q1: 如何判断一个经验值得创建胶囊？
A: 问自己三个问题：
1. 这个问题可能再次遇到吗？
2. 我的解决方案能说清楚吗？
3. 其他人或我以后能用吗？
如果都是"是"，就值得创建。

### Q2: 胶囊太泛或太窄怎么办？
A:
- 太泛：拆分成多个更具体的胶囊
- 太窄：扩大适用场景范围

### Q3: 应用失败后如何处理？
A:
1. 记录失败原因
2. 分析是场景匹配问题还是方法本身问题
3. 调整confidence
4. 更新场景绑定或考虑删除

### Q4: 如何避免胶囊库膨胀？
A:
- 定期合并功能相似的胶囊
- 设定合理的清理规则
- 追求质量而非数量
