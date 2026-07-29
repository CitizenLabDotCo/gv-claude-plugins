# DCCI consistency audit — check-by-check

Mode 4 of the skill. Run against a live read of DCCI. Output one-row-per-issue for the user, with suggested fix and CRM link so Jordan H. can triage quickly.

Severity framework: **High** = blocks accurate reporting or is customer-facing. **Medium** = leaves money on the table or misclassifies motion. **Low** = hygiene.

## Check 1 — Stale active contract

**Rule**: `Data-percontract` row where `Date-end < today` AND `Ended ≠ Ended`.

This happens when a contract has technically expired but the Ended flag hasn't flipped. Since `Ended` is calculated from `Date-end`, this only misbehaves if the formula is broken for a row or if `Date-end` was updated without recalc.

**Severity**: Medium. Misclassifies MRR recognition.

**Suggested fix**: Verify `Date-end` is correct; set `Ended = Ended`; set `Destination` appropriately (Renewed if a successor exists, Churned otherwise).

## Check 2 — Overdue renewal

**Rule**: `Data-percontract` where:
- `Date-renewal < today − 30 days`, AND
- `Destination = Ongoing` (meaning: the team still expects this to renew), AND
- No successor contract exists for the same `Cust-id` with `Date-start >= Date-renewal`.

Split by severity:
- **High**: > 60 days overdue.
- **Medium**: 30-60 days overdue.

**Context**: `Date-renewal` can legitimately sit ahead of `Date-end` on multi-year contracts (opt-out clauses). When `Date-renewal < today` and nothing new has been booked, either the customer silently continued on an auto-renewal or the renewal paperwork is lagging in DCCI.

**Suggested fix**: Ping the sales owner (`Owner-sales`) and GS owner (`Owner-gs`) for status. If renewed on paper but not yet booked, Jordan to add the row.

## Check 3 — Customer vs contract status mismatch

Two sub-checks:

**3a**: A `Data-percontract` row has `Destination = Churned`, but `Data-percustomer.Destination-last` for the same `Cust-id` is not `Churned` or `Churned On Hold`.

**3b**: `Data-percustomer.Destination-last` in {Churned, Churned On Hold}, but there's a `Data-percontract` row for the same `Cust-id` with `Ended = Ongoing`.

**Severity**: High for 3b (active contract on a churned customer — either the churn is misrecorded or we're still billing someone we've marked churned). Medium for 3a.

**Suggested fix**: Verify current commercial relationship; update the customer-level status to match the contract reality (or vice versa).

## Check 4 — Report-MRR reconciliation gap

**Rule**: For the latest complete month M:
- `Report-MRR` row 10, column M = $R$
- Sum of `Data-Recurring-Revenue-percustomer` column M across all rows = $S$
- If `|R − S| > €50`, flag.

**Severity**: High if >€500, Medium otherwise.

**Suggested fix**: Identify which customer contributes the delta by iterating through customer rows and comparing to the contract-level sum; likely a late-booked contract or a pro-ration edge case.

## Check 5 — Missing customer dimensions on active accounts

**Rule**: `Data-percustomer` where any of `Country`, `Region`, `Cust-type-L1`, `Cust-type-L2`, `Owner-gs` is blank, AND the customer has at least one `Data-percontract` row with `Ended = Ongoing`.

**Severity**: Medium. Breaks segment reporting (Mode 1).

**Suggested fix**: Backfill the dimension.

## Check 6 — Active contract with no recurring value

**Rule**: `Data-percontract` where `Ended = Ongoing` AND `Value-rec-mrr = 0` AND `Contract-type ≠ One-off`.

One-offs legitimately have zero recurring MRR. Masters and Upsells should always have recurring value unless they're pending entry.

**Severity**: High (we're recognizing no MRR for a supposedly-active customer-revenue contract).

**Suggested fix**: Verify `Value` is populated; re-check `Contract-type` classification.

## Check 7 — Duplicates

**7a**: Two `Data-percontract` rows with the same `Contract-id`. Shouldn't happen by construction (`Contract-id = <Cust-id>-<Contract-index>`).

**7b**: Two `Data-percustomer` rows with the same `Cust-name` (exact match after trimming whitespace). Sometimes legitimate (two distinct entities of the same parent), but worth human review.

**Severity**: High for 7a (data integrity). Low for 7b (flag for review).

**Suggested fix**: 7a — identify which row is correct, delete the duplicate. 7b — human check; if truly duplicate, merge.

## How to present the output

One combined table, sorted by severity then by customer:

| Cust-id | Cust-name | Contract-id | Check | Severity | Details | Suggested fix | CRM link |
|---|---|---|---|---|---|---|---|
| 123 | Stad X | 0123-0005 | 2 — Overdue renewal | High | Renewal 47 days overdue, no successor | Ping Owner-sales | [link] |

Also include a summary header: `Total issues: N (High: x, Medium: y, Low: z)` and the scan date.

If zero issues, that's a valid and celebratable result — say so plainly.
