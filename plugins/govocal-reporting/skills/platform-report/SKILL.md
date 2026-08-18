---
name: platform-report
description: "DRAFT recipe — Generate a platform-level report for a time window: reach, inclusion, participation, internal practice, benchmarks. The much-improved successor of the legacy 'progress reports'. Usage: /platform-report <period, e.g. 2026-H1> [vs <comparison period>]"
status: draft-for-data-gap-analysis
---

# Platform Report generator (DRAFT)

Produce a **platform-level** report for a platform owner / leadership / council: everything that happened on the platform in a period, structured from the perspective of **reach, inclusion and participation**, with an executive summary, internal-activity data, benchmarks against comparable municipalities, and an honest read on whether the platform is being used according to participation best practice. Successor to the legacy CitizenLab "progress reports", rebuilt.

Every section compares the period against a reference window (previous period and/or same period last year) — deltas are the story, levels are the footnote.

Annotations: `[OK]` = supported by today's reporting SQL layer / MCP tools. `[GAP-n]` = not supported; collected at the bottom. i4 refs = already documented in "i4 · MCP complete reporting data".

## 1. Structure

### Executive summary (≤5 bullets)
Written last. One bullet each: reach, participation, inclusion, internal practice, the single most important recommendation.

### Reach
- Visitors, pageviews, sessions by month; device mix; interface locales used `[OK: reporting_sessions/pageviews]`
- Visit → registration → participation funnel `[OK-partial: visitors OK; registered_at + created_at give completed registrations; started-but-not-completed registrations and acquisition source (invited / organic / SSO) missing — GAP-A / i4 item 10]`
- Channels: top referrers `[OK: raw referrer URL]` — but classified channels (search / social / email / campaign) and UTM parsing `[GAP-B / i4 item 9]`, and outreach attribution (invitations & email campaigns sent, delivered, opened → visits) `[GAP-B]`
- Projects launched in period, by method and by folder/department `[OK-partial: first_published_at + phases give launches & methods; folder NAME and project topics/areas missing — GAP-C / i4 item 5]`

### Participation
- Contributions by type and method; participants; depth mix (low/medium/high-effort); momentum over the period annotated with project launches `[OK: reporting_contributions]`
- Per-project league table: participants, participation rate, feedback coverage `[OK]`
- Returning participants across projects (cross-project retention: % of participants active in ≥2 projects in period) `[OK: participant_id spans projects]`
- Event participation: events held, attendances `[GAP-D / i4 item 7: attendances exist; events don't]`

### Inclusion
- Participant demographics vs registered users vs official base `[OK + GAP-E: reference distributions via MCP — i4 QoL]`
- Anonymous participation share `[OK]`
- **Inclusion-feature adoption by project teams** — are officers using the tools that widen the funnel?
  - Paper/offline inputs imported (`imported` share) `[OK: reporting_inputs.imported]` — but WHO imported, when, via which channel (FormSync vs manual upload) `[GAP-F]`
  - Offline votes added to voting phases `[OK: offline_votes_count > 0 per input; share of voting phases using it derivable]`
  - FormSync usage (scanned/synced paper forms) `[GAP-F: no reporting trace distinguishing FormSync from other imports — verify against citizenlab code]`
  - Events as offline channel `[GAP-D]`
  - Multilingual publishing: % of projects with content in all platform locales `[GAP-G: multiloc presence is in title_multiloc for projects/phases (derivable), but not for descriptions/forms]`

### Internal capacity & practice  ← the genuinely new part
- **Active staff**: number of admins / PMs / folder moderators active in period, vs previous period `[GAP-H / i4 item 8: reporting layer sees staff only as highest_role; no last-active, no per-staff actions]`
- Staff actions: projects created, phases configured, official feedback written, status changes, moderation actions — per period, per department if possible `[GAP-H: an activities/audit log exists in the product DB (verify via citizenlab code) but nothing is exposed]`
- **Best-practice adherence scorecard** — the "are we being used well" section, as data plus anecdotes:
  - % of finished projects that closed the loop: ran a report/results phase, published a report, or gave feedback on >X% of inputs `[OK-partial: received_feedback coverage OK; report/results-phase detection and published reports GAP-I]`
  - Median time-to-feedback and time-to-status-change on inputs `[GAP-J / i4 item 6: needs status/feedback event history]`
  - % of ideation projects actually using statuses (not everything left 'proposed') `[OK]`
  - % of voting phases that added offline votes; % of projects with imported inputs `[OK]`
  - % of projects with a description meeting a length/clarity floor; % with expected-impact/promise stated `[GAP-K: needs description text — same read path as resident-report GAP-1]`
  - Anecdotes: 2–3 concrete exemplary projects and 1–2 quiet failures (never named punitively — "one project collected 200 ideas and set no statuses")
