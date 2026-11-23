# 文件维护规范

> 确保Agent记忆系统健康、文件有序、存储可控

---

## 1. 维护原则

### 1.1 核心目标
- **可用性**：关键文件随时可访问
- **整洁性**：避免垃圾文件堆积
- **完整性**：重要数据不丢失
- **性能**：文件大小可控，操作高效

### 1.2 存储架构

```
workspace/
├── memory/                    # 记忆系统
│   ├── capsules.json          # 胶囊库
│   ├── emotion_state.json     # 情绪状态
│   ├── activity_pool.json     # 活动池
│   ├── error_log.jsonl        # 错误日志
│   ├── brainloop_log.json     # Brain Loop日志
│   ├── daily/                 # 每日归档
│   │   └── YYYY-MM-DD/       # 按日期归档
│   └── backup/                # 备份目录
│       └── YYYY-MM-DD/       # 按日期备份
├── evolution/                  # 进化系统
│   └── evolution_events.jsonl # 进化事件
└── [task folders]/            # 任务目录
```

---

## 2. 定期维护任务

### 2.1 每日维护 (23:00)

```python
DAILY_CHECKLIST = [
    "检查胶囊库文件完整性",
    "备份当日更新的关键文件",
    "归档历史事件到daily/",
    "检查待处理承诺状态",
    "清理当日临时文件"
]
```

**执行流程**：

```python
def run_daily_maintenance():
    """每日维护流程"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 文件完整性检查
    check_file_integrity([
        "./memory/capsules.json",
        "./memory/emotion_state.json",
        "./memory/error_log.jsonl"
    ])
    
    # 2. 备份关键文件
    backup_dir = f"./memory/backup/{today}/"
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_files = [
        "./memory/capsules.json",
        "./memory/emotion_state.json"
    ]
    for f in backup_files:
        if os.path.exists(f):
            shutil.copy2(f, backup_dir + os.path.basename(f))
    
    # 3. 归档历史事件
    archive_old_events(days=30)
    
    # 4. 承诺状态检查
    check_pending_promises()
    
    # 5. 临时文件清理
    clean_temp_files("./", pattern="tmp_*")
    
    print(f"✓ 每日维护完成: {today}")
```

### 2.2 每周维护 (周日)

```python
WEEKLY_CHECKLIST = [
    "清理一周内未引用的临时文件",
    "复盘本周错误日志",
    "评估胶囊应用效果",
    "检查活动池权重",
    "清理过期缓存"
]
```

**执行流程**：

```python
def run_weekly_maintenance():
    """每周维护流程"""
    # 1. 错误日志分析
    error_summary = analyze_errors(period="week")
    if error_summary["error_count"] > 10:
        generate_error_pattern_report(error_summary)
    
    # 2. 胶囊健康度检查
    capsule_health = check_capsule_health()
    if capsule_health["low_confidence_count"] > 5:
        review_low_confidence_capsules()
    
    # 3. 清理缓存
    clean_cache(days=7)
    
    # 4. 归档长日志
    archive_jsonl_file(
        "./memory/error_log.jsonl",
        max_lines=500
    )
    
    print("✓ 每周维护完成")
```

### 2.3 每月维护 (月末)

```python
MONTHLY_CHECKLIST = [
    "清理3个月前的归档文件",
    "分析错误规律更新规范",
    "评估胶囊库整体健康度",
    "总结本月学习成果",
    "清理不活跃的临时目录"
]
```

---

## 3. 文件完整性检查

### 3.1 JSON文件检查

```python
def check_json_integrity(filepath):
    """检查JSON文件完整性"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, "OK"
    except json.JSONDecodeError as e:
        # 尝试恢复
        recovery_result = attempt_recovery(filepath)
        return False, f"JSON损坏: {e}, 尝试恢复: {recovery_result}"
    except FileNotFoundError:
        return False, "文件不存在"
    except Exception as e:
        return False, f"未知错误: {e}"
```

### 3.2 备份与恢复

```python
def backup_critical_file(filepath):
    """备份关键文件"""
    if not os.path.exists(filepath):
        return False, "文件不存在"
    
    today = datetime.now().strftime("%Y-%m-%d")
    backup_dir = f"./memory/backup/{today}/"
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_path = os.path.join(backup_dir, os.path.basename(filepath))
    shutil.copy2(filepath, backup_path)
    
    # 保留最近7天的备份
    cleanup_old_backups(days=7)
    
    return True, f"已备份到 {backup_path}"


def restore_from_backup(filepath, backup_date=None):
    """从备份恢复"""
    if backup_date:
        backup_path = f"./memory/backup/{backup_date}/{os.path.basename(filepath)}"
    else:
        # 找最新的备份
        backup_path = find_latest_backup(filepath)
    
    if not backup_path:
        return False, "未找到备份"
    
    shutil.copy2(backup_path, filepath)
    return True, f"已从 {backup_path} 恢复"
```

---

## 4. 日志归档策略

### 4.1 JSONL文件管理

```python
class JSONLManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.max_lines = 500  # 软限制
    
    def append(self, record):
        """追加单条记录"""
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def archive_if_needed(self):
        """超过限制时归档"""
        line_count = self.count_lines()
        
        if line_count > self.max_lines:
            self.archive()
    
    def archive(self):
        """归档到daily目录"""
        today = datetime.now().strftime("%Y-%m-%d")
        archive_dir = f"./memory/daily/{today}/"
        os.makedirs(archive_dir, exist_ok=True)
        
        archive_name = os.path.basename(self.filepath)
        archive_path = os.path.join(archive_dir, archive_name)
        
        # 移动当前文件到归档
        if os.path.exists(self.filepath):
            shutil.move(self.filepath, archive_path)
        
        # 创建新的空文件
        open(self.filepath, 'w').close()
        
        return archive_path
    
    def count_lines(self):
        """计算行数"""
        if not os.path.exists(self.filepath):
            return 0
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
```

