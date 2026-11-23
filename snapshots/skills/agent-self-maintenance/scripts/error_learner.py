#!/usr/bin/env python3
"""
Error Learner - 错误学习工具
用于记录、分析和从错误中学习的系统
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Callable
from functools import wraps


class ErrorLearner:
    """错误学习工具"""
    
    def __init__(self, log_file: str = "./memory/error_log.jsonl"):
        self.log_file = log_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保日志文件存在"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            Path(self.log_file).touch()
    
    # ==================== 记录操作 ====================
    
    def log_error(self, error_data: Dict) -> Dict:
        """记录错误"""
        record = {
            "timestamp": error_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "error_type": error_data.get("error_type", "unknown"),
            "description": error_data.get("description", ""),
            "root_cause": error_data.get("root_cause", ""),
            "improvement": error_data.get("improvement", ""),
            "owner": error_data.get("owner", "agent"),
            "repeat_count": 1,
            "learned_at": None,
            "prevention_rules": []
        }
        
        # 检查是否有重复错误
        if self._is_duplicate(record):
            self._increment_repeat(record)
            return {"status": "incremented", "record": record}
        
        # 写入日志
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return {"status": "logged", "record": record}
    
    def _is_duplicate(self, record: Dict) -> bool:
        """检查是否重复错误"""
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    existing = json.loads(line.strip())
                    if existing.get("error_type") == record["error_type"]:
                        if existing.get("description") == record["description"]:
                            return True
                except:
                    continue
        return False
    
    def _increment_repeat(self, record: Dict):
        """增加重复计数"""
        lines = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 找到并更新重复记录
        for i, line in enumerate(lines):
            try:
                existing = json.loads(line.strip())
                if (existing.get("error_type") == record["error_type"] and
                    existing.get("description") == record["description"]):
                    existing["repeat_count"] = existing.get("repeat_count", 1) + 1
                    lines[i] = json.dumps(existing, ensure_ascii=False) + '\n'
                    break
            except:
                continue
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    # ==================== 查询操作 ====================
    
    def get_all_errors(self, limit: int = None) -> List[Dict]:
        """获取所有错误记录"""
        errors = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        errors.append(json.loads(line.strip()))
                    except:
                        continue
        
        if limit:
            errors = errors[-limit:]
        return errors
    
    def get_errors_by_type(self, error_type: str) -> List[Dict]:
        """按类型筛选错误"""
        return [e for e in self.get_all_errors() if e.get("error_type") == error_type]
    
    def get_errors_by_period(self, days: int) -> List[Dict]:
        """获取最近N天的错误"""
        cutoff = datetime.now() - timedelta(days=days)
        errors = []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line.strip())
                        record_time = datetime.strptime(
                            record["timestamp"], 
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if record_time >= cutoff:
                            errors.append(record)
                    except:
                        continue
        
        return errors
    
    def get_repeated_errors(self) -> List[Dict]:
        """获取重复出现的错误"""
        return [e for e in self.get_all_errors() if e.get("repeat_count", 1) > 1]
    
    # ==================== 分析操作 ====================
    
    def analyze_5why(self, error: Dict) -> Dict:
        """执行5Why根因分析"""
        why_analysis = {
            "original_problem": error.get("description", ""),
            "whys": []
        }
        
        # 如果已有根因，直接返回
        if error.get("root_cause"):
            why_analysis["root_cause"] = error["root_cause"]
            why_analysis["confidence"] = "high"
            return why_analysis
        
        # 基于错误类型推测根因模式
        error_type = error.get("error_type", "")
        description = error.get("description", "").lower()
        
        if "文件" in error_type or "file" in description:
            why_chain = [
                "文件操作失败",
                "文件格式/路径问题",
                "未使用标准工具",
                "缺乏操作规范",
                "未建立标准流程"
            ]
        elif "执行" in error_type or "execute" in description:
            why_chain = [
                "任务执行失败",
                "预期与实际不符",
                "缺少结果验证",
                "缺乏检查机制",
                "流程不够严谨"
            ]
        elif "工具" in error_type or "tool" in description:
            why_chain = [
                "工具调用失败",
                "参数或环境问题",
                "缺少错误处理",
                "缺少降级方案",
                "依赖外部稳定性"
            ]
        else:
            why_chain = [
                description or "出现问题",
                "可能的原因A",
                "更深层原因B",
                "根本原因C",
                "系统性问题D"
            ]
        
        why_analysis["whys"] = why_chain
        why_analysis["root_cause"] = why_chain[-1] if why_chain else "未知"
        why_analysis["confidence"] = "low"
        
        return why_analysis
    
    def generate_prevention_rules(self, error: Dict) -> List[str]:
        """生成预防规则"""
        rules = []
        error_type = error.get("error_type", "")
        
        # 基于错误类型生成规则
        if "文件" in error_type:
            rules.extend([
                "操作前先检查文件存在性",
                "使用标准JSON库而非字符串操作",
                "操作前先备份",
                "操作后验证文件完整性"
            ])
        elif "执行" in error_type:
            rules.extend([
                "执行前明确预期结果",
                "执行后验证实际结果",
                "记录关键节点状态"
            ])
        elif "工具" in error_type:
            rules.extend([
                "添加超时处理",
                "添加错误重试机制",
                "准备降级方案"
            ])
        
        # 从improvement字段提取
        if error.get("improvement"):
            rules.append(f"应用改进措施: {error['improvement']}")
        
        return list(set(rules))
    
    def analyze_patterns(self, errors: List[Dict] = None) -> Dict:
        """分析错误规律"""
        if errors is None:
            errors = self.get_all_errors()
        
        if not errors:
            return {"pattern_count": 0, "patterns": []}
        
        # 按类型统计
        type_counts = {}
        for e in errors:
            etype = e.get("error_type", "unknown")
            type_counts[etype] = type_counts.get(etype, 0) + 1
        
        # 按时间统计
        daily_counts = {}
        for e in errors:
            try:
                date = e["timestamp"].split(" ")[0]
                daily_counts[date] = daily_counts.get(date, 0) + 1
            except:
                continue
        
        # 找出重复错误
        repeated = [e for e in errors if e.get("repeat_count", 1) > 1]
        
        # 高频错误类型
        frequent_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        patterns = []
        for etype, count in frequent_types:
            if count >= 2:
                patterns.append({
                    "error_type": etype,
                    "count": count,
                    "severity": "high" if count >= 5 else "medium",
                    "suggestion": f"该类型错误已出现{count}次，需要重点预防"
                })
        
        return {
            "total_errors": len(errors),
            "unique_types": len(type_counts),
            "repeated_count": len(repeated),
            "patterns": patterns,
            "type_distribution": type_counts,
            "daily_trend": daily_counts
        }
    
    # ==================== 学习与改进 ====================
    
    def mark_as_learned(self, error: Dict, prevention_rules: List[str]) -> bool:
        """标记为已学习"""
        errors = []
        found = False
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line.strip())
                        if (record.get("timestamp") == error.get("timestamp") and
                            record.get("description") == error.get("description")):
                            record["learned_at"] = datetime.now().isoformat()
                            record["prevention_rules"] = prevention_rules
                            found = True
                        errors.append(record)
                    except:
                        continue
        
        if found:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                for record in errors:
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return found
    
    def get_learning_summary(self, days: int = 7) -> Dict:
        """获取学习总结"""
        recent_errors = self.get_errors_by_period(days)
        patterns = self.analyze_patterns(recent_errors)
        
        learned = [e for e in recent_errors if e.get("learned_at")]
        unlearned = [e for e in recent_errors if not e.get("learned_at")]
        
        return {
            "period_days": days,
            "total_errors": len(recent_errors),
            "learned_count": len(learned),
            "unlearned_count": len(unlearned),
            "top_patterns": patterns.get("patterns", [])[:5],
            "recommendations": self._generate_recommendations(unlearned)
        }
    
    def _generate_recommendations(self, unlearned_errors: List[Dict]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if len(unlearned_errors) > 10:
            recommendations.append("错误数量偏多，建议建立更严格的前置检查")
        
        # 按类型分析
        type_counts = {}
        for e in unlearned_errors:
            etype = e.get("error_type", "unknown")
            type_counts[etype] = type_counts.get(etype, 0) + 1
        
        for etype, count in type_counts.items():
            if count >= 3:
                recommendations.append(
                    f"'{etype}'类型错误频繁({count}次)，需要系统性改进"
                )
        
        if not recommendations:
            recommendations.append("当前错误在可控范围内，保持良好习惯")
        
        return recommendations
    
    # ==================== 自动错误捕获 ====================
    
    @staticmethod
    def auto_catch(error_learner=None, log_file="./memory/error_log.jsonl"):
        """自动错误捕获装饰器"""
        if error_learner is None:
            error_learner = ErrorLearner(log_file)
        
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # 记录错误
                    error_learner.log_error({
                        "error_type": type(e).__name__,
                        "description": str(e),
                        "root_cause": f"函数 {func.__name__} 执行异常",
                        "improvement": f"检查 {func.__name__} 的参数和执行环境",
                        "owner": "agent"
                    })
                    raise
            return wrapper
        return decorator


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="错误学习工具")
    parser.add_argument("--file", default="./memory/error_log.jsonl", help="错误日志文件")
    parser.add_argument("action", choices=["log", "list", "analyze", "patterns", 
                                          "summary", "learn", "export"],
                       help="操作类型")
    parser.add_argument("--type", help="错误类型")
    parser.add_argument("--description", help="错误描述")
    parser.add_argument("--root-cause", help="根因")
    parser.add_argument("--improvement", help="改进措施")
    parser.add_argument("--days", type=int, default=7, help="天数")
    
    args = parser.parse_args()
    learner = ErrorLearner(args.file)
    
    if args.action == "log":
        if not args.description:
            print("错误: 记录需要 --description 参数")
            return
        
        result = learner.log_error({
            "error_type": args.type or "unknown",
            "description": args.description,
            "root_cause": args.root_cause or "",
            "improvement": args.improvement or "",
            "owner": "agent"
        })
        print(f"✓ {result['status']}")
        print(json.dumps(result["record"], indent=2, ensure_ascii=False))
    
    elif args.action == "list":
        errors = learner.get_all_errors()
        print(f"共 {len(errors)} 条错误记录:\n")
        for e in errors[-20:]:  # 显示最近20条
            print(f"[{e['timestamp']}] {e['error_type']}")
            print(f"  描述: {e['description']}")
            if e.get("repeat_count", 1) > 1:
                print(f"  重复: {e['repeat_count']}次")
            print()
    
    elif args.action == "analyze":
        if args.type:
            errors = learner.get_errors_by_type(args.type)
        else:
            errors = learner.get_errors_by_period(args.days)
        
        print(f"分析了 {len(errors)} 条错误:\n")
        for e in errors[:5]:
            analysis = learner.analyze_5why(e)
            print(f"[{e['timestamp']}] {e['description']}")
            print(f"  5Why分析: {' → '.join(analysis.get('whys', [])[:3])}")
            print(f"  根因: {analysis.get('root_cause', '未知')}")
            print()
    
    elif args.action == "patterns":
        patterns = learner.analyze_patterns()
        print("错误规律分析:\n")
        print(json.dumps(patterns, indent=2, ensure_ascii=False))
    
    elif args.action == "summary":
        summary = learner.get_learning_summary(args.days)
        print(f"近{args.days}天学习总结:\n")
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    elif args.action == "learn":
        errors = learner.get_unlearned_errors() if hasattr(learner, 'get_unlearned_errors') else []
        print("未学习的错误:")
        print(json.dumps(errors[:5], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
