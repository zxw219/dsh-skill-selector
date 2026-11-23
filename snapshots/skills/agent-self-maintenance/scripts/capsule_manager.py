#!/usr/bin/env python3
"""
Capsule Manager - 胶囊管理工具
用于创建、查询、应用、更新和清理知识胶囊
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pathlib import Path


class CapsuleManager:
    """胶囊管理器"""
    
    def __init__(self, capsule_file: str = "./memory/capsules.json"):
        self.capsule_file = capsule_file
        self.capsules = self._load_capsules()
    
    def _load_capsules(self) -> List[Dict]:
        """加载胶囊库"""
        if os.path.exists(self.capsule_file):
            try:
                with open(self.capsule_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"[警告] {self.capsule_file} 文件损坏，尝试恢复")
                return self._recover_capsules()
        return []
    
    def _save_capsules(self):
        """保存胶囊库"""
        os.makedirs(os.path.dirname(self.capsule_file), exist_ok=True)
        with open(self.capsule_file, 'w', encoding='utf-8') as f:
            json.dump(self.capsules, f, ensure_ascii=False, indent=2)
    
    def _recover_capsules(self):
        """从备份恢复"""
        backup_dir = Path(self.capsule_file).parent / "backup"
        if backup_dir.exists():
            backups = sorted(backup_dir.glob("*/capsules.json"), reverse=True)
            for backup in backups:
                try:
                    with open(backup, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    continue
        return []
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        existing_ids = [c.get("id", "") for c in self.capsules]
        num = 1
        while f"capsule_{num:03d}" in existing_ids:
            num += 1
        return f"capsule_{num:03d}"
    
    # ==================== 创建操作 ====================
    
    def create_capsule(self, capsule_data: Dict[str, Any]) -> Dict:
        """创建新胶囊"""
        capsule = {
            "id": capsule_data.get("id", self._generate_id()),
            "gene": capsule_data.get("gene", "gene_learn_from_experience"),
            "type": capsule_data.get("type", "pattern_capsule"),
            "name": capsule_data["name"],
            "created_at": datetime.now().isoformat(),
            "source_event": capsule_data.get("source_event", ""),
            "context": capsule_data.get("context", ""),
            "pattern": {
                "what_worked": capsule_data.get("what_worked", ""),
                "when_to_apply": capsule_data.get("when_to_apply", []),
                "why_it_works": capsule_data.get("why_it_works", "")
            },
            "example_output": capsule_data.get("example_output", ""),
            "confidence": capsule_data.get("confidence", 0.6),
            "success_count": 0,
            "status": "pending",
            "bound_scenarios": [],
            "validation": ""
        }
        
        self.capsules.append(capsule)
        self._save_capsules()
        return capsule
    
    def create_from_template(self, name: str, context: str, 
                           what_worked: str, when_to_apply: List[str],
                           why_it_works: str) -> Dict:
        """从模板创建胶囊"""
        return self.create_capsule({
            "name": name,
            "context": context,
            "what_worked": what_worked,
            "when_to_apply": when_to_apply,
            "why_it_works": why_it_works
        })
    
    # ==================== 查询操作 ====================
    
    def get_capsule(self, capsule_id: str) -> Optional[Dict]:
        """获取单个胶囊"""
        for capsule in self.capsules:
            if capsule["id"] == capsule_id:
                return capsule
        return None
    
    def get_by_name(self, name: str) -> Optional[Dict]:
        """按名称查找胶囊"""
        for capsule in self.capsules:
            if capsule["name"] == name:
                return capsule
        return None
    
    def get_by_status(self, status: str) -> List[Dict]:
        """按状态筛选"""
        return [c for c in self.capsules if c.get("status") == status]
    
    def get_by_scenario(self, scenario: str) -> List[Dict]:
        """按场景筛选"""
        results = []
        for capsule in self.capsules:
            if capsule.get("status") in ["bound", "internalized"]:
                if any(scenario.lower() in s.lower() for s in capsule.get("bound_scenarios", [])):
                    results.append(capsule)
        return results
    
    def search_capsules(self, query: str) -> List[Dict]:
        """搜索胶囊"""
        query_lower = query.lower()
        results = []
        for capsule in self.capsules:
            searchable = " ".join([
                capsule.get("name", ""),
                capsule.get("context", ""),
                capsule.get("type", ""),
                " ".join(capsule.get("bound_scenarios", []))
            ]).lower()
            if query_lower in searchable:
                results.append(capsule)
        return results
    
    def find_best_match(self, scenario: str) -> Optional[Dict]:
        """查找最佳匹配的胶囊"""
        matches = self.get_by_scenario(scenario)
        if not matches:
            return None
        
        # 按置信度排序
        matches.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        return matches[0]
    
    # ==================== 更新操作 ====================
    
    def update_status(self, capsule_id: str, new_status: str) -> bool:
        """更新胶囊状态"""
        capsule = self.get_capsule(capsule_id)
        if not capsule:
            return False
        
        valid_statuses = ["pending", "reading", "bound", "internalized"]
        if new_status not in valid_statuses:
            return False
        
        capsule["status"] = new_status
        if new_status == "internalized":
            capsule["internalized_at"] = datetime.now().isoformat()
        
        self._save_capsules()
        return True
    
    def bind_scenarios(self, capsule_id: str, scenarios: List[str]) -> bool:
        """绑定场景"""
        capsule = self.get_capsule(capsule_id)
        if not capsule:
            return False
        
        capsule["bound_scenarios"] = list(set(capsule.get("bound_scenarios", []) + scenarios))
        
        # 如果已有场景绑定，自动升级到bound状态
        if capsule["status"] == "reading" and capsule["bound_scenarios"]:
            capsule["status"] = "bound"
        
        self._save_capsules()
        return True
    
    def record_application(self, capsule_id: str, success: bool, 
                          result: str = "") -> bool:
        """记录胶囊应用"""
        capsule = self.get_capsule(capsule_id)
        if not capsule:
            return False
        
        capsule["success_count"] = capsule.get("success_count", 0) + 1
        capsule["last_applied_at"] = datetime.now().isoformat()
        capsule["last_apply_result"] = result
        
        # 更新置信度
        self._update_confidence(capsule, success)
        
        # 如果首次成功应用，尝试内化
        if success and capsule["success_count"] == 1 and capsule["status"] == "bound":
            if capsule.get("confidence", 0) >= 0.7:
                capsule["status"] = "internalized"
                capsule["internalized_at"] = datetime.now().isoformat()
        
        self._save_capsules()
        return True
    
    def _update_confidence(self, capsule: Dict, success: bool):
        """更新置信度"""
        current = capsule.get("confidence", 0.5)
        
        if success:
            # 成功应用：提升置信度
            delta = min(0.1, (1 - current) * 0.2)
            capsule["confidence"] = round(current + delta, 3)
        else:
            # 失败应用：降低置信度
            capsule["confidence"] = round(current - 0.15, 3)
            if capsule["confidence"] < 0.4:
                capsule["confidence"] = 0.4  # 设置下限
    
    # ==================== 应用胶囊 ====================
    
    def apply_capsule(self, capsule_id_or_name: str, context: str = "",
                     **kwargs) -> Dict:
        """应用胶囊"""
        # 支持ID或名称
        capsule = self.get_capsule(capsule_id_or_name)
        if not capsule:
            capsule = self.get_by_name(capsule_id_or_name)
        
        if not capsule:
            return {
                "success": False,
                "error": f"未找到胶囊: {capsule_id_or_name}"
            }
        
        # 检查置信度
        if capsule.get("confidence", 0) < 0.5:
            return {
                "success": False,
                "error": "置信度过低，不建议应用",
                "confidence": capsule.get("confidence", 0)
            }
        
        # 执行应用
        result = {
            "success": True,
            "capsule_id": capsule["id"],
            "capsule_name": capsule["name"],
            "confidence": capsule.get("confidence", 0),
            "pattern": capsule.get("pattern", {}),
            "example_output": capsule.get("example_output", "")
        }
        
        # 记录应用
        self.record_application(capsule["id"], True, 
                               f"在场景'{context}'中应用成功")
        
        return result
    
    # ==================== 批量操作 ====================
    
    def batch_internalize(self, criteria: Dict = None) -> int:
        """批量内化胶囊"""
        if criteria is None:
            criteria = {"status": "bound", "success_count": ">=1"}
        
        internalized_count = 0
        for capsule in self.capsules:
            if capsule["status"] != "bound":
                continue
            
            # 检查条件
            if capsule.get("success_count", 0) >= 1:
                if capsule.get("confidence", 0) >= 0.7:
                    capsule["status"] = "internalized"
                    capsule["internalized_at"] = datetime.now().isoformat()
                    internalized_count += 1
        
        if internalized_count > 0:
            self._save_capsules()
        return internalized_count
    
    def cleanup_low_confidence(self, threshold: float = 0.4) -> int:
        """清理低置信度胶囊"""
        original_count = len(self.capsules)
        self.capsules = [
            c for c in self.capsules 
            if c.get("confidence", 0) >= threshold or c.get("status") == "internalized"
        ]
        removed_count = original_count - len(self.capsules)
        
        if removed_count > 0:
            self._save_capsules()
        return removed_count
    
    # ==================== 统计分析 ====================
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = {
            "total": len(self.capsules),
            "by_status": {},
            "by_type": {},
            "avg_confidence": 0,
            "high_confidence_count": 0,  # >= 0.8
            "low_confidence_count": 0,     # < 0.5
        }
        
        total_confidence = 0
        for capsule in self.capsules:
            # 按状态统计
            status = capsule.get("status", "unknown")
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            # 按类型统计
            cap_type = capsule.get("type", "unknown")
            stats["by_type"][cap_type] = stats["by_type"].get(cap_type, 0) + 1
            
            # 置信度统计
            conf = capsule.get("confidence", 0)
            total_confidence += conf
            if conf >= 0.8:
                stats["high_confidence_count"] += 1
            if conf < 0.5:
                stats["low_confidence_count"] += 1
        
        if self.capsules:
            stats["avg_confidence"] = round(total_confidence / len(self.capsules), 3)
        
        return stats
    
    def get_health_report(self) -> Dict:
        """获取健康度报告"""
        stats = self.get_stats()
        
        health_score = 100
        recommendations = []
        
        # 检查内化率
        internalized = stats["by_status"].get("internalized", 0)
        if stats["total"] > 0:
            internalized_rate = internalized / stats["total"]
            if internalized_rate < 0.3:
                health_score -= 20
                recommendations.append("内化率偏低，建议增加胶囊应用频率")
        
        # 检查平均置信度
        if stats["avg_confidence"] < 0.6:
            health_score -= 15
            recommendations.append("平均置信度偏低，部分胶囊可能需要清理或强化")
        
        # 检查高置信度胶囊比例
        if stats["high_confidence_count"] < 3:
            health_score -= 10
            recommendations.append("高置信度胶囊数量偏少")
        
        return {
            "score": max(0, health_score),
            "stats": stats,
            "recommendations": recommendations
        }


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="胶囊管理工具")
    parser.add_argument("--file", default="./memory/capsules.json", help="胶囊库文件路径")
    parser.add_argument("action", choices=["create", "list", "stats", "health", "apply", "search"],
                       help="操作类型")
    parser.add_argument("--name", help="胶囊名称")
    parser.add_argument("--context", help="使用背景")
    parser.add_argument("--what-worked", help="什么有效")
    parser.add_argument("--when-apply", nargs="+", help="何时适用")
    parser.add_argument("--why-works", help="为何有效")
    parser.add_argument("--query", help="搜索关键词")
    parser.add_argument("--capsule-id", help="胶囊ID")
    
    args = parser.parse_args()
    manager = CapsuleManager(args.file)
    
    if args.action == "create":
        if not args.name:
            print("错误: 创建需要 --name 参数")
            return
        
        capsule = manager.create_from_template(
            name=args.name,
            context=args.context or "",
            what_worked=args.what_worked or "",
            when_to_apply=args.when_apply or [],
            why_it_works=args.why_works or ""
        )
        print(f"✓ 胶囊创建成功: {capsule['id']}")
        print(json.dumps(capsule, indent=2, ensure_ascii=False))
    
    elif args.action == "list":
        capsules = manager.capsules
        print(f"共 {len(capsules)} 个胶囊:\n")
        for c in capsules:
            print(f"  [{c['id']}] {c['name']} | {c['status']} | confidence: {c.get('confidence', 0):.2f}")
    
    elif args.action == "stats":
        stats = manager.get_stats()
        print("胶囊库统计:")
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif args.action == "health":
        report = manager.get_health_report()
        print(f"健康度评分: {report['score']}/100")
        if report['recommendations']:
            print("\n建议:")
            for rec in report['recommendations']:
                print(f"  - {rec}")
    
    elif args.action == "apply":
        if not args.capsule_id:
            print("错误: 应用需要 --capsule-id 参数")
            return
        
        result = manager.apply_capsule(args.capsule_id, context=args.context or "")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "search":
        if not args.query:
            print("错误: 搜索需要 --query 参数")
            return
        
        results = manager.search_capsules(args.query)
        print(f"找到 {len(results)} 个匹配:\n")
        for c in results:
            print(f"  [{c['id']}] {c['name']} | confidence: {c.get('confidence', 0):.2f}")


if __name__ == "__main__":
    main()
