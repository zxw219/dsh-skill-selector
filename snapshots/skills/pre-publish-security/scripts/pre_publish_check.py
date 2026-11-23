#!/usr/bin/env python3
"""
发布前安全检查模块
"""

import re
import json
from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

class IssueLevel(Enum):
    PASS = ("通过", "✅")
    WARNING = ("警告", "⚠️")
    FAIL = ("失败", "❌")

@dataclass
class SecurityIssue:
    category: str
    issue: str
    level: IssueLevel
    location: str = ""
    suggestion: str = ""

class PrePublishChecker:
    """发布前安全检查器"""
    
    # API白名单（可配置）
    ALLOWED_DOMAINS = [
        "api.openai.com",
        "api.anthropic.com",
        "api.coze.cn",
        "api.github.com",
        "api.twitter.com",
    ]
    
    # 密钥模式
    SECRET_PATTERNS = [
        (r"api[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9_-]{20,}", "API密钥"),
        (r"password\s*[=:]\s*['\"][^'\"]+['\"]", "密码硬编码"),
        (r"secret\s*[=:]\s*['\"]?[a-zA-Z0-9_-]{20,}", "密钥硬编码"),
        (r"token\s*[=:]\s*['\"]?[a-zA-Z0-9_-]{20,}", "Token硬编码"),
        (r"bearer\s+[a-zA-Z0-9_-]{20,}", "Bearer Token"),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub Token"),
        (r"sk-[a-zA-Z0-9]{48}", "OpenAI API Key"),
    ]
    
    # 危险函数
    DANGEROUS_FUNCTIONS = {
        "eval": "代码注入风险",
        "exec": "代码注入风险",
        "os.system": "命令注入风险",
        "subprocess": "命令注入风险",
        "pickle.load": "反序列化风险",
    }
    
    def __init__(self, allowed_domains: List[str] = None):
        self.allowed_domains = allowed_domains or self.ALLOWED_DOMAINS
    
    def check_file(self, content: str, filename: str = "") -> List[SecurityIssue]:
        """
        检查文件内容
        
        Args:
            content: 文件内容
            filename: 文件名
            
        Returns:
            问题列表
        """
        issues = []
        
        # 1. 密钥检测
        issues.extend(self._check_secrets(content, filename))
        
        # 2. 危险函数检测
        issues.extend(self._check_dangerous_functions(content, filename))
        
        # 3. API域名检测
        issues.extend(self._check_api_domains(content, filename))
        
        return issues
    
    def _check_secrets(self, content: str, filename: str) -> List[SecurityIssue]:
        """检测密钥硬编码"""
        issues = []
        
        for pattern, secret_type in self.SECRET_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # 隐藏敏感值
                masked = self._mask_secret(match.group())
                issues.append(SecurityIssue(
                    category="密钥检测",
                    issue=f"发现{secret_type}: {masked}",
                    level=IssueLevel.FAIL,
                    location=filename,
                    suggestion="使用环境变量或配置文件管理密钥"
                ))
        
        return issues
    
    def _mask_secret(self, secret: str) -> str:
        """掩码敏感信息"""
        if len(secret) <= 8:
            return "***"
        return secret[:4] + "***" + secret[-4:]
    
    def _check_dangerous_functions(self, content: str, 
                                   filename: str) -> List[SecurityIssue]:
        """检测危险函数"""
        issues = []
        
        for func, risk in self.DANGEROUS_FUNCTIONS.items():
            # 精确匹配函数名
            pattern = rf"\b{re.escape(func)}\s*\("
            if re.search(pattern, content):
                issues.append(SecurityIssue(
                    category="代码安全",
                    issue=f"使用危险函数: {func}",
                    level=IssueLevel.WARNING,
                    location=filename,
                    suggestion=f"注意{risk}，确保输入已验证"
                ))
        
        return issues
    
    def _check_api_domains(self, content: str, 
                          filename: str) -> List[SecurityIssue]:
        """检测API域名"""
        issues = []
        
        # 提取URL
        url_pattern = r"https?://([a-zA-Z0-9.-]+)"
        urls = re.findall(url_pattern, content)
        
        for domain in urls:
            # 检查是否在白名单
            is_allowed = any(
                allowed in domain or domain in allowed 
                for allowed in self.allowed_domains
            )
            
            if not is_allowed:
                issues.append(SecurityIssue(
                    category="域名白名单",
                    issue=f"调用未授权域名: {domain}",
                    level=IssueLevel.WARNING,
                    location=filename,
                    suggestion="请确认该域名可信并添加到白名单"
                ))
        
        return issues
    
    def generate_report(self, issues: List[SecurityIssue]) -> str:
        """生成检查报告"""
        if not issues:
            return "✅ 所有检查项通过，可以发布"
        
        lines = ["# 安全检查报告", ""]
        
        # 按类别分组
        by_category = {}
        for issue in issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)
        
        # 生成报告
        fail_count = sum(1 for i in issues if i.level == IssueLevel.FAIL)
        warn_count = sum(1 for i in issues if i.level == IssueLevel.WARNING)
        
        lines.append(f"检查结果: {fail_count}个失败, {warn_count}个警告")
        lines.append("")
        
        for category, category_issues in by_category.items():
            lines.append(f"## {category}")
            for issue in category_issues:
                icon = issue.level.value[1]
                lines.append(f"- {icon} {issue.issue}")
                if issue.suggestion:
                    lines.append(f"  建议: {issue.suggestion}")
            lines.append("")
        
        # 最终结论
        if fail_count > 0:
            lines.append("❌ 存在失败项，请修复后重新检查")
        elif warn_count > 0:
            lines.append("⚠️ 存在警告项，请确认后发布")
        else:
            lines.append("✅ 所有检查通过")
        
        return "\n".join(lines)


if __name__ == "__main__":
    checker = PrePublishChecker()
    
    # 测试代码
    test_code = '''
    import openai
    api_key = "sk-EXAMPLE-DO-NOT-USE"
    response = openai.ChatCompletion.create(
        api_key=api_key,
        api_base="https://custom-api.com/v1"  # 未授权域名
    )
    result = eval(user_input)  # 危险函数
    '''
    
    issues = checker.check_file(test_code, "test.py")
    print(checker.generate_report(issues))
