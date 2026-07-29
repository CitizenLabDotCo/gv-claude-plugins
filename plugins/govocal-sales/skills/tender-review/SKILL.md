---
name: tender-review
description: >-
  Master tender/RFP reviewer for Go Vocal across the whole bid lifecycle: strategic scoring + price-to-
  win simulation AND a pre-submission red-team. ALWAYS use when anyone says "review this tender", "score
  our response", "improve our [tender] bid", "what price should we bid", "price to win [tender]", "build
  a scoring simulator", "simulate [competitor] against us", "review our submission", "check our bid
  before we send it", "pre-submission review", "red-team this tender", "analyse the bestek / cahier des
  charges / RFP", or shares a draft about to go out. Takes a Google Drive folder (+ our draft),
  auto-extracts the award model and price formula, runs the exclusion/DQ gate, scores our response
  against the grid AND the won/lost checklist (SLA gold-standard, template traps), ranks fixes by
  points-at-stake, simulates who wins at which price, and returns ready-to-paste rewrites. Publishes to
  Notion (always) + an interactive price simulator. Native rewrites, English QA for FR/DE; never invents.
---

# Tender review (master)

## Why this skill exists

Go Vocal keeps losing winnable tenders by fractions of a point — Moncton by 0.56, Gateshead by 0.25%,
Hutt by 0.6 — and the debriefs always say the same: it came down to the detail, not the product. We
also sometimes risk disqualification on a single missed mandatory. This skill is the one place to (1)
understand exactly how a tender scores, (2) score our draft against it and against our own hard-won
loss patterns, (3) catch the avoidable packaging mistakes before they go out, and (4) pick the price
that wins without giving away margin. It merges two earlier skills (strategic proposal review +
pre-submission red-team) into one lifecycle tool.

It is opinionated about **process, rubric, and the loss-pattern checklist**, and flexible about the
**evidence** — each tender's criteria tree and price formula are extracted from that tender's own docs.

## Two modes (one workflow)

The same pipeline runs at either stage; pick the emphasis in intake:

- **Strategic review & price-to-win** (early/mid-bid): map the scoring, score our draft for margin,
  simulate price-to-win. Emphasis on where the points and the price live.
- **Pre-submission red-team** (final QA before sending): full loss-pattern checklist, SLA gold-standard,
  template-trap sweep, points-at-stake ranking, and customer-ready paste rewrites. Emphasis on
  disqualification risks and avoidable point-losers.

If a draft exists and submission is near, **do both** — the scoring map feeds the red-team, and the
red-team findings feed the quality scores in the simulator. Default to both unless told otherwise.

## Deliverables

Every full run produces:

1. **Review on a Notion page** — verdict, exclusion/DQ risks, scorecard (RAG + points-at-stake),
   prioritised fixes, **ready-to-paste rewrites**, and "what's strong — keep it". **Always Notion,
   never a Google Doc or `.docx`** unless the user explicitly asks for one.
2. **Interactive scoring simulator** (HTML artifact) — configurable weights, our price, named
   competitor prices, the tender's actual price formula, quality per bidder; live totals + price-sweep
   + price-to-win.
3. **Price-to-win recommendation** — the price (or range) that maximises win probability given a margin
   floor, with sensitivity to competitor-price assumptions.

In a pure pre-submission red-team where price isn't in scope, deliverables 2–3 are optional — but still
read the price formula so the scorecard can weight fixes correctly.

## Inputs

- **Required:** a **Google Drive folder** (or file list) with the buyer's documents — the RFP/ITT/
  bestek/cahier des charges, the **scoring/award criteria with weightings**, mandatory/pass-fail
  requirements, SLA/support and hosting/security requirements, word limits, and any Q&A log. The
  **scoring section and price form matter most**.
- **Required for review:** our **draft** — technical/quality answers, SLA doc, pricing schedule,
  implementation plan, references, method statements, forms/declarations. Usually in Drive; may be a
  Notion page, an upload, or Google Docs — handle whatever the user points to.
- **For the simulation:** **competitor name(s) + assumed price** each, and our **cost floor**. Without
  them we model price-to-win at break-even quality and let the user set prices live in the simulator.
- **Optional:** stage/mode, output language, the Notion parent, target ACV, whether we are incumbent.

Batch the questions in `references/intake_questions.md`. If the scoring grid isn't available, say so and
review against the checklist anyway, flagging that fixes can't be weighted precisely.

## How the skill runs

Four phases, with a **human checkpoint after Phase 1** (the extracted scoring model). Getting the award
model and price formula right matters more than anything downstream.

### Phase 0 — Intake
Ask the questions in `references/intake_questions.md` in one batch. Confirm the mode/stage and the
Notion parent. Don't invent answers for blanks — flag them.

### Phase 1 — Ingest & map (the foundation)
1. **Read everything from Drive** (`search_files` to list the folder, `read_file_content`;
   `download_file_content` + the `pdf` skill for scans). Identify buyer docs vs. our submission docs.
   For a large submission, scan it with `Grep` for the specific signals below rather than reading it
   whole.
2. **Build the requirements & scoring map:** every **scored** criterion with weight and what it asks
   for, every **mandatory/pass-fail** requirement, the SLA/hosting/Social-Value/word-limit rules.
3. **Run the exclusion / disqualification gate** — list each hard requirement with the exact source
   quote; a single miss can void the bid.
