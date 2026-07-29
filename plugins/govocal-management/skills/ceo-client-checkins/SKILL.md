---
name: ceo-client-checkins
description: >
  Prepare Wietse's weekly CEO-to-CEO client check-in emails — 6 personalized Gmail drafts
  for the most important accounts from the Planhat CEO List, prioritized by churn risk,
  MRR, renewal urgency, and last touch. Region-specific 20-min meeting slots pulled from
  Wietse's Google Calendar (US/CA clients: Thursday 15:00–18:00 Brussels only; EU clients:
  Thursday 15:00–18:00 OR Tuesday 09:00–12:00 Brussels). Use this skill whenever Wietse
  says "run CEO check-ins", "draft client outreach emails", "prepare this week's client
  check-ins", "run the Thursday client emails", "weekly client touchbase", "6 client
  emails", "who should I reach out to this week", "time for client drafts", or anything
  about the recurring 20-min CEO touchbase flow with Planhat CEO List accounts. Also runs
  on the Thursday 8am scheduled task. Primary goal: book 3 client calls per week to surface
  blockers early and anticipate churn. Also trigger on casual phrasings like "let's do the
  CEO calls thing" or "client check-in time".
---

# CEO Client Check-ins — Wietse Van Ransbeeck

You are preparing this week's CEO-to-CEO client check-in emails for Wietse (Co-Founder & CEO of Go Vocal, wietse@govocal.com).

## Why this exists

Wietse wants a steady rhythm of short, honest check-ins with client leaders. The **primary purpose** of every call is to LISTEN — what's working on the platform, what's creating friction, what challenges they face. These conversations directly shape Go Vocal's roadmap and where the company invests next. A secondary purpose is rapport and briefly sharing direction — but only after listening.

**Success:** 3 of 6 drafted emails convert to a booked 20-min call this week. Over time, Wietse stays close to clients, surfaces blockers early, and anticipates churn before it hits.

Every email is a draft in Gmail. Wietse reviews, tweaks, sends. Nothing goes out automatically.

## Data sources

- **Planhat** (MCP: `ca415ee5-405d-4561-a64c-a943bf04815f`) — the Company model contains the CEO List. The EndUser model contains contacts.
- **Google Calendar** (MCP: `d3c0af37-689b-411d-952e-3ab2ca4ba5dc`) — source of truth for Wietse's availability.
- **Gmail** (MCP: `4e617867-277d-4d23-bcd2-b67103642785`) — where drafts are created.
- **Notion** (MCP: `a458e9bb-9eff-467d-a2a8-d03ee1f921ca`) — the "CEO Client Check-ins — Log" page tracks every run so the skill can avoid contacting the same account twice in 8 weeks.
- **Slack** (MCP: `dc83c5c0-c7c0-49ec-ba2a-d0df9be7b18a`) — final summary DM to Wietse (user_id `U0945ADLJ`).

## End-to-end workflow

### 1. Pull candidate accounts from Planhat

Call `list_model_records` on MODEL `Company` with:

- FILTER: `{"custom.CEO List[equal to]": "true"}`
- SELECT: `["name", "country", "custom.Region List", "custom.Country locale", "custom.Language", "owner", "phase", "custom.Lifecycle Phase", "mrr", "arr", "h", "hDiff", "renewalDate", "renewalDaysFromNow", "custom.Bad health recovery potential", "lastTouch", "lastTouchByType.email", "domains"]`
- LIMIT: 50

Filter OUT any company where:
- `phase == "4. Churned"` or `custom.Lifecycle Phase == "4. Churned"`, or
- `custom.Lifecycle Phase == "5.Hibernation"`, or
- The account was logged in the Notion "CEO Client Check-ins — Log" within the last 8 weeks (see step 5).

### 2. Rank by weighted priority score

Don't just pick the least-recently-contacted account. Pick the ones where a CEO touch has the highest business value right now. Compute a score for each candidate:

