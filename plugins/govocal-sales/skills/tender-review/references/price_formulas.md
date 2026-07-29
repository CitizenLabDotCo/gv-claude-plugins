# Price-scoring formula library

Public tenders score price in several different ways. Picking the wrong one quietly breaks every
simulation, so the goal of Phase 1 is to find the **exact** formula in the tender's own words and map
it to one of the patterns below. Always capture the verbatim quote and its source document/section.

## How to find the formula

Look in the award/scoring annex, the section on *gunningscriteria* (NL) / *critères d'attribution*
(FR) / *Zuschlagskriterien* (DE) / *award criteria* (EN), and on the price form itself. Search for:

- NL: "prijs", "puntenverdeling", "laagste prijs", "score = ", "formule", "% van de punten"
- FR: "prix", "note prix", "offre la moins-disante", "formule", "barème"
- DE: "Preis", "Preisbewertung", "günstigster Preis", "Formel", "Wertung"
- EN: "price score", "lowest price", "pricing formula", "weighting", "points awarded"

Record: the **price weight** (e.g. 50%), the **max price points** (e.g. 50), the **reference price**
the formula uses (lowest bid? a budget ceiling? the average?), any **caps/floors**, and whether price
is the *total* or a *weighted basket* of unit prices.

## The patterns

Notation: `P_own` = our price, `P_i` = a bidder's price, `P_min` = lowest valid bid, `P_max` = highest
bid (or budget ceiling), `P_avg` = average of valid bids, `MaxPts` = maximum price points.

### 1. Lowest-price proportional (inverse) — the BE/NL default
The most common in Belgian/Flemish municipal tenders (this is what Mechelen and Hamont-Achel use).

```
price_score(P_i) = (P_min / P_i) × MaxPts
```
Lowest bid gets the full `MaxPts`; everyone else is scaled down by ratio. Convex: the penalty for
being more expensive shrinks as you go higher. **Beating the lowest price is the only way to max this**
— so the simulation must know (or assume) competitor prices to be meaningful.

### 2. Linear interpolation between lowest and highest (or ceiling)
```
price_score(P_i) = MaxPts × (P_max − P_i) / (P_max − P_min)
```
Lowest gets `MaxPts`, highest (or the ceiling) gets 0, linear in between. More punishing in the middle
than pattern 1. Confirm whether `P_max` is the highest *submitted* bid (depends on competitors) or a
fixed budget ceiling (independent of competitors) — this materially changes the sweep.

### 3. Relative reduction from a reference / budget
```
price_score(P_i) = MaxPts × (P_ref − P_i) / P_ref      (P_ref = ceiling or estimated value)
```
Scores the % below the reference price. Independent of competitors if `P_ref` is a fixed budget.

### 4. Relative to the average bid
```
price_score(P_i) = MaxPts × (P_avg / P_i)        (or a linear variant around P_avg)
```
Used to discourage abnormally low bids. Highly competitor-dependent and non-monotonic to reason about
— simulate explicitly, never eyeball.

### 5. Proportional difference from lowest ("points lost per % above min")
```
price_score(P_i) = MaxPts × (1 − (P_i − P_min) / P_min)      (floored at 0)
```
Common variant: each X% above the lowest costs a fixed number of points. Capture the exact step.

### 6. Threshold / below-ceiling pass + scored remainder
Price must be under a ceiling to be admissible (else **exclusion** — record it as an exclusion ground),
then the admissible price is scored by one of the patterns above.

### 7. MEAT — Most Economically Advantageous Tender (quality/price ratio)
Total isn't `quality_points + price_points`; instead the award uses a ratio, e.g.
```
value = quality_score / P_own        (highest value wins)
```
or a price-per-quality-point. When a tender is MEAT-ratio rather than additive-points, the simulator
must compute and compare the ratio, not a weighted sum. Detect this explicitly — it changes the model.

### 8. Additive weighted total (the wrapper)
Most tenders are additive: `total = Σ (criterion_score_normalised × weight)`, with price being one
criterion scored by patterns 1–6. Confirm whether sub-scores are on a common 0–100 scale then weighted,
or each criterion has its own absolute max points that already encode the weight. Both appear; the
arithmetic differs.

## Turning the formula into the simulation

1. Implement the detected price formula as a function `price_score(P, context)` where `context`
   carries `P_min`, `P_max`, `P_avg`, `P_ref` as needed — note which of these depend on competitor
   prices (so the sweep recomputes them as our price and competitor prices change).
2. Combine with quality via the wrapper (additive or MEAT) from the award model.
3. Sweep `P_own`; at each point recompute competitor-dependent references, then total scores for every
   bidder. **Price-to-win = highest `P_own` (≥ cost floor) where our total ≥ the best competitor's.**
4. `scripts/simulate_scores.py` implements patterns 1–8 — use it to verify any non-trivial case rather
   than doing the algebra by hand.

## Gotchas

- "Lowest price gets max" with proportional scaling (pattern 1) means **our own price changes `P_min`
  only if we become the cheapest** — handle that branch.
- When the reference is the *highest submitted bid* or the *average*, adding/removing a competitor or
  changing one competitor's price shifts everyone's score. Always recompute, never cache.
- Watch for price being a **basket of weighted unit prices / a TCO over the contract term**, not a
  single headline number. Score the same quantity the tender scores.
- VAT, contract duration (2+1+1 etc.), and optional line items: make sure our price and competitor
  prices are compared on the **same basis** the tender uses.
- If the tender gives a worked example, reproduce it with the implemented formula as a unit check.
