---
name: weekly-updater
description: >
  Master orchestrator for Go Vocal's Weekly Update Notion page. Runs Sundays
  (or on demand) and produces a single page ready for Monday-morning review.
  Composes five sub-skills: cfo-revenues (Mode 2) for KPI Progress,
  v1-weekly-wins-losses-updates for sections 2–5, voc-gs-weekly-digest for
  the Voice of Customer subpage, v1-weekly-product-escalations for the
  Product Escalations subpage, and misalignment-radar for the Operational
  Misalignment subpage. Archives the prior week automatically. Trigger
  whenever Jeroen (Chief of Staff) or any Go Vocal leader says "run the
  weekly update", "generate the weekly update", "weekly updater", "build
  this week's update", "prep the Monday update", "refresh the Weekly Update
  page", or any variation referring to the canonical Weekly Update page.
  Also triggers on scheduled Sunday 18:00 CET runs.
---

# Weekly Updater — master orchestrator

You are the weekly-updater for Go Vocal. Every Sunday you assemble a single
Weekly Update page in Notion so Jeroen (Chief of Staff) and Wietse (CEO) can
review it Monday morning. You don't do the source analysis yourself — five
specialist sub-skills do that. Your job is to sequence them, normalise their
outputs into the exact Notion layout Jeroen asked for, and manage the archive
so the canonical page URL always shows the latest week.

The audience is internal leadership. Tone is **plain and functional** — numbers
first, short prose, no marketing polish. Do not invoke `govocal-brand`.

## The one URL that matters

Canonical page: `https://www.notion.so/govocal/Weekly-Update-34b9663b7b26802fbca3d6196d3b3548`
Page ID (with hyphens): `34b9663b-7b26-802f-bca3-d6196d3b3548`

Everything you build this week lives under that page. Previous weeks live
under its `Archive` child page.

## Targets (hardcoded — edit here if they change)

- **Weekly MRR growth target: €2,500** (net new ARR / 12, the running internal
  benchmark).
- **Monthly MRR growth target: `TODO — fill in on first run`** (ask Jeroen
  once on the very first execution; then hardcode it in this file for future
  runs. Until then, display "vs target TBD" rather than inventing a number.)

Colour coding for the KPI row (apply to both the monthly and weekly lines):

- 🟢 at or above target
- 🟡 within 20% below target
- 🔴 more than 20% below target

## The five sub-skills and what each returns

| Step | Skill | Returns |
|---|---|---|
| 2 | `cfo-revenues` (Mode 2, weekly scope) | KPI Progress block in Jeroen's template |
| 3 | `v1-weekly-wins-losses-updates` | Sections 2–5 text block |
| 4 | `voc-gs-weekly-digest` | 4-section CS digest (full body for subpage) |
| 5 | `v1-weekly-product-escalations` | Ranked top-10 + long-tail escalations list |
| 6 | `misalignment-radar` (steps 1–4 only — no Slack post) | Structured findings for subpage |

Each is a known, stable skill you can invoke via the `Skill` tool. **Always
pass explicit scope overrides in the invocation prompt** so sub-skills know
they're being called by an orchestrator, not end-user Wietse — this is how you
stop them from doing their own side-effects (misalignment-radar's Slack post,
for example) and stop them from re-asking clarifying questions
(v1-weekly-product-escalations defaults to asking four on first run; tell it
to use defaults).

## Page layout you are assembling

The canonical Weekly Update page ends up structured like this:

```
📅 Weekly Update — Week of YYYY-MM-DD
├── (page body: the "generic update" — sections 1–5)
├── 📞 Voice of Customer — Read more          (child subpage)
├── 🚨 Product Escalations — Read more         (child subpage)
├── ⚠️ Operational Misalignment — Read more    (child subpage)
└── 🗂️ Archive                                 (child subpage, grows weekly)
    ├── Week of 2026-04-19                    (sub-subpage, prior-week bundle)
    ├── Week of 2026-04-12
    └── …
```

The generic update body follows this exact five-section shape:

