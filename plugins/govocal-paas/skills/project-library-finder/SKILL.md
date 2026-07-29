---
name: project-library-finder
description: Find the best Go Vocal client projects in the project library — ranked shortlist of 5 with deep-dive context on why they ran it, citizen highlights, and real-world impact. Always trigger when Wietse says "find me good projects", "best participation projects", "interesting client cases", "library deep-dive", "what's worth highlighting in [month/quarter]", "show me top projects on [topic]", "any standout projects using [method]", "good case studies for sales", "best projects this month", "dig into the library", or anything about surfacing high-quality projects from library.govocal.com for internal inspiration, sales/marketing case studies, talks, LinkedIn posts, or board updates. Casual phrasings like "got any cool projects to highlight?" or "what should I show clients" also trigger this skill.
---

# Project Library Finder

## What this skill does

Go Vocal runs a public project library at https://library.govocal.com/projects that aggregates every project across every customer platform (~32k projects) and scores each one on four dimensions (Influence, Process Design, Participation, Feedback). This skill pulls a ranked shortlist of 5 outstanding projects from that library for any combination of **time period**, **topic**, and **method**, then deep-dives each one for the narrative pieces Wietse cares about: why the city ran it, standout citizen ideas, participation numbers, and real-world impact when available.

The output is a structured chat shortlist that Wietse skims, picks favorites from, and forwards to sales/marketing for full case study work.

## When inputs are missing — ask once, then go

Before running, confirm three things if not given:

1. **Time period** — default: "last 3 months" (active during that window).
2. **Topic** — default: "any topic". If given, try the Go Vocal topic taxonomy first, fall back to free-text search across title + description.
3. **Method** — default: "any participation method other than information / native_survey weighted normally". If given, the named method must appear as at least one participation phase of the project.

Don't ask all three if only one is genuinely ambiguous. If the user said "best mobility projects from Q1", run with topic=mobility, time=Jan-Mar of current year, method=any.

## Workflow

### Step 1: Pull candidates from Metabase

The base data lives in Metabase database id `3`, schema `cl2_library`, source table `4118` (the data behind https://metabase.hq.govocal.com/question/3200-project-library). See `references/data-sources.md` for the schema and `references/sql-templates.md` for ready-to-use SQL.

Key filters:
- `status IN ('finished', 'active')` — exclude planned/stale/deleted. Wietse cares about projects with real participation.
- Time period: active during window → `practical_start_at <= :end_date AND (practical_end_at >= :start_date OR practical_end_at IS NULL)`.
- Topic: when given, match against `topic_titles` (taxonomy) first; if <5 candidates, broaden to ILIKE on `title_en` + `description_en`.
- Method: when given, the project must have a phase with `participation_method = :method` (join through phases table). See sql-templates.md.
- Always pull all 4 sub-scores and the methods used so you can re-rank with Wietse's weights, not the library's default.

Aim to retrieve ~30-50 candidates (don't trust top-5 directly from the library — its default weighting is different from Wietse's).

### Step 2: Re-rank with Wietse's weights

The library's default weighting is 50% participation, 16.6% × 3 for the others. **Wietse's weighting is different — use this:**

| Dimension | Weight |
|---|---|
| Participation | **40%** |
| Influence | **30%** |
| Process Design | **20%** |
| Feedback | **10%** |

`weighted_score = 0.40*score_participation + 0.30*score_influence + 0.20*score_process + 0.10*score_feedback`

All sub-scores are 1-5. Treat NULL as 0 for ranking purposes but flag in the output.

**Method-ladder penalty (default, can be overridden):** Wietse cares most about projects using higher-ladder methods. The influence score already partly captures this, but apply an additional soft penalty when a project's *only* participation methods are `information` or `native_survey` — subtract 0.5 from the weighted score. This penalizes but does not exclude (many participants + strong feedback loop can still surface a survey-led project). If the user says "include all methods" or "ignore method weighting", skip this penalty.

See `references/scoring.md` for the full rationale and `references/method-ladder.md` for the ladder.

### Step 3: Deep-dive the top 5

For each of the 5, gather the narrative pieces below. **Run these enrichment steps in parallel via subagents whenever possible** — one Explore agent per project is the right pattern.

What to find for each project:

1. **Why the city ran it (context / issue at stake)**
   - Read project + phase descriptions on library.govocal.com (sidepanel "Read more...") OR via Chrome MCP on the actual tenant project page (click the external-link icon next to the project title).
   - Query the web: search `"<project title>" <city name>` and `<city> <topic> participation plan` for press articles, city strategic plans, or council documents that explain the political/policy backdrop.

2. **Participation highlights**
   - **Citizen ideas / proposals / quotes:** Get the top-voted or top-commented ideas via the govocal MCP (`govocal_list_ideas` sorted by `popular` or `votes`, filter by `project_id`). If the tenant differs from the currently-authenticated govocal tenant, fall back to reading the live project page via Chrome MCP — citizen ideas + comments are public on most tenant platforms. Pull 2-3 standout items with author + permalink.
   - **Numbers and reach:** participants count, contributions count, comment count — these are on the library card and in the Metabase data (`participants_count`, `inputs_count`, `comments_count`).

3. **Real-world impact (when available)**
   - Check idea statuses on the project page — Go Vocal platforms tag ideas with statuses like "Under consideration", "Implemented", "Rejected", "Accepted". A project where many ideas reached "Implemented" is a strong impact signal.
   - Look for an official feedback / status update on the project (often a final phase or a project-level update). 
   - Web search: `<city> <project> outcome` or `<city> <topic> budget decision <year>` for press coverage of the city acting on the input.

If any of these come up empty, say so explicitly — don't fabricate. ("No impact data surfaced in search; the project finished only 2 months ago.")

### Step 4: Output

Use the template in `assets/output-template.md`. Keep the chat output tight — Wietse wants a quick skim, not a wall of text. He'll forward favorites to sales/marketing who will do full case study work.

## Source-of-truth pointers

- **The library itself**: https://library.govocal.com/projects (Wietse is logged in; admin view shows all sub-scores, annotations, and a sidepanel that links to the live project)
- **The wiki**: https://www.notion.so/govocal/Project-Library-ad3a39274d2c48fba042b38e3d29cdc5 — definitive doc on how scores are computed, status semantics, topic taxonomy
- **Base Metabase query**: https://metabase.hq.govocal.com/question/3200-project-library
- **Metabase database**: id `3`, schema `cl2_library` (see `references/data-sources.md`)
- **Govocal MCP**: tenant-scoped; works for citizen ideas/comments only on the currently-authenticated tenant. For other tenants, use Chrome MCP on the public project URL.

## What this skill does NOT do

- Does not write a full sales/marketing case study — Wietse forwards favorites to the relevant team who do that work.
- Does not modify the library (no annotations, no pinning).
- Does not deep-dive on projects with `status = 'planned'` or `'deleted'` — those don't have meaningful participation yet.
- Does not include external survey phases in participation numbers — the library doesn't track participants for those (known limitation in the wiki).
