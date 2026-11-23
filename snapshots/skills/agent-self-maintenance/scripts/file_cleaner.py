#!/usr/bin/env python3
"""
File Cleaner - 文件清理工具
用于定期维护和清理Agent记忆系统
"""

import json
import os
import shutil
import fnmatch
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class FileCleaner:
    """文件清理工具"""
    
    def __init__(self, base_dir: str = "./memory"):
        self.base_dir = Path(base_dir)
        self.backup_dir = self.base_dir / "backup"
        self.daily_dir = self.base_dir / "daily"
        
        # 确保目录存在
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.daily_dir.mkdir(parents=True, exist_ok=True)
    
    # ==================== 完整性检查 ====================
    
    def check_json_integrity(self, filepath: str) -> Tuple[bool, str]:
        """检查JSON文件完整性"""
        path = Path(filepath)
        if not path.exists():
            return False, "文件不存在"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, "OK"
        except json.JSONDecodeError as e:
            return False, f"JSON损坏: {e}"
        except Exception as e:
            return False, f"错误: {e}"
    
    def check_all_critical_files(self) -> Dict:
        """检查所有关键文件"""
        critical_files = [
            "capsules.json",
            "emotion_state.json",
            "error_log.jsonl",
            "brainloop_log.json"
        ]
        
        results = {"passed": [], "failed": []}
        
        for filename in critical_files:
            filepath = self.base_dir / filename
            if filepath.exists():
                is_ok, msg = self.check_json_integrity(str(filepath))
                if is_ok:
                    results["passed"].append({"file": filename, "status": msg})
                else:
                    results["failed"].append({"file": filename, "status": msg})
            else:
                results["failed"].append({"file": filename, "status": "文件不存在"})
        
        return results
    
    # ==================== 备份操作 ====================
    
    def backup_file(self, filepath: str) -> Optional[str]:
        """备份单个文件"""
        path = Path(filepath)
        if not path.exists():
            return None
        
        today = datetime.now().strftime("%Y-%m-%d")
        backup_subdir = self.backup_dir / today
        backup_subdir.mkdir(parents=True, exist_ok=True)
        
        backup_path = backup_subdir / path.name
        shutil.copy2(filepath, backup_path)
        
        return str(backup_path)
    
    def backup_critical_files(self) -> List[str]:
        """备份所有关键文件"""
        critical_files = ["capsules.json", "emotion_state.json"]
        backed_up = []
        
        for filename in critical_files:
            filepath = self.base_dir / filename
            if filepath.exists():
                backup_path = self.backup_file(str(filepath))
                if backup_path:
                    backed_up.append(backup_path)
        
        # 清理旧备份（保留7天）
        self.cleanup_old_backups(days=7)
        
        return backed_up
    
    def restore_from_backup(self, filename: str, 
                           backup_date: Optional[str] = None) -> bool:
        """从备份恢复文件"""
        if backup_date:
            backup_path = self.backup_dir / backup_date / filename
        else:
            # 找最新的备份
            backup_dates = sorted(
                [d.name for d in self.backup_dir.iterdir() if d.is_dir()],
                reverse=True
            )
            for date in backup_dates:
                candidate = self.backup_dir / date / filename
                if candidate.exists():
                    backup_path = candidate
                    break
            else:
                return False
        
        if not backup_path.exists():
            return False
        
        target_path = self.base_dir / filename
        shutil.copy2(backup_path, target_path)
        return True
    
    # ==================== 归档操作 ====================
    
    def count_jsonl_lines(self, filepath: str) -> int:
        """计算JSONL文件行数"""
        path = Path(filepath)
        if not path.exists():
            return 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    
    def archive_jsonl(self, filepath: str, max_lines: int = 500) -> Optional[str]:
        """归档超限的JSONL文件"""
        line_count = self.count_jsonl_lines(filepath)
        
        if line_count <= max_lines:
            return None
        
        path = Path(filepath)
        today = datetime.now().strftime("%Y-%m-%d")
        archive_subdir = self.daily_dir / today
        archive_subdir.mkdir(parents=True, exist_ok=True)
        
        # 归档文件名：原名_日期_序号.jsonl
        archive_name = f"{path.stem}_{today}_001{path.suffix}"
        archive_path = archive_subdir / archive_name
        
        # 移动文件到归档
        shutil.move(str(path), str(archive_path))
        
        # 创建新的空文件
        path.touch()
        
        return str(archive_path)
    
    def archive_old_events(self, days: int = 30) -> int:
        """归档历史事件"""
        archived = 0
        
        for jsonl_file in self.base_dir.glob("*.jsonl"):
            line_count = self.count_jsonl_lines(str(jsonl_file))
            if line_count > 100:  # 超过100条就归档
                result = self.archive_jsonl(str(jsonl_file), max_lines=500)
                if result:
                    archived += 1
        
        return archived
    
    # ==================== 清理操作 ====================
    
    def cleanup_old_backups(self, days: int = 7) -> List[str]:
        """清理过期备份"""
        cutoff = datetime.now() - timedelta(days=days)
        removed = []
        
        for backup_date_dir in self.backup_dir.iterdir():
            if not backup_date_dir.is_dir():
                continue
            
            try:
                dir_date = datetime.strptime(backup_date_dir.name, "%Y-%m-%d")
                if dir_date < cutoff:
                    shutil.rmtree(backup_date_dir)
                    removed.append(str(backup_date_dir))
            except ValueError:
                # 不是日期格式，跳过
                continue
        
        return removed
    
    def cleanup_old_archives(self, days: int = 90) -> List[str]:
        """清理过期归档"""
        cutoff = datetime.now() - timedelta(days=days)
        removed = []
        
        for archive_date_dir in self.daily_dir.iterdir():
            if not archive_date_dir.is_dir():
                continue
            
            try:
                dir_date = datetime.strptime(archive_date_dir.name, "%Y-%m-%d")
                if dir_date < cutoff:
                    shutil.rmtree(archive_date_dir)
                    removed.append(str(archive_date_dir))
            except ValueError:
                continue
        
        return removed
    
    def cleanup_temp_files(self, pattern: str = "tmp_*", days: int = 1) -> List[str]:
        """清理临时文件"""
        cutoff = datetime.now() - timedelta(days=days)
        removed = []
        
        for path in Path(".").glob(pattern):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if mtime < cutoff:
                    path.unlink()
                    removed.append(str(path))
        
        return removed
    
    def cleanup_empty_dirs(self, base_dir: Optional[str] = None) -> List[str]:
        """清理空目录"""
        if base_dir is None:
            base_dir = "."
        
        removed = []
        for root, dirs, files in os.walk(base_dir, topdown=False):
            for dirname in dirs:
                dirpath = Path(root) / dirname
                if not any(dirpath.iterdir()):  # 空目录
                    dirpath.rmdir()
                    removed.append(str(dirpath))
        
        return removed
    
    # ==================== 维护任务 ====================
    
    def run_daily_maintenance(self) -> Dict:
        """执行每日维护"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "file_check": self.check_all_critical_files(),
            "backup_result": [],
            "archive_result": [],
            "temp_cleanup": [],
            "success": True,
            "errors": []
        }
        
        # 1. 文件完整性检查
        if report["file_check"]["failed"]:
            report["success"] = False
            report["errors"].append("部分文件检查失败")
        
        # 2. 备份关键文件
        report["backup_result"] = self.backup_critical_files()
        
        # 3. 归档历史事件
        archived = self.archive_old_events()
        report["archive_result"] = {"files_archived": archived}
        
        # 4. 清理临时文件
        report["temp_cleanup"] = self.cleanup_temp_files(days=1)
        
        return report
    
    def run_weekly_maintenance(self) -> Dict:
        """执行每周维护"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "daily_maintenance": self.run_daily_maintenance(),
            "old_backups_cleaned": [],
            "empty_dirs_cleaned": [],
            "success": True
        }
        
        # 清理旧备份
        report["old_backups_cleaned"] = self.cleanup_old_backups(days=7)
        
        # 清理空目录
        report["empty_dirs_cleaned"] = self.cleanup_empty_dirs(str(self.base_dir))
        
        return report
    
    def run_monthly_maintenance(self) -> Dict:
        """执行每月维护"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "weekly_maintenance": self.run_weekly_maintenance(),
            "old_archives_cleaned": [],
            "success": True
        }
        
        # 清理3个月前的归档
        report["old_archives_cleaned"] = self.cleanup_old_archives(days=90)
        
        return report
    
    # ==================== 软限制检查 ====================
    
    def check_soft_limits(self) -> Dict:
        """检查软限制"""
        alerts = []
        
        # 胶囊数量
        capsules_file = self.base_dir / "capsules.json"
        if capsules_file.exists():
            try:
                with open(capsules_file, 'r', encoding='utf-8') as f:
                    capsules = json.load(f)
                if len(capsules) > 80:
                    alerts.append({
                        "type": "capsule_count",
                        "level": "warning",
                        "message": f"胶囊数量 {len(capsules)} 接近限制(100)"
                    })
            except:
                pass
        
        # 错误日志行数
        error_log = self.base_dir / "error_log.jsonl"
        if error_log.exists():
            line_count = self.count_jsonl_lines(str(error_log))
            if line_count > 400:
                alerts.append({
                    "type": "error_log_size",
                    "level": "warning",
                    "message": f"错误日志 {line_count} 条，建议归档"
                })
        
        return {
            "alerts": alerts,
            "alert_count": len(alerts)
        }
    
    # ==================== 健康度 ====================
    
    def get_health_score(self) -> int:
        """计算系统健康度"""
        score = 100
        
        # 检查文件完整性
        check_result = self.check_all_critical_files()
        score -= len(check_result["failed"]) * 15
        
        # 检查软限制
        alerts = self.check_soft_limits()
        score -= alerts["alert_count"] * 5
        
        # 检查备份
        if not list(self.backup_dir.glob("*")):
            score -= 10
        
        return max(0, score)
    
    def get_full_report(self) -> Dict:
        """获取完整健康报告"""
        return {
            "health_score": self.get_health_score(),
            "file_integrity": self.check_all_critical_files(),
            "soft_limits": self.check_soft_limits(),
            "backup_count": len(list(self.backup_dir.glob("*/*"))) if self.backup_dir.exists() else 0,
            "archive_count": len(list(self.daily_dir.glob("*/*"))) if self.daily_dir.exists() else 0
        }


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="文件清理工具")
    parser.add_argument("--dir", default="./memory", help="基础目录")
    parser.add_argument("action", choices=["daily", "weekly", "monthly", 
                                          "check", "backup", "health", "clean"],
                       help="操作类型")
    parser.add_argument("--days", type=int, default=7, help="天数阈值")
    
    args = parser.parse_args()
    cleaner = FileCleaner(args.dir)
    
    if args.action == "daily":
        result = cleaner.run_daily_maintenance()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "weekly":
        result = cleaner.run_weekly_maintenance()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "monthly":
        result = cleaner.run_monthly_maintenance()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "check":
        result = cleaner.check_all_critical_files()
        print("文件完整性检查:")
        print(f"  通过: {len(result['passed'])}")
        print(f"  失败: {len(result['failed'])}")
        if result['failed']:
            for f in result['failed']:
                print(f"    - {f['file']}: {f['status']}")
    
    elif args.action == "backup":
        result = cleaner.backup_critical_files()
        print(f"已备份 {len(result)} 个文件:")
        for f in result:
            print(f"  - {f}")
    
    elif args.action == "health":
        score = cleaner.get_health_score()
        print(f"健康度评分: {score}/100")
        
        soft_limits = cleaner.check_soft_limits()
        if soft_limits["alerts"]:
            print("\n告警:")
            for alert in soft_limits["alerts"]:
                print(f"  [{alert['level']}] {alert['message']}")
    
    elif args.action == "clean":
        if args.days:
            removed = cleaner.cleanup_old_backups(days=args.days)
            print(f"清理了 {len(removed)} 个过期备份")
            for r in removed:
                print(f"  - {r}")


if __name__ == "__main__":
    main()
