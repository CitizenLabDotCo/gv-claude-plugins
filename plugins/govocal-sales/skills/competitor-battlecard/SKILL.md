---
name: competitor-battlecard
description: Build a Go Vocal competitor battlecard — a paired concept note (.docx) and detailed comparison spreadsheet (.xlsx) that honestly positions Go Vocal against a named competitor. ALWAYS use this skill when Wietse or the team says things like "battlecard for [competitor]", "compare us to [X]", "build a concept note vs [competitor]", "enablement for [X] deal", "write a note convincing [X] clients to switch to Go Vocal", "comparison document against [competitor]", or anything about positioning Go Vocal head-to-head with another participation / civic-tech platform (CitizenLab, Cap Collectif, Decidim, Fluicity, Neighborland, CivicPlus, Bang the Table, Commonplace, Konveio, Granicus, etc.). Also trigger on casual phrasings like "need to prep something for our pitch against X" or "can you pull together a battlecard". Output is always in the competitor's regional language (French for FR competitors, Dutch for NL/BE-Flemish, German for DE/AT, Spanish for ES, English default).
---

# Competitor Battlecard

## Why this skill exists

Sales and Customer Success keep needing the same two things to convert a competitor's client or defend a deal: (1) a short concept note that tells the story of why Go Vocal is the natural next step, and (2) a detailed spreadsheet that's honest about where we win and where the competitor still does things better. You wrote those once for Decidim/OSP — this skill generalises the pattern so any competitor can be processed the same way.