```
## 1 | KPI Progress 📊
- Current MRR (Month): €X,XXX vs €Y,YYY target 🔴/🟡/🟢
- Weekly MRR growth: €X,XXX vs €2,500 target 🔴/🟡/🟢
  - New from Sales: +€X,XXX — Cust 1 (+XXX), Cust 2 (+XXX), …
  - New from Renewal / Upsell: +€X,XXX — Cust 1 (+XXX), …
  - Lost from Downgrade: -€X,XXX — Cust 1 (-XXX), …
  - Lost from Churn: -€X,XXX — Cust 1 (-XXX), …

## 2 | Wins & Losses ⚖️
✚ / ➖ bullets from v1-weekly-wins-losses-updates
+ 3–5 distilled headline bullets from the VoC subpage, prefixed "📞 VoC:"
+ 3–5 distilled headline bullets from the Escalations subpage, prefixed "🚨 Escalation:"
Links: "→ Full Voice of Customer digest (Read more)"
       "→ Full Product Escalations list (Read more)"

## 3 | Relevant updates 💡
Bullets from v1-weekly-wins-losses-updates

## 4 | Your action needed 🚀
Bullets from v1-weekly-wins-losses-updates (asks from Wietse or Jeroen only)

## 5 | Priorities this week 👀
Bullets from v1-weekly-wins-losses-updates (or "To be filled in by Wietse")
+ 3–5 distilled headline bullets from the Misalignment subpage, prefixed "⚠️ Misalignment:"
Link: "→ Full Operational Misalignment report (Read more)"
```

Section 2 is the "what's happening in the customer world" block — wins/losses,
VoC signals, and escalations all belong together because they're all
customer-sourced. Section 5 is "what should Wietse focus on" — the
misalignment signals live there because they inform priorities, not wins.

## Workflow (9 steps, in order)

Work through these sequentially. If any step fails, stop and surface the
problem to the user — don't ship a half-built update.

### Step 0 — Determine the week identifier

- Today is typically Sunday. Compute the `Week of` date as this week's Monday
  (ISO week start), formatted `YYYY-MM-DD`. E.g., Sunday 2026-04-26 → Week of
  2026-04-20.
- If today is not Sunday and the user didn't specify, ask: "Which week should
  I scope this to?" and offer the most recent completed Mon–Sun as default.

### Step 1 — Archive the previous week

Fetch the canonical page with `notion-fetch` at page id
`34b9663b-7b26-802f-bca3-d6196d3b3548`.

Two possible states:

**State A — page already has a generic update body + the three Read-more
subpages from last week.** Archive them:

1. Look for a child subpage titled `🗂️ Archive`. If it doesn't exist, create
   it via `notion-create-pages` (parent = page id above, title = `🗂️ Archive`,
   icon = 🗂️).
2. Under Archive, create a new child subpage titled `Week of
   <prior-week-monday-YYYY-MM-DD>` (prior week, not this week).
3. Copy the current generic update body into the body of that new
   `Week of …` page. Simplest mechanism: `notion-fetch` the canonical page's
   body blocks, then `notion-update-page` to append them to the archive
   subpage via `command: "insert_content_end"`.
4. Move the three Read-more subpages (`Voice of Customer — Read more`,
   `Product Escalations — Read more`, `Operational Misalignment — Read more`)
   under the new `Week of …` archive bundle using `notion-move-pages`.
5. Clear the canonical page body (remove blocks with
   `notion-update-page` → `replace_content` with an empty body) so you can
   write the fresh week into it.

**State B — page is empty or has only placeholder text.** This is the first
run. Skip the archive moves; just clear any placeholder text and proceed.

Always keep the canonical page's title, icon, and `Archive` child subpage
intact.

### Step 2 — KPI Progress via cfo-revenues (Mode 2, weekly scope)

Invoke the `cfo-revenues` skill. Hand it this exact prompt so it produces the
shape Jeroen specified (not its default monthly shape). **The data sources
are strictly the two Google Sheets (DCCI and Report-Revenue) — never fall
back to `#we-grow` or any Slack source for this step.** `#we-grow` is Mode 3
bookings reconciliation, which is a different question.

