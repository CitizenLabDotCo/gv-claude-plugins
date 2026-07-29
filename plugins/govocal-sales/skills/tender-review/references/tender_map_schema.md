# `tender_map.json` schema

The single source of truth produced in Phase 1 and read by every later phase and by
`scripts/simulate_scores.py`. Keep it faithful to the tender — every figure traceable to a source.

```json
{
  "tender": {
    "name": "Stad Mechelen — participatieplatform",
    "authority": "Stad Mechelen",
    "language": "nl",
    "currency": "EUR",
    "deadline": "2026-05-22",
    "contract_term": "2+1+1 years",
    "price_basis": "total price over full term, excl. VAT",
    "incumbent": null,
    "source_docs": ["bestek.pdf", "gunningscriteria_bijlage.pdf", "inschrijvingsformulier.xlsx"]
  },

  "exclusion_grounds": [
    {
      "id": "E1",
      "requirement": "Tenderer must provide WCAG 2.1 AA conformance.",
      "type": "exclusion",
      "source": "bestek §3.4",
      "quote": "De inschrijver dient te voldoen aan WCAG 2.1 AA."
    }
  ],

  "criteria": [
    {
      "id": "C1",
      "name": "Price",
      "weight": 50,
      "max_points": 50,
      "scoring_method": "price_formula",
      "price_formula": {
        "pattern": "lowest_proportional",
        "max_points": 50,
        "reference": "P_min",
        "competitor_dependent": true,
        "quote": "score = (laagste prijs / ingediende prijs) × 50",
        "source": "gunningscriteria §2.1",
        "caps": null
      }
    },
    {
      "id": "C2",
      "name": "Quality",
      "weight": 40,
      "max_points": 40,
      "scoring_method": "rubric",
      "subcriteria": [
        {
          "id": "C2.1",
          "name": "Functionality & flexibility",
          "max_points": 20,
          "requirement_type": "scored-mandatory",
          "source": "bestek §4.1"
        },
        {
          "id": "C2.2",
          "name": "User-friendliness",
          "max_points": 20,
          "requirement_type": "scored-optional",
          "source": "bestek §4.2"
        }
      ]
    },
    {
      "id": "C3",
      "name": "MVOO (socially responsible procurement)",
      "weight": 10,
      "max_points": 10,
      "scoring_method": "rubric",
      "requirement_type": "scored-optional",
      "source": "bestek §5"
    }
  ],

  "award_model": {
    "type": "additive",
    "note": "total = sum of criterion points (each max already encodes its weight)",
    "max_total": 100
  },

  "requirements": [
    {
      "id": "R12",
      "maps_to": "C2.1",
      "text": "Platform must support map-based surveys.",
      "type": "scored-mandatory",
      "must_or_nice": "must",
      "source": "bestek §4.1.7"
    }
  ],

  "bidders": [
    { "id": "govocal", "name": "Go Vocal", "is_us": true },
    { "id": "comp1", "name": "TreeCompany", "is_us": false }
  ]
}
```

## Field notes

- **`scoring_method`**: `price_formula` | `rubric` | `meat_ratio` | `pass_fail`.
- **`price_formula.pattern`**: one of the patterns in `price_formulas.md`
  (`lowest_proportional`, `linear_interpolation`, `relative_reference`, `relative_average`,
  `proportional_difference`, `threshold`, `meat_ratio`, `additive_wrapper`).
- **`competitor_dependent`**: `true` if the reference price (min/max/avg/submitted) depends on what
  competitors bid — the sweep must recompute it. `false` for fixed budget/ceiling references.
- **`award_model.type`**: `additive` or `meat`. If sub-scores are normalised to 0–100 before weighting,
  set `"normalised": true` and store `weight` (%) rather than absolute `max_points`.
- **`requirement_type`**: `exclusion` | `scored-mandatory` | `scored-optional` | `informational`.
- **`must_or_nice`**: editorial tag for the must-have/nice-to-have map in the review.
- Keep a `source` (doc + section) on everything. If a value is assumed rather than stated, prefix with
  `ASSUMED:` so it is never mistaken for a tender fact.
