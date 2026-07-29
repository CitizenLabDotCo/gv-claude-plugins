---
name: voc-gs-weekly-digest
description: >
  Generates the Go Vocal Customer Success Weekly Digest for the Head of Customer Success.
  Pulls meeting transcripts from Fireflies for the past 7 days, verifies and enriches each
  account against PlanHat (health score, CSM owner, lifecycle phase), extracts verbatim
  customer quotes with clickable timestamps, and formats everything into a structured
  four-section digest covering Customer Pain Points, Product Feedback, Blockers & Risks,
  and Adoption / Usage Signals.

  Trigger this skill whenever someone says: "weekly digest", "CS digest", "customer success
  digest", "generate the weekly report", "what came up in customer calls this week",
  "pull insights from Fireflies this week", or any variation asking for a summary of recent
  customer conversations. Also trigger for "digest for week N" or any date-range variant.
---

# CS Weekly Digest

## What this skill produces

A structured weekly digest for the Head of Customer Success, grounded entirely in real
Fireflies meeting data and live PlanHat account data. Every insight traces back to a
specific moment in a real conversation. Every account entry shows health, CSM, and a
link to the PlanHat profile.

---

## Step 1 — Determine the date range

Default: the past 7 days (Mon–Sun of the current week). If the user specifies a week
number or date range, use that. Note the week number for the digest header.

---

## Step 2 — Fetch Fireflies conversations

Use `fireflies_get_transcripts` with `fromDate` and `toDate` set to the date range.
Retrieve all meetings from the past 7 days.

For each meeting, note:
- Meeting title
- Participant list (names + email addresses)
- Meeting ID (needed for deep links)

---

## Step 3 — Match meetings to PlanHat accounts

For each Fireflies meeting, find the corresponding PlanHat company using **both signals**:

**Signal A — Company name match**
Extract keywords from the meeting title and search PlanHat with
`list_model_records` (MODEL: Company, FILTER: `name[contains]`).

**Signal B — Email domain match**
Extract the email domains of non-Go Vocal participants (anyone not at @govocal.com).
Query PlanHat with `list_model_records` (MODEL: Company, FILTER: `domains[contains]`).

A meeting is matched if either signal returns a PlanHat company. Use both to reduce
missed matches — titles are sometimes vague, and domain matching catches those cases.

**Exclude meetings with no PlanHat match** — they are either internal or unknown accounts.
Also exclude any meeting that is clearly internal (e.g. "Planhat x GoVocal: Team Training",
"All Hands", "Sprint Planning") even if a loose name match exists.

---

## Step 4 — Filter by account eligibility

For each matched PlanHat company, fetch:
```
SELECT: ["name", "phase", "mrr", "h", "owner", "domains", "custom.Lifecycle Phase"]
```

**Include the account if:**
- `mrr > 0` (active paying contract), OR
- `phase` is "1. Onboarding" (recently signed, MRR may not yet be set)

**Exclude the account if:**
- `phase` is "4. Churned"
- `mrr` is 0 or null AND phase is not Onboarding

Do NOT use the `status` field — it is unreliable in this PlanHat instance. Use `phase`
and `mrr` as the authoritative eligibility signals.

---

## Step 5 — Resolve CSM owner names

The `owner` field on a Company record is a User ID. Look up each unique owner ID
using `list_model_records` (MODEL: User) to get first + last name. Cache the results
so you don't re-query the same ID twice.

---

## Step 6 — Fetch full transcripts

For each eligible meeting, call `fireflies_get_transcript` with the meeting ID.
The transcript returns sentences attributed to speakers.

**Critical rule — never quote Go Vocal team members.**
Identify Go Vocal speakers as anyone whose name matches the internal team list OR
whose email domain is @govocal.com. Known Go Vocal names to filter out:
Aline, Joris, Fraser, Sophie, Sarah, Maya, Cindy, Aline Muylaert, Joris Gallens,
Fraser Henderson, Sophie Zinn, Sarah Horton, Maya Masterson, Cindy Eyang Biteghe.

Only extract quotes from **customer speakers** — the people who are not on that list
and not @govocal.com.

**Timestamp estimation**
Fireflies' toon-format transcripts do not embed per-sentence timestamps. Estimate
timestamps by position: `(sentence_index / total_sentences) × meeting_duration_minutes`.
Where summary-level timestamps are available from Fireflies metadata, prefer those for
accuracy. Mark estimated timestamps with `~` (e.g. `~14:35`).

**Translation**
If a quote is in Dutch or French, translate it to English for the digest and mark it
`[tr. from Dutch]` or `[tr. from French]` after the timestamp. The translation should
be natural but faithful — do not paraphrase, do not add meaning.

---

## Step 7 — Identify themes and structure the digest

