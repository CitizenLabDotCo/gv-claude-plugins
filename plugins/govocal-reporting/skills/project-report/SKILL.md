---
name: project-report
description: Generate a client-facing Go Vocal project report (styled HTML → PDF) from the reporting MCP, following the Project Report Recipe. Usage - /project-report <project url, slug, or name> [optional focus questions]
---

# Project Report generator

Produce a client-facing participation report for one Go Vocal project, for a platform admin/PM. Full recipe: Notion → "Recipe: Project Report (client-facing)". This skill is its executable condensation. Work autonomously; only stop if the connected platform doesn't match the requested one.

## 0. Resolve target

1. Parse the argument: project URL/slug/name, and optional focus questions.
2. Verify the connected Community Platform MCP is the right platform: `list_projects` and check project URLs/slugs match the tenant in the argument (e.g. stlouis.govocal.com). If it clearly isn't, STOP and tell the user which platform is connected.
3. Find the project; pull `list_phases` for it. Phase participation methods determine which report sections exist (voting → results section; native_survey → answers section; information → reach only). If the project has embedded `survey` or `document_annotation` phases, the report must state that participation there is invisible to the reporting layer.

## 1. Data pull (quantitative)

Call `get_reporting_sql_schema` once, then `run_reporting_sql_query` (single SELECTs, ≤1000 rows → always aggregate in SQL). Conventions: participants = `COUNT(DISTINCT participant_id)` on `reporting_contributions`; resident traffic = sessions where `highest_role = 'user' OR highest_role IS NULL`; timestamps UTC.

Pull, scoped to the project (and window if given):
1. Project + phases (dates, methods) — `reporting_projects`, `reporting_phases`
2. Traffic by week: visitors (`COUNT(DISTINCT visitor_id)`), pageviews, device mix, top referrers — `reporting_pageviews` ⤷ `reporting_sessions`
3. Contributions by type × phase × week — `reporting_contributions`
4. Participants: total, per phase, active in ≥2 phases (returning) — `reporting_contributions`
5. Inputs: counts, `status_code` distribution, `received_feedback` share, likes/dislikes/comments/votes per input, `imported` share, `offline_votes_count` — `reporting_inputs`
6. Themes: inputs per tag rolled up to parent — `reporting_input_tags`
7. If voting phase: results = `SUM(weight)` per input + offline votes; ballots = distinct voters — `reporting_input_votes`
8. If survey phase: per question — AVG/distribution on `value_numeric` (scales/ratings/sentiment), option counts on `value_text` — `reporting_input_question_answers`. Flag ranking/matrix/mapping questions as not covered.
9. Demographics of participants vs ALL registered users (the representativeness base) — `reporting_user_question_answers`, `reporting_users`
9b. Official population base (Representativeness dashboard): clients/CSMs can upload census data per demographic field at `<tenant>/admin/dashboard/representation`. Not in the reporting MCP — fetch via the signed-in browser: `GET <tenant>/web_api/v1/users/custom_fields/<field_id>/reference_distribution` (admin-auth; 404 = nothing uploaded for that field; field ids from `list_user_custom_fields`). If present, this is the authoritative participants-vs-population base — prefer it over any external lookup.
10. Anonymous share of contributions (`user_id IS NULL`)
11. Survey open-text answers: `value_text` where `question_type IN ('text','multiline_text')` — sample if >200

## 2. Derived metrics

- Funnel: visitors → participants (participation rate), per phase + overall; name the largest drop-off.
- Depth mix: low (reactions) / medium (votes, polls) / high (inputs, comments).
- Conversation ratio: comments per input; % inputs with ≥1 comment.
- Closing-the-loop coverage: % non-survey inputs with feedback or non-default status; % still 'proposed'. This is the conscience metric.
- Momentum curve: weekly contributions annotated with phase boundaries.
- Representativeness gaps, three-tier base: (1) uploaded reference distribution (step 9b) if present → compare participants vs population, label "official base data uploaded to your platform"; (2) else derive a population base from official statistics (WebSearch census/statistics office), label the source+year and frame as approximate; (3) always also show participants vs registered users. Flag gaps >10pp. Whenever tier 1 is empty, add a recommendation: upload census base data via the Representativeness dashboard (`/admin/dashboard/representation`) so future reports use the official base.
- Controversy index (ideation/proposals): per input & theme, dislike share among reactions (floor: ≥10 reactions); 30–70% dislikes + above-median comments = contested.

## 3. Text & voice (qualitative)

