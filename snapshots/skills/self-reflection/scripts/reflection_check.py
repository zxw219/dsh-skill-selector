#!/usr/bin/env python3
"""
自我反思检查模块
诚实性检查和置信度评估
"""

import re
from enum import Enum
from typing import Dict, List, Tuple, Optional

class ConfidenceLevel(Enum):
    CERTAIN = ("确定", "✅")
    LIKELY = ("较确定", "⚠️")
    UNCERTAIN = ("不确定", "❓")
    UNKNOWN = ("不知道", "❌")

class ReflectionChecker:
    ABSOLUTE_WORDS = ["绝对", "肯定", "一定", "完全", "所有", "全部", "每个"]
    
    def __init__(self):
        self.last_check = None
    
    def check(self, response: str, context: str = "") -> Dict:
        warnings = []
        suggestions = []
        modified = response
        
        # 事实性检查
        has_source = any(w in response for w in ["根据", "显示", "研究"])
        has_absolute = any(w in response for w in self.ABSOLUTE_WORDS)
        
        if has_source and not has_absolute:
            fact_status, factuality = "✅", "有来源依据"
        elif has_absolute:
            fact_status, factuality = "⚠️", "建议保守表述"
        else:
            fact_status, factuality = "⚠️", "无法验证"
        
        # 承诺度检查
        for word in self.ABSOLUTE_WORDS:
            if word in modified:
                replacement = {"绝对": "通常", "肯定": "很可能", "一定": "可能会", 
                              "完全": "基本", "所有": "大多数", "全部": "大部分"}
                modified = modified.replace(word, replacement.get(word, "可能"))
        
        commit_status = "⚠️" if modified != response else "✅"
        commitment = "已修改" if commit_status == "⚠️" else "无过度承诺"
        
        # 置信度
        if fact_status == "✅" and commit_status == "✅":
            confidence = ConfidenceLevel.CERTAIN
        elif fact_status == "⚠️":
            confidence = ConfidenceLevel.LIKELY
        else:
            confidence = ConfidenceLevel.UNCERTAIN
        
        result = {
            "factuality": factuality,
            "factuality_status": fact_status,
            "commitment": commitment,
            "commitment_status": commit_status,
            "confidence": confidence,
            "warnings": warnings,
            "suggestions": suggestions,
            "modified_response": modified if modified != response else None
        }
        
        self.last_check = result
        return result
    
    def format_result(self, result: Dict) -> str:
        lines = [
            "【反思检查】",
            f"- 事实性：{result['factuality_status']} {result['factuality']}",
            f"- 承诺度：{result['commitment_status']} {result['commitment']}",
            f"- 置信度：{result['confidence'].icon} {result['confidence'].label}",
        ]
        if result['suggestions']:
            lines.append(f"- 建议：{' '.join(result['suggestions'])}")
        return "\n".join(lines)


if __name__ == "__main__":
    checker = ReflectionChecker()
    test = "根据数据显示，这个方案绝对可行。"
    result = checker.check(test)
    print(checker.format_result(result))
