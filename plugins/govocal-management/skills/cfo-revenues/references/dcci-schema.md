# DCCI Schema Reference

Full column reference for **Data-Custcont-Input** — the authoritative recognized-revenue book. Two canonical tabs: `Data-percontract` (one row per contract) and `Data-percustomer` (one row per customer, with rollups).

The spreadsheet is sourced primarily from Salesforce but manually validated and booked by the admin team (@Jordan H.). When discrepancies surface between Salesforce and DCCI, DCCI is the source of truth for recognized revenue — Salesforce is upstream.

Google Drive file id: `170ifajrUyCmyzlUCN33CdFFxO1YjyyzZVJKtThTOywA`.

## Data-percustomer columns

Customer-level identity and rollups across all of a customer's contracts.

### Identity and geography

| Column | Meaning | Valid values |
|---|---|---|
| `Cust-id` | Unique numeric customer identifier. Zero-padded to 4 digits when composing `Contract-id`. | Free number |
| `Cust-name` | Customer display name | Free text |
| `Region` | Geographical rollup | Europe, North-America, South-America, Asia (plus commercial subdivisions: Flanders, Netherlands, Francophonie, DACH, UK, North America, Scandinavia, etc., as surfaced in Report-Revenue) |
| `Country` | ISO 3166-1 alpha-2 country code | 2-letter codes (BE, NL, FR, DE, DK, UK, CA, US, MY, …) |
| `Locale` | Language code | 2-letter codes (NL, FR, EN, DE, DK, …) |
| `Country-Locale` | Combined `<country>-<locale>` | Calculated |
| `Cust-type-L1` | Top-level customer type | Government, Non-government |
| `Cust-type-L2` | Sub-type | Local, Regional, National, Non-profit, Partner, Intermediary, … |
| `Lead-L1` | Who holds the customer relationship | HQ, Partner, Intermediary |
| `Lead-L2` | Sub-classification of the lead relationship | Free text / partner names |
| `Target-cust` | Whether customer is in the "target" commercial focus | Target (all governments where we have a direct relationship, no intermediary, no DE-market) / Non-target |

### Population (for local governments)

| Column | Meaning | Valid values |
|---|---|---|
| `Population` | Number of inhabitants | Integer |
| `Population-source` | Where the figure was pulled from | Statbel-20yymmdd (BE), Cbs-20yymmdd (NL), WikipediaEN-20yymmdd (other) |
| `Population-group` | Bucketed size | XL (>250k), L (>100k), M (>30k), S (>10k), XS (>0k) |

### Ownership

| Column | Meaning |
|---|---|
| `Owner-sales` | Sales owner (AE) |
| `Owner-gs` | GovSuccess owner (CSM) — the reliable ownership field |

### System links

| Column | Meaning |
|---|---|
| `Tenant-id`, `Tenant-id2` | AdminHQ tenant identifiers |
| `SF-account-id` | Salesforce account id |

### Rollups across all contracts

| Column | Meaning |
|---|---|
| `Contract-id-first` / `Contract-id-last` | First and most recent contract ids for the customer |
| `Date-start-first` | Start date of the customer's first contract ever |
| `Date-end-last` | End date of the most recent contract |
| `Duration-total` | Sum of `Duration` across all contracts (in months) |
| `Value-total` | Sum of `Value` (EUR) across all contracts — recurring + one-time |
| `Value-total-rec` | Sum of recurring value across contracts |
| `Value-total-rec-ARR` | `Value-total-rec-mrr` × 12 |
| `Value-total-rec-mrr` | **Customer-level MRR** = `Value-total-rec / Duration-total` (EUR) |
| `Value-total-one`, `Value-total-one-impl`, `Value-total-one-serv` | One-time fees breakdown |
| `In-out-bound-first` | Whether the customer came inbound or outbound, from first contract |
| `Target-master-last` | Combined Target flag: Target if both `Target-cust` and most recent `Target-contract` = Target |
| `Ended-last` | Whether the most recent contract has ended (Ended / Ongoing) |
| `Destination-last` | **Customer-level churn status** — Ongoing / Renewed / Churned / Churned On Hold |
| `Lifecycle-stage` | 0. To start, 1. Onboarding, 2. Continuous, 3. Pre-renewal, 4. Churned |
| `Date-launch-first` | When the platform reached 20+ users |
| `Days-until-launch-first` | `Date-launch-first` − `Date-start-first` |
| `Days-since-launch-first` | Today − `Date-launch-first` (bounded by `Date-end-last`) |
| `Days-since-start-first` | Today − `Date-start-first` (bounded by `Date-end-last`) |

