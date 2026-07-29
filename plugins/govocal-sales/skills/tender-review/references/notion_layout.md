# Notion page layout

The review **always** lives here — Notion is the default and only home for the written output (never a
Google Doc or .docx unless the user explicitly asks). Publish with the Notion MCP, under the parent the
user named (default: a "Tenders" page) or appended to the deal's existing page.

**Lead clean — no noise.** The first block is the verdict + price-to-win callout. Don't open with a
stack of labels, meta lines, or disclaimers, and don't carry over source noise (internal "à ne pas
remettre" notes, "Tab 1"/"Template" banners, confidentiality boilerplate). A single short "estimates to
validate with the team" line goes at the **end**, in Sources & assumptions.

## Title
`{Tender name} — review & recommendations` (or `… — pre-submission review` in red-team mode).

## Structure

1. **Verdict & price-to-win** — callout. Bid/adjust/do-not-submit lean + the single biggest risk;
   recommended price (range) and the competitor scenario it assumes; current vs improved total.
2. **Disqualification & mandatory risks (fix first)** — table: requirement · source · MET/NOT MET/
   UNCLEAR · action. Red for any NOT MET/UNCLEAR. "None found" if clean.
3. **Scorecard** — table: area/criterion · RAG (🔴🟠🟢) · points-at-stake · headline gap. Highest
   points-at-stake first.
4. **Prioritised fixes** — numbered, ordered by impact: `[area] — [the gap, where it is in our doc] →
   [what to change]` with the recommendation type (DEEPEN/REWRITE/ADD/FIX) and ~points at stake. Mark
   items that need an **action** (price change, attach a certificate) vs. a paste.
5. **Ready-to-paste rewrites** — one block per significant fix, headed by where it goes (section /
   question number). The text is finished prose in Go Vocal's voice **in the tender's language**, in a
   quote/code block so it copies cleanly. `[à compléter]`-style placeholders only where a real value is
   genuinely needed.
6. **What's strong — keep it** — the genuinely good parts, so the writer doesn't dilute them.
7. **Price-to-win** — the sweep result + low/expected/high competitor scenarios; link/embed the
   simulator artifact.
8. **Sources & assumptions** — links to the Drive docs; everything ASSUMED labelled; the single
   "validate with the team" line.

## Conventions
- Rewrite snippets in **quote/code blocks** so the team can copy them straight into the proposal.
- One row per fix, typed and sorted by points-at-stake.
- Link back to source Drive documents rather than pasting long extracts.
- If the deal already has a Notion page, offer to append there instead of creating a new one.
- End with a **Sources** section listing the tender documents and internal pages used.