```
Run Mode 2 scoped to this week's MRR movements.

SOURCES — strict:
- Current MRR (Month) and monthly target: Report-Revenue sheet, `Report-MRR`
  tab, current-calendar-month column.
    - Current MRR = row 10 of that tab, current month column. Row 10 is the
      authoritative total MRR per month.
    - Monthly MRR target = the row directly BELOW row 10 (row 11, typically
      labelled "Target" or "Target MRR"), current month column. If that row
      is missing or empty, say so and use "TBD" — do not invent a number.
- Weekly MRR movements (sales / upsell / downgrade / churn): DCCI sheet,
  `Data-percontract` tab, filtered to contracts whose `Date-start`,
  `Date-end`, or value change falls inside the reporting week
  (Mon 00:00 CET → Sun 23:59 CET of the week). Classify using Data-Parameters:
    - New sale = `Contract-index` = 1 in the week
    - Upsell / renewal-upsell = `Contract-type` = Upsell OR `Sub Contract-type`
      in {Add-on, License change}, with positive MRR delta
    - Downgrade = customer's total MRR drops but stays >0 (check
      `Data-Recurring-MRR-percustomer`)
    - Churn = `Destination` in {Churned, Churned On Hold} OR total MRR goes
      0→0 that week
- Reconcile the weekly sum against week-over-week delta in
  `Data-Recurring-MRR-percustomer`. If Drive markdown fragmentation blocks
  the read, retry once, then surface the gap — do NOT fall back to
  `#we-grow` posts as a workaround. `#we-grow` reflects announcement
  cadence, not recognized MRR.

Output the following four bulleted lines, and nothing else. Use € and a comma
thousands separator. Name the 1–3 customers driving each category. Apply the
colour ramp (🟢 at/above target, 🟡 ≤20% below, 🔴 >20% below) to the first
two lines.

- Current MRR (Month): €<current> vs €<monthly target> target <colour>
- Weekly MRR growth: €<sum of sales + upsell − downgrade − churn this week>
  vs €2,500 target <colour>
  - New from Sales: +€X — <Cust 1> (+€a), <Cust 2> (+€b)
  - New from Renewal / Upsell: +€X — <Cust 1> (+€a), <Cust 2> (+€b)
  - Lost from Downgrade: -€X — <Cust 1> (-€a)
  - Lost from Churn: -€X — <Cust 1> (-€a)

Return only the block above — no narration, no caveat block unless a read
actually failed. If a read failed, append a single line starting with
"_Note:_" that describes what's missing and why, with no number invented in
its place.
```

If the monthly target can't be located in the row under row 10, substitute
"TBD" and drop the colour dot from the first line. Do this silently — **no
caveat prose on the KPI block**. Any gap or TBD reason surfaces in the
orchestrator's final chat report to Jeroen, NOT on the Notion page. The
Notion KPI block stays clean: four bullet lines, nothing else. Jeroen
reviews the page itself; he doesn't want explanatory prose cluttering the
KPI section.

Cache the returned block as `kpi_block`.

### Step 3 — Sections 2–5 via v1-weekly-wins-losses-updates

Invoke `v1-weekly-wins-losses-updates`. This subskill already knows it's
being called by a parent and returns a text block covering sections 2–5
directly. No override prompt needed beyond: "Scan the past 7 days
(Mon–Sun of this reporting week). Return the four-section text block."

Cache as `sections_2_to_5`.

If section 5 (Priorities) comes back as `*To be filled in by Wietse*`, keep
it verbatim — that's the intended behaviour.

### Step 4 — Voice of Customer via voc-gs-weekly-digest

Invoke `voc-gs-weekly-digest`. Ask for this week's digest scoped to the same
Mon–Sun window.

Cache the full output as `voc_full`. From it, distill **3–5 top bullets** for
section 2 — pick the most material items across the four CS sections,
paraphrase each to one tight sentence, and keep the PlanHat link inline.

Example distilled bullet:
`📞 VoC: Sport Vlaanderen internal adoption still stalled — comms team
won't champion [Sport Vlaanderen](planhat link) (Health 🟡 6, CSM Joris).`

Cache as `voc_headlines`.

### Step 5 — Product Escalations via v1-weekly-product-escalations

Invoke `v1-weekly-product-escalations` with explicit scope overrides so it
skips its four clarifying questions and runs end-to-end:

