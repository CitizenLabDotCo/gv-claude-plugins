# Notion Intent Signals database — schema and views

## Purpose

One rolling database accumulates every week's top-10 signals over time. This is where Wietse, the Growth team, and the AEs look each Tuesday for fresh leads — and where pattern analysis happens later (which countries are heating up, which signal types are converting, which AEs are following through).

## First-run setup

The first time the skill runs, create the database at:
**Notion → Growth workspace → new page titled "Intent Signals Radar"**

If the Growth workspace is ambiguous, DM Wietse: "I'm about to create the Intent Signals database. Which parent page should it live under?" and wait for confirmation.

## Database properties

| Property | Type | Details |
|---|---|---|
| **City** | Title | "Lyon", "Aarhus", "Ottawa", etc. |
| **Country** | Select | ISO country name. Color-code by region for visual scanning. |
| **Population** | Number | From Wikipedia or national census. |
| **Population tier** | Select | XS (<30k) / S (30–100k) / M (100–250k) / L (250–500k) / XL (500k+) |
| **Geography tier** | Select | Tier 1 / Tier 2 / Tier 3 |
| **Signal type** | Select | Tender / Budget / Strategic plan / Council resolution / Press release / News mention / New team |
| **Signal strength** | Number | Final score after base + bonuses + modifier, 0–20. |
| **Priority** | Formula | 🔥 if score ≥ 15, ⚡ if active-opp, 📈 if score 10–14, 👀 if score < 10 |
| **Detected date** | Date | The date Claude first surfaced this signal. |
| **Signal date** | Date | The date the source was published (may predate detection by up to 14 days). |
| **Source URL(s)** | URL (multi) | Store all source URLs — tender portal, press article, budget PDF. |
| **Native-language excerpt** | Rich text | 1–2 sentence quote from the original source, in its original language. |
| **English dossier** | Rich text | 150-word briefing: what happened, why it matters, how Go Vocal is positioned, what the AE should know. |
| **CRM status** | Select | Net-new / Cold lead / Active opp / Dormant / Customer expansion (for Planhat hits) |
| **Salesforce link** | URL | Deep link to the Salesforce account if one exists. |
| **Planhat link** | URL | Deep link to Planhat if a customer-expansion signal. |
| **Suggested AE owner** | Person (or select if Notion doesn't have the team) | Based on Salesforce territory. |
| **Gmail draft URL** | URL | Deep link to the Gmail draft in Wietse's inbox. |
| **Week-of tag** | Text | "2026-W17", "2026-W18" — ISO week, for easy weekly filtering. |
| **Status** | Select | New / Wietse reviewed / Sent to AE / AE engaged / No action / Archived |
| **Progression link** | Relation | Link to earlier DB rows for the same city if the signal has progressed (e.g., budget → tender). |

## Standing views

### 1. This week
- Filter: `Detected date` in last 7 days
- Sort: `Signal strength` desc
- Display: Board by `Priority`, grouped 🔥 → ⚡ → 📈 → 👀
- **This is the default view** — Wietse's Tuesday-morning landing page.

### 2. Deal acceleration
- Filter: `CRM status` = "Active opp"
- Sort: `Signal strength` desc
- Purpose: AEs check this view during pipeline reviews to find intel on their live deals.

### 3. All-time log
- No filter
- Sort: `Detected date` desc
- Purpose: Historical record, pattern analysis, win/loss research.

### 4. Customer expansion
- Filter: `CRM status` = "Customer expansion"
- Sort: `Signal strength` desc
- Purpose: Planhat CSMs see intent signals from existing customers for upsell conversations.

### 5. By country (optional)
- Group by: `Country`
- Useful for regional sales leads doing country-level reviews.

## Writing rows

Each weekly run appends 10 rows (or fewer if the market is thin). When appending:

1. Set `Detected date` = today.
2. Set `Signal date` = the actual publication date of the source.
3. Populate the English dossier using this template:

   > **What happened** (1–2 sentences): [concrete description of the signal, with source citation]
   > **Why it matters** (1–2 sentences): [what about this signal makes it ICP-relevant — size, politics, stage, budget]
   > **How Go Vocal is positioned** (1 sentence): [the comparable reference city, if one exists, or the positioning angle]
   > **AE should know** (1–2 bullets): [anything that would change the outreach — existing AE relationship, known competitor in play, political sensitivity]

4. Paste the Gmail draft URL into `Gmail draft URL` *after* creating the draft, so the Notion row links to the email.
5. Set `Status` = "New" (default). Wietse will flip to "Wietse reviewed" after his Tuesday read.

## Preventing duplicates

Before creating a row, query the DB for:
- Same `City` + `Country`
- `Detected date` within last 90 days

If there's a match AND the new signal is the same type (e.g., another tender when one was already logged), skip. If the new signal is a **progression** (e.g., a tender following a previously logged budget line), create the new row and use `Progression link` to relate it to the earlier row. These are the most interesting entries.

## Maintenance

Every quarter Claude should:
- Archive rows with `Status` = "No action" and `Detected date` older than 6 months.
- Generate a quarterly summary view: top countries by signal count, conversion from signal → engaged, signal-type mix.

(A separate skill or scheduled task can handle this — not part of the weekly run.)