- Fetch a purposive sample of idea bodies/comments via `get_resource`: top-engagement, most-contested, 1–2 per top theme (idea/comment text is NOT in the SQL views).
- Summarize per theme and per open question (2–4 sentences); always state the base ("based on 143 open answers").
- Quotes: 3–6 verbatim, ≤30 words, across themes AND stances (≥1 dissenting voice), anonymous ("a resident"), PII-screened. A quote illustrates a data-backed finding, never carries a claim alone.
- Sentiment: use `sentiment_linear_scale`/`rating` scores where instrumented; otherwise AI-classify sampled text and report coarsely ("roughly two-thirds supportive — AI-assessed on N answers"). Never decimal precision on AI sentiment.
- Contested topics: read contested inputs' threads; characterize the axis of disagreement. Division is signal, not failure → converts to a recommendation (options survey, deliberative follow-up).
- Cross-group patterns (max 1–3): cross-tab answers/themes × demographics via SQL (join through input author). Every compared group ≥20 participants; rank by effect size; comparative language only ("about twice as likely"); correlation not causation; each pattern ends with one "so what" sentence.
- Local context enrichment: if a pattern has a place/group dimension, WebSearch official sources (statistics office, municipal district profiles) to interpret it. Cite source+year, neutral official terminology (never "impoverished"), frame as hypothesis for the PM to confirm ("consistent with"). Area data describes places, not the individuals who spoke.

## 4. Benchmarks (test mode: manual sources + marked dummies, pending MCP expansion)

The benchmark MCP tooling isn't wired up yet. For now, source benchmarks in this order — never silently invent:

1. **Project Library scores & cohort ranks (real, fetch via browser)**: with claude-in-chrome, open `https://library.govocal.com/projects` and search/filter for the tenant + project. From the project card take: the four dimension scores (Participation, Process Design, Influence, Feedback) and the cohort ranks with sample sizes (rank for tenant / country / topic / overall). Rules: if any dimension is unscored ("?"), do NOT use the total score — report scored dimensions only. Label the source in method notes: "Go Vocal Project Library (internal), fetched <date>".
2. **Platform-internal comparison (real, via reporting SQL)**: this project vs the platform's other projects — participation rate, participants, feedback coverage. Label "compared with other projects on your platform".
3. **Peer-cohort rate percentiles (dummy for now)**: where the report design calls for "vs similar-sized cities in your region" and no real source is reachable, insert plausible placeholder values and mark them unmistakably — in the report body append "(DUMMY — pending MCP expansion)" in the accent color, and list every dummied number in the method notes. Never let a dummy look real.

**Test-mode rule**: any report containing dummy-marked or manually-fetched benchmark data is for internal testing only — say so in the final chat message and stamp "INTERNAL TEST — not for client delivery" in the report footer until benchmarks come from the real tooling.

## 5. Interpretation & narrative rules

- Report each phase against its promise (translate IAP2 level: "residents were asked to co-shape, not just react").
- Counts are activity; only statuses/feedback/decisions are influence. No causal claims ("coincides with", not "caused").
- Every gap ships with a concrete, platform-doable next step.
- Absolute + relative together ("312 participants, 4.1% of visitors"); no percentage on base <30 without the base; caveats inline where the metric appears (visitor month-boundary overcount; anonymous overcount; UTC).
- Tone: busy PM; headline findings first; 2–4 pages; exec summary ≤5 bullets.

## 6. Output: styled HTML → PDF

Write the report to the scratchpad as `report-<slug>.html`, then print to PDF.

**Styling (non-negotiable, LLM fills content only):**
- Editorial NYT-style: serif display headlines (Georgia/"Times New Roman" stack or a loaded serif), **sans-serif body** (system-ui/Helvetica stack), generous whitespace, thin hairline rules, muted ink-on-paper palette, clean lines.
- Tenant palette step: before writing, visit the tenant's platform URL (WebFetch or browser) and extract the brand's primary color(s). Use them as **accents only** (cover band, section rules, chart accent color). The editorial style always wins.
- Charts: Vega-Lite specs rendered via vega-embed (CDN scripts are fine in this local HTML). One shared theme config: minimal gridlines, direct labels over legends, one accent color per chart, annotation for the takeaway. Conventions: momentum = annotated area with phase bands; funnel = horizontal bars with conversion rates; representativeness = dumbbell/paired bars; survey scales = diverging stacked bars.
- Print CSS: `@page { size: A4; margin: 18mm }`, page-break rules before h2 sections.

**Report sections** (conditional on methods): Header (project, window, phases timeline, the promise) → Executive summary → Reach → Participation → Who participated → What they said (themes, summaries, quotes, sentiment, contested topics, cross-group patterns) → Results (voting/polls, if any) → Closing the loop → Comparisons (if any) → Recommendations (3–5) → Method notes (definitions, coverage gaps, caveats, data window + generation date).

**PDF**: wait for charts to render, then:
`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=<scratchpad>/report-<slug>.pdf --virtual-time-budget=10000 file://<path to html>`
Copy the PDF to `~/Desktop/` and tell the user both paths.

## Hard guardrails

- No PII: no names/emails; quotes anonymous & PII-screened; sensitive topics (health, migration, safety incidents) get paraphrase, not quotes.
- Demographic cells <5: suppress; <30: show the base. Compared groups in patterns ≥20 each.
- Never fabricate a benchmark, trend, or cause. "No data" is a valid, required statement.
- The report states its data window and generation date.
