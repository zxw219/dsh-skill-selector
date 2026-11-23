#!/usr/bin/env python3
"""
记忆蒸馏模块
自动将热记忆蒸馏为暖记忆和冷记忆
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

class MemoryDistiller:
    """记忆蒸馏器"""
    
    # 重要关键词（标记冷记忆）
    IMPORTANCE_KEYWORDS = [
        "重要", "关键", "核心", "必须记住",
        "长期", "永久", "项目", "客户",
        "决策", "结论", "方案", "合同"
    ]
    
    # 中等重要性（暖记忆）
    MEDIUM_IMPORTANCE = [
        "任务", "待办", "计划", "安排",
        "进度", "状态", "进度"
    ]
    
    def __init__(self, storage_path: str = "./memory_storage"):
        self.storage_path = Path(storage_path)
        self.hot_memory = []
        self.warm_memory = []
        self.cold_memory = []
        self._load_memories()
    
    def _load_memories(self):
        """加载已有记忆"""
        # 加载暖记忆
        warm_file = self.storage_path / "warm_memory.json"
        if warm_file.exists():
            with open(warm_file, 'r', encoding='utf-8') as f:
                self.warm_memory = json.load(f)
        
        # 加载冷记忆
        cold_file = self.storage_path / "cold_memory.json"
        if cold_file.exists():
            with open(cold_file, 'r', encoding='utf-8') as f:
                self.cold_memory = json.load(f)
    
    def _save_memories(self):
        """保存记忆到文件"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # 保存暖记忆
        warm_file = self.storage_path / "warm_memory.json"
        with open(warm_file, 'w', encoding='utf-8') as f:
            json.dump(self.warm_memory, f, ensure_ascii=False, indent=2)
        
        # 保存冷记忆
        cold_file = self.storage_path / "cold_memory.json"
        with open(cold_file, 'w', encoding='utf-8') as f:
            json.dump(self.cold_memory, f, ensure_ascii=False, indent=2)
    
    def add_hot_memory(self, content: str, source: str = "session"):
        """添加热记忆"""
        memory = {
            "content": content,
            "source": source,
            "created_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": datetime.now().isoformat()
        }
        self.hot_memory.append(memory)
        return memory
    
    def distill(self) -> Dict:
        """
        蒸馏记忆
        将热记忆分类到暖记忆或冷记忆
        """
        results = {"warm": [], "cold": [], "cleared": []}
        
        for memory in self.hot_memory:
            # 判断重要性
            importance = self._judge_importance(memory["content"])
            
            if importance == "cold":
                self.cold_memory.append({
                    **memory,
                    "archived_at": datetime.now().isoformat(),
                    "category": "permanent"
                })
                results["cold"].append(memory["content"][:50])
            elif importance == "warm":
                self.warm_memory.append({
                    **memory,
                    "created_at": datetime.now().isoformat()  # 重置时间
                })
                results["warm"].append(memory["content"][:50])
            else:
                results["cleared"].append(memory["content"][:50])
        
        # 清空热记忆
        self.hot_memory.clear()
        
        # 保存到文件
        self._save_memories()
        
        return results
    
    def _judge_importance(self, content: str) -> str:
        """判断记忆重要性"""
        content_lower = content.lower()
        
        # 检查冷记忆关键词
        for keyword in self.IMPORTANCE_KEYWORDS:
            if keyword in content:
                return "cold"
        
        # 检查暖记忆关键词
        for keyword in self.MEDIUM_IMPORTANCE:
            if keyword in content:
                return "warm"
        
        return "clear"
    
    def cleanup_expired(self, days: int = 7) -> List:
        """清理过期的暖记忆"""
        cutoff = datetime.now() - timedelta(days=days)
        results = []
        
        new_warm = []
        for memory in self.warm_memory:
            created = datetime.fromisoformat(memory["created_at"])
            if created < cutoff:
                results.append(memory["content"][:50])
            else:
                new_warm.append(memory)
        
        self.warm_memory = new_warm
        self._save_memories()
        
        return results
    
    def search(self, query: str, scope: str = "all") -> List:
        """
        搜索记忆
        
        Args:
            query: 搜索关键词
            scope: 搜索范围 (all/hot/warm/cold)
        """
        results = []
        search_scopes = []
        
        if scope == "all":
            search_scopes = ["hot", "warm", "cold"]
        else:
            search_scopes = [scope]
        
        if "hot" in search_scopes:
            for memory in self.hot_memory:
                if query.lower() in memory["content"].lower():
                    results.append(("hot", memory))
        
        if "warm" in search_scopes:
            for memory in self.warm_memory:
                if query.lower() in memory["content"].lower():
                    results.append(("warm", memory))
        
        if "cold" in search_scopes:
            for memory in self.cold_memory:
                if query.lower() in memory["content"].lower():
                    results.append(("cold", memory))
        
        return results
    
    def get_summary(self) -> Dict:
        """获取记忆摘要"""
        return {
            "hot_count": len(self.hot_memory),
            "warm_count": len(self.warm_memory),
            "cold_count": len(self.cold_memory),
            "last_distill": datetime.now().isoformat()
        }


if __name__ == "__main__":
    distiller = MemoryDistiller()
    
    # 测试添加记忆
    distiller.add_hot_memory("这是一个重要项目决策，需要永久记住")
    distiller.add_hot_memory("今天的待办任务清单")
    distiller.add_hot_memory("用户问了一个简单问题")
    
    # 蒸馏
    results = distiller.distill()
    print("蒸馏结果:", results)
    
    # 搜索
    results = distiller.search("重要")
    print("搜索结果:", results)
    
    # 摘要
    summary = distiller.get_summary()
    print("记忆摘要:", summary)
