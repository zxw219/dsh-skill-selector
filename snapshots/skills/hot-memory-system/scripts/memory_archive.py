#!/usr/bin/env python3
"""
记忆归档管理模块
管理冷记忆的归档、检索和清理
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class MemoryArchiver:
    """记忆归档器"""
    
    def __init__(self, archive_path: str = "./memory_archive"):
        self.archive_path = Path(archive_path)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.archive_path / "index.json"
        self._load_index()
    
    def _load_index(self):
        """加载索引文件"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {"archives": [], "categories": {}}
    
    def _save_index(self):
        """保存索引文件"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def archive(self, content: str, title: str, category: str = "general", 
                tags: List[str] = None, metadata: Dict = None) -> str:
        """
        归档记忆
        
        Args:
            content: 记忆内容
            title: 标题
            category: 分类
            tags: 标签列表
            metadata: 额外元数据
            
        Returns:
            归档ID
        """
        archive_id = f"archive_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 创建归档文件
        archive_file = self.archive_path / f"{archive_id}.json"
        archive_data = {
            "id": archive_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(archive_data, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        self.index["archives"].append({
            "id": archive_id,
            "title": title,
            "category": category,
            "tags": tags or [],
            "created_at": archive_data["created_at"]
        })
        
        # 更新分类统计
        if category not in self.index["categories"]:
            self.index["categories"][category] = []
        self.index["categories"][category].append(archive_id)
        
        self._save_index()
        
        return archive_id
    
    def retrieve(self, archive_id: str) -> Optional[Dict]:
        """检索归档"""
        archive_file = self.archive_path / f"{archive_id}.json"
        if archive_file.exists():
            with open(archive_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def search(self, query: str, category: str = None, 
               tags: List[str] = None) -> List[Dict]:
        """搜索归档"""
        results = []
        
        for archive_info in self.index["archives"]:
            # 分类过滤
            if category and archive_info["category"] != category:
                continue
            
            # 标签过滤
            if tags:
                if not any(tag in archive_info.get("tags", []) for tag in tags):
                    continue
            
            # 内容搜索
            archive = self.retrieve(archive_info["id"])
            if archive and query.lower() in archive["content"].lower():
                results.append(archive)
            elif archive and query.lower() in archive["title"].lower():
                results.append(archive)
        
        return results
    
    def list_by_category(self, category: str) -> List[Dict]:
        """按分类列出归档"""
        results = []
        for archive_id in self.index["categories"].get(category, []):
            archive = self.retrieve(archive_id)
            if archive:
                results.append(archive)
        return results
    
    def update(self, archive_id: str, content: str = None,
               title: str = None, tags: List[str] = None) -> bool:
        """更新归档"""
        archive = self.retrieve(archive_id)
        if not archive:
            return False
        
        if content:
            archive["content"] = content
        if title:
            archive["title"] = title
        if tags:
            archive["tags"] = tags
        
        archive["updated_at"] = datetime.now().isoformat()
        
        archive_file = self.archive_path / f"{archive_id}.json"
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(archive, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        for idx, info in enumerate(self.index["archives"]):
            if info["id"] == archive_id:
                self.index["archives"][idx]["title"] = archive["title"]
                self.index["archives"][idx]["tags"] = archive["tags"]
                break
        
        self._save_index()
        return True
    
    def delete(self, archive_id: str) -> bool:
        """删除归档"""
        archive_file = self.archive_path / f"{archive_id}.json"
        if archive_file.exists():
            archive_file.unlink()
            
            # 从索引中移除
            self.index["archives"] = [
                a for a in self.index["archives"] if a["id"] != archive_id
            ]
            
            # 从分类中移除
            for category in self.index["categories"]:
                self.index["categories"][category] = [
                    aid for aid in self.index["categories"][category] 
                    if aid != archive_id
                ]
            
            self._save_index()
            return True
        return False
    
    def get_categories(self) -> Dict[str, int]:
        """获取所有分类及其数量"""
        return {
            cat: len(ids) 
            for cat, ids in self.index["categories"].items()
        }


if __name__ == "__main__":
    archiver = MemoryArchiver()
    
    # 测试归档
    archive_id = archiver.archive(
        title="项目X技术方案",
        content="这是详细的技术方案内容...",
        category="project",
        tags=["技术", "方案", "重要"]
    )
    print(f"归档ID: {archive_id}")
    
    # 搜索
    results = archiver.search("技术方案")
    print(f"搜索结果: {len(results)} 条")
    
    # 按分类列出
    results = archiver.list_by_category("project")
    print(f"项目分类: {len(results)} 条")
    
    # 获取分类
    categories = archiver.get_categories()
    print(f"分类统计: {categories}")
