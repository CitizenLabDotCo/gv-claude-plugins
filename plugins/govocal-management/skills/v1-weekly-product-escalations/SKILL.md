---
name: v1-weekly-product-escalations
description: |
  Scan Fireflies meeting transcripts, PlanHat conversations, and Slack channels from the last 7 days to uncover product escalations — customer-reported bugs, missing-feature blockers, UX friction, and integration failures — and return a ranked list (top 10 + long-tail) with evidence links. ALWAYS trigger this skill when Jeroen, Irene, Koen, or any product/CS lead asks about: "product escalations", "customer blockers", "what's blocking the team", "what's blocking customers", "uncover product escalations", "churn-risk signals", "weekly product escalation report", "what came up in customer calls this week", "any product issues we should know about", or anything about surfacing product pain from customer-facing conversations. Trigger even on casual phrasings like "anything broken this week?" or "what do I need to escalate to product?".
---

# Weekly Product Escalations

You are surfacing product escalations for Go Vocal's product leadership. The goal is to help product, engineering, and CS leads quickly see what has been blocking the team or customers in the last 7 days — things that customers have **directly mentioned to us** and internal escalations that need product attention.

**Default time window:** last 7 days (rolling). If the user specifies a different window, use theirs.

**Default output:** ranked list in chat — top 10 + long-tail appendix. No Notion page, no Slack post, unless the user asks for one.

---

## Clarifying questions (only if missing)

Before running, confirm these four dimensions if the user hasn't already given them. If they gave you some of the answers already (e.g., they said "last 14 days") skip those questions.

1. **Scope of "escalation"**: bugs/broken functionality, missing features blocking deals/renewals, UX friction, integration/API issues — or all of the above.
2. **Source weighting**: all three equally (default), or customer-direct first, or Slack-first.
3. **Output format**: chat list (default), Notion page, Slack draft, or artifact.
4. **Prioritization**: composite score (default — tier × frequency × urgency) or single-dimension.

Defaults above represent what the user has already set. Don't re-ask unless the user prompt suggests a different mode.

---

## Sources

Run these three source scans **in parallel** — they're independent.

### 1. Fireflies — customer meeting transcripts

Use `fireflies_get_transcripts` with `fromDate` and `toDate` covering the window, `limit: 50`, `format: toon`. Read every summary and action_items list.

Then run targeted `fireflies_search` queries for high-signal keywords (the search grammar is single-keyword per query):

```
keyword:"bug" scope:sentences from:YYYY-MM-DD to:YYYY-MM-DD limit:20
keyword:"broken" scope:sentences from:... to:... limit:20
keyword:"blocker" scope:sentences from:... to:... limit:20
keyword:"urgent" scope:sentences from:... to:... limit:20
keyword:"can't" scope:sentences from:... to:... limit:20
keyword:"missing" scope:sentences from:... to:... limit:20
keyword:"limitation" scope:sentences from:... to:... limit:20
```

For each transcript that carries signal, record: meeting title, date, organizer email, `meeting_link`, 1-line summary, and the relevant action_item lines.

### 2. PlanHat — customer conversations

**Scan every non-bounce conversation from the window — not a narrow filter.** Category and sentiment slices are unreliable (the "negative" bucket is dominated by bounces; real escalations often sit under "General Enquires" or unsentimented threads). Pull the full set, drop the bounces, then read what's left.

Use `list_model_records` on `Conversation`. **Three things to get right:**

**a) One filter: the time window.**
```
{ "createdAt[more than]": "<start_date>" }
```
No category or sentiment filter — those slices miss real escalations.

**b) Filter out email bounces client-side.** Bounces are noise, not escalations. After pulling records, drop any conversation where:
- `fromAddress` starts with `mailer-daemon` or contains `Mail Delivery Subsystem`, OR
- `subject` contains `Delivery Status Notification` / `Address not found` / `Undelivered` / `delivery has failed`, OR
- `companyId == 0` (bounces are usually unassigned).

Everything that survives is a real customer touchpoint worth reading.