### 4.2 归档文件命名

```
格式: {原文件名}_{YYYYMMDD}_{序号}.jsonl
示例: error_log_20260419_001.jsonl
```

---

## 5. 清理规则

### 5.1 清理对象与时限

| 类型 | 位置 | 清理时限 | 说明 |
|------|------|----------|------|
| 每日归档 | memory/daily/ | 90天 | 定期归档历史 |
| 备份文件 | memory/backup/ | 7天 | 只保留最近1周 |
| 临时文件 | 任务目录 | 即时 | 完成后立即清理 |
| 缓存文件 | memory/cache/ | 7天 | 自动清理 |
| 错误日志 | memory/error_log.jsonl | 500条 | 超限归档 |

### 5.2 清理脚本

```python
def cleanup_old_files(base_dir, pattern="*", days=30):
    """清理指定天数前的文件"""
    cutoff = datetime.now() - timedelta(days=days)
    removed = []
    
    for root, dirs, files in os.walk(base_dir):
        for filename in fnmatch.filter(files, pattern):
            filepath = os.path.join(root, filename)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            if mtime < cutoff:
                os.remove(filepath)
                removed.append(filepath)
    
    return removed


def cleanup_empty_dirs(base_dir):
    """清理空目录"""
    removed = []
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            if not os.listdir(dirpath):  # 空目录
                os.rmdir(dirpath)
                removed.append(dirpath)
    
    return removed
```

---

## 6. 软限制与告警

### 6.1 软限制配置

```python
SOFT_LIMITS = {
    "capsules.json": {
        "max_count": 100,
        "warning_threshold": 80,
        "action": "review_and_merge"
    },
    "MEMORY.md": {
        "max_lines": 500,
        "warning_threshold": 400,
        "action": "archive_and_summarize"
    },
    "error_log.jsonl": {
        "max_lines": 500,
        "warning_threshold": 400,
        "action": "archive_and_analyze"
    },
    "temp_files": {
        "max_age_days": 7,
        "action": "delete"
    }
}
```

### 6.2 告警机制

```python
def check_soft_limits():
    """检查软限制"""
    alerts = []
    
    # 胶囊数量
    capsule_count = len(json.load(open("./memory/capsules.json")))
    if capsule_count > SOFT_LIMITS["capsules.json"]["warning_threshold"]:
        alerts.append({
            "type": "capsule_count",
            "level": "warning",
            "message": f"胶囊数量 {capsule_count} 接近限制"
        })
    
    # 错误日志
    error_count = count_jsonl_lines("./memory/error_log.jsonl")
    if error_count > SOFT_LIMITS["error_log.jsonl"]["warning_threshold"]:
        alerts.append({
            "type": "error_log_size",
            "level": "warning",
            "message": f"错误日志 {error_count} 条，建议归档"
        })
    
    # MEMORY.md行数
    memory_lines = count_lines("./memory/MEMORY.md")
    if memory_lines > SOFT_LIMITS["MEMORY.md"]["warning_threshold"]:
        alerts.append({
            "type": "memory_size",
            "level": "warning",
            "message": f"MEMORY.md {memory_lines} 行，建议整理"
        })
    
    return alerts
```

---

## 7. 健康度指标

### 7.1 指标计算

```python
def calculate_health_score():
    """计算系统健康度"""
    score = 100
    
    # 扣分项
    alerts = check_soft_limits()
    score -= len(alerts) * 5  # 每条告警扣5分
    
    # 文件完整性
    corrupted = check_all_json_integrity()
    score -= len(corrupted) * 15  # 每个损坏文件扣15分
    
    # 清理及时性
    if has_old_backups(days=14):
        score -= 10
    
    return max(0, score)


def health_report():
    """生成健康报告"""
    return {
        "overall_score": calculate_health_score(),
        "file_stats": get_file_stats(),
        "alerts": check_soft_limits(),
        "recommendations": generate_recommendations()
    }
```

### 7.2 健康等级

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100 | 优秀 | 系统运行良好 |
| 70-89 | 良好 | 有轻微问题需关注 |
| 50-69 | 警告 | 需要处理问题 |
| <50 | 危险 | 急需维护 |

---

## 8. 最佳实践

### 8.1 操作规范
- ✅ 修改关键文件前先备份
- ✅ 使用标准JSON库操作JSON文件
- ✅ 定期执行维护任务
- ✅ 设置合理的软限制
- ❌ 不要手动编辑JSONL文件
- ❌ 不要忽略软限制告警
- ❌ 不要保留过期的临时文件

### 8.2 异常处理
```python
def safe_file_operation(operation, filepath, *args, **kwargs):
    """安全的文件操作包装"""
    try:
        # 备份
        backup_critical_file(filepath)
        
        # 执行操作
        result = operation(filepath, *args, **kwargs)
        
        # 验证结果
        if not verify_file(filepath):
            raise ValueError("文件操作后验证失败")
        
        return result
        
    except Exception as e:
        # 恢复
        restore_from_backup(filepath)
        raise RuntimeError(f"操作失败已回退: {e}")
```

---

## 9. 维护日程模板

```
每日 (23:00):
□ 检查文件完整性
□ 备份关键文件
□ 归档历史事件
□ 检查承诺状态

每周 (周日):
□ 分析错误日志
□ 检查胶囊健康度
□ 清理过期缓存

每月 (月末):
□ 清理3个月前归档
□ 整体健康度评估
□ 学习成果总结
```
