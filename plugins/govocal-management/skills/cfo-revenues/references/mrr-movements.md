# MRR Movement Classification

How to classify MRR evolution into the four canonical CFO categories. Primary source of truth is `Data-Recurring-MRR-percustomer` (customer-level MRR per month). Secondary validation comes from `Data-percontract` for attributing the motion to a specific deal.

## The four categories

Let `MRR(cust, M)` = the customer's recognized MRR in month M (from `Data-Recurring-MRR-percustomer`).

### New MRR from sales

**Definition**: `MRR(cust, M-1) = 0` AND `MRR(cust, M) > 0` AND the customer has a contract with `Contract-index = 1` active in month M.

**Contract-level confirmation**: a new `Data-percontract` row with `Contract-index = 1`, `Origin = New`.

**Amount**: `MRR(cust, M)` (all of it is new sales MRR).

**Edge case — Returned customer**: `MRR(cust, M-1) = 0`, `MRR(cust, M) > 0`, but the customer had a prior contract that ended months ago. `Contract-index > 1`, and the new contract carries `Origin = Returned`. By convention this is **also classified as new MRR from sales** (they came back, same motion as a new logo) unless Wietse asks to separate them out. Flag it in the narrative if material.

### New MRR from upgrade

**Definition**: `MRR(cust, M) > MRR(cust, M-1) > 0`.

**Amount**: `MRR(cust, M) − MRR(cust, M-1)`.

**Contract-level drivers** (look for one or more in `Data-percontract` for the same customer with `Date-start` in month M):
- `Contract-type = Upsell` AND `Sub Contract-type = Add-on` — new product bolted on while master runs
- `Contract-type = Upsell` AND `Sub Contract-type = License change` — tier step-up or scope change
- `Contract-type = Master` renewing at higher MRR than the previous Master contract — renewal with price uplift

**Edge case — Cross-sell**: a new product/module for an existing customer is always **upgrade**, never new sales. The Contract-index will be >1 and the Contract-type will be Upsell.

**Edge case — Mid-month start of upsell contract**: the MRR step shows up partially in the start month (pro-rated) and fully from the next month. Upgrade attribution happens in the month where the customer's total MRR first reflects the new level.

### Lost MRR from downgrade

**Definition**: `0 < MRR(cust, M) < MRR(cust, M-1)`.

**Amount**: `MRR(cust, M-1) − MRR(cust, M)`.

**Contract-level drivers** (one or more in `Data-percontract`):
- A contract ending (`Date-end` in M-1 or early M) that's replaced by a smaller renewal
- A tier step-down at renewal — usually `Contract-type = Master`, `Sub Contract-type = License change`
- An upsell/add-on contract ending without replacement

**Edge case — Hibernation**: no explicit flag in DCCI. Manifests as a sudden MRR drop (or a new contract with much lower value replacing the old one). If the customer's new contract has `Sub Contract-type = Fixed-term` and short `Duration`, or if the #we-grow post mentioned "hibernation extension", classify as downgrade — and call it out by name in the narrative so it's distinguishable from a genuine license step-down.

**Edge case — Price concessions / discounts**: not tracked explicitly. If `Value` drops materially from one contract to the next for the same customer and tier, it's a downgrade even if the nominal scope didn't change.

### Lost MRR from churn

**Definition**: `MRR(cust, M-1) > 0` AND `MRR(cust, M) = 0`.

**Amount**: `MRR(cust, M-1)` (all of it lost to churn).

**Contract-level confirmation**: `Data-percontract.Destination = Churned` on the last contract, AND `Data-percustomer.Destination-last` in {Churned, Churned On Hold}.

**Edge case — Gap before return**: a customer with `MRR(cust, M-1) > 0`, `MRR(cust, M) = 0` is churned in month M. If they later come back (e.g., 4 months later), that later reactivation is a **new sale (Returned)** — it's a separate motion, not a reversal of the churn.

## Reconciliation identity

For every month M:

```
Report-MRR row 10 in M  −  Report-MRR row 10 in M-1
  =  New MRR from sales  +  New MRR from upgrade
      −  Lost MRR from downgrade  −  Lost MRR from churn
```

If this doesn't hold within rounding (< €50 absolute), there's a classification gap. Investigate before shipping. Usual causes:
- A late-booked contract moved MRR in a month that didn't yet have it when the movement rows were computed.
- A pro-ration asymmetry (contract started mid-month in M-1 but the movement row only counted the delta in M).
- A mis-coded `Contract-index` or `Origin` that pushed a customer into the wrong bucket.

## Classification priority when signals disagree

If the customer's MRR delta (`Data-Recurring-MRR-percustomer`) says one thing and the contract metadata (`Data-percontract`) says another:

1. **MRR-level truth wins for the aggregate number.** If the customer's MRR went from 1500 to 1900, the number is €400 upgrade, regardless of what contract flags say.
2. **Contract metadata wins for the narrative.** Use `Contract-type` and `Sub Contract-type` to explain *why*. "Stad Oostende: €400 upgrade from a Premium tier license change."
3. **Disagreement is a flag.** If `Origin = New` but the customer had MRR in M-1, that's a DCCI inconsistency — raise it in Mode 4 (audit).

## Currency considerations

DCCI stores all contract `Value` in EUR, FX-converted at `Date-start`. Ongoing contracts keep their original EUR value even if the underlying currency (e.g., USD, GBP) moves. This means:

- A pure FX change does **not** drive an MRR movement — contracts keep their locked-in EUR once booked.
- However, a new contract (renewal, upsell) at a new `Date-start` gets FX-converted at that date's rate. So a renewal at the same native-currency price can show as a slight upgrade or downgrade in EUR terms.

When reporting movements in a region with non-EUR contracts (UK = GBP, North America = CAD/USD, Scandinavia = DKK/NOK), decompose material FX-driven changes separately. See `fx-notes.md` for the mechanics.

## Output structure

For any MRR evolution question, return the quartet as the default:

```
New MRR
  Sales:    € X
  Upgrade:  € Y
Lost MRR
  Downgrade: € Z
  Churn:     € W
Net: € (X + Y − Z − W)
```

Even when a category is €0, keep the line visible — the four-box structure is the narrative. Follow with per-customer drivers for any material line.
