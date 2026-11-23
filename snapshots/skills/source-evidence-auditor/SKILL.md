---
name: source-evidence-auditor
description: Audits research claims against their supporting sources, dates, provenance, directness, and cross-source agreement; flags stale, unsupported, overstated, or citation-unready statements; and produces a repair plan. 审计研究结论与信源之间的证据链，检查时效、出处、直接性和交叉印证，定位无依据、过度表述或不可引用的问题并给出修复方案。
version: "1.0.0"
---

# Source Evidence Auditor｜信源证据审计器

Check whether a report, briefing, article, recommendation, or decision memo says no more than its evidence supports.

## Core rule

Audit at the claim level, not merely at the document level. A credible source attached somewhere in a document does not automatically support every nearby statement.

## Workflow

### 1. Define the audit boundary

Identify:

- the artifact or claims being audited
- the relevant time window and jurisdiction
- the required confidence level
- whether citations must be publication-ready
- any source restrictions, such as primary sources only

For current, fast-changing, legal, medical, financial, political, pricing, schedule, product-specification, or software-version claims, verify against fresh sources rather than relying on memory.

### 2. Split prose into atomic claims

Separate statements that can independently be true or false. Distinguish:

- **Fact** — externally verifiable statement
- **Attribution** — what a person or organization said
- **Estimate** — modeled or approximate value
- **Interpretation** — reasoned reading of evidence
- **Prediction** — statement about future outcomes
- **Recommendation** — proposed action based on facts and judgment

Do not require a citation for pure framing or clearly labeled opinion, but do require evidence for the factual premises underneath it.

### 3. Map each claim to evidence

For every material claim, record:

- exact supporting source and locator
- source type and publisher
- publication date and event/data date
- whether the source is primary, secondary, or tertiary
- directness of support
- whether another independent source agrees or conflicts
- whether the claim wording exceeds the evidence

Use [references/evidence-matrix.md](references/evidence-matrix.md).

### 4. Score evidence fitness

Rate each dimension as Strong, Adequate, Weak, or Missing:

- **Authority** — expertise and responsibility for the information
- **Directness** — source actually establishes the claim rather than merely mentioning the topic
- **Freshness** — dates fit the claim's volatility and requested time window
- **Provenance** — original data, method, author, and publication path are traceable
- **Independence** — corroborating sources are not all repeating one origin
- **Citation readiness** — stable link or locator lets a reader verify the statement

Use consistent anchors: **Strong** means direct, current, traceable support with no material mismatch; **Adequate** means usable support with a minor limitation that does not change the claim; **Weak** means indirect, stale, incomplete, or materially limited support; **Missing** means no inspectable support for that dimension.

Treat a polished page, high search rank, or many reposts as presentation signals, not proof.

### 5. Assign a verdict

Use one verdict per claim:

- **Supported** — wording matches strong or adequate evidence
- **Supported with qualification** — core is supported but scope, date, or certainty must be narrowed
- **Disputed** — credible sources materially disagree
- **Unsupported** — no source directly supports the statement
- **Stale** — evidence is too old for the claim
- **Unverifiable** — source or underlying data cannot be inspected

Never convert absence of evidence into evidence of absence.

### 6. Repair the artifact

For every non-supported verdict, choose one action:

- add a primary or more direct source
- update the source or data date
- narrow the wording
- label the statement as estimate, inference, or prediction
- expose disagreement between sources
- remove the claim

Preserve useful nuance. Do not flatten uncertain evidence into false certainty.

### 7. Final gate

Before declaring the artifact citation-ready, confirm:

- every material factual claim has a mapped source
- dates and jurisdictions match the claim
- quotations and attributions point to the original speaker or record when available
- numbers retain units, scope, and denominator
- inferences are labeled as inferences
- cited links or locators actually reach the supporting material
- unresolved disputes are visible to the reader

## Output

Return:

1. audit scope and standard
2. claim-evidence matrix
3. blockers ordered by impact
4. corrected wording or sourcing action for each blocker
5. overall readiness: **Ready**, **Ready with qualifications**, or **Not ready**

If browsing or source access is unavailable, audit the supplied evidence only and clearly list which claims still require external verification.

In user-visible output, omit secrets, personal information, and unnecessary local paths unless the user explicitly needs them.