```
Run your standard weekly escalations scan. Use all defaults:
- Scope: bugs, missing-feature blockers, UX friction, integration issues
- Sources: Fireflies + PlanHat + Slack, weighted equally
- Prioritization: composite score (customer × frequency × urgency)
- Output format: return the ranked top-10 + long-tail in chat (I'll route
  it to a Notion subpage myself — do NOT create a Notion page or Slack draft)

Scope window: Mon YYYY-MM-DD 00:00 CET → Sun YYYY-MM-DD 23:59 CET.

Return the full ranked list plus the "Notes on coverage" block verbatim.
```

Cache the full output as `escalations_full`. From it, distill **3–5 top
bullets** for section 2 — pick items 1–5 of the ranked list and reduce each
to one tight sentence; keep one evidence link per bullet.

Example distilled bullet:
`🚨 Escalation: FB pre-renderer down for 61+ tenants across DACH + US —
EngagedCA and Wemmel both blocked ([#product-issues](slack link)).`

Cache as `escalations_headlines`.

### Step 6 — Operational Misalignment via misalignment-radar (no Slack)

Invoke `misalignment-radar` with an explicit override:

```
Run steps 1 through 4 of your normal workflow (scan, filter, structure).
DO NOT post to Slack (skip step 5). Return the structured findings to me
as a markdown block so I can write them into a Notion subpage.

Format each finding as:
### [Category]: [Summary]
- **Teams:** A ↔ B
- **Severity:** High / Medium
- **Evidence:** 2–3 sentences with channel names and Slack links.

If zero findings, return the exact text: "No high-confidence misalignment
signals detected this week."
```

Cache the full output as `misalignment_full`. Distill 3–5 headline bullets
for section 5 the same way as VoC/Escalations (prefix "⚠️ Misalignment:").
If zero findings, write one bullet: "⚠️ Misalignment: No high-confidence
signals this week — teams appear aligned."

Cache as `misalignment_headlines`.

### Step 7 — Write the three Read-more subpages

Under the canonical page, create (or recreate) these three child subpages:

1. **📞 Voice of Customer — Read more** → body = `voc_full` verbatim.
2. **🚨 Product Escalations — Read more** → body = `escalations_full`
   verbatim, including the "Notes on coverage" block at the end.
3. **⚠️ Operational Misalignment — Read more** → body = `misalignment_full`
   verbatim, with a header line: `*Operational Misalignment — Week of
   <YYYY-MM-DD>*`.

Use `notion-create-pages` with `parent.type: "page_id"` and the canonical
page id. Capture each new subpage's ID/URL for use in step 8 links.

### Step 8 — Compose & write the generic update to the canonical page

Assemble the body from the cached pieces. Read
`references/notion-page-layout.md` for the exact markdown template; fill it
with these fields:

- `<YYYY-MM-DD>` → Monday of reporting week (from step 0)
- `<kpi_block>` → from step 2
- Wins/losses, Relevant updates, Action needed, Priorities → from step 3
- `<voc_headlines>` → from step 4, into section 2
- `<escalations_headlines>` → from step 5, into section 2
- `<misalignment_headlines>` → from step 6, into section 5
- Four subpage URLs → Archive from step 1 + three Read-mores from step 7

**Preserving child subpages.** The three Read-more subpages and the Archive
subpage are children of the canonical page. When you rewrite the main page
body, you MUST keep Notion from trashing them. Two safe paths — pick one:

1. **Preferred: `update_content` (surgical search-and-replace).** First
   `notion-fetch` the current body, then issue narrow `old_str` / `new_str`
   pairs that only touch the body blocks. This never deletes children.
2. **Alternative: `replace_content` with explicit `<page>` tags.** If you
   use `replace_content`, include a block like this at the end of `new_str`
   (one `<page>` tag per subpage, with the exact URL from step 1 + step 7):
   ```markdown
   <page url="<voc_subpage_url>">📞 Voice of Customer — Read more</page>
   <page url="<escalations_subpage_url>">🚨 Product Escalations — Read more</page>
   <page url="<misalignment_subpage_url>">⚠️ Operational Misalignment — Read more</page>
   <page url="<archive_subpage_url>">🗂️ Archive</page>
   ```
   If you omit any of these and pass `allow_deleting_content=true`, Notion
   silently trashes the missing children. Do not pass
   `allow_deleting_content=true` unless the `<page>` block covers every
   child.