4. **Map must-haves vs nice-to-haves** and tag how each contributes to scoring (`exclusion` /
   `scored-mandatory` / `scored-optional` / `informational`).
5. **Auto-extract the price formula** — read `references/price_formulas.md`, identify the pattern,
   capture the verbatim wording and parameters.
6. **Write `tender_map.json`** (schema in `references/tender_map_schema.md`) — the single source of truth.
7. **CHECKPOINT:** show weights, the price formula in plain words, the exclusion list, and the must/nice
   map; confirm before building on them.

### Phase 2 — Score our response (two lenses, one scorecard)
Apply **both** reference files together:
- `references/scoring_review_rubric.md` — per scored criterion: does our answer **acknowledge the
  requirement**, answer the *actual* question, and replace vague promises with **concrete commitments**?
  Assign a band + the **margin** (points recoverable).
- `references/pre_submission_checklist.md` — the ten loss-pattern areas, the **SLA gold-standard facts**
  (don't undersell what we actually deliver), and the **template traps** (other clients' names left in,
  stray hosting lines, "GoVocal"/"CitizenLab" leftovers, content that "won't be evaluated", etc.).

For every finding, estimate **points-at-stake = criterion weight × distance from full marks**, and type
it **DEEPEN / REWRITE / ADD / FIX**. Surface mandatory/DQ risks first regardless of weight. Lead with
what we actually deliver — our most common self-inflicted wound is describing *less* than we provide.
**Never invent facts**; where a real number/date/name is needed but unknown, leave a clearly-marked
placeholder (`[invul]` NL · `[à compléter]` FR · `[ergänzen]` DE · `[fill in]` EN) and a verify note.

Convert the per-criterion bands into **quality scores per bidder** to feed the simulator (keep an
**as-is** and an **improved** set so the score lift from the fixes is visible).

### Phase 3 — Price-to-win simulation
Build the price model from the extracted formula (verify non-trivial cases with
`scripts/simulate_scores.py` — don't hand-wave the arithmetic). Enter our quality (Phase 2) and
estimated competitor quality; configure **named competitor prices** (adjustable); **sweep our price**
and compute totals for every bidder; find the **price-to-win** (highest price ≥ cost floor where we
still out-score the strongest competitor). Repeat across low/expected/high competitor-price scenarios.

### Phase 4 — Deliverables
- **Notion page (always):** publish per `references/notion_layout.md` — verdict + price-to-win first,
  then exclusion/DQ, scorecard, prioritised fixes, ready-to-paste rewrites, and "what's strong". Create
  under the parent the user named (default: a "Tenders" page) or append to the deal's existing page. Do
  **not** make a Google Doc/`.docx` unless explicitly asked.
- **Simulator artifact:** adapt `assets/simulator_template.html` to this tender and publish with the
  Cowork `create_artifact` tool. Fresh per tender.
- **Price-to-win:** surface the headline in chat *and* on the Notion page and simulator.

## Two registers (important)
- **Scorecard & findings** are internal — direct, points-focused, for the bid team.
- **Ready-to-paste rewrites** are external — finished prose in Go Vocal's voice to the buyer, in the
  tender's language, no internal jargon, no "we should". If a reviewer has to rewrite your rewrite
  before pasting, it has failed.

## Language rules
Proposal-text rewrites always in the **tender's language** (NL/FR/DE/EN). Internal analysis/QA: for
**French or German** tenders write it in **English** (native rewrite snippet alongside each); NL/EN may
be in the tender language. Detail and placeholder tokens in `references/language_rules.md`.

## Guardrails
- **Never invent** prices, requirements, scores, deadlines, certifications, or competitor figures.
  Separate what the tender *states*, what we *assume* (label it), and what must be *verified*.
- The price formula and weights are load-bearing — confirm them at the Phase 1 checkpoint.
- Competitor prices/quality are assumptions the user owns; always show how the recommendation shifts
  across scenarios, never one number as certain.
- **Be honest about real product gaps** — don't coach overclaiming; flag genuine gaps for Product.
- **Mind the qualification** — if the buyer is clearly buying something we're not, say so; it may be a
  low-probability bid.
- **Keep outputs clean — no noise.** Lead with substance (verdict / price-to-win), not a stack of
  labels, meta lines, or disclaimers; one short "estimates to validate" note at the end. Strip
  ingestion noise (internal "à ne pas remettre" notes, "Tab 1"/"Template" banners, boilerplate).
- This skill **reviews, simulates, and recommends — it does not submit anything.**

## Reference files
- `references/intake_questions.md` — the batched intake (incl. mode/stage).
- `references/price_formulas.md` — price-scoring formula library. **Read in Phase 1.**
- `references/tender_map_schema.md` — JSON schema for `tender_map.json`.
- `references/scoring_review_rubric.md` — per-criterion scoring + points-at-stake + rewrite typing.
  **Read in Phase 2.**
- `references/pre_submission_checklist.md` — the ten loss-pattern areas, SLA gold-standard facts, and
  template traps. **Read in Phase 2.**
- `references/language_rules.md` — language + placeholder tokens.
- `references/notion_layout.md` — the Notion page structure (the always-on home for the review).
- `assets/simulator_template.html` — the configurable scoring-simulator template to adapt per tender.
- `scripts/simulate_scores.py` — compute/verify total scores and price-to-win for a `tender_map.json`.
