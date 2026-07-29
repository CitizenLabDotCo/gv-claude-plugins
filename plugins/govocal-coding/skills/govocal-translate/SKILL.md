---
name: govocal-translate
description: Translate GoVocal screens, prototypes or copy into another language. ALWAYS use this when asked to translate anything (a page, component copy, microcopy, an email, a locale variant) — it fetches the live product glossary first so terms match the real platform, and it asks the scoping questions (target locale, audience, register) BEFORE translating. Never translate GoVocal copy from general knowledge alone.
---

# GoVocal Translation — glossary-first

GoVocal ships in ~40 locales, and the product has **canonical terms** per language
(an "input" is *bijdrage* in nl-NL, *contribution* in fr-FR, *Beitrag* in de-DE —
never a literal translation). Those decisions live in the main product repo and are
maintained by the translation team via Polyglit. A prototype that invents its own
terms reads as wrong to every reviewer, so: **fetch the glossary fresh, every time,
before translating a single word.** It changes; never rely on a cached or remembered
copy.

## Step 1 — pull the live glossary (always, first)

```bash
gh api -H "Accept: application/vnd.github.raw" \
  repos/CitizenLabDotCo/citizenlab/contents/polyglit.glossary.json
```

Format: `{ "source term (en)": { "<locale>": "translation", … }, … }` (~100 terms).
Glossary terms are **binding** — use them exactly, including casing conventions you
see in the values. If a term you need is missing for your target locale, fall back to
Step 2 phrasing precedent, and flag the gap in chat.

Locale tiers and the machine-translation context blurb live next to it in
`polyglit.jsonc` (same fetch, different path). Tier l1 — `da-DK`, `nl-NL` (→ `nl-BE`),
`fr-FR` (→ `fr-BE`), `de-DE` (→ `de-AT`) — is fully proofread quality; derived locales
(`nl-BE` etc.) start from their parent and only diverge where regionally needed.

## Step 2 — check phrasing precedent in the real UI strings

The full live UI strings per locale are in the same repo:

- `front/app/translations/{locale}.json` — resident-facing platform
- `front/app/translations/admin/{locale}.json` — back office
- `back/config/locales/{locale}.yml` (+ `back/engines/*/*/config/locales/`) — backend & emails

```bash
gh api -H "Accept: application/vnd.github.raw" \
  repos/CitizenLabDotCo/citizenlab/contents/front/app/translations/nl-NL.json > /tmp/nl-NL.json
```

Before writing your own phrasing for a common pattern (buttons, empty states, form
errors, dates), grep the target-locale file for how the platform already says it —
including register (formal vs informal address: whatever the existing strings use for
that locale is the answer, don't decide it yourself). The English source
(`en.json`) is the key-to-meaning map when a translated string is ambiguous.

## Step 3 — ask before translating

Translation requests are usually underspecified. **Ask first** (one round, then
proceed):

- **Which locale(s), exactly?** "Dutch" is ambiguous — nl-NL or nl-BE? "French" —
  fr-FR or fr-BE? If they say "the l1 languages", that's da-DK + nl-NL + fr-FR + de-DE.
- **Which surface?** Resident-facing vs admin/back-office copy pull from different
  string files and can differ in register.
- **Full screen or copy only?** Translating a prototype screen may also mean dates,
  numbers, seeded content (names, project titles) — ask whether demo content should
  be localized too or stay as-is.

## Step 4 — translate

- Glossary terms exactly; platform phrasing for common patterns; match the register
  of the existing locale files.
- Product context (from `polyglit.jsonc`): a civic engagement platform where local
  governments run participation projects (ideation, surveys, participatory budgeting,
  voting, polls) and residents take part. Translate for residents of that place, not
  for developers.
- Keep untranslatables untouched: brand names ("Go Vocal"), `.gv-*` class names, code,
  URLs, and anything that is a design-system token rather than copy.
- When you had to invent a term (not in glossary, no precedent), list those choices in
  chat at the end so a human can vet them.
