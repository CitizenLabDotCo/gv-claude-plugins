---
name: resident-report
description: "DRAFT recipe — Generate a resident-facing, cross-phase project summary: what we asked, what we heard, what we did. Published in every platform locale. Usage: /resident-report <project url, slug, or name>"
status: draft-for-data-gap-analysis
---

# Resident Report generator (DRAFT)

Produce a **resident-facing** summary of a whole project, closing the loop with the people who took part (and those who didn't). Where the project report speaks to the PM ("here's what your data says"), this speaks to the resident: **"here's what we asked, here's what you told us, here's what we did with it."** It is a cross-phase narrative, not a phase dashboard.

Audience & voice: plain language (~B1 reading level), warm and direct, second person ("you told us"), zero jargon, no internal metrics language (no "funnel", no "conversion"). Short: 1–2 pages / one scrollable page. **Must be produced in every public platform locale** — this is a hard requirement, not a nice-to-have.

Annotations: `[OK]` = supported by today's reporting SQL layer / MCP tools. `[GAP-n]` = not supported; numbered gaps collected at the bottom.

## 1. Structure

### Header — the promise
Project title, dates, hero framing: what the municipality set out to do and what it promised participants. Pull the project description and the "how will my input be used" framing. `[GAP-1: project/phase description text is not in the SQL views; get_resource works per-project but descriptions, promise copy and phase descriptions need a supported, multiloc read path — today this is scraping-adjacent]`

### What we asked — per phase, in order
One short block per phase: the phase's question to residents, in the residents' own framing, with the method translated to plain language ("we collected your ideas", "you voted on the shortlist", "we asked 14 questions about the budget"). Needs: phase list + methods `[OK: reporting_phases]`, phase titles multiloc `[OK: title_multiloc]`, the actual questions asked `[OK-partial: get_form_fields returns the form; question labels in SQL views are primary-locale only — [GAP-2] multiloc question/option labels]`, phase description copy `[GAP-1]`.

### Who took part
Simple, honest numbers a resident can feel: "1,214 of you took part — 342 ideas, 4,510 votes, 557 survey answers." Participants `[OK: reporting_contributions]`, per-method counts `[OK]`, events held and attendance `[OK-partial: attendances exist in reporting_contributions but events themselves are not entities — [GAP-3] no reporting_events view (title, dates, phase) to say "including 120 of you at 3 town halls"]`. Optionally one representativeness sentence phrased constructively ("we heard less from residents under 30 — next time we'll…") `[OK: reporting_user_question_answers + reference distributions via GAP-4]`. `[GAP-4: reference distributions / R-score not exposed in reporting MCP — browser workaround today (also in i4 QoL)]`

### What you told us
3–6 headline themes with counts and 2–4 short anonymous quotes, per the project-report coding protocol (full coverage, bidirectional codes, PII screen — inherit §3 of the project-report skill wholesale). Tags `[OK: reporting_input_tags — but labels primary-locale only, [GAP-2]]`. Survey open text `[OK: reporting_input_question_answers]`. **Idea & comment text for ideation projects `[GAP-5: same as i4 item 3 — body text unreachable in SQL; blocks the heart of this report for the most common method]`.** Voting results in plain terms ("the community garden won with 400 votes — including 60 cast on paper at the market") `[OK: reporting_input_votes + offline_votes_count]`.

### What we did — the decision
The reason this report exists. Per theme or shortlisted input: status today ("accepted", "being implemented") `[OK: status_code/status_label — labels primary-locale only, [GAP-2]]`, the official feedback the city gave `[GAP-6: official feedback TEXT (and author/date) is not reachable — reporting_inputs has only the received_feedback boolean. Without the text this section cannot be written]`, and WHEN things moved `[GAP-7: no status-change history — same as i4 item 6; needed to say "in March the council approved…"]`. If the project ran a report/close-the-loop phase or published results on the platform, link it `[GAP-8: no queryable record of published report-builder reports / result pages per project-phase]`.

### What happens next + thank you
Next phases if any `[OK: reporting_phases where start_at > now]`, how to stay involved (follow project, upcoming projects) `[OK: reporting_projects]`, sign-off.

## 2. Rules
- Every number a resident sees must be exact and locale-formatted; no percentages without the base in words ("about 1 in 12 visitors").
- Never publish a demographic cell < 5; representativeness phrased as commitment, not confession.
- Quotes: anonymous, ≤30 words, PII-screened, across stances; at least one dissenting voice — residents notice sanitized reports.
- If a decision hasn't been made yet, say so plainly with a date expectation; a resident report with no "what we did" section must explain why.
- Output in ALL public locales. `[GAP-2 is the blocker: tag/status/question/option labels come back in the primary locale only; multiloc variants (or a locale parameter on the views) are required. Free-text theme summaries and narrative are LLM-translated — labels must come from the platform to match what residents saw.]`

## 3. Output: styled HTML → PDF (and, later, a platform page)

Same HTML → headless-Chrome → PDF pipeline as the project report. Alternative target: publish as a platform page/report for the phase `[GAP-8 / format decision — see opportunity doc Solutioning]`.

**Styling (non-negotiable, LLM fills content only). This report is the city speaking to its residents — it should look like the city published it, not like an analytics vendor did.**
- **Brand as primary, not accent**: before writing, visit the tenant platform URL and extract the brand palette + logo treatment. Brand color carries the cover band, section headers and chart accent. If the brand color fails WCAG AA contrast on white, auto-darken it for text uses and say so in a code comment — accessibility beats brand fidelity.
- **Typography**: warm humanist sans-serif throughout (system-ui/"Segoe UI"/Helvetica stack) — no editorial serif here; this is a letter from the city, not a newspaper. Large base size (18px screen / ≥12pt print), line length ≤ 70 characters, line height ≥ 1.5, real paragraphs — no dense stat blocks.
- **Layout**: one scrollable page or 1–2 A4 pages. Card-like section per phase for "what we asked" (a simple vertical timeline). Resident quotes styled as large pull-quotes with the brand color rule. Photography slots with captions (use the project header image if available; never stock-photo filler).
- **Charts: 1–2 maximum, human-scale**: whole numbers, big direct labels, no legends, no gridlines, one brand accent. "Who took part" = pictogram-style or simple horizontal bars ("1,214 of you"); results = horizontal bars with the winning option annotated in words. Every chart gets alt text; nothing encoded by color alone.
- **Multilingual robustness**: layout must tolerate ~30% text expansion between locales and support RTL when a platform locale requires it; numbers and dates locale-formatted per output language.
- **Print CSS**: `@page { size: A4; margin: 18mm }`, no page break inside a phase card.
- Footer: project name, data window, generation date, and "Questions? Contact …" line in the output locale.

## Collected gaps (resident report) — verified against citizenlab code, Aug 18 2026
All data below EXISTS in the product DB unless marked otherwise; the gap is view/MCP exposure.
- **GAP-1** Project & phase description/promise copy: `projects.description_multiloc`, `phases.description_multiloc` exist; need a multiloc read path in the reporting layer (or documented get_resource contract).
- **GAP-2** Multiloc labels: tags, statuses, form questions & options, user custom-field options — all stored as multiloc in DB; the views resolve to primary locale only. Need multiloc columns or a `locale` parameter. Blocks the all-locales requirement. (Supersets i4 item 2.)
- **GAP-3** `reporting_events` view: `events` (title/description multiloc, start/end, location, attendees_count, maximum_attendees) + `events_attendances` exist in full (i4 item 7).
- **GAP-4** Reference distributions / R-score via MCP (i4 QoL item).
- **GAP-5** Idea & comment body text in reporting layer (i4 item 3) — hardest blocker, most common method. Bodies in `ideas.body_multiloc` / `comments.body_multiloc`; needs PII stance decided.
- **GAP-6** Official feedback text + author + date per input. NEW — not in i4. `official_feedbacks` table has exactly this (body_multiloc, author_multiloc, user_id, idea_id, created_at); pure view work. Without it "what we did" is unwritable.
- **GAP-7** Status-change history with timestamps (i4 item 6). Exists as `activities` rows (item_type 'Idea', action 'changed_status', payload.change = [old,new], acted_at) — view can be derived.
- **GAP-8** Published reports as queryable entities. NEW — not in i4. `report_builder_reports` has phase_id, visible (the published-to-residents flag), year/quarter; pure view work.