**c) Payload size — paginate with small pages.** The Conversation model returns heavy payloads; a `LIMIT: 25` query routinely exceeds the 25k-token response cap. To scan the full week:
- `LIMIT: 10`, minimal `SELECT`: `["subject", "snippet", "companyId", "createdAt", "category", "sentiment", "type"]`, `SORT: "-createdAt"`.
- Increment `OFFSET` by 10 each call until either (i) the page returns fewer than 10 records or (ii) `createdAt` drops below the window start.
- If a single page still errors with "result exceeds maximum allowed tokens", re-query with `LIMIT: 3`, or read the saved result file in ≤ 30k-char chunks and parse it with `jq` / Python.

For each surviving conversation, capture: subject, snippet, companyId (resolve to company name when it matters for ranking), createdAt, category, sentiment. Then scan subjects + snippets for the same signal keywords used elsewhere (bug, broken, not working, blocker, urgent, issue, can't, missing, limitation, escalate, churn, frustrated, unhappy, disappointed). Surface anything that describes a customer hitting a product problem — even if the conversation is categorised as "General Enquires" or has no sentiment score.

### 3. Slack — CSM, CS, and dev channels

`slack_search_public_and_private` does **not** support `OR` operators — space-separated terms are ANDed. Run one search per keyword, in parallel.

**Channels to scope with `in:#channel` for direct scans:**

| Channel | Slack ID | Why |
|---|---|---|
| #product-issues | C01J9DHRJTE | Formal escalation intake |
| #client-first-line-support | C01CGFE4BAN | CSM → support triage |
| #product-questions | C01JFNF05C1 | Feature/capability asks from sales/CS |
| #dev-tandem-quality-quest | C06CJ4D3B0R | Quality/security triage |
| #dev-tandem-formsync | C08P5QNA1M3 | FormSync-specific |
| #dev-tandem-scheduling | C0AF9V3AQ2E | Scheduling/phase-boundaries |
| #team-govsuccess | C98UFE3S8 | Weekly CSM digest — often surfaces recurring issues |
| #partner-engagedca-govocal | C0AT3JUKC4V | Flagship US partnership |
| #temp-engagedcalifornia-all-teams | C0ASTJ9A3E2 | EngagedCA cross-team |
| #temp-osp-customers | C0AP2H2Q083 | OSP migration customers |
| #temp-osp-onboarding | C0AN9C1RJHG | OSP onboarding stand-ups |

**Keyword searches to run across the workspace** (one per call, `sort: timestamp`, `after: YYYY-MM-DD`):
```
bug              broken          escalation       blocker
urgent           "not working"   "doesn't work"   feature request
client issue     churn risk      limitation       "can't"
```

For each hit, capture: channel name, author, CET timestamp, message text, permalink, and 2–3 surrounding context messages (the Slack tool returns context by default — keep it).

---

## Consolidation

Before scoring, merge duplicates:

- **Cross-source dedupe.** If the same escalation appears in Slack, Fireflies, and PlanHat, merge it into one entry with all evidence links. This also bumps the frequency score.
- **Group by root cause.** E.g., "FB OAuth broken on Wemmel" and "61 FB privacy URLs returning 502 across DACH + US" are the same underlying pre-renderer issue — one entry.
- **Separate symptoms that share a customer but have different root causes.** E.g., EngagedCA's survey re-entry bug and their email deliverability issue should stay as two bullets (different fixes needed), even though they're the same account.

## Scoring — composite (sum of three 1–5 dimensions, range 3–15)

**1. Customer weight** — who's affected?
- 5 = strategic partner / flagship reference client (e.g. EngagedCA, Lyon/OSP, Gravesham in renewal)
- 4 = high-MRR tier
- 3 = standard tier
- 2 = demo / prospect
- 1 = internal only

**2. Frequency** — how widespread?
- 5 = many tenants simultaneously (e.g. 61+ URLs, cluster-wide incident)
- 4 = recurring — same issue across multiple weeks
- 3 = multiple customers this week
- 2 = one customer, single instance
- 1 = internal reproduction only

**3. Urgency language** — how loud is the signal?
- 5 = "churn risk", "critical", "blocker", Wietse/Irene-level escalation, RFP commitment at stake
- 4 = "broken", "not working", "can't use X"
- 3 = "bug", "issue", clear functional complaint
- 2 = "confusing", "friction", UX request
- 1 = "nice to have", open feature request

Sort descending by total. Ties broken by customer weight, then urgency, then frequency.

---

## Output format

Always return in chat using this structure. Keep paragraphs to 2–4 sentences — product leaders are scanning, not reading.

```
# Product escalations — last 7 days ([YYYY-MM-DD] – [YYYY-MM-DD])

Here are the product escalations I could triangulate across Fireflies, PlanHat, and Slack, ranked by composite priority (customer tier × frequency × urgency).

**1. [Customer / scope] — [one-line escalation headline]**
[Who flagged it, what's happening, why it matters. Name specific people and numbers where useful.]
- [Evidence link 1 — Slack permalink]
- [Evidence link 2 — Fireflies meeting URL]
- [Evidence link 3 — Notion ticket if referenced]

**2. ...**
...up to **10.**

---

**Long-tail (lower priority but worth noting)**

- **[Customer] — [summary]** ([link])
- **[Customer] — [summary]** ([link])

---

**Notes on coverage**
- Fireflies: searched transcripts [date range] + keyword searches ([list keywords used]); N transcripts scanned.
- PlanHat: scanned all conversations from [start_date] onward via paginated `list_model_records` (N pages × 10 records); **bounce notifications excluded** client-side (mailer-daemon + Delivery Status Notification subjects + companyId=0). N non-bounce conversations reviewed.
- Slack: [channels scanned] + workspace-wide keywords [list].

[Optional offer at the end, e.g.: "Want me to draft a #product-issues message for the top 5, or turn this into a live artifact?"]
```

---

## Coverage rules — state what you searched

Always close with the "Notes on coverage" block so the user can tell what might have been missed. In particular:

- Explicitly state that **PlanHat bounce notifications were filtered out**. This is important because the first run without this filter surfaced only email bounces in the negative-sentiment bucket, which is misleading.
- List the exact Fireflies keywords queried (not just "did keyword searches").
- List the Slack channels scoped with `in:` and the workspace-wide keywords.
- If PlanHat Conversation queries hit the token-limit error, say so — don't silently drop data.

---

## Workflow checklist

Run these in order:

1. **Calculate the date range** — 7 days back from today (check current date via `date` or env). Convert to ISO (`YYYY-MM-DD`) for Fireflies/PlanHat and to Unix timestamps if needed for Slack `oldest/latest`.
2. **Launch all three source scans in parallel** (same message, multiple tool calls):
   - Fireflies: one `fireflies_get_transcripts` for the window, plus N `fireflies_search` keyword queries.
   - PlanHat: paginate through **all** Conversations in the window (time-filter only, no category/sentiment filter), `LIMIT: 10` per page, minimal `SELECT`. **Drop bounces client-side**, then keyword-scan the remainder.
   - Slack: one `slack_search_public_and_private` per keyword, plus `in:#channel` scopings for the high-signal channels listed above.
3. **Consolidate** — dedupe across sources, group by root cause.
4. **Score** — apply the composite rubric.
5. **Sort** — descending by total score.
6. **Draft** — top 10 in the structured format above, rest as long-tail.
7. **Always include the "Notes on coverage" block** so the user can see what was searched.
8. **Offer a follow-up** — e.g. drafting a Slack message for #product-issues, creating a live artifact, or scheduling a weekly run via the `schedule` skill.

---

## Tone

Match the CEO-to-TL register used elsewhere in Go Vocal weekly updates: direct, concise, named. Avoid hedging language ("there may be some issues with…"). If something is broken, say so; if a customer is at risk, say who and why. Product leads will action this list — clarity beats politeness.
