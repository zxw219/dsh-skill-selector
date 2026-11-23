---
name: track-cross-platform-hotspots
description: Fully automatic, profile-driven monitoring of news, trends, releases, research, products, and public signals across independent platforms. Use when Codex needs to create a daily or ad-hoc hotspot brief, identify the main story reported by multiple platforms, monitor selected interest directions, change a user's focus profile, or turn mixed links/feeds/search results into a verified cross-platform consensus report.
---

# Track Cross-Platform Hotspots

Run the complete workflow after invocation. Do not ask routine questions, narrate progress, or require the user to choose sources manually.

## 1. Resolve the focus profile

Use `scripts/profile.py` for persistent preferences.

Resolve `<skill-root>` as the absolute directory containing this `SKILL.md`. Always execute bundled scripts by absolute path; never assume the user's current working directory is the Skill directory.

- If the user names directions, save them before gathering.
- If a profile exists, use it silently.
- If none exists, initialize preset `ai-media-tech` and mention the chosen default only in the final result.
- Treat natural-language directions as valid custom directions; do not limit users to presets.
- Load `references/direction-catalog.md` only when presenting choices or expanding queries.

```powershell
python -X utf8 "<skill-root>/scripts/profile.py" show --json
python -X utf8 "<skill-root>/scripts/profile.py" init --preset ai-media-tech
python -X utf8 "<skill-root>/scripts/profile.py" set --directions "AI,影像,科技" --languages "zh,en" --region global
python -X utf8 "<skill-root>/scripts/profile.py" presets
```

Default state lives outside the Skill at `~/.codex/state/track-cross-platform-hotspots/profile.json`. Respect `SIGNAL_RADAR_HOME` when set.

## 2. Gather automatically

Translate every direction into two to four focused queries. Search the default 24-hour window; widen to 72 hours only when the 24-hour result is too sparse and label the wider window.

Use the best available collection adapter:

1. web search plus original pages;
2. connected feeds, databases, or news apps;
3. user-supplied links, JSON, CSV, or text.

Read `references/adapter-contract.md` when connecting a new source type. Collect the original editorial origin, not only an aggregator page. Prefer primary sources for technical claims and direct announcements; use independent reporting to establish convergence.

Store normalized items as UTF-8 JSON in `work/` using this shape. For mixed-language inputs, add `semantic_title`: a concise pivot-language restatement that preserves the named entities, action, object, and distinguishing model/version without adding facts. This lets the deterministic stage compare events beyond a finite alias dictionary.

```json
[{"platform":"example","title":"...","semantic_title":"Microsoft acquires Activision Blizzard","url":"https://...","published_at":"ISO-8601","direction":"AI","summary":"optional"}]
```

## 3. Detect candidate convergence

Run the deterministic clustering script:

```powershell
python -X utf8 "<skill-root>/scripts/cluster_hotspots.py" --input work/signals.json --output work/hotspots.json --profile auto
```

The script removes tracking parameters, discounts generic wording, blocks conflicting event types, and requires distinct platforms plus distinct canonical URLs. Its result is a candidate set, not final proof.

## 4. Verify the main hotspot

For the top candidate, open at least two original reports and verify all of the following:

- they describe the same concrete event, not merely the same company or topic;
- they come from independent platforms or editorial origins;
- one platform is not merely linking to the same original article;
- dates fall inside the declared window;
- the representative title and primary link refer to the same report.

Reject a candidate on any failed condition and verify the next candidate. Never invent consensus. If none survives, state `暂未出现跨平台主热点`.

## 5. Rank and deliver

Rank verified clusters by:

1. number of independent platforms;
2. user direction weight;
3. recency;
4. prominence within each platform;
5. likely user impact.

Return a compact brief in the user's language:

1. **主热点** — one representative headline, why it matters, platform count, and two to four direct source links;
2. **方向速览** — up to three signals per selected direction;
3. **观察** — one short cross-platform pattern or `暂无可靠共振`;
4. **范围** — time window and active directions.

Keep claims proportional to evidence. Separate verified reporting from inference. Link near each claim.

## 6. User controls

Interpret these requests without rebuilding the Skill:

- “主要看 AI、游戏和出海” → replace active directions.
- “再加机器人” → append with `--add-directions "机器人"`.
- “降低财经权重” → update with `--weights "财经=0.5"`.
- “只看中文来源” → set languages to `zh`.
- “排除明星八卦” → append with `--add-exclusions "明星八卦"`.
- “恢复默认” → initialize `ai-media-tech` with `--force`.
- “每天早上发一份” → create a scheduled automation only after the cadence is explicit; the scheduled prompt must invoke this Skill and use the saved profile.

## Failure handling

- Retry transient collection errors once, then continue with other adapters.
- Do not let one unavailable source block the whole brief.
- If fewer than two independent platforms are available, provide direction signals but no main hotspot.
- If live access is unavailable, process supplied material or state the exact missing capability in one sentence.

## Validation

After modifying this Skill, run:

```powershell
python -X utf8 "<skill-root>/scripts/profile.py" self-test
python -X utf8 "<skill-root>/scripts/cluster_hotspots.py" --self-test
python -X utf8 <skill-creator>/scripts/quick_validate.py .
```
