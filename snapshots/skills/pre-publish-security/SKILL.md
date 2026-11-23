---
name: pre-publish-security
description: 在发布代码或内容前检查密钥、外部域名、用户数据、危险函数、依赖与许可证问题，并给出阻断、警告和修复建议。A pre-publication security audit for secrets, external domains, user-data exposure, dangerous functions, dependencies, and license concerns, with blockers, warnings, and repair guidance.
metadata:
  version: 1.0.0
version: "1.0.0"
---

# 发布前安检（Pre-publish Security）

## 功能概述
代码/内容发布前的全面安全检查，确保发布安全。

## 检查项目

### 1. 密钥/凭证检测
- API密钥
- 数据库密码
- OAuth密钥
- JWT密钥
- 云服务凭证

### 2. 外部API域名白名单
检查所有外部API调用：
- 必须在白名单内
- 禁止调用未授权域名
- 记录所有API依赖

### 3. 用户数据外泄风险
- 个人信息泄露检测
- 敏感数据脱敏检查
- 日志脱敏验证

### 4. 代码安全
检查危险函数：
- `eval()` - 代码注入风险
- `exec()` - 代码注入风险
- `json.loads()` - 需要验证输入
- `subprocess` - 命令注入风险
- `os.system` - 命令注入风险

### 5. 依赖安全
- 检查已知漏洞库
- 检查版本兼容性
- 许可证合规性

## 检查流程

```
准备发布
    ↓
密钥检测 → 发现 → 阻止并标记
    ↓
域名白名单 → 未授权 → 阻止
    ↓
数据泄露 → 风险 → 要求确认
    ↓
代码安全 → 危险函数 → 警告
    ↓
依赖检查 → 漏洞 → 警告
    ↓
全部通过 → 允许发布
```

## 使用方法

### 自动检查
发布前自动执行所有检查项。

### 检查报告
生成详细检查报告，包括：
- 检查项列表
- 发现问题
- 修复建议
- 最终结论

## 注意事项
- 安全检查优先于发布
- 警告级别需要人工确认
- 禁止绕过安全检查