- Seats vs activity: active staff / licensed seats `[GAP-L: seat/license count is off-platform (billing/Metabase), not in tenant DB]`

### Community sentiment
- Community monitor quarterly scores + trend, IF response volume ≥ threshold (state n) `[OK-partial: responses live as sentiment_linear_scale answers on the hidden community-monitor project — derivable via SQL; the computed quarterly scores & completeness rules are product logic we'd have to re-derive — GAP-M: expose computed monitor scores per quarter]`
- General sentiment from the period's open text corpus, AI-coded with the project-report protocol, reported coarsely `[OK]`
- 3–5 quotes across projects, themes and stances `[OK for surveys; ideation quotes GAP / i4 item 3]`

### Benchmarks
- "Compared to platforms of similar-sized municipalities in your country / other countries": registrations per 1k population, participation rate, projects per year, closing-the-loop coverage `[GAP-N: inherently cross-tenant — cannot come from the tenant-scoped SQL layer. Today this data lives off-platform: Metabase (cross-tenant usage) and the Project Library (per-project scores: Participation, Process Design, Influence, Feedback + cohort ranks by country/topic/size). Needs a benchmark service/API with defined cohorts (country × population band) and agreed metric definitions + the Library re-weighting (participation 50%) — this is i4 item 4, still to be scoped properly]`
- Project Library scores for the period's flagship projects `[OK-manual today: browser fetch per project-report skill §4; needs API — part of GAP-N]`

### Recommendations (3–5) + Method notes
Concrete, platform-doable, tied to the scorecard ("6 projects closed without feedback — schedule reports for each"). Method notes: definitions, windows, caveats (UTC/timezone `[GAP / i4 QoL]`, visitor month-boundary overcount).

## 2. Rules
- Staff-practice findings are framed as capability-building, not surveillance: aggregate first, anecdotes anonymized-by-default, individual naming only for praise.
- Never compare departments/PMs on raw volume without workload context.
- Community monitor: suppress below minimum n; state n always.
- Benchmarks: real or absent — never estimated (inherits project-report §4 test-mode rule until GAP-N tooling exists).
- Deltas need denominators: "up 40%" always with absolute numbers.

## 3. Output: styled HTML → PDF, 4–8 pages + 1-page council version

Same HTML → headless-Chrome → PDF pipeline as the project report.

**Styling (non-negotiable, LLM fills content only). This is the analytical sibling of the project report: editorial, dense, ink-on-paper — built to survive a leadership meeting.**
- **Editorial NYT-style**: serif display headlines (Georgia/"Times New Roman" stack or loaded serif), sans-serif body (system-ui/Helvetica), thin hairline rules, generous margins, muted palette. Tenant brand color extracted from the platform URL and used as **accent only** (section rules, chart accent, delta highlights) — the editorial style always wins.
- **KPI rows**: each section opens with a row of stat tiles — big numeral, small label, and the period delta as ▲/▼ with sign and absolute value ("▲ +1,240 (+18%)"). Delta color is redundant with the arrow (colorblind-safe); reference-period values in muted gray beneath. Never a delta without its absolute.
- **Charts: Vega-Lite, one shared theme config**: minimal gridlines, direct labels over legends, one accent per chart, an annotation carrying the takeaway. Conventions: momentum = area chart with project-launch markers; funnel = horizontal bars with conversion rates between stages; representativeness = dumbbell/paired bars; period comparisons = slope charts or paired bars (never grouped-bar forests); per-project league table = table with inline bars and sparklines; **best-practice scorecard = table with trend arrows and a filled/unfilled dot scale, no traffic-light red** (practice findings are capability-building, not grading — see §2).
- **Density with hierarchy**: two-column stat layouts allowed; every page answers "so what" in one bold-serif sentence near the top. The executive summary page must stand alone if torn off.
- **Council one-pager**: derived from the same data pull and theme — exec summary bullets + the three most decision-relevant charts, nothing else.
- **Print CSS**: `@page { size: A4; margin: 18mm }`, page break before each h2 section, running footer with platform name, period, vs-period, and generation date.

