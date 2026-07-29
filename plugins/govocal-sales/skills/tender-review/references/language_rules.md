# Language rules

The aim: rewrites paste straight into the proposal, while internal QA stays legible to the deal team.

## Decision

- **Proposal-text rewrites** → always the **tender's language** (NL / FR / DE / EN).
- **Internal analysis, QA notes, scoring justifications, recommendations:**
  - Tender in **French or German** → write the internal analysis in **English** (QA happens in English),
    with the native rewrite snippet alongside each recommendation.
  - Tender in **Dutch or English** → analysis may be in the tender's language.
  - When unsure, confirm in intake.
- The **simulator UI** and the **price-to-win headline** → English labels are fine (internal tool);
  keep criterion names in the tender's language so they're recognisable.

## Placeholder tokens (never fabricate a fact — leave a marked gap)

| Tender language | Placeholder | "Verify internally" note |
|---|---|---|
| Dutch | `[invul]` | `(intern te bevestigen)` |
| French | `[à compléter]` | `(à confirmer en interne)` |
| German | `[ergänzen]` | `(intern zu bestätigen)` |
| English | `[fill in]` | `(verify internally)` |

Use a placeholder whenever a real number, date, SLA, certification, named auditor, or commitment is
needed but not known from our materials. Pair it with a one-line note on what to verify and where it
goes. This mirrors the Mechelen review, where six `[invul]` placeholders were left for facts that must
not be guessed (current Lighthouse score, uptime %, audit party, OSLO/LDES estimate, API auth, SCIM
roadmap).

## Tone of rewrites

Match Go Vocal's tender voice: confident, specific, consultative. Lead by **acknowledging the
requirement**, then answer it directly, then evidence it. Avoid over-claiming — where we genuinely lag,
frame honestly with the mitigation rather than bluffing (honest "no" + roadmap beats a vague yes).
