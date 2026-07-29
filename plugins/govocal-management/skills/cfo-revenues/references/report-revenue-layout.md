# Report-Revenue Layout

Google Drive file id: `1vLX-44JzG3fDqCH_kHdwHjcFJy4Cf-mfFBYUVDv6rsM`.

This is the recognition sheet — where DCCI contract values get laid out month-by-month across their duration (pro-rated for mid-month starts/ends). It's the authoritative source for MRR over time.

## Tab: Data-Recurring-Revenue

- One row per contract (same grain as `Data-percontract` in DCCI).
- Columns run jan-17 through the current horizon (extends yearly) with `Total <YYYY>` totalling columns after each December.
- Cells = recognized recurring revenue for that contract in that month, EUR, pro-rated.
- Not the right tab for customer-level MRR evolution — sum this by `Cust-id` or go to the customer rollup.

Use when: you need contract-level attribution (which contract drove that movement?), or you need to check whether a specific contract started/ended mid-month.

## Tab: Data-Recurring-Revenue-percustomer

- One row per customer.
- Same monthly-column layout.
- Each cell = sum of recognized recurring revenue for the customer across all their contracts that month.
- **This is the primary source for customer-level MRR evolution.** If customer X's cell in month M-1 is €0 and month M is €2,000, that's a new sale. If M-1 is €2,000 and M is €3,500, that's an upgrade. Etc.

Use when: you need to classify movements per customer without drilling into contract structure.

## Tab: Data-Recurring-MRR-percustomer

- Customer-level MRR per month.
- Cleanest source for computing sales / upgrade / downgrade / churn by comparing month-to-month customer totals.
- Functionally similar to `Data-Recurring-Revenue-percustomer` but specifically framed for MRR analysis.

Use when: classifying MRR movements or tracking a specific customer's MRR trajectory.

## Tab: Report-MRR — THE AUTHORITATIVE MRR NUMBER

**Row 10 is the total recognized MRR per month across all contracts, unfiltered.** Every reconciliation ends here.

- Columns are months (jan-17 onward, Dutch month abbreviations: jan, feb, mrt, apr, mei, jun, jul, aug, sep, okt, nov, dec).
- "Total <YYYY>" columns appear after each December for the annual rollup.
- This row is definitive: any mismatch with sum of `Data-Recurring-Revenue-percustomer` for the same month is a bug, not a judgment call.

### Pre-computed MRR movement rows — USE THESE

Report-Revenue already contains rows that pre-compute the four movement categories, broken out by region. Use them directly rather than re-deriving from scratch:

- `New MRR from sales <Region>` — customers starting MRR from €0
- `New MRR from upgrade <Region>` — same-customer MRR increase
- `Lost MRR from churn <Region>` — customers going to €0 MRR
- `Lost MRR from downgrade <Region>` — same-customer MRR decrease

Regions observed: **Flanders, Netherlands, Francophonie, DACH, UK, North America**, with extras for Scandinavia / Asia / South America / Other as they gain scale. Sum across regions for a company total.

For a monthly financial report, the job is:
1. Read the pre-computed rows for the target month.
2. Aggregate by region (or sum for a total view).
3. Compute Net = Sales + Upgrade − Downgrade − Churn.
4. Reconcile: Report-MRR(M) − Report-MRR(M-1) should equal Net. If not, investigate (usually a gap between when a movement was recognized and when it was classified; sometimes a late-booked contract by the admin team).
5. Attach drivers — for each material line, the 1-3 customers responsible. Pull those from `Data-Recurring-MRR-percustomer`.

### When pre-computed numbers don't match first-principles

If a movement pre-computed in Report-Revenue disagrees with what you compute from `Data-Recurring-MRR-percustomer`, that's a data issue — not a classification ambiguity. Flag it to the user; don't pick one silently.

## Performance note

`Data-Recurring-Revenue` is wide (contracts × months) and occasionally errors on read due to sheet size. If that happens:

1. Retry once after 30 seconds.
2. If still failing, switch to `Data-Recurring-MRR-percustomer` (smaller, customer-level) for the analysis, and flag to the user that the contract-level tab was unavailable so conclusions are customer-grained.
3. `Report-MRR` row 10 is tiny and almost always readable — use it as the reconciliation anchor even when larger tabs fail.
