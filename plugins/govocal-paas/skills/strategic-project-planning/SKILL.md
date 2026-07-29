---
name: strategic-project-planning
description: >-
  Turn a CITY NAME into a recommended 12-month citizen-participation programme on a Notion page.
  Trigger on "/strategic-project-planning [city]", "strategic project planning for [city]", "plan
  participation for [city]", "build a participation plan/roadmap for [city]", "what should [city] run
  this year", "draft a project plan for [city]", or naming a city and asking for participation
  projects. Resolves the city as a client or prospect via Planhat; pulls the
  strategic plan from the web using the local term (meerjarenplan, coalitieakkoord, corporate plan,
  Regierungsprogramm, kommuneplan, projet de ville, etc.); pulls Planhat context (health, maturity,
  usage, NPS, documents, conversations) and meeting notes (Fireflies/Granola); applies Go Vocal
  best-practice setups by maturity tier; and writes a programme — SMART objective, strategic cascade
  (initiative -> policy objective -> key project), 12-month timeline and per-project detail — to a
  structured Notion page in the city's local language. Never invents data.
---

# Strategic project planning

Given a **city name**, produce a recommended 12-month participation programme and publish it as a
polished **Notion page**, grounded in (a) the city's own strategic plan, (b) live Planhat account
context, and (c) Go Vocal best-practice setups. Never invent data — only use what the sources state.

## Inputs

- **Required:** city / organisation name (e.g. "Oostende", "Cambridge City Council", "Stadt Wien").
- **Optional:** country (helps resolve the right plan terminology and Planhat record), output language
  (defaults to the city's local language), horizon start month (defaults to next month), a SMART
  objective if the user already has one.

If the city is ambiguous (multiple matches) ask one quick clarifying question; otherwise proceed.

## Workflow

### 1. Resolve the city → client or prospect (Planhat)
- Search the **Planhat MCP** for a Company matching the city (`search_records`, then
  `list_model_records` MODEL "Company"). 
- **Client** = a Planhat Company exists → pull full context (steps 2 + 3). 
- **Prospect** = no Planhat record → strategic plan + public context only; do NOT fabricate usage or
  account figures.

### 2. Strategic plan (web) — country-aware
- Web-search + fetch the city's strategic plan using the correct LOCAL term for the country:
  - Belgium: `meerjarenplan` / `bestuursakkoord` (NL) · `projet de ville` / `déclaration de politique` (FR)
  - Netherlands: `coalitieakkoord` / `collegeprogramma` / `bestuursakkoord`
  - United Kingdom / Ireland: `corporate plan` / `corporate strategy`
  - Germany / Austria: `Regierungsprogramm` / `Koalitionsvereinbarung` / `Stadtentwicklungskonzept` / `Zukunftsvertrag`
  - France / Luxembourg: `projet de ville` / `projet de territoire` / `programme municipal`
  - Denmark / Norway / Sweden / Finland: `kommuneplan` / `kommuneplanstrategi` / `översiktsplan` / `kaupunkistrategia`
  - USA / Canada: `strategic plan` / `general plan` / `citywide plan` / `official plan`
- Prefer the **official municipal domain**. Capture: official title, verified URL, 4–8 strategic
  themes (initiatives), and 3–6 verbatim priority quotes with a section/page reference.

### 3. Account context + maturity (Planhat — clients only)
- Pull: status, Lifecycle Phase, Customer Segment, health, csmScore, NPS, renewal score, MRR/ARR,
  renewal date, region, population, and usage fields — published projects, active users (90d),
  community members, engagement opportunities, participants (60d) — plus custom Maturity/Culture/
  Resources/Org scores, add-ons sold, recent **Conversations**, and any **Documents** on file.
- **Derive the maturity tier** from usage: published projects ≥30 **or** community members ≥10k **or**
  active users ≥500 = **Advanced**; ≥8 projects / ≥2k members / ≥100 active = **Growing**; else **Starting**.
- **Meeting notes:** pull recent transcripts/summaries for the account from **Fireflies** and/or
  **Granola** (last ~6 months) and extract concrete signals (asks, blockers, ambitions).

### 4. SMART objective
- Seed the baseline from the matching Planhat usage field (e.g. metric "community members" → current
  community members) and propose a **+20–30% target over 12 months** unless the user set one. Pick the
  most relevant strategic theme. Specific, Measurable, Achievable, Relevant, Time-bound.

### 5. Best-practice setup (see `references/best-practices.md`)
- Choose project types by **maturity tier** (Starting → light-touch + close-the-loop + standards;
  Growing → mapping, surveys, youth, multi-annual; Advanced → participatory budgeting, co-design,
  community monitor, always-on proposals).
- For each project anchor a **real Go Vocal case study** (Inspiration Hub — Metabase card 3231 via the
  `govocal-metabase` skill, or `project-library-finder`). Reflect any add-ons already sold.
- **Cascade every project:** strategic initiative (theme) → policy objective it serves → the project,
  tagged **policy priority** (the plan names that aim as a priority) or **mapped for participation**
  (the plan maps the topic for participation).
- **Coverage check:** ensure every strategic initiative has at least one project; flag gaps.

### 6. Build the programme
- 8–14 projects across the 12-month horizon, each with: name (local language), strategic theme,
  policy objective, cascade reason, methods, phases, expected reach (numeric where possible),
  why-it-fits-the-plan, influence, and one inspiration case study. Balance flagship engagements with
  lighter, always-on touchpoints. Compute projected reach vs the objective gap.

### 7. Publish to Notion (optimize for Notion — see `references/notion-layout.md`)
- Create a new page with the **Notion MCP** (`notion-create-pages`), written in the **city's local
  language**, using native Notion blocks (H1/H2, callout for the objective, a database/table for the
  12-month timeline, toggles per project, dividers, coloured callouts for priority vs participation,
  a bookmark to the strategic plan URL). Return the Notion page URL.

## Output

A single Notion page titled e.g. **"[City] — voorgesteld participatieprogramma 2026–2027"** containing:
Cover/intro · **Insights** (plan + Planhat + notes, with sources) · **SMART objective** (callout) ·
**Strategic cascade** (initiative → policy objective → project, tagged) · **12-month timeline** (table)
· **Per-project detail** (toggles) · plan source link. Plus a short chat summary with the page URL.

## Guardrails
- **Never fabricate.** Prospects get plan-only content; absent meeting notes/NPS are omitted, not invented.
- Output language = the city's local language (chrome + content).
- Cite sources inline (plan section refs; "Planhat", "Fireflies/Granola", document names).
- This drafts a recommendation; it does not contact the city or change Planhat/Notion records beyond
  creating the new page.