## Data-percontract columns

One row per contract. Contracts belong to exactly one customer via `Cust-id`.

### Identity

| Column | Meaning |
|---|---|
| `Contract-id` | Unique contract id in `xxxx-yyyy` form where `xxxx` = zero-padded `Cust-id`, `yyyy` = zero-padded `Contract-index` |
| `Cust-id`, `Cust-name` | Customer the contract belongs to |
| `Contract-index` | Sequence number of this contract within the customer — **`1` means first-ever contract, which marks a new sale** |
| `Contract-name` | `<Cust-name>-<Contract-index>` |

### Dates

| Column | Meaning |
|---|---|
| `Date-moved-to-won` | When the deal was marked won in Salesforce (triggers the #we-grow post) |
| `Date-start` | Contract start |
| `Date-end` | Contract end — calculated as `Date-start` + `Duration` |
| `Duration` | Contract length in months |
| `Date-renewal` | When the contract is up for renewal — for single-year contracts equals `Date-end`; for multi-year contracts reflects opt-out clauses |

### Product

| Column | Meaning | Valid values |
|---|---|---|
| `Tier-version` | Product version | V1_20160101, V2_20200601 |
| `Tier-level` | Licence plan | Essential, Standard, Premium (recent contracts often carry fuller labels like "Premium (New)", "Standard + (Pre Nov 25)") |
| `Opt-out` | Whether contract has opt-out | Opt-out / No-opt-out |
| `Opt-out-comment` | Describes the opt-out mechanism (notice period, cadence) |
| `Contract-type` | Master / Upsell / One-off — Master = main/first licence; Upsell = added while Master runs; One-off = grant / implementation / ad hoc |
| `Sub Contract-type` | Continuous (standard) / Fixed-term (non-target, time-boxed) / Pilot (6-12 months with upsell intent) / License change / Add-on / Implementation fee / ad hoc support |
| `Target-contract` | Target (local/regional/national gov) / Non-target |
| `Target-master` | Target if both `Target-cust` = Target AND `Target-contract` = Target |

### Values (all EUR)

| Column | Meaning |
|---|---|
| `Value` | Full contract value — recurring + one-time, EUR (FX-converted at `Date-start`) |
| `Value-rec` | Recurring portion = `Value` − `Value-one` |
| `Value-rec-arr` | ARR equivalent = `Value-rec-mrr` × 12 |
| `Value-rec-mrr` | **Contract-level MRR** = `Value-rec` / `Duration` (EUR) |
| `Value-one` | One-time total = `Value-one-impl` + `Value-one-serv` |
| `Value-one-impl` | Implementation fee |
| `Value-one-serv` | Service fee |
| `Value-yearone` | Year-1 value = `Value-rec-mrr` × min(`Duration`, 12) + `Value-one` |

### Invoicing (native currency)

| Column | Meaning | Valid values |
|---|---|---|
| `Invoice-value` | Invoice amount in `Invoice-currency` |
| `Invoice-currency` | Contract billing currency | CAD, DKK, EUR, GBP, NOK, USD |
| `Invoice-status` | Waiting for order / To invoice / Invoiced partly / Invoiced / Payment overdue / Paid partly / Paid |
| `Invoice-comment` | Free text |
| `Invoice-nr`, `Invoice-date` | Bookkeeping |

### Lifecycle

| Column | Meaning | Valid values |
|---|---|---|
| `Ended` | Calculated from `Date-end < today` | Ended / Ongoing |
| `In-out-bound` | Acquisition channel | Inbound, Outbound, - |
| `Origin` | What happened before the contract started | New, Renewed, Returned |
| `Destination` | **Contract-level outcome** — what happens after `Date-end` | Ongoing, Renewed, Churned |
| `CRM-link` | Direct link to the Salesforce opportunity |
| `Comments` | Free text notes |

## Related reference material surfaced in DCCI

The DCCI file also contains tabs for:
- Zendesk/Salesforce pipeline import (sales team's source-of-truth-in-progress)
- AdminHQ tenant metadata (tenant id, creation, state, host)
- Engagement metrics (eng-opps, session-count, user-count, visitors)
- Churn reason taxonomy (1. Bad fit, 2. Misaligned expectations, 3. Stakeholder/championship issues, 4. Bad adoption, 5. Missed outcome, 6. High cost of ownership — each with numbered sub-reasons)
- Renewal forecast (`Forecast-chance` 0-1, `Forecast-value-rec`, `Outcome`)

These aren't part of the core revenue recognition flow but are useful when the question asks for qualitative colour (why did X churn? what's the renewal forecast?).
