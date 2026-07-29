# FX handling in DCCI

## The model

- Every contract is booked in `Invoice-currency` (native). Currencies observed: EUR, GBP, USD, CAD, DKK, NOK, and occasional CLP in #we-grow.
- At `Date-start`, the native `Invoice-value` is converted to EUR via Google Finance and stored in `Value` (and downstream: `Value-rec`, `Value-rec-mrr`, `Value-rec-arr`, `Value-one`, etc.).
- **That EUR value is locked in for the life of the contract.** It does not float with the exchange rate afterwards. Recognition in Report-Revenue uses the locked-in EUR amount month by month.

This means a pure FX swing between months does **not** move MRR for ongoing contracts. Renewals and new contracts are the re-rating events.

## When FX *does* show up in an MRR movement

A renewal or new contract in a non-EUR currency gets FX-converted at its own `Date-start`. If the native-currency price is identical to the old contract but the FX rate has moved, the EUR MRR shifts — and this shows up in Report-Revenue as an "upgrade" or "downgrade" that isn't a genuine commercial motion.

**Example**:
- UK customer has a 12-month Premium contract at £12,000 starting Jan 2026. GBP/EUR ≈ 1.18 at that date → EUR Value = €14,160, MRR = €1,180/month.
- They renew in Jan 2027 at the same £12,000, but GBP/EUR ≈ 1.15 → EUR Value = €13,800, MRR = €1,150/month.
- Report-Revenue shows a **€30 downgrade** in UK MRR.
- Reality: zero commercial motion. It's FX.

## How to decompose an MRR movement into commercial vs FX

For each non-EUR customer that contributes to a movement in month M:

1. Pull their old and new contracts from `Data-percontract`. Note the native `Invoice-currency` and `Invoice-value` on each.
2. If `Invoice-currency` and native `Invoice-value/Duration` are unchanged between old and new contracts → the EUR delta is 100% FX.
3. If native monthly value changed → split the delta:
   - **FX component** = (old native MRR × new FX rate) − (old EUR MRR)
   - **Commercial component** = (new native MRR × new FX rate) − (old native MRR × new FX rate)
4. Report both, labelled clearly.

If you don't have the FX rates handy, approximate: any movement < 5% of the old EUR MRR for a non-EUR customer with unchanged native pricing is overwhelmingly FX. Flag it as such and move on.

## Currencies and typical drivers

| Currency | Regions | Notes |
|---|---|---|
| EUR | Flanders, Netherlands, Francophonie, DACH | No FX risk. Default. |
| GBP | UK | Material exposure; 1-3% swings common annually. |
| USD | North America (US) | Material exposure. |
| CAD | North America (Canada) | Material exposure. |
| DKK, NOK | Scandinavia | Usually small absolute values; FX noise can be material relative to customer size. |
| CLP | South America (Chile) — seen in #we-grow | Highly volatile; decompose carefully. |

## Reporting convention

When FX explains a non-trivial share of a movement for a region:

> Francophonie showed a €1.6k downgrade this month. **€1.2k is genuine** (Mairie X stepped down from Premium to Standard), **€0.4k is FX** (two Swiss customers got re-rated on renewal at a weaker CHF/EUR).

Never hide FX behind a commercial narrative — it confuses everyone. And never round FX away just because it's small; if it adds up to a meaningful line at region level, it deserves a sentence.

## Operating rule

If a non-EUR customer's MRR moves and you can't tell whether it's commercial or FX, **say so explicitly and flag for Jordan to verify**. Don't guess.
