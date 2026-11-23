# Direction catalog

Presets are starting points, not a closed taxonomy. Preserve user-written custom directions.

| Preset | Directions | Suggested weights |
|---|---|---|
| `ai-media-tech` | AI、影像、科技 | 1.0、0.9、0.8 |
| `business-markets` | 商业、财经、公司 | 1.0、1.0、0.8 |
| `creator-growth` | 内容创作、平台趋势、品牌营销 | 1.0、0.9、0.8 |
| `product-builder` | AI 产品、开发工具、开源项目 | 1.0、0.9、0.8 |
| `world-brief` | 国际、政策、经济 | 1.0、0.9、0.9 |
| `consumer-digital` | 消费电子、互联网产品、生活方式 | 1.0、0.9、0.7 |

## Query expansion

For each direction, combine the direction with event terms rather than searching the broad noun alone.

- releases: 发布、推出、上线、launch、release
- business: 收购、融资、上市、财报、acquisition、funding、earnings
- research: 论文、研究、benchmark、paper、study
- policy: 政策、监管、禁令、regulation、ban
- incidents: 故障、召回、泄露、outage、recall、breach

Use exclusions from the profile as negative terms where supported. Avoid query explosion: at most four web search queries per batch.

## Direction updates

- Replace directions when the user says “只看 / 主要看 / 改成”.
- Merge directions when the user says “再加 / 同时关注”.
- Keep weights in `[0.1, 2.0]`; default to `1.0`.
- Use direction text as the stable identifier after trimming and case-folding.