Read across all transcripts and identify the key insights from the week. Group them
into the four sections below. There is no fixed number of themes per section — include
as many numbered items as the data warrants. If a section has nothing meaningful to
report, omit it rather than pad it.

Themes should be cross-account where possible (grouping 2–3 accounts around a shared
pattern is more useful than one theme per account). But a single-account theme is fine
if the insight is significant enough to stand alone.

---

## Step 8 — Write the digest

Use this exact format throughout:

### Header
```
CUSTOMER SUCCESS WEEKLY DIGEST
**Week [N] · [Date Range] · Prepared for Head of Customer Success**
```

### Section format
```
[emoji] **[Section Title]**

**[N]. [Theme headline — short, specific, actionable]**

* [3–5 line paragraph describing the theme. Name the accounts involved.
  Be concrete about what was said and what it means. No filler.]

> "[Verbatim customer quote]" — [Speaker first name + last name] ([timestamp link])  [tr. from X if applicable]
[Account Name](planhat profile url) · Health [emoji] [score] · CSM: [First Last]

> "[Second quote if relevant]" — [Speaker] ([timestamp link])
[Account Name](planhat profile url) · Health [emoji] [score] · CSM: [First Last]

**[N+1]. [Next theme]**
...
```

### The four sections (use these exact titles and emojis)
1. 🔴 **Customer Pain Points** — friction, frustration, unmet needs, usage problems
2. 💬 **Product Feedback** — feature requests, UX observations, missing capabilities
3. ⚠️ **Blockers & Risks** — renewal risk, launch delays, churn signals, internal resistance
4. 📈 **Adoption / Usage Signals** — momentum, positive sentiment, onboarding progress, re-engagement

### Timestamp deep links
Format: `([MM:SS](https://app.fireflies.ai/view/[Meeting-Title-Hyphenated]::[MeetingID]?t=[seconds]))`

Convert MM:SS to seconds for the `?t=` parameter. For example, 14:35 → `?t=875`.

The meeting title in the URL should use the Fireflies format: title words joined by
hyphens, special characters removed or replaced (apostrophes dropped, spaces → hyphens).
The separator between title and ID is `::` (double colon — not `--`).

Example:
`([03:13](https://app.fireflies.ai/view/Jackie-Denton-and-Fraser-Henderson::01KP66HX800HG74D7Z9AN93KGY?t=193))`

### PlanHat profile links
Format: `[Account Name](https://app.planhat.com/profile/[planhat_company_id])`

Use the `_id` field from the PlanHat Company record.

### Health score emoji coding
- 🟢 score 8–10
- 🟡 score 5–7
- 🔴 score 0–4

### Footer
```
*[N] conversations · Week [N] · [Date Range]*
```

---

## Quality rules

**Quotes must be verbatim.** Do not paraphrase. If a sentence is too long, use the
most meaningful clause rather than summarising what the person said. Use `...` to
indicate omissions only when the omission doesn't change meaning.

**One quote per speaker per theme is enough.** Don't stack multiple quotes from the
same person under one theme unless they're saying distinctly different things.

**Paragraph discipline.** The bullet paragraph under each theme should be 3–5 lines.
It exists to give context to the quotes — what was being discussed, why it matters,
which accounts are involved. Don't repeat information that's already in the quote.

**No Go Vocal team members may appear as quote sources.** Ever. Even if their comment
is insightful. The digest is about what customers said.

**Do not invent or hallucinate.** Every claim in the digest must be traceable to the
Fireflies transcript. If you're unsure whether something was said, don't include it.

---

## Example output unit

🔴 **Customer Pain Points**

**1. Internal adoption stalled by organisational skepticism**

* Two accounts are struggling to get internal colleagues to champion or use the platform.
  Sport Vlaanderen's communications team won't proactively propose platform use — they
  simply don't believe enough in its value. At Gravesham, the platform has drifted into
  an information bulletin board, shaped by how internal departments adopted it without
  consultation intent.

> "You can just tell they're not embracing it, because they don't believe in it enough themselves." — Jens De Rycke ([~48:00](https://app.fireflies.ai/view/Sport-Vlaanderen-Go-Vocal::01KNP7FN7KWQ6C5XT21TPTXSD2?t=2880)) [tr. from Dutch]
[Sport Vlaanderen](https://app.planhat.com/profile/63c7ec67cb7b747170421b46) · Health 🟡 6 · CSM: Joris Gallens

> "We're not using it as a consultation platform as much as we should." — Jackie Denton ([03:13](https://app.fireflies.ai/view/Jackie-Denton-and-Fraser-Henderson::01KP66HX800HG74D7Z9AN93KGY?t=193))
[Gravesham Borough Council](https://app.planhat.com/profile/6644beb065057c22c23ccade) · Health 🟡 6 · CSM: Fraser Henderson