```
priority_score =
    0.35 * churn_risk       # (100 - health), where missing health → 60
  + 0.25 * mrr_weight       # log10(max(mrr, 1)) / log10(10000) * 100, capped at 100
  + 0.20 * renewal_urgency  # renewalDays < 60 → 100, < 120 → 70, < 180 → 40, else → 15
  + 0.20 * days_due         # min(days_since_lastTouchByType.email, 180) / 180 * 100
```

Soft bumps (add to raw score):
- `+10` if `phase == "3. Pre-renewal"`
- `+10` if `custom.Bad health recovery potential` contains "High"
- `+5` if `hDiff` (30-day health change) is negative

Rank descending. Pick the **top 6**. If fewer than 6 candidates survive filtering, use what you have and flag it in the Slack summary.

### 3. Find the right contact per account

For each selected company, call `list_model_records` on MODEL `EndUser` with:

- FILTER: `{"companyId[equal to]": "<COMPANY_ID>", "archived[equal to]": "false", "custom.Block emails[equal to]": "false"}`
- SELECT: `["name", "firstName", "lastName", "email", "position", "primary", "custom.Role", "custom.COUNTRY"]`
- LIMIT: 30

Pick ONE contact using this priority (stop at the first match):

1. `custom.Role` contains `"Key Strategic Contact"`
2. `custom.Role` contains `"Key Admin"` AND `position` matches (case-insensitive) any of: "director of community engagement", "citizen participation", "civic engagement", "participation citoyenne", "burgerparticipatie", "directeur participation", "engagement director", "democratic engagement"
3. `custom.Role` contains `"Strategic Contact"`
4. `custom.Role` contains `"Key Admin"` (regardless of position)
5. `primary == true`
6. Any contact whose `position` matches keywords like "mayor", "director", "CEO", "alderman", "chef", "burgemeester", "alcalde", "directeur"

If none match, skip the company with status `NO_CONTACT` in the log and move to the next-ranked account from step 2 (so you still end up with 6).

### 4. Determine email language per contact

Use this mapping, in order — use the first signal that resolves to a language:

1. EndUser `custom.COUNTRY` → `BE-NL` or `NL` → **Dutch**; `BE-FR` or `FR` → **French**; anything else → fall through
2. Company `custom.Country locale` → `NL-NL` or `BE-NL` → **Dutch**; `FR-FR` or `BE-FR` → **French**; else fall through
3. Company `custom.Language` → `NL` → **Dutch**; `FR` → **French**; else fall through
4. Default → **English**

### 5. Check the Notion log and append this run's entries

Search Notion for a page titled exactly **"CEO Client Check-ins — Log"**. If it doesn't exist, create it as a database under Wietse's private workspace (no parent) with the schema in the "Notion log schema" section below. Then search its data source for entries from the last 8 weeks and use those companyIds to exclude from step 1 on the next run.

Before creating any Gmail drafts, append 6 new rows for this run — one per selected company — with status `Pending`. After successfully creating each Gmail draft, update that row to `Drafted`. If a company was skipped in step 3, write status `NO_CONTACT`. This log is the source of truth for deduping.

### 6. Pull 2–3 concrete 20-min slots from Wietse's calendar

Determine the slot window based on the client's country/region:

- **US / CA clients** (company `country` in `["United States", "Canada"]` OR `custom.Region List == "North America"`) → Thursday 15:00–18:00 **Europe/Brussels** ONLY.
- **All other clients** (EU, UK, DACH, Francophonie, Netherlands, Flanders, etc.) → Thursday 15:00–18:00 **OR** Tuesday 09:00–12:00 Europe/Brussels.

Look at the next **14 days starting tomorrow**. For each candidate window, call `suggest_time`:

```
attendeeEmails: ["primary"]
startTime: <window start as ISO>
endTime: <window end as ISO>
durationMinutes: 20
timeZone: "Europe/Brussels"
preferences: {"startHour": "<window start hour>", "endHour": "<window end hour>", "excludeWeekends": true, "pageSize": 5}
```

