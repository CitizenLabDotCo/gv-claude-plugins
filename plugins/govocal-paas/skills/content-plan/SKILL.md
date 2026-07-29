---
name: content-plan
description: "Turn a Go Vocal project draft (from the upstream `govocal-project-setup` skill) into a complete phase-by-phase communication plan PLUS all ready-to-use enablement assets, packaged as one .docx per project. Use whenever a GSM or Wietse says 'content plan for [project]', 'comms plan', 'communication calendar', 'draft the launch comms', 'make the enablement assets', 'promotion plan for the consultation', 'run the content-plan skill on draft X', or otherwise wants the outreach for a participation project planned and written — Facebook / Instagram / X posts, website snippet, PR release, emails to the registered audience, physical letters. Position in the skill chain: govocal-project-intake → govocal-project-setup → content-plan (this skill). Goal: optimize reach for the project and unburden the client champion."
metadata:
  version: "0.1.0"
---

# Go Vocal — Content Plan Skill

## What this skill does

You turn one **project draft row** (written by the upstream `govocal-project-setup` skill) into two things, delivered as **one .docx package per project**:

1. **A communication plan** — a dated comms calendar: what goes out, when, on which channel, mapped to the project phases. Not a list — a calendar.
2. **All enablement assets** — every post, snippet, release, email, and letter the calendar calls for, drafted in the project's local language and the account's own tone of voice, ready to publish after the GSM fills the placeholders.

Why a package and not loose drafts: the client champion (usually a communication or participation officer) should be able to open one document and execute the whole outreach. Every asset they don't have to write themselves is reach the project gains and time the champion gets back.