## Collected gaps (platform report) — verified against citizenlab code, Aug 18 2026
Legacy baseline confirmed: the old "progress report" is the report-builder **PlatformTemplate** (frontend `Admin/reporting/.../Templates/PlatformTemplate`) — exec summary + visitors/traffic/registrations/participants/demographics/projects/methods widgets, stored quarterly in `report_builder_reports` (year, quarter). This recipe supersedes it.

Data EXISTS in DB unless marked ⚠️ (capture gap) or 🌐 (off-platform).
- **GAP-A** Registration funnel (i4 item 10): `users.created_at` vs `registration_completed_at`, `invite_status`, `email_confirmed_at`, `identities` (SSO provider) all exist — reporting_users currently *excludes* incomplete registrations, so funnel needs a dedicated view. Acquisition source: invited/SSO/imported inferable; ⚠️ organic source per user never captured.
- **GAP-B** Outreach (i4 item 9): `email_campaigns_campaigns` (~45 types, context/project-scoped) + `email_campaigns_deliveries` with **delivery_status incl. opened & clicked** + `invites` all exist — pure view work. ⚠️ UTM/query-string on sessions is NOT captured anywhere (pageview path stores no query string) — real product capture work, not view work.
- **GAP-C** Project metadata in SQL: folder names, topics, areas (i4 item 5).
- **GAP-D** `reporting_events` view (i4 item 7): `events` + `events_attendances` exist in full.
- **GAP-E** Reference distributions / R-score via MCP (i4 QoL).
- **GAP-F** Import provenance — NEW: `idea_imports` (import_user_id, file_id, user_created, approved_at, locale) + `idea_import_files` (project_id, import_type, num_pages) exist. FormSync is the LLM scanned-PDF path inside bulk_import_ideas and lands in these same tables — distinguishable via file/import metadata. View work.
- **GAP-G** Multiloc completeness signals — NEW (shared with resident-report GAP-2 family).
- **GAP-H** Staff activity — i4 item 8, now concrete: `activities` audit table (item_type, action incl. changed_status/published/created, payload, user_id, project_id, acted_at) + `users.last_active_at` + `users.roles` jsonb all exist. Propose view: `reporting_staff_activities(user_id, role, action_type, item_type, project_id, acted_at)` + role detail beyond highest_role. Also phase-level offline voters (`phases.manual_voters_amount`, last_updated_by/at) not in views.
- **GAP-I** Published reports as queryable entities — NEW: `report_builder_reports.visible` + `phase_id` (shared with resident-report GAP-8).
- **GAP-J** Status/feedback event history (i4 item 6): derivable from `activities` changed_status + `official_feedbacks.created_at`.
- **GAP-K** Description/content text read path (shared with resident-report GAP-1).
- **GAP-L** 🌐 Seats/licenses — off-platform (billing/Metabase); decide whether in scope at all.
- **GAP-M** Community monitor — NEW, narrower than feared: responses ARE in the views (hidden project, `sentiment_linear_scale` answers). Missing: `custom_fields.question_category` (quality_of_life / service_delivery / governance_and_trust) not exposed, and quarterly aggregates are computed on the fly by `Surveys::AverageGenerator` — either expose the category column (small) or a scores view mirroring product logic.
- **GAP-N** 🌐 Cross-tenant benchmark service (country × population-band cohorts; Library scores API + participation-50% re-weighting) — i4 item 4, still unscoped; the one gap that cannot live in the tenant-scoped SQL layer by design. Sources today: Metabase (cross-tenant usage) + Project Library (browser-scraped).
- Minor: `browser_name`/`os_name` exist on impact_tracking_sessions but aren't in reporting_sessions.