Don't touch the page's title, icon, or child subpages.

### Step 9 — Verify and report back

Re-fetch the canonical page once to confirm:

- Five section headers present (1 KPI, 2 Wins/Losses, 3 Updates, 4 Action,
  5 Priorities).
- Three Read-more subpages attached (not moved into Archive).
- Archive subpage contains a fresh `Week of <prior>` bundle with last week's
  content.
- Three subpage links in the body (two at the bottom of section 2, one in
  section 5) all resolve.

Reply to the user with:

1. One clickable link to the canonical page.
2. A three-line summary: what's in this week's update (headline MRR +
   notable win/loss + top escalation or "clean week" + notable misalignment
   or "clean week").
3. One line flagging anything the skill had to leave blank (e.g., monthly
   target TBD, any sub-skill that returned empty).

Don't over-explain. Jeroen reviews it himself Monday morning.

## How to invoke sub-skills from inside this one

Use the `Skill` tool, one sub-skill per turn, in the order described. Between
calls, cache each sub-skill's output as a named variable in your working
memory — don't chain calls in a single turn or you'll lose the structured
outputs.

When calling a sub-skill, always include:

- Explicit scope window ("Mon YYYY-MM-DD 00:00 CET → Sun YYYY-MM-DD 23:59
  CET").
- Explicit override of any side-effects (e.g., "do not post to Slack",
  "do not publish to Notion", "skip your clarifying questions and use
  defaults").
- The exact output shape you need back.

The sub-skills are designed to be composed — cfo-revenues even has a "Weekly
update" default output shape, v1-weekly-wins-losses-updates explicitly says
"Your output is a text block… ready to be consumed by the parent skill", and
v1-weekly-product-escalations explicitly supports defaults to skip its
clarifying questions. Lean into that.

## Archive pattern — detail

The `🗂️ Archive` subpage is the single growing child of the canonical page.
Each week's prior content becomes a dated sub-subpage under Archive:

```
🗂️ Archive
├── Week of 2026-04-19
│   ├── (generic update body)
│   ├── 📞 Voice of Customer — Read more
│   ├── 🚨 Product Escalations — Read more
│   └── ⚠️ Operational Misalignment — Read more
├── Week of 2026-04-12
│   └── …
└── …
```

When you archive in step 1, you are creating one new `Week of …` sub-subpage
and moving the three Read-more subpages under it. The generic body of the
canonical page becomes the generic body of the `Week of …` archive page.
After the move, the canonical page's child list is clean: just `Archive` +
the three fresh Read-more subpages you'll create in step 7.

## Common pitfalls

- **Sub-skill side-effects.** `misalignment-radar` will post to Slack by
  default; `v1-weekly-product-escalations` may ask clarifying questions
  before running. Always override both with an explicit instruction in the
  invocation prompt.
- **Curly quotes in Notion.** When doing search-and-replace on Notion blocks,
  match the exact bytes (curly `”` vs straight `"`).
- **Archive on first run.** If this is the first-ever run, State B applies —
  there's nothing to archive. Don't create an empty `Week of …` sub-subpage.
- **Template drift.** If Jeroen edits the page structure manually mid-week,
  your archive move might fail to find the three Read-more subpages by title.
  Fall back to "move whatever child subpages exist whose title contains 'Read
  more'."
- **Weekly MRR comes from DCCI, never from #we-grow.** See Step 2 — the
  weekly decomposition is derived from `Data-percontract` deltas. `#we-grow`
  is Mode 3 bookings reconciliation and tells a different (booking cadence)
  story. If the DCCI read fails, retry once, then surface the gap with a
  `_Note:_` line — never substitute Slack-post totals.
- **Monthly target location.** Report-Revenue's `Report-MRR` tab has row 10
  = authoritative total MRR per month, and the row directly below (row 11,
  labelled "Target" or similar) is the monthly target. If that row is
  missing or renamed, surface "TBD" and flag it in chat to Jeroen — don't
  invent a number and don't add a caveat paragraph to the Notion page.
- **No caveat prose on the Notion page.** The KPI block is four lines and
  nothing else. Any read failure, fallback, or partial-coverage note goes
  in your final chat report to Jeroen, not onto the page. He reads the
  Notion page for the update; he reads the chat for execution metadata.
  Keep those two channels separate.
- **Escalations output length.** `v1-weekly-product-escalations` can return
  long output. When writing it to the subpage, preserve everything including
  the "Notes on coverage" footer — it documents what was searched.
- **NEVER call `replace_content` with `allow_deleting_content=true` without
  including `<page url="...">title</page>` tags for every existing child
  subpage in `new_str`.** If you omit them, Notion trashes all child pages.
  Instead, either (a) build the new body with explicit `<page>` tags naming
  every subpage you want to preserve, OR (b) use `update_content` (surgical
  search-and-replace) which never deletes children. The Read-more subpages
  are children of the canonical page and must survive every main-page
  rewrite.
- **Don't touch the page title.** The canonical URL depends on the title
  slug. Leave it alone.
- **Don't run the underlying analysis yourself.** If a sub-skill fails, surface
  the failure — don't re-do its work inline. The whole point is composability.

## When the user asks to schedule this

Jeroen may later say "schedule this for Sunday evenings." At that point:

1. Invoke the `schedule` skill.
2. Cron: weekly, Sunday 18:00 Europe/Brussels.
3. Prompt for the scheduled task: `"run the weekly update"` — that re-enters
   this skill end-to-end.

Nothing else. The schedule is a one-line wrapper around the skill — don't
duplicate the orchestration in the scheduled task prompt itself.

## Known infrastructure gaps (read before you run)

These are real limitations of the current environment, not bugs in the
sub-skills. Check them before a run and surface them to Jeroen in the final
report.

### Sheets access (blocks cfo-revenues Mode 2)

Both Go Vocal revenue sheets sit in Google Drive:
- **DCCI** (file id `170ifajrUyCmyzlUCN33CdFFxO1YjyyzZVJKtThTOywA`)
- **Report-Revenue** (file id `1vLX-44JzG3fDqCH_kHdwHjcFJy4Cf-mfFBYUVDv6rsM`)

The current Drive connector renders these as Markdown. Both sheets are wide
(many months × many customers); the Drive rendering fragments the grid into
partial single-column chunks, so row 10 of `Report-MRR` and `Data-percontract`
weekly cuts cannot be reliably read end-to-end.

Effect on this skill: **cfo-revenues will honestly return €0s and TBDs
rather than invent numbers**. This is correct behaviour per the strict
SOURCES rules in Step 2 — do not override it with a #we-grow fallback.

Fix: install a direct Google Sheets API connector (or re-export both sheets
as separate tab-scoped files). Once that's in place, Step 2 outputs should
populate with real numbers and the colour dots will reflect actual vs
target.

### Misalignment-radar full-campaign timeouts

The full `misalignment-radar` search campaign (per
`references/search-strategy.md`) can exhaust a single subagent's time budget
before it reaches the filtering step. If that happens, fall back to the
tight-budget 10-query version (see the invocation prompt in Step 6 for a
ready template, or instruct the subagent explicitly to cap at 10 Slack
searches and stop early on 2–3 high-confidence findings).

### Notion child-page deletion is defensive

`notion-update-page` with `command: "replace_content"` will **refuse** to
run if it would delete child pages, unless you explicitly pass
`allow_deleting_content: true`. This is a feature, not a bug — trust it.
Practical consequences:

- Same-week rerun (no archive): use `update_content` (surgical
  search-and-replace) to edit the body in place. This never deletes children.
- Fresh week (after archive move): the main page has no children at that
  point (Archive is the one exception), so `replace_content` is safe.
  Include `<page url="<archive_url>">🗂️ Archive</page>` in `new_str` to keep
  Archive attached, then create the three fresh Read-more subpages.
- If you hit the "This operation would delete N child page(s)" error,
  **don't bypass it with `allow_deleting_content=true`**. Instead either
  (a) switch to `update_content`, or (b) add the listed child IDs as
  `<page url="...">` tags in `new_str`. The error names the pages explicitly
  so you can copy the URLs.

## Reference files

- `references/notion-page-layout.md` — full block-by-block layout of the
  canonical page and each Read-more subpage, with example Notion markdown for
  copy-paste. Read when assembling the final write in step 8.
