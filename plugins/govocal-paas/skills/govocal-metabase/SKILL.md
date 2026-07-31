---
name: govocal-metabase
description: 'Conventions for querying Go Vocal''s Metabase via the Metabase MCP. ALWAYS use when a request touches Metabase, the product database, dashboards, saved cards/questions, the ⭐ curated models (Visitors, Users, Active users, Participants, Tenants, Projects, Folders, Participation contexts, Contributions, Inputs, Sessions), or the History-Tracked Questions collection. Trigger on phrases like "query/ask Metabase", "pull X from the product DB", "how many active users / projects / tenants / contributions", "build a Metabase question/card/dashboard", "export from Metabase", "browse models", or any analytics question about Go Vocal product data (note: MRR/ARR live in Planhat, not here). Also trigger on metabase.hq.govocal.com URLs (or the older metabase.hq.citizenlab.co) and card/dashboard/collection IDs. Pair with the Metabase MCP tools (execute, list, retrieve, search, export).'
---

# Go Vocal Metabase guide

## What this skill does

A field guide for using Go Vocal's Metabase well. It pairs with the Metabase MCP and teaches Claude:

- Which data sources, collections and curated `⭐` models exist at Go Vocal, and which to reach for first.
- How to pick the right MCP tool (`search`, `list`, `retrieve`, `execute`, `export`) for a given question.
- The data gotchas that quietly break analyses - the active-tenant filter, the `users`-table traps, the "yesterday not today" rule, and why snapshot data can't answer point-in-time questions.
- How the History-Tracked Questions mechanism works, and the rules a question must follow to be picked up by it.
- How to export to Google Sheets safely (snapshot vs live, no PII, keep it minimal).

Use it whenever a request would otherwise have Claude write blind SQL against the Go Vocal product database.

