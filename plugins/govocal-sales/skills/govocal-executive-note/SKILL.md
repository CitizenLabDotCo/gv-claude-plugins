---
name: govocal-executive-note
description: Build a Go Vocal executive note for a city — a branded .docx positioning Go Vocal as the right engagement platform (cover, Why this note, Go Vocal in numbers, five USPs with The opportunity / What we offer + a product image, The bottom line). Auto-detects two modes: GREENFIELD (no incumbent) outputs the note only; COMPETITIVE (a named rival) outputs the note as a comparison PLUS a feature spreadsheet (.xlsx). Use when the team says 'executive note for [city]', 'Go Vocal note for [city]', 'make the case to [city] leadership', 'first-platform note for [city]' (greenfield); or 'executive note for [city] vs [competitor]', 'battlecard for [competitor]', 'compare us to [X]', 'comparison vs [competitor]', 'enablement for the [X] deal' (competitive — Cap Collectif, Decidim, Fluicity, CivicPlus, Granicus, etc.). Output language follows the city/competitor region (FR, NL, DE, ES; English default).
---

# Go Vocal Executive Note

## Why this skill exists

Sales, CS and the CEO repeatedly need a short, branded note that tells a city *why Go Vocal is the right platform* — sometimes greenfield (no incumbent), sometimes against a named competitor (the original battlecard use case). It is the same artifact and the same house style; the only question is whether there is a rival to compare against.

This skill is opinionated about **structure** and **tone** (five USPs, consultative framing, honest flags where we lag) and flexible about the **evidence** (which city context, which features, which screenshots). Feature copy is always grounded in the live product documentation, never invented.

## The two modes (auto-detected)

Detect the mode from the request; if ambiguous, ask one question.

- **GREENFIELD** (default) — no incumbent platform named. Output: **executive note only** (`.docx`). The cover is a single partnership label (`GO VOCAL · CITY`), the five "The opportunity" paragraphs open from the city's own situation, not from a competitor's gap.
- **COMPETITIVE** — a rival is named or implied. Output: **executive note framed as a comparison** (`.docx`) **+** **comparison spreadsheet** (`.xlsx`). The cover is `GO VOCAL × COMPETITOR`; the opportunity paragraphs open from "we've heard from teams moving from {competitor}…"; the spreadsheet is generated via `scripts/generate_spreadsheet.py`. See `references/usp_templates.md`, `references/spreadsheet_scaffold.md`, `references/research_sources.md`.

Both modes share one generator (`scripts/generate_concept_note.py`) driven by a briefing JSON. The `mode` field on the briefing selects the cover; image specs are honoured in both modes.

## The deliverables

Land everything in `<workspace_outputs>/executive_notes/{City}/` (or `battlecards/{Competitor}/` in competitive mode):

1. `Go_Vocal_{City}_Executive_Note.docx` — always.
2. `Go_Vocal_vs_{Competitor}_Comparison.xlsx` — competitive mode only.
3. `briefing_{city}.json`, plus a short `research_notes.md` listing sources used.

## The five USPs (fixed framing, tailored evidence)

Always five pillars. The default titles are below, but they can be **retitled per request** (e.g. "Combine every channel in one hub", "Automated periodic reporting and a live view for leadership", etc.). Keep the order and the underlying themes:

1. **Hybrid input & representativeness** — 360 Input, FormSync 2.0 (paper, ~95% OCR), ECHO by Dembrane (in-person voice-to-insight), Representativeness Dashboard. *Split FormSync and ECHO into their own bullets when the city has meaningful paper/in-person channels.*
2. **Analysis & automated reporting** — AI Sensemaking, Report Builder + ready-made reports, Community Monitor (always-on leadership dashboard). Use the "~55% reduction in reporting cycle time" stat only where credible, flagged for validation.
3. **Streamlined back-office & cross-department workflows** — publication & approval workflows, project templates + Inspiration Hub, roles/permissions & smart groups, planning calendar + email campaigns + webhooks/automations.
4. **Accessible, multilingual resident experience & CMS** — mobile-first WCAG 2.2 AA UX, native multilingual + Weglot auto-translation, ESRI map surveys, three no-code builders.
5. **Best practices & a global peer network** — client-led roadmap (15-person product team, 8–10-week cycles), community of practice + Inspiration Hub, dedicated Government Success Manager.

Only each USP's **"The opportunity"** paragraph is rewritten per city, from the fed-in context. "What we offer" bullets stay stable and are pruned/expanded to the city's use cases.

## ALWAYS ground feature copy in the live product doc

Before writing any "What we offer" bullet or feature caption, consult the **current Go Vocal product documentation** so descriptions, names and stats are accurate and never invented:

- **Modular Proposal Template (V-latest)** — Google Doc `1f69Rhprxd_AZY4WlzztVkMgpxhrB41jynerdWZnprSI`. This is the source of truth for feature names, descriptions and figures (FormSync accuracy, ECHO, 360 Input, Sensemaking, Community Monitor, Report Builder, workflows & automations, security/hosting, roadmap, etc.).

See `references/product_doc.md` for exactly which sections map to which USP, and how to cite. If a feature is needed that isn't in the doc, flag it to the user for validation rather than guessing.

## How the skill runs

### Phase 1 — Intake & research (human checkpoint before generating)

