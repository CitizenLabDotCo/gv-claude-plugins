---
name: V1_Weekly-Wins-Losses-Updates
description: |
  Subskill: scan Slack team channels and draft sections 2–5 of the weekly Team Lead update for Go Vocal (Wins & losses, Relevant updates, Your action needed, Priorities). Returns a ready-to-use text block consumed by the parent skill. Trigger this subskill whenever the parent skill needs the Slack-sourced content for the weekly TL update.
---

# Weekly TL Update — Slack Content Subskill

You are preparing sections 2–5 of a weekly update that Jeroen (Chief of Staff) drafts for CEO Wietse to post to team leads. The audience is: Koen, Irene, Aline, Ellen, Emile, James, Sarah, and Wietse. The tone should be direct, concise, and CEO-appropriate — not a detailed operational log.

**Your output is a text block** covering sections 2–5, ready to be consumed by the parent skill. Do not publish to Notion or ask for review — just return the drafted content.

## Update structure (sections handled by this subskill)

```
**2 | Wins & losses ⚖️**
**3 | Relevant updates 💡**
**4 | Your action needed 🚀**
**5 | Priorities this week 👀**
```

---

## 2 | Wins & losses ⚖️

**What it shows:** Notable highs and lows from across the company in the past week.

### How to gather wins & losses

This is the most judgement-intensive section. You must **read team channels directly** — keyword searches alone will miss important items.

**Channels to scan** (read messages from last Monday 00:00 UTC to now):

| Channel | Slack ID |
|---|---|
| #team-govsuccess | C98UFE3S8 |
| #govocal-dach | C014XBG860J |
| #govocal-uk | C015QPG97V1 |
| #govocal-netherlands | C015P6A1UUD |
| #govocal-francophonie | C015QHDTL02 |
| #govocal-northam | C0173HA9PPX |
| #team-leads | CNTBVJLE4 |
| #team-product | C036GLX6X1D |
| #team-sales | CE2BHKY22 |
| #we-grow | C0634TK3NBD |

Use `slack_read_channel` with `oldest` and `latest` parameters (Unix timestamps) to read each channel for the past 7 days. Do NOT rely only on keyword searches like "win", "loss", "churn" — you'll miss context-dependent items.

### What qualifies as a win or loss

**Wins (✚):**
- Deals closed or renewed (especially above-average value)
- Near-churns saved
- Strategic milestones (new market entry, first deal in a segment, land-and-expand)
- Completed initiatives that benefit multiple teams (e.g. churn analysis, new tooling)

**Losses (➖):**
- Churn or significant downgrade (mention qualitatively if exact MRR delta is unavailable)
- Lost pipeline opportunities
- Competitive threats (new competitors spotted, lost deals to competitors)
- Operational blockers (key migrations stuck, low event attendance vs goals)
- Revenue at risk (accounts flagged for potential churn)
- GRR/NRR below target

### Filtering rules

These are important — getting them wrong leads to noisy, unhelpful updates:

1. **Do NOT include items already communicated 2+ times.** If something has been mentioned in previous weekly updates or discussed extensively in #team-leads, skip it. The update should surface what's new.
2. **Keep granularity at the CEO-to-TL level.** Don't include things like "Zelda is finalizing a pricing table" — that's too operational. Think: would Wietse mention this in a 2-minute standup with all TLs?
3. **Don't add a conclusion bullet** summarizing overall MRR or KPI performance — the parent skill handles that context.
4. **Items involving both a deal outcome and strategic context** (e.g. a renewal with a significant downgrade) should appear here with the qualitative context (e.g. "renewed but at 50% MRR downgrade, 36-month lock-in").

### Formatting

Each item is a bullet starting with ✚ or ➖, followed by 1-2 sentences. Be specific (name the customer, the person, the number where available) but concise.

---

## 3 | Relevant updates 💡

Company-wide updates that are relevant for all team leads. These come from scanning the same Slack channels plus #team-leads and #team-product.

Examples: product launches, pricing changes, upcoming events, process changes, hiring updates, tool rollouts.

Keep items short — one or two lines each. Group related items under a sub-header if needed (e.g. "OSP update", "Meetup", "Product Marketing").

---

## 4 | Your action needed 🚀

**Critical rule:** This section contains ONLY things explicitly asked FROM team leads BY Wietse or Jeroen in the last 7 days.

- NOT requests from other people in the company (e.g. Lydie asking country managers to do something does NOT belong here)
- NOT general FYIs or suggestions
- Only concrete asks directed at TLs from the CEO or Chief of Staff

Scan #team-leads (CNTBVJLE4) and relevant channels for messages from Wietse or Jeroen that contain explicit requests/asks for team leads.

If there are no action items from Wietse or Jeroen in the past week, write: "No new action items this week."

---

## 5 | Priorities this week 👀

**Do NOT fill this in.** These are Wietse's personal priorities for the week. Always write:

```
*To be filled in by Wietse*
```

Only pre-fill this if Jeroen explicitly provides Wietse's priorities for the week.

---

## Workflow checklist

When executing this subskill, follow these steps in order:

1. **Calculate the date range**: Determine last Monday 00:00 UTC and convert to Unix timestamp. Double-check the year!
2. **Scan all team channels** listed above — read them directly, don't just keyword search
3. **Draft sections 2–5** following the structure and rules above
4. **Return the text block** to the parent skill

---

## Avoiding repetition across weeks

Before finalizing wins & losses, fetch the previous week's update from the Notion database "121 Wietse - Jeroen". Check what was already mentioned — if an item appeared there (or in the week before), don't include it again unless there's a meaningful new development. The weekly update should feel fresh, not like a status tracker that repeats the same items.

To find the previous update, search the database for pages tagged "Weekly TL" and pick the most recent one before the current week.
