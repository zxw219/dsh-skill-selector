#!/usr/bin/env python3
"""
任务复杂度分类器
自动判断任务复杂度等级（L1-L4）
"""

import re
from typing import Dict, Tuple

class TaskClassifier:
    """任务复杂度分类器"""
    
    # L1特征：简单问答
    L1_INDICATORS = [
        r"^(你好|hi|hello|hey)",  # 问候语
        r"^(什么是|什么叫)",  # 简单定义
        r"^(请问|问一下)",  # 简单询问
        r"今天天气|现在时间|当前时间",  # 简单查询
        r"^(帮我|给我)(查一下|看一下)",  # 单次查询
    ]
    
    # L2特征：中等任务
    L2_INDICATORS = [
        r"搜索|查找|检索",
        r"总结|概括|归纳",
        r"比较|对比",
        r"分析|解读",
        r"(帮我|给我).*(并|然后)",  # 简单串联
    ]
    
    # L3特征：复杂任务
    L3_INDICATORS = [
        r"(深度|详细|全面)(分析|研究|调研)",
        r"(多|很多|大量).*(方面|维度|角度)",
        r"(系统|完整|彻底)(梳理|整理|处理)",
        r"(制作|生成|编写).*(报告|方案|计划)",
        r"(综合|整合|汇总).*(数据|信息|资料)",
    ]
    
    # L4特征：长期任务
    L4_INDICATORS = [
        r"(批量|大规模|海量)(处理|生成|分析)",
        r"(后台|异步|离线)(处理|运行|执行)",
        r"(定时|定期|周期)(任务|处理|运行)",
        r"(持续|长期|监控)",
        r"(10万|100万|1000万|亿).*(数据|记录|条目)",
    ]
    
    @classmethod
    def classify(cls, task: str) -> Tuple[int, str]:
        """
        分类任务复杂度
        
        Args:
            task: 任务描述
            
        Returns:
            (level, reason): 复杂度等级和判断理由
        """
        task_lower = task.lower()
        
        # 检查L4（最高优先级）
        for pattern in cls.L4_INDICATORS:
            if re.search(pattern, task_lower):
                return 4, "检测到长期任务特征：批量处理/大规模数据/后台运行"
        
        # 检查L3
        for pattern in cls.L3_INDICATORS:
            if re.search(pattern, task_lower):
                return 3, "检测到复杂任务特征：深度分析/多维度处理/系统整理"
        
        # 检查L2
        for pattern in cls.L2_INDICATORS:
            if re.search(pattern, task_lower):
                return 2, "检测到中等任务特征：搜索/总结/比较/分析"
        
        # 检查L1（默认）
        for pattern in cls.L1_INDICATORS:
            if re.search(pattern, task_lower):
                return 1, "检测到简单问答特征：单轮对话/无需工具调用"
        
        # 未知情况，默认为L2
        return 2, "默认分类为中等任务"
    
    @classmethod
    def get_strategy(cls, level: int) -> Dict:
        """
        获取执行策略
        
        Args:
            level: 复杂度等级
            
        Returns:
            策略字典
        """
        strategies = {
            1: {
                "name": "L1 简单问答",
                "response_mode": "immediate",
                "notification": None,
                "estimated_time": "<5秒"
            },
            2: {
                "name": "L2 中等任务",
                "response_mode": "start_complete",
                "notification": ["start", "complete"],
                "estimated_time": "5-30秒"
            },
            3: {
                "name": "L3 复杂任务",
                "response_mode": "progress",
                "notification": ["start", "progress_30s", "complete"],
                "estimated_time": "30秒-5分钟"
            },
            4: {
                "name": "L4 长期任务",
                "response_mode": "async",
                "notification": ["queued", "complete"],
                "estimated_time": ">5分钟"
            }
        }
        return strategies.get(level, strategies[2])


def classify_task(task: str) -> Dict:
    """
    便捷函数：分类任务
    
    Args:
        task: 任务描述
        
    Returns:
        包含level、strategy、reason的字典
    """
    level, reason = TaskClassifier.classify(task)
    strategy = TaskClassifier.get_strategy(level)
    
    return {
        "level": level,
        "reason": reason,
        "strategy": strategy
    }


if __name__ == "__main__":
    # 测试用例
    test_tasks = [
        "你好，今天天气怎么样？",
        "帮我搜索一下AI的最新发展动态",
        "请深度分析2024年新能源市场的发展趋势",
        "批量处理这100万条数据",
        "什么是机器学习？"
    ]
    
    for task in test_tasks:
        result = classify_task(task)
        print(f"任务: {task}")
        print(f"  等级: L{result['level']}")
        print(f"  理由: {result['reason']}")
        print(f"  策略: {result['strategy']['name']}")
        print()
