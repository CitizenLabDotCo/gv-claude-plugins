---
name: 121-followup
description: >
  Post-meeting processing for Wietse's recurring 1:1 and 1:2 meetings with his
  leadership team (Guillem, Sarah, Ellen, Ellen+Emile, Ellen+Aline, Jeroen,
  Jordan, Irene). ALWAYS use this skill when Wietse says things like "just
  had my 121 with [name]", "done with my 122 with [names]", "process my
  [name] meeting", "121 followup", "capture my to-dos from the [name] 121",
  or any variation implying he just finished a recurring leadership 1:1 or
  1:2 and wants to process the outputs into to-dos. Also runs in POLLING
  MODE on a scheduled daily task that checks the Granola "121s" folder for
  new finalized recordings and processes any not yet captured. The skill
  reads the latest Granola notes from the meeting, scans Wietse's Slack
  self-DMs from the last 24 hours, and the Notion 121 page for that meeting;
  extracts personal to-dos and appends them as plain bullets at the bottom
  of his Notion To-Do List; and drafts targeted Slack DMs in English to
  whichever leadership team members have items relevant to their domain.
---

# 121 Followup

Convert raw outputs from Wietse's recurring leadership 1:1s and 1:2s into:

1. Personal to-dos appended to Wietse's Notion To-Do List
2. Delegation Slack DMs in English to leadership team members whose domain came up

Two modes:

- **Manual mode** — Wietse triggers explicitly after a meeting. Skip to Step 0.
- **Polling mode** — A scheduled task fires daily and asks the skill to check the Granola "121s" folder for any new finalized recordings not yet processed. Run Step P first, then loop Steps 1–6 once per unprocessed meeting found.

---

## Step P — Polling mode (scheduled runs only)

If the trigger phrase looks like a scheduled run ("daily 121 sweep", "check for new 121 recordings", "polling run", "scheduled 121-followup") rather than a specific meeting:

1. Find the Granola "121s" folder using `list_meeting_folders`. List meetings finalized in the last 48h from that folder using `list_meetings` with the folder ID and a 48h time range. (Window is generous; the dedup check below catches anything already done.)

2. For each meeting found, dedup-check the Notion To-Do List. Fetch page ID `1a69663b7b2680f8b96ce4bc87cd4c63` and scan for any existing bullet whose source tag matches this meeting's partner+date — e.g. `(from 121 Jeroen, 2026-11-04)`. If a match exists, skip the meeting.

3. For each remaining unprocessed meeting, identify the partner(s) from the meeting title (`121 Wietse Jeroen` → Jeroen; `122 Wietse Ellen Emile` → Ellen+Emile), then run Steps 1–6 once for that meeting.

4. If nothing new is found, stop quietly. Don't post anything. Don't draft any DMs.

If the trigger looks like a manual run instead, skip to Step 0.

---

## Step 0 — Identify the meeting (manual mode)

Wietse's recurring leadership meetings:

| Meeting | Partner(s) | Domain |
|---------|-----------|--------|
| 121 Guillem | Guillem | Marketing |
| 121 Sarah | Sarah | North America |
| 121 Ellen | Ellen | COO / RevOps |
| 122 Ellen + Emile | Ellen, Emile | Sales |
| 122 Ellen + Aline | Ellen, Aline | Government Success |
| 121 Jeroen | Jeroen | Chief of Staff |
| 121 Jordan | Jordan | Finance |
| 121 Irene | Irene | Product |

Parse the partner(s) from Wietse's trigger phrase. If unclear, ask once: *"Which 121 — Guillem, Sarah, Ellen, Ellen+Emile, Ellen+Aline, Jeroen, Jordan, or Irene?"*

---

## Step 1 — Read the Granola notes

Use `query_granola_meetings` with a natural language query for the most recent meeting matching the partner(s):

```
"most recent 121 between Wietse and [partner name], action items and decisions"
```

For 1:2s, include both names (`"most recent 122 between Wietse, Ellen, and Emile"`).

If the result is thin, fall back to `list_meetings` (last 48h, filtered by participants) and then `get_meeting_transcript` on the matching meeting ID.