From the returned free slots across all relevant windows for this client, pick 3 that are SPREAD:
- Different days where possible
- For EU clients, ideally mix Tue-morning and Thu-afternoon
- Skip any slot overlapping an existing event (trust the `suggest_time` response)

Format each slot for the email body in the email's language. Use Brussels local time and label it clearly. Examples:

- **English**: `Thursday, 30 April — 15:30 (Brussels time)`
- **Dutch**: `Donderdag 30 april — 15:30 (Brussel)`
- **French**: `Jeudi 30 avril — 15h30 (heure de Bruxelles)`

For US/CA clients, append the local US time for context: e.g., `Thursday, 30 April — 15:30 Brussels / 09:30 ET`. Work out the offset from Europe/Brussels:
- US Eastern: Brussels −6h (summer) / −6h (winter)
- US Central: Brussels −7h
- US Mountain: Brussels −8h
- US Pacific: Brussels −9h
- Canada Eastern: same as US Eastern

If fewer than 3 free slots exist across the available windows, use 2 and note it in the Slack summary. Don't drop below 2. If even 2 aren't possible, flag the account and move on.

### 7. Create a Gmail draft per contact

Use `create_draft`. Use the templates in "Email templates" below. Interpolate `{first_name}`, `{company_name}`, `{slot_1}`, `{slot_2}`, `{slot_3}`. If only 2 slots are available, omit the `{slot_3}` line cleanly (don't leave a blank bullet).

Do NOT add custom personalization beyond first name + company name. The template's sincerity is the point — fake-personalized openings ("I noticed you recently...") feel hollow and almost always wrong. If there's a significant signal you think Wietse should reference (e.g., a health drop, renewal in 30 days), mention it in the Slack summary instead so he can add it manually before sending.

### 8. Post a Slack DM summary to Wietse

Send a Slack DM to Wietse (channel_id `U0945ADLJ`) with this structure:

```
*CEO check-ins — {date}*

{N} drafts waiting in Gmail. Target: 3 booked this week.

1. *{Company}* ({language}) — {Contact Name}, {Position}
   Slots: {slot_1} / {slot_2} / {slot_3}
   Why this week: {short reason — e.g., "renewal in 42 days + health dropped 12 pts", "highest MRR on the list, 4 months since last email"}

2. ...

(if any NO_CONTACT cases, list them here with company name + why)
(if any slot-shortage cases, note them here)

Log: {Notion page URL}
```

The "Why this week" line is valuable — it tells Wietse what the priority signal was so he can tune a sentence before sending.

## Email templates

### English

**Subject:** `20-min catch-up?`

**Body:**
```
Hi {first_name},

I'm Wietse, CEO and co-founder of Go Vocal. I'd love to check in with you on how our partnership between {company_name} and Go Vocal is currently going for you.

I'm especially interested in what's working well with the platform, where you're encountering friction, and any challenges you're facing. These conversations directly shape how we improve and where we invest next. I can also briefly share what we're building, but the focus is on hearing your perspective.

Would any of these work for a 20-minute call?

• {slot_1}
• {slot_2}
• {slot_3}

If none of these fit, feel free to suggest a time that does and I'll make it work.

Best,
Wietse

—
Wietse Van Ransbeeck
Co-founder & CEO, Go Vocal
```

### Dutch (NL, BE-NL)

**Subject:** `20 minuten bijpraten?`

**Body:**
```
Beste {first_name},

Ik ben Wietse, CEO en medeoprichter van Go Vocal. Ik zou graag even met jou willen afstemmen over hoe ons partnerschap tussen {company_name} en Go Vocal momenteel voor jullie verloopt.

Ik ben vooral benieuwd naar wat goed werkt op het platform, waar jullie wrijving ervaren, en welke uitdagingen jullie tegenkomen. Deze gesprekken bepalen rechtstreeks hoe we verbeteren en waarin we volgend investeren. Ik kan ook kort delen waaraan we werken, maar de focus ligt op jullie perspectief.

Past één van deze momenten voor een gesprek van 20 minuten?

• {slot_1}
• {slot_2}
• {slot_3}

Past geen van deze? Stel gerust zelf een moment voor dat wel schikt — dan zorg ik dat het lukt.

Hartelijke groet,
Wietse

—
Wietse Van Ransbeeck
Medeoprichter & CEO, Go Vocal
```

### French (FR, BE-FR)

**Subject:** `20 minutes d'échange ?`

**Body:**
```
Bonjour {first_name},

Je suis Wietse, CEO et cofondateur de Go Vocal. J'aimerais faire le point avec vous sur la manière dont notre partenariat entre {company_name} et Go Vocal se déroule actuellement de votre côté.

Je suis particulièrement intéressé par ce qui fonctionne bien sur la plateforme, les points de friction que vous rencontrez, et les défis auxquels vous êtes confrontés. Ces échanges influencent directement nos améliorations et nos prochains investissements. Je peux aussi partager brièvement ce que nous construisons, mais l'essentiel est d'entendre votre perspective.

Un de ces créneaux vous conviendrait-il pour un appel de 20 minutes ?

• {slot_1}
• {slot_2}
• {slot_3}

Si aucun ne convient, n'hésitez pas à me proposer un autre moment — je m'adapterai.

Bien cordialement,
Wietse

—
Wietse Van Ransbeeck
Co-fondateur & CEO, Go Vocal
```

## Notion log schema

If the "CEO Client Check-ins — Log" database doesn't exist, create it with this schema (SQL DDL passed to `notion-create-database`):

```sql
CREATE TABLE (
  "Company"       TITLE,
  "Run Date"      DATE,
  "Contact Name"  RICH_TEXT,
  "Contact Email" EMAIL,
  "Position"      RICH_TEXT,
  "Language"      SELECT('EN':blue, 'NL':orange, 'FR':red),
  "Region"        SELECT('EU':green, 'US/CA':purple, 'Other':gray),
  "Slots Proposed" RICH_TEXT,
  "Priority Score" NUMBER,
  "Why This Week"  RICH_TEXT,
  "Status"        SELECT('Pending':gray, 'Drafted':blue, 'Sent':green, 'Booked':green, 'Declined':red, 'No reply':yellow, 'NO_CONTACT':red),
  "Planhat Company ID" RICH_TEXT,
  "Notes"         RICH_TEXT
)
```

Future runs read this database to dedupe: skip any `Planhat Company ID` that appears with a `Run Date` within the last 56 days (8 weeks).

## Operating rules

**Always drafts, never sends.** Use `create_draft`, not anything that sends. Wietse is the last human in the loop.

**Don't overshoot personalization.** The templates are deliberately CEO-to-CEO: warm, direct, humble, no marketing gloss. Inserting fake-personalized lines almost always reads worse than leaving it clean.

**Respect time zones in the output.** Clients shouldn't have to do math. When slots are shown to a US client, include both Brussels and their local time.

**Log before you draft.** Always append the run rows to Notion first, so if draft creation fails midway, the log still reflects what was attempted.

**Be honest about shortages.** If the CEO List is empty, if suggest_time returns no slots, if a company has no usable contact — say so in the Slack summary. Don't silently skip.

**Tone over template fidelity.** If a specific client context (near-term renewal, known escalation) genuinely changes what should be said, surface it in the Slack summary for Wietse to add manually. Don't improvise the email body.

## When invoked manually (not scheduled)

If Wietse invokes this skill on demand ("run CEO check-ins now", "let's do the drafts"), execute the same workflow but:

- Confirm with him first whether to target 6 drafts or a different number for this run
- If it's been less than 3 days since the last scheduled run, mention the dedupe window so he knows to expect different accounts

## Reporting back

End your run with a concise summary in chat: number of drafts created, any NO_CONTACT cases, any slot shortages, the Notion log URL, and a one-line "next run" reminder (Thursday 08:00 Brussels).
