---
name: intent-signals-radar
description: Surface buying-intent signals each week from ICP cities (100k+ population in democratic EU + North America) that indicate they are actively looking for a digital citizen engagement platform. Use this skill whenever Wietse says "run intent radar", "weekly intent briefing", "who should we prospect", "any new tenders", "intent signals", "show me cities looking for participation platforms", or anything about surfacing net-new outbound leads from government procurement, budget decisions, or participation initiatives. Also runs on the scheduled Tuesday 07:00 Brussels slot. Produces 10 ranked signals with full dossiers in the rolling Notion Intent Signals DB, plus a Gmail draft in Wietse's CEO voice for each signal. Even casual phrasings like "find me some prospects", "what's happening in procurement this week", or "anything to go after?" should trigger this skill.
---

# Intent Signals Radar

## Purpose

Every week, surface the 10 strongest buying-intent signals from ICP cities — governments actively signaling they want a digital citizen engagement platform. The goal is to convert outbound prospecting from cold guessing into timed, signal-driven outreach where Go Vocal shows up exactly when a city has said "we are doing this now."

A signal is worth surfacing only if a specific, named ICP institution has made a *public*, *verifiable*, *recent* move toward digital participation. Speculation, industry news, and generic civic-tech coverage do not qualify.

## When to run

- **Scheduled**: every Tuesday at 07:00 Brussels time
- **On demand**: when Wietse asks for intent signals, prospects, tenders, or weekly outbound intel
- **Ad hoc**: when Growth leadership asks "is anything live in [country/region]?"

## ICP definition (who qualifies)

A city/institution qualifies if **all** of these are true:

1. **Org type**: Local government (city, municipality, district). Regional, state, federal, or government-adjacent (healthcare, school district, transit authority) qualify only as Tier 2 fit.
2. **Population**: ≥ 100,000 inhabitants. Cities between 100k–250k are Tier 2, 250k+ are Tier 1. Sub-100k only qualifies if it's a national/regional capital.
3. **Geography**: Democratic EU (all EU-27, UK, Norway, Switzerland, Iceland) + North America (US, Canada) + Oceania (Australia, NZ). Exclude countries with no credible democratic local-government mandate.