Source of truth for the content of this skill: [Notion - Metabase guide](https://www.notion.so/govocal/Metabase-4fc6e42692844223905cc5b61226f9c2).

## What Metabase is at Go Vocal

Metabase is hooked up to a **nightly full copy** of the product (application) database. Highly relational, almost 1:1 with the app schema, so it's powerful but not optimized for reporting.

- Host: `https://metabase.hq.govocal.com` (older Notion docs link to `metabase.hq.citizenlab.co` - same instance, post-rebrand domain is the canonical one)
- Models browser: `https://metabase.hq.govocal.com/browse/models` - listed via the MCP with `search({ models: ["dataset"] })` (Metabase calls models "datasets" in its API)
- Data is yesterday's. A question that counts "today" will be empty or partial - filter on yesterday when measuring daily metrics.
- Reloads are **full**, not incremental: history shown today is "history from today's perspective". Tenants/projects/users that have since been deleted are gone. For true point-in-time tracking, use the History-Tracked Questions mechanism (see below).
- Self-hosted, open-source. Schema drifts as the product changes. Expect breakage. Issues go to `#metabase` on Slack.

## The Metabase MCP - which tool when

The MCP exposes five tools (server prefix `mcp__Metabase__Unofficial___Community___`):

| Tool | When to use |
|---|---|
| `search` | First stop for finding existing cards, dashboards, tables, collections by name/keyword. Set `models` (e.g. `["card"]`, `["dashboard"]`, `["table"]`). Use `search_native_query: true` to grep inside SQL of cards. |
| `list` | Enumerate all of one model type (`cards`, `dashboards`, `tables`, `databases`, `collections`). Paginate with `limit`/`offset`. Use when you need an overview, not a targeted lookup. |
| `retrieve` | Fetch full details for known IDs (up to 50 at once). Use after `search`/`list` to get the actual SQL, dashboard cards, table fields, etc. |
| `execute` | Run a query and get rows back (max 500). Two modes: **card mode** (`card_id` + optional `card_parameters`) re-uses a saved question with its filters; **SQL mode** (`database_id` + `query`) runs custom SQL. **Prefer card mode** when a `⭐` model or curated question already answers the question. |
| `export` | Same as `execute` but supports up to 1M rows and writes a file (CSV/JSON/XLSX) to Downloads/Metabase. Use whenever the result set is large or the user wants a file. |

**Workflow rule of thumb:** `search` → `retrieve` to inspect → `execute` (card mode if possible). Reach for SQL mode only when no curated card/model fits.

**Security:** `execute`/`export` in SQL mode can run any SQL the Metabase user is allowed to. Don't write DELETE/UPDATE/DROP/TRUNCATE/ALTER unless the user explicitly asks. Default to read-only SELECTs.

## The `⭐` models - always start here

The Platform Squad maintains a small set of **fat, well-defined models** marked with a ⭐ in their name. They denormalize common joins so you don't have to. Use them in preference to raw tables. They live in the `Our Analytics` collection, pinned to the top, and are also visible at `https://metabase.hq.govocal.com/browse/models`.

**Discover the current list at runtime.** Card/model IDs do drift as the team adds, retires or renames models. Don't trust the table below blindly - before running anything, enumerate:

```
search({ query: "", models: ["dataset"], max_results: 50 })
```

Then filter results whose name starts with ⭐ (or whatever the current convention is). Cross-reference against the table below for "did the canonical model I expected disappear or get renamed?".

**Canonical list per the Notion guide (verify IDs via `search` before relying on them):**

| Concept | Model | Card/Model ID | Notes |
|---|---|---|---|
| People - Visitors | ⭐ Visitors | 1310 | Unique humans visiting. Registered users count as 1 across all history; anonymous visitors are unique within a calendar month (browser+IP). |
| People - Users | ⭐ Users | 1311 | Humans with an account. Use this, not the raw `users` table. |
| People - Active users (30d) | ⭐ Active users (30 days) | 1312 | Users active in the last 30 days. |
| People - Participants | ⭐ Participants | 1319 | Humans who generated a contribution. Not all are users (anonymous participation exists). |
| Platform - Tenants | ⭐ Tenants | 1322 | A tenant = a CitizenLab/Go Vocal platform. |
| Platform - Projects | ⭐ Projects | 1323 | All projects, in or outside folders. For participation-method settings on continuous projects use Participation contexts. |
| Platform - Folders | ⭐ Folders | 1324 | Project folders on homepages. |
| Platform - Participation contexts | ⭐ Participation contexts | 1333 | Unified view of (continuous projects ∪ phases of timeline projects). Use when answering "which participation methods are used most". |
| Action - Contributions | ⭐ Contributions | 1315 | Participatory actions on the platform. **Excludes** embedded 3rd-party surveys and workshops (not consistently measurable). |
| Action - Inputs | ⭐ Inputs | 1325 | Ideas or native survey responses. |
| Action - Sessions | ⭐ Sessions | 1314 | One platform load by one human. |
| Target population | - | - | Not in the product yet, so not in Metabase. |

If the user asks for something that one of these models clearly answers, run it as `execute` in card mode rather than writing SQL by hand. See `references/queries.md` for ready-to-use snippets.

## Data gotchas - read this before writing SQL

These have bitten people. Apply them automatically.

1. **Filter to active tenants by default.** All `⭐` models include data from **all tenants** - demo, trial, churned. Almost every business question wants only active customers. Add `tenant → Core lifecycle stage = 'active'`. If the user wants "all tenants" or "trial + active", confirm before opening it up.
2. **Don't query the raw `users` table without filters.** It includes (a) people invited but who never accepted (`invite_status = 'pending'`) and (b) people who started but didn't finish registration (`registration_completed_at IS NULL`). Either start from ⭐ Users (preferred), or apply both filters: `invite_status <> 'pending' AND registration_completed_at IS NOT NULL`.
3. **Daily counts: filter on yesterday, not today.** Metabase reloads overnight, so "today" is empty or partial. The history-tracking script always stamps yesterday's date on results it gathers today, for this reason.
4. **Don't trust "evolution over time" derived from a single snapshot.** Plotting projects by `created_at` against tenant `created_at` won't show the historical reality - things have been deleted, tenants have churned. For time-series of point-in-time metrics, define a History-Tracked Question instead.
5. **Joins: prefer ⭐ models over raw tables.** Most cross-table questions are already denormalized in the ⭐ models. If you find yourself joining four+ raw tables, check the ⭐ collection first.

## History-Tracked Questions (point-in-time metrics)

For metrics that need a true historical series (e.g. "active tenants over the last 12 months"), Go Vocal runs a daily script ([cl2-script-historic](https://github.com/CitizenLabDotCo/cl2-script-historic)) that executes every question in the **History-Tracked Questions** collection (collection ID 66) and appends the result to a single table.

- Output lives in: database `CitizenLab` → schema `historical_data` → table `metrics`, columns `metric`, `date`, `value`.
- Stored value is yesterday's value, stamped with yesterday's date.
- Reference card to copy from: question 1320 (`active_tenants`).

**Rules for a question to be picked up by the script** (all must hold, otherwise it's silently ignored):

1. Lives in collection 66 (History-Tracked Questions). Permission gate - ask in `#metabase` if needed.
2. Returns exactly **one row**.
3. Returns exactly **one column**.
4. Returns a **number**.
5. Question name is unique and `lowercase_with_underscores` - this becomes the `metric` value.
6. If counting "today's X", filter on **yesterday** (see gotcha #3).

When a user asks "track this over time", first check `historical_data.metrics` for an existing series; only create a new tracked question if nothing fits.

## Collections

Folder-like structure for cards/dashboards/models. Three flavors:

- **Personal collection** - your own scratch space. Default landing spot for exploration.
- **Team collections** - one per team. Anything broadly useful to the team.
- **Our analytics** - the shared root, contains the ⭐ models pinned at top.

Don't pollute team or shared collections with one-off exploratory questions. Save junk to your personal collection.

## Questions vs dashboards vs models

- **Question** - a single saved query. Default pick when starting a new analysis.
- **Dashboard** - combines multiple saved questions and applies shared filters.
- **Model** - a question intended to be built on by others. **Don't create models** unless they're clearly reusable and well-defined. The ⭐ models are the canonical example.

## Exporting to Google Sheets

Two paths. Default to (1) Snapshot.

**(1) Snapshot - one-off:** Run the question, `Download full results` → CSV → import to Sheets. Best for one-off analyses.

**(2) Live - `importdata()`:** Enable sharing on the question, copy the CSV URL, paste into `=importdata("...")` in Sheets. Only use this when the sheet really needs live data (e.g. used as a dashboard). Downsides + rules:

- **Keep it minimal** - few rows, few columns. Do aggregation in Metabase, not Sheets.
- **No PII.** Sheets isn't on our DPA subprocessor list. No names, emails, avatar URLs, or user IDs.
- **Assume it will break.** Schema drifts; nobody guarantees your question keeps working.
- **Clean up.** `importdata` keeps polling forever and loads the Metabase server. Delete it when unused, disable sharing on the question.

If the user asks for a Metabase export from Claude, prefer the `export` MCP tool (writes a real file) over generating a CSV by hand.

## Output conventions

When answering a Metabase question end-to-end:

1. State which curated model or saved card you're using and why (or "no ⭐ model fits, going to SQL").
2. Show the filters applied (especially the active-tenants filter).
3. Return the numbers, then link the card/dashboard if one exists (`https://metabase.hq.govocal.com/question/<id>` or `/dashboard/<id>`).
4. Flag any caveat the gotchas section raises - e.g. "this is a today's-snapshot view, not point-in-time".

## When to escalate / ask in `#metabase`

- Need write access to History-Tracked Questions collection.
- Card is broken after a schema change.
- Unsure whether a metric definition matches the one a stakeholder is using.
- Metabase itself is slow/unresponsive.

## Reference files

- `references/queries.md` - copy-paste card-mode payloads and SQL snippets for the most common questions.
