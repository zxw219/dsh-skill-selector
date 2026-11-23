#!/usr/bin/env python3
"""
素材整理归档模块
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AssetOrganizer:
    """素材整理器"""
    
    TAG_CATEGORIES = {
        "scene": ["indoor", "outdoor", "studio", "location"],
        "subject": ["portrait", "group", "crowd", "solo"],
        "mood": ["positive", "negative", "neutral", "emotional"],
        "tech": ["4K", "1080P", "720P", "raw", "log", "slowmo"]
    }
    
    FILE_TYPES = {
        "video": [".mp4", ".mov", ".avi", ".mkv"],
        "image": [".jpg", ".jpeg", ".png", ".raw", ".tiff"],
        "audio": [".mp3", ".wav", ".aac", ".flac"],
        "document": [".pdf", ".doc", ".docx", ".txt"]
    }
    
    def __init__(self, base_path: str = "./assets"):
        self.base_path = Path(base_path)
        self.index_file = self.base_path / "asset_index.json"
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """加载索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"assets": [], "projects": {}, "tags": {}}
    
    def _save_index(self):
        """保存索引"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _detect_type(self, filename: str) -> str:
        """检测文件类型"""
        ext = Path(filename).suffix.lower()
        for file_type, extensions in self.FILE_TYPES.items():
            if ext in extensions:
                return file_type
        return "unknown"
    
    def register(self, filepath: str, project: str = "general",
                tags: List[str] = None, notes: str = "") -> Dict:
        """注册素材"""
        filename = Path(filepath).name
        asset_type = self._detect_type(filename)
        
        # 生成标准命名
        date_str = datetime.now().strftime("%Y-%m-%d")
        new_name = f"{date_str}_{project}_{asset_type}"
        if tags:
            new_name += f"_{'_'.join(tags[:2])}"
        
        asset = {
            "id": f"asset_{len(self.index['assets']) + 1}",
            "filename": filename,
            "project": project,
            "type": asset_type,
            "tags": tags or [],
            "notes": notes,
            "registered_at": datetime.now().isoformat(),
            "path": str(filepath)
        }
        
        self.index["assets"].append(asset)
        
        # 更新项目索引
        if project not in self.index["projects"]:
            self.index["projects"][project] = []
        self.index["projects"][project].append(asset["id"])
        
        # 更新标签索引
        for tag in (tags or []):
            if tag not in self.index["tags"]:
                self.index["tags"][tag] = []
            self.index["tags"][tag].append(asset["id"])
        
        self._save_index()
        return asset
    
    def search(self, query: str = "", project: str = None,
               tags: List[str] = None) -> List[Dict]:
        """搜索素材"""
        results = self.index["assets"]
        
        # 按项目筛选
        if project:
            results = [a for a in results if a["project"] == project]
        
        # 按标签筛选
        if tags:
            results = [a for a in results 
                      if all(tag in a.get("tags", []) for tag in tags)]
        
        # 按关键词搜索
        if query:
            query_lower = query.lower()
            results = [a for a in results
                      if query_lower in a["filename"].lower()
                      or query_lower in a.get("notes", "").lower()]
        
        return results
    
    def get_project_summary(self, project: str) -> Dict:
        """获取项目素材统计"""
        assets = self.search(project=project)
        
        summary = {
            "project": project,
            "total": len(assets),
            "by_type": {},
            "by_tag": {}
        }
        
        for asset in assets:
            # 按类型统计
            asset_type = asset["type"]
            summary["by_type"][asset_type] = summary["by_type"].get(asset_type, 0) + 1
            
            # 按标签统计
            for tag in asset.get("tags", []):
                summary["by_tag"][tag] = summary["by_tag"].get(tag, 0) + 1
        
        return summary


if __name__ == "__main__":
    organizer = AssetOrganizer()
    
    # 注册素材
    asset = organizer.register(
        filepath="video_001.mp4",
        project="TestProject",
        tags=["indoor", "4K", "portrait"],
        notes="测试视频"
    )
    print(f"注册成功: {asset['id']}")
    
    # 搜索
    results = organizer.search(project="TestProject")
    print(f"找到 {len(results)} 条素材")
    
    # 项目统计
    summary = organizer.get_project_summary("TestProject")
    print(f"项目统计: {summary}")