See `references/scoring-rubric.md` for the full fit-tier weighting (grounded in Go Vocal's existing ICP framework).

## Signal sources to scan each week

Scan these source buckets in order of signal strength. See `references/tender-portals.md` for the full list of portal URLs, search patterns, and local-language keywords.

### 1. Tender/RFP portals (strongest signal — 10 pts base)

Official procurement publications. A published tender is the nearest thing to "we are about to buy."

- **EU-wide**: TED (Tenders Electronic Daily)
- **France**: BOAMP, marches-publics.gouv.fr
- **Belgium**: e-Notification (FR/NL)
- **Netherlands**: TenderNed
- **Germany**: bund.de, evergabe-online.de
- **UK**: Contracts Finder, Find a Tender
- **Spain**: Plataforma de Contratación del Sector Público
- **Italy**: CONSIP, regional portals
- **Nordics**: Mercell, Visma Opic, Hilma (FI), Doffin (NO)
- **US**: SAM.gov, DemandStar, BidNet, state portals
- **Canada**: MERX, BuyandSell.gc.ca, provincial portals
- **AU/NZ**: AusTender, GETS

**Keywords (translated per portal's working language)**: "citizen participation", "public consultation platform", "digital engagement", "e-participation", "participatory budget", "ideation platform", "deliberative democracy", "citizen panel software".

### 2. Municipal budget & strategic plan documents (7 pts base)

City budgets and multi-year strategic plans that explicitly commit funds or roadmap items to digital participation. Scrape city websites, council meeting document repositories, and national open-data portals for the current budget year.

### 3. Council resolutions, mayor speeches, press releases (5 pts base)

Official city communications announcing participation initiatives — launch of a participatory budget, a new consultation platform, a citizens' assembly, or a participation office being stood up.

### 4. News & council minutes (3 pts base)

Local press coverage and published council minutes mentioning participation projects. Use Google News, local press aggregators (e.g. Westinfo, La Gazette des Communes), and council minutes archives.

**Why job-board signals are not scanned in v1**: Wietse's explicit scope for this skill. LinkedIn job postings ("Participation Director" hires) are covered separately by Growth's lead-enrichment workflow and should not be duplicated here. If a new hire is announced in a press release, that counts as a source-3 signal.

## Scoring rubric

The full rubric is in `references/scoring-rubric.md`. Summary:

**Base points (by signal type)**
| Signal | Points |
|---|---|
| Published tender/RFP referencing digital engagement | 10 |
| Budget line item or strategic plan commitment | 7 |
| Council resolution / mayor announcement / press release | 5 |
| Local news coverage / council minutes mention | 3 |

**Bonuses (stackable)**
- Multi-source confirmation (same signal appears in ≥2 independent sources): +2
- Population ≥ 500k: +2
- National or regional capital: +1
- Tier 1 geography (UK, France, Flanders, CA, TX, and Go Vocal White-Glove markets): +2
- Signal dated in last 7 days (vs 8–14 days): +1
- Explicit budget figure ≥ €/$ 100k: +2
- Mentions specific platform capability (ideation, participatory budgeting, deliberation): +1

**Cap**: 20 points. The top 10 scored signals each week go into the Notion DB.

## Freshness and deduplication

- **Freshness window**: only consider signals published or first indexed in the last 14 days.
- **Dedupe**: before scoring, query the rolling Intent Signals Notion DB (see `references/notion-db-schema.md`) for any signal already logged in the past 90 days against the same city. If present, skip — do not re-surface. This keeps the weekly briefing genuinely new.
- If a previously logged signal has *materially progressed* (e.g. a budget mention in week 1 becomes a published tender in week 4), log it as a new signal with a `progression` link back to the earlier row. Those are some of the most actionable signals.

## Language handling

- **Scan**: read sources natively in FR, NL, DE, ES, IT, PT, EN, and the Nordic languages. Local-language scanning is non-negotiable — most municipal signals never appear in English.
- **Summarize**: write the Notion dossier and the Gmail draft in English. Wietse reviews in English; the AE can translate if needed.
- **Quote the source in the original language** inside the dossier (a 1–2 sentence snippet) so the AE can verify and optionally reuse it.

## CRM cross-check (before writing to Notion)

For every candidate signal, cross-check Planhat and Salesforce via their MCP connectors:

1. **Planhat lookup** by city name + country. If the city is an active Planhat customer (status = Live, Onboarding, or Renewing), **drop the signal** — this is not a net-new prospect. Log it to a separate `Customer expansion signals` view instead so the CSM sees it.
2. **Salesforce lookup** by account name. Tag each surviving signal with its CRM status:
   - `net-new` — no Salesforce account exists
   - `cold lead` — account exists, no open opp, last touch > 90 days
   - `active opp` — an open opportunity exists → this becomes **deal-acceleration intel**, flag with ⚡
   - `dormant` — closed-lost or closed-no-decision in last 12 months → flag as `recycle candidate`

3. **Suggested owner**: based on Salesforce territory rules (country → region → AE), tag each signal with the likely AE owner. If ambiguous, tag with the regional sales lead.

## Output format

### Notion: rolling Intent Signals database

Append one row per top-10 signal to the rolling DB. See `references/notion-db-schema.md` for the full property list. Each row contains: city, country, population, signal type, score, source link(s), native-language quote, English dossier, CRM status, suggested AE owner, linked Gmail draft URL, and the week-of tag.

The database has three standing views:
- **This week** (filter: `Detected date` in last 7 days, sort by score desc)
- **All-time log** (no filter, sort by date desc)
- **Deal acceleration** (filter: CRM status = active opp)

### Gmail: one draft per signal, in Wietse's voice

Create a Gmail draft for each of the 10 signals:
- **To**: best-effort contact (mayor, city manager, head of participation). Use the CRM contact if present; otherwise leave the `to:` field empty and put the suggested recipient + reasoning in the first line of the body.
- **Subject**: specific and signal-referencing. Never generic.
- **Body**: Wietse's CEO-to-Mayor first-touch voice. See `references/outreach-voice.md` for patterns and sample drafts. ~120 words. References the specific signal concretely (tender number, budget line, press-release quote). Offers a 20-minute conversation, not a demo.
- **Link the draft back** into the Notion row as `Gmail draft URL`.

### Chat summary (on on-demand runs only)

When run on-demand, also post a short chat summary: "10 signals logged. Highlights: [top 3 by score, one line each]. Full briefing in Notion: [link]."

Do not post a chat summary on the scheduled Tuesday run — the Notion DB + Gmail drafts are the delivery.

## Workflow for each weekly run

1. **Load context**
   - Read `references/scoring-rubric.md`, `references/tender-portals.md`, `references/outreach-voice.md`, `references/notion-db-schema.md`.
   - Query the Notion Intent Signals DB for the last 90 days of logged signals (for dedupe).
   - Note today's date; set the freshness window to (today - 14 days) → today.

2. **Scan sources in parallel by region** (spawn subagents — one per region: UK/IE, FR/BE-FR/LU, NL/BE-NL, DACH, Nordics, Iberia, Italy, US, Canada, AU/NZ). Each subagent returns a raw list of candidate signals with: city, country, source URL, signal type, publication date, native-language excerpt.

3. **Merge + dedupe** against the 90-day DB history. Drop already-logged signals unless they've materially progressed.

4. **Score** each surviving candidate using the rubric. Keep the top 25.

5. **CRM cross-check** the top 25 (Planhat first — drop customers; Salesforce second — tag status and suggest owner).

6. **Re-rank** if needed (deal-acceleration ⚡ signals get a +1 priority bump for surfacing — they're the most AE-actionable).

7. **Select final top 10** and, for each:
   - Draft the English dossier (~150 words): what happened, why it matters, how Go Vocal is positioned, what the AE should know before reaching out.
   - Draft the Gmail outreach in Wietse's voice (~120 words) and save as a Gmail draft.
   - Create the Notion row with all properties, the dossier, and the Gmail draft URL.

8. **Validate before finishing**:
   - All 10 rows written? (If fewer valid signals exist, write what you have and flag it in the Tuesday-run log.)
   - All 10 Gmail drafts created and linked?
   - Any signal with a score ≥ 15? (If so, DM Wietse a heads-up — these are rare enough that they warrant his eye before he sees the weekly Notion view.)

## Guardrails

- **Never send** the Gmail drafts. Always draft-only. Wietse sends manually after review.
- **Never create a Salesforce lead** from this skill. The whole point is to surface intel so a human decides whether to enter an account.
- **Do not fabricate signals.** If a week is thin on strong signals, deliver 4 great ones, not 10 mediocre ones. Flag the thinness in the Tuesday log so Wietse knows it's a genuine market observation, not a skill failure.
- **Respect robots.txt and rate limits** when scraping city websites. Prefer official APIs, RSS feeds, and open-data portals over scraping.
- **GDPR-aware**: when pulling contact info from LinkedIn/websites, record only business-purpose public contacts (mayor, press, procurement office). Never scrape personal data from citizen-facing portals.

## Reference files

- `references/tender-portals.md` — full list of EU + North America + ANZ tender portals with URLs, search patterns, and local-language keywords
- `references/scoring-rubric.md` — detailed point system + Go Vocal ICP geography tiers
- `references/outreach-voice.md` — Wietse's CEO-to-Mayor outreach patterns with sample drafts
- `references/notion-db-schema.md` — Intent Signals database schema (properties, views, setup instructions)

## First-run setup (one-time)

The very first time this skill runs:

1. Create the **Intent Signals** rolling database in Notion under the Growth workspace (ask Wietse for the exact parent page if ambiguous). Use the schema in `references/notion-db-schema.md`.
2. Set up the three standing views.
3. Flag to Wietse in chat: "Database created at [URL]. Future weekly runs will append here."
