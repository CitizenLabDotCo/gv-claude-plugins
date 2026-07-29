# Scoring review rubric

How to score Go Vocal's draft against the extracted award model — the per-criterion lens of Phase 2.
Run this together with `pre_submission_checklist.md` (the loss-pattern lens); both feed one scorecard
ranked by points-at-stake.

## The exclusion gate (run first)
For every `exclusion` requirement in `tender_map.json`, state **MET** (quote our text), **NOT MET** (why
— can void the bid), or **UNCLEAR** (silent/ambiguous — a risk). Surface any NOT MET / UNCLEAR at the
very top of every output. A single unmet mandatory sinks an otherwise winning bid.

## Scoring each scored criterion
For every `scored-mandatory` and `scored-optional` criterion:

1. **Located?** Find where our draft answers it. Nothing answering a scored criterion = a **missing piece**.
2. **Acknowledges the requirement?** The most common weakness — we describe our platform but never say
   "the requirement is X; here is how we meet X." Evaluators tick a checklist; if we don't name it, they
   can't tick it. Reward explicit acknowledgement, in the buyer's own terms.
3. **Answers the actual question?** Not an adjacent one we'd rather answer (e.g. "data export" when they
   asked "data segmentation"). Adjacent answers read as evasion.
4. **Concrete vs vague?** Turn "included", "on request", "no extra cost" into **commitments**: a number,
   a timeline, a named mechanism, an SLA, a cadence. Vague reassurance ≈ 7/10; concrete commitment 9–10.
   Where the buyer states explicit targets, **quote them back** with committed figures.

### Estimated band + margin
- **9–10 / full** — acknowledges, answers directly, concrete and evidenced.
- **7–8** — correct but generic, missing a commitment or proof. *Margin lives here.*
- **4–6** — partial, adjacent, or buried.
- **0–3** — absent, off-topic, or contradicts a requirement.

Record the **margin** (points recoverable if lifted to full).

## Sizing the prize — points-at-stake
For every finding (from this rubric **or** the checklist), estimate
**points-at-stake = criterion weight × distance from full marks**. This turns a long list into a priority
order: a 🟠 on a 30%-weighted criterion beats a 🔴 on a 2% one. Sort all fixes by points-at-stake, but
list mandatory/DQ risks first regardless of weight.

## Typing each recommendation
- **DEEPEN** — right direction, needs a commitment/number/proof. (Highest ROI; 7–8 → 9–10.)
- **REWRITE** — answers the wrong thing or hides the point; restructure to acknowledge + answer first.
- **ADD (missing)** — no answer exists; draft one.
- **FIX** — factual error, inconsistency, or a self-inflicted weakness (e.g. SLA/support-hours framing).

Each recommendation carries a **ready-to-paste rewrite** in the tender's language (see
`language_rules.md`). Where a real fact/number is required but unknown, insert the language placeholder
and a "verify internally" note — never fabricate.

## Lead with what we actually deliver
Our most common self-inflicted wound is describing *less* than we provide. Where the draft undersells a
real capability, pull the real thing forward (cross-check the SLA gold-standard and service-description
items in `pre_submission_checklist.md`). Be honest about genuine product gaps — flag them for Product
rather than overclaiming.

## Feeding the simulator
Convert each criterion's band into a **quality score (0–max)** for Go Vocal. For competitors, use
battlecard/competitive-intelligence knowledge if available, else a labelled neutral assumption. Keep two
sets — **as-is** (current draft) and **improved** (recommendations applied) — so the score lift from the
rewrites is visible and motivates the work.
