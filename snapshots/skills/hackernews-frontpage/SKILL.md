---
name: hackernews-frontpage
description: 获取 Hacker News 首页热门新闻，列出标题、链接、分数和评论数；用户想看 HN 热门、科技新闻或 Hacker News 首页时使用。
metadata:
  version: "1.1.0-local"
  source: "独立适配自 garrytan/gstack 的 hackernews-frontpage；使用 Hacker News 公共数据"
---

# Hacker News 首页

获取当前 Hacker News 热门条目。使用当前可用的网页读取、HTTP 请求或浏览器工具，无需 GStack 或 Browser Use 程序。

## 获取方法

- 优先读取 https://news.ycombinator.com/ ，保留首页顺序。默认最多 30 条，用户指定数量时按需调整。
- 无法可靠提取首页时，使用官方公共 API https://hacker-news.firebaseio.com/v0/topstories.json 获取条目 ID，再读取 https://hacker-news.firebaseio.com/v0/item/{id}.json 。接口文档为 https://github.com/HackerNews/API 。说明此时使用 topstories 排序，可能与浏览器首页因时间或个性化而稍有不同。
- 从实时响应提取标题、原文链接、分数、评论数和讨论链接。API 对应字段为 title、url、score、descendants；讨论链接为 https://news.ycombinator.com/item?id={id} 。没有 url 时使用讨论链接；缺失字段标为未知，不编造。
- 报告获取时间。失败或部分条目无法读取时说明实际范围，不把旧数据说成当前新闻。

## 输出

默认用中文简洁列表或表格，提供标题、原文链接、分数、评论数及讨论链接。按用户要求可输出 JSON：stories 中包含 rank、title、url、points、comment_count、discussion_url，并包含实际返回的 count。

只看过标题时只翻译或概述标题；需要文章内容总结时，先读取原文。
