# Research sources — Phase 1, Step 2

The goal: rate every row of the tailored spreadsheet with at least one cited source. Anything without a source becomes a YELLOW "Unverified" row for the user to validate in Step 5.

## Order of operations

Work through these in order and stop when you have enough. Don't chase everything — diminishing returns kick in fast after the competitor's own docs are read.

### 1. Competitor's website

Pages to read, in order of value:
- **Product pages / features page.** Usually the clearest list of what they claim to do.
- **Pricing page.** Tells you what's gated behind tiers (e.g. "AI analysis" on Enterprise only) — useful for the honest comparison.
- **Case studies / customer stories.** Name-drop real clients and describe use cases, which hints at where they're strongest in practice.
- **Blog / news.** Recent posts reveal where they're investing; repeated mentions of a feature mean it's their current push.
- **About / team page.** Team size is useful for USP 5 (especially for SaaS competitors).

Extract: feature names, direct quotes about capabilities, named clients, team size, funding / ownership.

### 2. Knowledge base / docs site

Often at `docs.{competitor}.com`, `help.{competitor}.com`, `{competitor}.com/docs`, `{competitor}.readme.io`, or on GitHub for open-source competitors. This is the highest-signal source — marketing pages oversell, docs can't lie.

What to look for:
- Exhaustive feature lists with screenshots
- Admin / back-office screenshots (tells you what the UI actually looks like)
- API documentation (tells you what's exposed, which hints at architecture maturity)
- Release notes / changelog (tells you cadence)

### 3. Internal Notion — Industry Competitors

If Notion is connected in the current environment:
- Use `notion-search` for the competitor name
- Or `notion-fetch` on "Industry Competitors" if a URL was provided in the intake

Extract everything in the competitor's row: current positioning, known weaknesses, recent deals we've won or lost to them, strategic notes.

If Notion isn't connected, say so and ask the user to paste the relevant section.

### 4. Slack

If Slack is connected:
- Search public channels (#sales, #competitive-intel, #wins, #losses, #product) for the competitor name
- Focus on the last 3-6 months
- Look for: deal retrospectives, feature parity discussions, client migration stories

If Slack isn't connected, skip.

### 5. Public proposals and FOIA

Government procurement processes in many countries publish winning proposals or responses. These are unusually high-signal because the competitor has to substantiate their claims to win.

Search patterns:
- `filetype:pdf "{competitor}" "participatory budget"`
- `filetype:pdf "{competitor}" proposal`
- `filetype:pdf "{competitor}" "technical response"`
- `"{competitor}" RFP site:.gov` / `site:.gouv.fr` / `site:.gov.uk`
- FOIA portals: US `foia.gov`, UK `whatdotheyknow.com`, FR `cada.fr`

If one turns up, read it carefully — it often contains feature matrices, pricing structures, and implementation timelines.

## What counts as a source

Each spreadsheet row's `source` field should be one of:
- A URL (competitor website, docs, blog post, case study, proposal PDF)
- An internal reference: `"Notion — Industry Competitors, {competitor} section"`, `"Slack #sales, message from {person} on {date}"`
- `"User input — {person} confirmed on {date}"` after Step 5 validation
- `"Unverified — needs client input"` — the YELLOW flag

## Citation quality

Prefer the most specific source available:
- A URL to the exact docs page beats a URL to the homepage
- A docs page beats a marketing page
- A proposal PDF often beats both if it's recent
- Internal Notion notes beat guesses but are lower-trust than primary sources
- Claude's own knowledge is the worst — only use as last resort and mark unverified

## What to avoid

- Do not read competitor reviews (G2, Capterra, Gartner) for feature claims — they're unreliable. They're OK for positioning / sentiment but not for ratings.
- Do not trust old press releases (>2 years) as evidence the feature still exists.
- Do not fabricate specifics. If the docs don't say it and the user can't confirm it, it's YELLOW.

## Handing off to Step 4

When research is done, the briefing JSON you produce should have, for every spreadsheet row:
```json
{
  "requirement": "...",
  "gv_status": "🟢 | 🟡 | 🔴",
  "gv_detail": "...",
  "competitor_status": "🟢 | 🟡 | 🔴",
  "competitor_detail": "...",
  "source": "https://... | Notion — ... | Unverified — needs client input"
}
```
