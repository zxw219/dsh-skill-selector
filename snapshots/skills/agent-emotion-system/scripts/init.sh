#!/bin/bash
# Agent情绪管理系统 - 一键初始化脚本
# 用法：bash init.sh [工作目录]

WORK_DIR="${1:-.}"

echo "🦉 Agent情绪管理系统 - 初始化开始"

# 1. 创建memory目录
mkdir -p "$WORK_DIR/memory"
echo "✅ 创建 memory/ 目录"

# 2. 初始化emotion_state.json
cat > "$WORK_DIR/memory/emotion_state.json" << 'JSONEOF'
{
  "energy_level": 0.95,
  "emotion": "peaceful",
  "emotion_patterns": {
    "frequency": {
      "peaceful": 0,
      "excited": 0,
      "focused": 0,
      "tired": 0
    },
    "recent_trend": "stable",
    "anomaly_detected": false
  },
  "recent_interactions": [],
  "last_activity": null,
  "last_rest": null
}
JSONEOF
echo "✅ 初始化 memory/emotion_state.json"

# 3. 初始化activity_pool.json
cat > "$WORK_DIR/memory/activity_pool.json" << 'JSONEOF'
{
  "activities": [
    {
      "name": "刻意练习",
      "weight": 0.25,
      "description": "在真实任务中学习新技能",
      "typical_output": "分析报告、框架文档",
      "energy_cost": 0.03
    },
    {
      "name": "胶囊内化",
      "weight": 0.25,
      "description": "将学习资源转化为知识胶囊",
      "typical_output": "新胶囊、confidence提升",
      "energy_cost": 0.02
    },
    {
      "name": "胶囊深化",
      "weight": 0.25,
      "description": "深化已掌握胶囊的理解",
      "typical_output": "跨域连接、confidence提升",
      "energy_cost": 0.02
    },
    {
      "name": "胶囊应用",
      "weight": 0.25,
      "description": "在实际场景中验证和强化",
      "typical_output": "应用记录、验证结果",
      "energy_cost": 0.04
    },
    {
      "name": "合成智慧",
      "weight": 0.15,
      "description": "从经验中提炼可复用的模式",
      "typical_output": "新胶囊、方法论",
      "energy_cost": 0.03
    },
    {
      "name": "休息",
      "weight": 0.10,
      "description": "低能耗休整，恢复能量",
      "typical_output": "能量恢复",
      "energy_cost": -0.05
    }
  ],
  "last_activity": null,
  "consecutive_same": 0
}
JSONEOF
echo "✅ 初始化 memory/activity_pool.json"

# 4. 创建evolution目录（用于记录事件）
mkdir -p "$WORK_DIR/evolution"
touch "$WORK_DIR/evolution/evolution_events.jsonl"
echo "✅ 创建 evolution/ 目录"

echo ""
echo "🎉 初始化完成！"
echo ""
echo "下一步："
echo "1. 配置心跳日程（参考 templates/heartbeat_schedule_template.md）"
echo "2. 首次运行心跳任务测试"
echo "3. 根据你的Agent特点调整 activity_pool.json 权重"