You do **not** post or send anything. Everything is a draft; the GSM delivers the package to the client. (Long term the assets will be pushed into the platform via the Go Vocal MCP — email into the project's email section, posts published directly. Structure the assets cleanly so that step stays a thin layer later.)

---

## Inputs

Triggered with one of:
- A specific Drafts DB row URL/ID → use that row
- "Content plan for [project name]" → find the matching row in the Drafts DB
- "Content plan" with nothing else → most recent row with `Status = Reviewed` (fall back to `Draft`, but flag that the draft itself hasn't been GSM-reviewed yet — comms built on an unreviewed draft may need rework)

Drafts DB (written by `govocal-project-setup`):
- **data_source_id:** `3759663b7b2680c7998b000c5be34eda`
- **URL:** https://app.notion.com/p/govocal/3759663b7b26803abf89e261c7f05fff

From the row, always read:
- `Archetype`, `Statutory` (+ `Jurisdiction`, `Instrument` if true) — drive the channel matrix
- `Recipe`, `Phase count`, `Duration (weeks)` — drive the calendar spine
- `Tone`, `Tenant URL` — drive voice and channel discovery
- The **project payload** JSON in the page body — phase titles, descriptions, durations, events, languages. Phase descriptions tell you what participants are asked to do in each phase; the comms must sell exactly that, never something grander.
- The **GSM decision report** in the page body — "Things missing" there are usually placeholders here.

If the row can't be found, stop and point the user to the setup skill. Never build a comms plan from scratch without a draft — the whole value is that comms match the designed process.

A test/eval run may instead hand you the draft payload as a JSON file; treat it exactly like a fetched row.

---

## Reference files (read on demand)

| Reference | Read when |
|---|---|
| `references/channel-matrix.md` | **Every run** — channel × archetype matrix, cadence + moment-that-matters per archetype, cross-cutting rules, bilingual rules |
| `references/social-posts.md` | The calendar includes Facebook, Instagram, or X entries |
| `references/website-and-pr.md` | The calendar includes a website snippet or PR release |
| `references/email-and-letter.md` | The calendar includes registered-audience emails or physical letters (it almost always includes emails) |

---

## Workflow

### Step 1 — Load the draft
Fetch the Drafts DB row and extract the fields above. Note the project language(s) from the payload (`settings.languages`, e.g. `nl-BE`) — all assets are drafted **directly in the local language**, not in English-then-translate. If the municipality is officially bilingual (common in BE), apply the bilingual rules in `references/channel-matrix.md`.

### Step 2 — Discover the account's channels and tone
Scrape what the account actually uses, before deciding what to write:
- Tenant/municipality website (from `Tenant URL` — the municipality's own site, not just the participation platform)
- Facebook page, Instagram account, X profile — search for them; read a handful of recent posts each for tone, typical length, emoji habits, hashtag habits, language(s) used
- Recent PR releases / news section, for the PR voice

**Tone-of-voice fallback chain, in order of precedence:**
1. The account's real channels (scraped) — the strongest signal; residents already know this voice
2. `Tone` from the setup draft
3. Market default (institutional-warm for the region)

**If a channel doesn't exist for this account, skip it and say so** in the GSM report — never invent posts for a channel the municipality doesn't use. A core channel missing (no Facebook for a broad-audience project) is worth flagging as a recommendation, not worth faking.

### Step 3 — Build the comms calendar
Read `references/channel-matrix.md`. Apply the channel × archetype matrix and the cadence table — don't reason the strategy from scratch; the matrix encodes what works. Then shape it to this project:

- The calendar spine = the phase timeline from the draft. Comms cluster at phase boundaries (launch, each transition, close) — that mirrors the bookend pattern high-scoring projects share.
- **Date every entry.** If the draft has real dates, use them. If not, anchor on `{{project_start_date}}` and express entries as offsets ("Launch day", "Week 3 — Wed") so the whole calendar re-dates itself when the start date lands.
- Apply the cross-cutting rules (results-back on every active channel, no silent gaps > 2 weeks on 6+ week projects, ○-channels only if the account uses them).
- If `Statutory = true`, apply the statutory overlay column: the website snippet becomes the formal notice, letters may be legally required (check `Instrument` + minimum notice period), the closing email carries the response-document link.
- Project-level **events** in the payload get their own calendar entries (announce + reminder on the channels the matrix marks for that archetype).

### Step 4 — Draft every asset
For each calendar entry, read the relevant channel reference and draft the asset in full — in the local language, in the scraped tone. Rules that hold across all channels:

- **One placeholder syntax:** `{{snake_case}}` — e.g. `{{results_date}}`, `{{mayor_quote}}`, `{{paper_form_location}}`. Anything the draft doesn't supply is a placeholder, never a guess. This makes late-phase drafts safely incomplete instead of confidently wrong.
- End **every asset** with a short **"Placeholders to fill"** list, so nothing ships half-baked.
- **Never invent facts** — no invented dates, venues, budget figures, officials' names, quotes, or resident sentiment. The upstream skills' rule applies here with extra force: these texts are published under the municipality's name.
- Every asset that can carry a CTA points to the **project page URL** (`{{project_url}}` until known).
- Sell the phase, not the dream: the ask in the asset must match what the phase actually lets residents do (the phase description is the source of truth). Overpromising influence is the fastest way to burn trust — and it contradicts the influence level the setup skill deliberately chose.

### Step 5 — Assemble the .docx package
Read the `docx` skill's SKILL.md, then build one document. Apply the `govocal-brand` skill to the **document shell** (cover, headings, layout — it's a Go Vocal deliverable); the **asset copy inside stays in the municipality's voice**, not Go Vocal's. Structure:

1. **Cover** — project title, tenant, archetype, date range, skill version
2. **How to use this pack** — half a page for the champion: fill placeholders, the calendar is the checklist, where each asset goes
3. **Comms calendar** — one table: date/offset, phase, channel, asset title, status. This is the plan at a glance.
4. **Assets, grouped by phase, then channel** — each with its calendar date, the final copy, and its "Placeholders to fill" list
5. **GSM report** (last section) — see Output notes below

Filename: `content-plan_<tenant>_<project-slug>.docx`. Deliver the file to the user.

### Step 6 — Recap
4–6 lines to the GSM: archetype → which channels are on/off (and why any were skipped), how many assets across how many moments, the single moment that matters most for this archetype, and the 2–3 highest-impact placeholders to chase first.

---

## Operating principles

1. **The matrix decides, you adapt.** Channel selection and cadence come from `references/channel-matrix.md`; your judgment goes into the copy and the local fit, not into re-deriving strategy per run.
2. **Results-back is sacred.** Every plan ends with a results-back communication on every active channel. The closing loop is worth ~1 full point on the project's Feedback score and it's the part clients most often skip — the calendar must make skipping it feel like ripping a page out.
3. **Local language, local voice.** A resident should not be able to tell these posts weren't written by their own city's comms officer.
4. **Skip honestly.** No account presence on a channel → no assets for it, one line in the GSM report, optionally a recommendation to open the channel if the archetype leans on it.
5. **Placeholders over plausibility.** A visible `{{results_date}}` gets filled; a plausible invented date gets published.
6. **Cite the draft.** Every strategy call in the GSM report cites the draft field that drove it (archetype, statutory, phase, event, tone), same discipline as the setup skill.

---

## Output notes — the GSM report section

Close the docx with a section the GSM can scan in 60 seconds:

- **Decisions & why** — channels on/off (citing the matrix + scrape), cadence chosen, language(s), tone source used (scraped / draft / default)
- **Channels skipped** — which and why (not used by account / archetype says off)
- **Statutory obligations** (only if `Statutory = true`) — formal notice, letter requirement, minimum notice period, response-document commitment — each mapped to the asset that satisfies it
- **Master placeholder list** — every `{{placeholder}}` across all assets, deduplicated, ordered by how much they block (launch-blocking first)
- **Recommendations** — e.g. "no Instagram account, but this is a Community-engagement project — the lead channel is missing; consider opening one or shifting weight to Facebook"

## What you do NOT do

- Do not post, send, or schedule anything, anywhere.
- Do not modify the draft row or the intake row.
- Do not draft assets for channels the account doesn't use.
- Do not draft flyers or posters (not in v1 — say so if asked).
- Do not translate mechanically: bilingual assets are drafted natively in each language, not word-for-word mirrored.

---

## Changelog

**0.1.0** — initial skill, from the spec: [Content plan skill — Notion](https://app.notion.com/p/govocal/Content-plan-skill-37d9663b7b26806b9249e4ccb85c5f22)

Upstream: `govocal-project-intake` → `govocal-project-setup` → this skill.
