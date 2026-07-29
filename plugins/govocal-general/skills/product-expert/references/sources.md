# Live sources & refresh procedure

Snapshot baked 2026-07-03 from Modular Proposal **V12 (May 2026)** + Feature Wiki +
support KB + API docs. Freshness rule: **if the question hinges on something recent
(feature status, exact wording, pricing, roadmap) or the snapshot is >1 release old,
verify against the live source below before answering.** If a connector is missing,
answer from the snapshot and say so ("per proposal V12; couldn't verify live").

## Source map

| Source | Where | Access | Use for |
|---|---|---|---|
| **Modular Proposal Template (EN-NorthAm master)** | Google Doc `1eJaXC6AGwvZczNeHR9z5qTkpMkQZJmfa3k6NSRDnKII` | Google Drive connector | Canonical sales narrative, feature positioning, exact proposal wording. First tab = changelog → cheapest way to diff versions. |
| Proposal SOP + localization rules | Notion page `30a9663b7b26801c9545f1daa458471f` | Notion connector | Update cadence, RACI, writing guidelines source. |
| **Localized proposals** | DACH `1akm1c8-aiFfSjwE7gl8J9ss-qXf1w0wd` · FR `1BRxIi7b5AgOg9IZ-zFZNFnA-CzBupwU-ED3aFip9zys` · NL-NL `1mFE_8UQqVDRY80VtGEvhlnGG7sH9NSg22kY37xBNHdE` · NL-BE `1zvIdU2Aa6B5mQ23PMbIhIuzZueON1vPJa-euJLMJzs8` (⚠ stale, 2024-07, "Needs updates") · EN-UK `1rjdCrzjBClfsVx3qEt79toLgNO_Xf5968_NzYlJIKhM` | Google Drive connector | Localized wording; terminology ground truth per market. |
| **Feature Wiki** (Notion DB) | data source `collection://adaf040d-1ca3-4169-ab8a-036108ee6e5a` | Notion connector — SQL query is plan-gated; use `notion-search` with `data_source_url` | **The authority on feature status** (In Development / Beta / Just launched / Post-Launch / Sunset), Core vs Add-on, tier, release dates. Check before promising anything recent. |
| **Enablement Assets library** (Notion DB) | database `3099663b7b2680509538dd602a2a8c1f`, data source `collection://3099663b-7b26-80cc-90c0-000b09314384` | Notion connector | Finding decks, one-pagers, demo scripts per language/tier. Also "I want to sell X" / "I want to know how X works" pages. |
| **Support knowledge base** | https://support.govocal.com/{en,nl,fr,de,da,it,es}/ | Public — WebFetch | How features actually behave; the honest constraints. Collections: Getting Started · Admin Configurations · Managing Projects & Participation Methods (largest, 29 articles) · Monitoring & Offline Participation · Data Analysis & Reporting · FAQ · Product Changelog. |
| **Public API docs** | https://developers.govocal.com/api/ (OpenAPI JSON: https://developers.citizenlab.co/api-docs/ee/public_api/master/open_api.json) | Public — WebFetch | API capability questions. v2, JWT auth (client_id/secret from Admin > Tools > Public API Access, 24h expiry). Resources: projects/phases, posts/ideas, comments, voting baskets, users/reactions, events/attendances, email campaigns, files, areas, topics, volunteering. Read-only. |
| **GOVOCAL.md** (product model, source-grounded) | `~/Claude/GV-Prototypes/GOVOCAL.md` | Local file | The living product-truth file (help center + real codebase). `references/product-model.md` here is derived from it. |
| Source code | github.com/CitizenLabDotCo/citizenlab | Public | Deepest ground truth (enums, field types, method keys). |

## Refresh procedure (`/product-expert refresh`)

1. Read the **changelog tab** of the EN proposal Google Doc; note versions newer than the
   snapshot version recorded in `capabilities.md`'s header.
2. For each changelog entry, update the affected sections of `capabilities.md` /
   `proposal-map.md` / `commercial.md`.
3. `notion-search` the Feature Wiki for pages edited since the snapshot date; update
   feature statuses in `capabilities.md` and `feature-index.md`.
4. Re-check localized docs' "Last Updated" in the Enablement Assets DB; refresh glossaries
   only for locales that moved.
5. Diff `~/Claude/GV-Prototypes/GOVOCAL.md` against `product-model.md`'s sync date; pull
   through product-model changes.
6. Update every touched file's snapshot header (date + proposal version).