Extract:

- Action items for Wietse — things he committed to or needs to follow up on
- Decisions made — resolved topics that don't need more discussion
- Items to delegate — things relevant to a leadership team member's domain that Wietse should ping them about
- Open questions — things still needing input

If the transcript is garbled, rely on the AI summary rather than the raw text.

---

## Step 2 — Read the Notion 121 page

Use `notion-search` with a query like `"121 Wietse [partner]"` or `"122 Wietse [partner1] [partner2]"`. Fetch the most recent page (this week's or today's entry).

Read for additional context: items already noted, plan from previous week, anything pre-meeting that didn't make it into Granola. Read-only — do not update this page.

---

## Step 3 — Scan Wietse's Slack self-DMs (last 24h)

Wietse uses his own Slack DM as a scratchpad. Use `slack_read_channel` with Wietse's own user ID as `channel_id` and a 24h window.

Look for quick notes, reminders, half-formed thoughts, or links he typed to himself before/during/after the meeting. Cross-reference with Granola so you don't double-count.

---

## Step 4 — Append personal to-dos to the Notion To-Do List

Target: `https://www.notion.so/govocal/To-Do-List-1a69663b7b2680f8b96ce4bc87cd4c63` (page ID `1a69663b7b2680f8b96ce4bc87cd4c63`).

Use `notion-fetch` first to read the current state and avoid duplicates. (In polling mode, reuse the fetch from Step P.)

Use `notion-update-page` with `update_content` to append new bullets at the bottom. Format:

- Plain bullet points, one per line
- Written in English
- Concise, starting with a verb ("Follow up on...", "Review...", "Decide on...", "Reach out to...")
- Source tag at the end is required for dedup, exact format: `(from 121 Jeroen, 2026-11-04)`. Use ISO date so polling-mode dedup matches reliably.
- Match the existing style of items already on the page

Don't duplicate items already on the page.

---

## Step 5 — Draft delegation Slack DMs

Draft a Slack DM in English using `slack_send_message_draft` for any action item relevant to a leadership team member's domain. Use `slack_search_users` at runtime to look up each recipient's Slack user ID, and pass that ID as `channel_id`.

Domain map:

| Person | What to send them |
|--------|-------------------|
| Guillem | Marketing, brand, content, demand gen, events, comms |
| Sarah | North America market, US/CA accounts, NA pipeline, NA hiring |
| Ellen | COO topics, RevOps, ops processes, cross-functional alignment, finance ops handoffs |
| Emile | Sales pipeline, forecast, deal-specific issues, sales team, sales enablement |
| Aline | Government Success, customer health, churn/renewal, CSM team, EU/UK customer issues |
| Jordan | Finance, FP&A, fundraising, board reporting, FX, contracts |
| Jeroen | Chief of Staff topics, board prep, weekly update, cross-functional projects, OKRs |
| Irene | Product roadmap, product escalations, R&D priorities, product/customer feedback loops |

Send a DM only if the meeting produced something specifically for that person's domain. No filler messages.

### Writing style

Write as Wietse messaging a peer — direct, no formal memo tone. Start with the substantive point. End with a concrete next step or question.

Apply these humanization principles (from the `humanizer` skill):

- No AI vocabulary: avoid "crucial", "pivotal", "highlight", "underscore", "align with", "landscape", "testament", "foster", "leverage"
- No bold inline-headers on every bullet
- No rule of three — don't pack everything into groups of three
- No em-dashes (—) — use commas or periods
- No sycophantic openers — no "Great question!", "Absolutely!", "Of course!"
- Vary sentence length
- Be specific — name concrete deals, accounts, people
- First person where natural ("Wanted to flag...", "I'd like...")
- Re-read each draft. If it feels too polished, rough it up.

---

## Step 6 — Report back

Once everything is staged:

1. Link to the updated Notion To-Do List with the count of new items added
2. List the Slack DM drafts created, one line per recipient
3. 3–5 bullet recap of the meeting's key outcomes
4. Flag anything ambiguous

In polling mode, batch the report across all meetings processed in the run — one short section per meeting. If nothing was processed, stay silent.
