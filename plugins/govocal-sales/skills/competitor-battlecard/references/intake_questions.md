# Intake questions — Phase 1, Step 1

Ask these at the start of every run. The first five are required; the rest are optional but sharpen the output.

## Required

1. **Competitor name.** The name as the user refers to it internally (e.g. "Cap Collectif", "CitizenLab", "Bang the Table"). This becomes the `{Competitor}` token in file names.

2. **Their home country / primary market.** Needed to decide output language (see `language_map.md`).

3. **Any live deal or client this battlecard is for.** If yes: which municipality / institution, and what's the immediate use case driving the decision (PB, consultation, petitions, planning, etc.)? This lets us weight the spreadsheet towards the rows that matter.

4. **Primary links.** Ask for any of: company website, product / features page, pricing page, knowledge base, docs site. The more the user hands over, the less time we spend scraping.

5. **Any internal artefacts?** Check if the user can share: previous proposal PDFs (theirs or ours), Notion sub-pages, Slack threads they already have open, sales-call notes, a case study from a client who migrated off them.

## Optional but valuable

6. **Which language for output?** Default suggested from `language_map.md`, but confirm — some competitors are HQ'd in France but win mostly in the UK, etc.

7. **Any specific angle the user wants emphasised?** E.g. "focus on analysis — that's where this client cares most" or "they're going to push on open-source, prep that argument".

8. **Anything we should NOT say?** E.g. client-specific sensitivities, pending legal matters, colleagues from the competitor that are now at Go Vocal and shouldn't be referenced.

## Delivery

Prefer the `AskUserQuestion` tool if available — one batch with multi-select where sensible. If not, send the questions as a short numbered list. Don't ask them one at a time; context-switching burns the user's patience.

## Fallbacks

If the user only gives you the name and nothing else — that's fine. The skill can infer most of this from a web search in Phase 1, Step 2. But flag it honestly: "I'll work from web research only; expect more YELLOW / unverified rows in the spreadsheet."