1. **Detect mode** (greenfield vs competitive) and **city/competitor + language** (`references/language_map.md`).
2. **Intake** — ask the questions in `references/intake_questions.md` in one batch. Capture: city context (departments, regions, demographics/languages, local service-channel names, priority use cases, evaluation/RFP situation), and which of the 5 USPs to emphasise / retitle.
3. **Pull product copy** from the product doc (above) for every feature you'll cite.
4. **Competitive only:** research the rival per `references/research_sources.md`; build the spreadsheet rows with honest 🟢/🟡/🔴 and a `source` per competitor rating.
5. **Write the briefing JSON** (schema = `assets/example_briefing_johannesburg.json` for greenfield, `assets/example_briefing_decidim.json` for competitive). Set `mode`, `language`, cover (logo/hero specs), five USPs, image specs, bottom line.
6. **Pause for validation** — present the unverified items (local facts, stats like the 55% figure, any product feature not in the doc) and confirm before generating.

### Phase 2 — Generation

```bash
python scripts/generate_concept_note.py <briefing.json> <output.docx> <assets_dir>
# competitive mode also:
python scripts/generate_spreadsheet.py  <briefing.json> <output.xlsx>
```

`<assets_dir>` defaults to the briefing's folder; point it at this skill's `assets/` so bundled imagery resolves. A USP image renders centred below that section's text when the file exists; a missing image renders nothing (no placeholder).

## Imagery — bundled in the skill

All Go Vocal house imagery lives **inside this skill** under `assets/` (not in any user's local files), extracted from a signed-off reference note so every run reuses the same look:

- `assets/brand/go_vocal_logo.png` — cover logo (top-left).
- `assets/brand/icons/` — the six cherry stat icons for the "Go Vocal in numbers" row (one per `numbers` entry, via its `icon` field).
- `assets/product/usp1_formsync.png`, `usp2_sensemaking.png`, `usp3_dashboard.png`, `usp4_map.png` — the four bundled USP screenshots, which map 1:1 to the five USP themes.

The cover pairs the Go Vocal logo with the **city's own logo/seal** (`cover.city_logo`, per run). **If a USP has no fitting bundled image** (e.g. USP 5) — pull a figure from the product doc (e.g. the Inspiration Hub as `product/usp5_inspiration_hub.png`) or leave it out.

### City logo — ask the user for it

The city's own logo/seal is **not** auto-fetched. If `cover.city_logo` isn't supplied, **ask the user to provide the official city logo** — ideally a transparent or white-background PNG. Don't scrape it: city logos and coats of arms are frequently trademarked, and the official brand mark (often a wordmark) is rarely the same as a Wikimedia coat of arms. Save what the user gives you under `assets/brand/city_logos/<slug>.png` and set `cover.city_logo.path`. If the supplied logo is on a dark background, flag it — it will need a transparent/white-background version to sit cleanly next to the Go Vocal logo on the white cover.

Each USP image renders **centred below that section's text** (`placement: "full"` → full 16cm width for wide shots, else 13cm; `width_cm` overrides). **A missing image renders nothing — no placeholder box.** So if a city has no fitting figure for a USP (e.g. USP 5), just leave it out, or pull a fitting figure from the product doc. See `assets/MANIFEST.md` for filenames.

## Brand rules (non-negotiable)

Handled in the generator; do not improvise.
- **Fonts:** Chivo for headings / cover title / USP titles / numbers; **Libre Franklin for all running body copy** (per `govocal-brand`). Both are Google Fonts — note to the user they must be installed for correct rendering.
- **Colours:** dark purple `#1E155D`, medium purple `#43369B`, cherry `#FF3E52` (accents/labels only), lilac `#F0EEFA` (USP title + number blocks). See `references/brand_tokens.md`.
- "Go Vocal" is always two words; clients are "municipalities", end-users are "residents".

## Tone rules (non-negotiable)

- **Consultative, not sales-y.** Every "The opportunity" opens from a practitioner's reality, not a Go Vocal claim.
- **No competitor bashing.** Where a rival does something well, say so; where Go Vocal lags, flag 🟡/🔴 and state what's on the roadmap.
- **Specific over generic.** Pull concrete feature names from the product doc.
- **Three feature bullets per USP by default**; USP 1, 3 and 4 can stretch to 4–5 when there's real substance (e.g. split FormSync and ECHO out under USP 1).

## Visual ground truth

Before generating, open `assets/reference_examples/` (signed-off Decidim note EN/FR) for competitive layout, and `assets/example_briefing_johannesburg.json` for the greenfield shape. Output must look identical to these, only with different content. If it doesn't match, fix the generator, not the output file.

## Files in this skill

- `scripts/generate_concept_note.py` — branded docx generator; mode-aware cover, logo/hero/USP images, Chivo+Libre Franklin.
- `scripts/generate_spreadsheet.py` — xlsx generator (competitive mode).
- `scripts/localisation.py` — label dictionary (EN/FR/NL/DE/ES).
- `references/intake_questions.md` — greenfield + competitive intake.
- `references/product_doc.md` — product-doc pointer + USP→section map + citation rules.
- `references/usp_templates.md` — canonical five USPs, variables, USP-5 angles.
- `references/research_sources.md`, `references/spreadsheet_scaffold.md`, `references/language_map.md`, `references/brand_tokens.md`.
- `assets/example_briefing_johannesburg.json` — greenfield worked example (wired to bundled assets).
- `assets/example_briefing_decidim.json` — competitive worked example.
- `assets/brand/`, `assets/product/` — bundled imagery (+ `MANIFEST.md`).
- `assets/reference_examples/` — signed-off visual ground truth.