The skill is opinionated about the *structure* and *tone* (five fixed USPs, consultative framing, honest YELLOW/RED flags where we lag) and flexible about the *evidence* (which features, which gaps, which stats are pulled from the competitor's own materials).

## The two deliverables

Every run produces, in the competitor's regional language:

1. `Go_Vocal_vs_{Competitor}_Concept_Note.docx` — cover + "Why this note" + Go Vocal in numbers + five USPs (each with "The opportunity" / "What we offer" + 3-5 feature bullets) + "The bottom line".
2. `Go_Vocal_vs_{Competitor}_Comparison.xlsx` — Overview/Legend tab + 6 product tabs (Engagement Methods, Back-Office & Workflows, Analysis & Reporting, UX & Frontend, Technical & Infrastructure, Support & Services), with 🟢 / 🟡 / 🔴 status per row for both Go Vocal and the competitor, plus details text.

Rows in the spreadsheet are **competitor-tailored**: the six tabs are the canonical scaffold, but the exact requirements shown depend on what the competitor actually does. A competitor that doesn't play in participatory budgeting shouldn't have that whole category stretched; a competitor that's strong on mapping or AI should have those rows expanded.

## The five USPs (fixed framing, tailored evidence)

Always the same five pillars, in this order:

1. **Hybrid input & representativeness** (360° Input Manager, FormSync 2.0, Representativeness Dashboard)
2. **Analysis & reporting** (AI Sensemaking, Ready-made reports, Demographic pattern detection; include the "~55% reduction in reporting cycle time" stat where credible)
3. **Streamlined back-office workflows** (Publication & approval workflows, Gantt timelines & department workspace, Project templates, Role-based access & smart groups, Email campaigns & automations)
4. **Interactive engagement, UX & CMS** (Map surveys for planning, Mobile-first adaptive resident UX, Three no-code builders — Content / Form / Report)
5. **Roadmap velocity & community** (Client-led roadmap with 15-person product team, Regional community of practice + Inspiration Hub, Dedicated GovSuccess Manager)

What *changes per competitor* is the "The opportunity" paragraph in each USP — it opens with what we heard from practitioners about that specific competitor's gap, not a generic Decidim story. See `references/usp_templates.md` for the canonical text and the variables to swap.

USP 5 needs a **context-aware angle**: open-source / self-hosted competitors get the "slow, fragmented support" framing; SaaS competitors get a team-size / release-cadence / success-service comparison. Detail in `references/usp_templates.md`.

## How the skill runs

The skill runs in two phases — research, then generation — with a human confirmation in between. That's deliberate: battlecards are high-stakes, and the competitor intel often contains outdated or wrong claims. You do not want to generate a polished docx on shaky evidence.

### Phase 1 — Structured intake & research

**Step 1. Intake.** Ask the user the questions in `references/intake_questions.md` in a single batch (via AskUserQuestion if the tool is available, otherwise just a numbered list). Don't invent answers for fields the user leaves blank — flag them as gaps to resolve in Step 2.

**Step 2. Research.** With the inputs from Step 1, gather evidence in this order — stop as soon as you have enough to rate every spreadsheet row with reasonable confidence:

1. Company website (product pages, pricing, case studies, blog).
2. Their public knowledge base / docs site — these are gold for figuring out which features actually exist.
3. Go Vocal's internal competitor intel, if connected. Look for a Notion page / workspace titled "Industry Competitors" (or similar) and fetch the competitor's row. If Notion is not connected, ask the user to paste the relevant section.
4. Slack — search public channels for recent mentions of the competitor name, if Slack is connected.
5. Previous proposals. Search `filetype:pdf "{competitor} proposal"` and `filetype:pdf "{competitor} response"` with government procurement keywords. FOIA-published or publicly-available winning proposals are a very high-signal source.

See `references/research_sources.md` for specific search queries, what to extract, and how to cite.

**Step 3. Language decision.** Based on the competitor's country of origin *and* their primary client base, pick the output language from `references/language_map.md`. Default to English if the competitor plays internationally and doesn't have a clear home region. Confirm with the user before generating.

**Step 4. Build a briefing.** Produce a `briefing.json` in the competitor's output subfolder containing:
- Competitor profile (name, HQ, positioning one-liner, hosting model, rough team size, open-source vs SaaS)
- Tailored "opportunity" paragraphs for each of the five USPs
- USP 5 angle choice (open-source / SaaS)
- Spreadsheet rows — the competitor-tailored list of requirements, with GV status + detail and competitor status + detail, *and* a `source` field for every competitor rating (URL, internal note, or "unverified — needs client input")
- A list of YELLOW / unverified rows the user needs to validate

**Step 5. Pause for validation.** Present the briefing summary to the user — especially the unverified rows — and ask them to confirm or correct before generating. This is the single most important checkpoint; ship nothing without it.

### Phase 2 — Generation

**Step 6. Generate outputs.** Run the two generator scripts:

```bash
python scripts/generate_concept_note.py <briefing.json> <output_path.docx>
python scripts/generate_spreadsheet.py  <briefing.json> <output_path.xlsx>
```

Both scripts take the briefing JSON and produce branded files. They read the language field off the briefing and localise labels (headers, legends, USP section titles like "L'enjeu / Ce que nous proposons" in French, "De uitdaging / Wat wij bieden" in Dutch, etc.). The full label dictionary lives in `scripts/localisation.py` — extend it if a new language comes up.

**Step 7. Deliver.** Land both files in the workspace's outputs folder under `battlecards/{Competitor}/`, alongside the briefing JSON and a short `research_notes.md` that lists the sources used. In Cowork this is typically the user's selected folder or `/mnt/outputs/`; in other environments, use whatever "shareable outputs" folder the current session exposes. Give the user links and a one-paragraph summary of where we clearly win and where we need to be honest about gaps.

## Tone rules (non-negotiable)

These are hard-won from the Decidim iteration. Keep them:

- **Consultative, not sales-y.** Every "The opportunity" paragraph opens from a practitioner's frustration we've heard, not a Go Vocal claim. "We've heard from teams moving from {competitor}..." is a good pattern.
- **No competitor bashing.** Where the competitor genuinely does something well, say so. Where we lag today, flag RED or YELLOW and say what's on the roadmap. The Decidim note had a "Written honestly: where Decidim does something Go Vocal doesn't yet, we say so" note on the Overview tab — keep that pattern.
- **Specific over generic.** A feature bullet like "drag-and-drop Content Builder for project pages" beats "modern CMS". Pull specifics from the competitor's own docs so the reader recognises the comparison.
- **Three features per USP is the default**, but USPs 3 and 4 can stretch to 5 when there's real substance (as in the Decidim note — back-office workflows have five bullets there).

## Brand rules

Go Vocal brand is already handled in the generator scripts (Chivo font, dark purple `#1E155D`, cherry `#FF3E52`, lilac `#F0EEFA` for accents). Don't invent new colours or fonts. The brand reference lives in `references/brand_tokens.md`.

## Visual ground truth — always check `assets/reference_examples/` first

Before generating, open the four canonical reference files in `assets/reference_examples/` (the signed-off Decidim battlecard in EN + FR, `.docx` + `.xlsx`). They are the single source of truth for layout and design — every battlecard this skill produces must look and feel identical to these, only with different content. See `assets/reference_examples/README.md` for guidance.

If the generated output doesn't visually match the references, that's a regression in the generator scripts — fix the scripts, not the output file.

## Output naming & location

- Folder: `<workspace_outputs>/battlecards/{Competitor}/` where `<workspace_outputs>` is the current environment's shareable outputs folder (the user's selected folder, `/mnt/outputs/`, `~/Downloads/`, etc. — do not hardcode).
- Files inside: `Go_Vocal_vs_{Competitor}_Concept_Note.docx`, `Go_Vocal_vs_{Competitor}_Comparison.xlsx`, `briefing.json`, `research_notes.md`
- `{Competitor}` is the competitor's short name, title-cased, spaces replaced with underscores (e.g. `Cap_Collectif`, `CitizenLab`, `Bang_the_Table`).

## Files in this skill

- `scripts/generate_concept_note.py` — docx generator; reads briefing JSON.
- `scripts/generate_spreadsheet.py` — xlsx generator; reads briefing JSON.
- `scripts/localisation.py` — shared label dictionary for EN / FR / NL / DE / ES.
- `references/usp_templates.md` — canonical five USPs with variables and both USP-5 angles.
- `references/intake_questions.md` — the exact questions to ask the user in Step 1.
- `references/research_sources.md` — where to look, what to extract, how to cite.
- `references/brand_tokens.md` — Go Vocal brand tokens.
- `references/language_map.md` — country → output language mapping.
- `references/spreadsheet_scaffold.md` — the six canonical tabs and the base row library.
- `assets/example_briefing_decidim.json` — full worked example for Decidim, to use as a reference shape.
- `assets/reference_examples/` — canonical signed-off `.docx` + `.xlsx` in EN and FR. Open these *before* generating a new battlecard — they are the visual ground truth for layout and design.
