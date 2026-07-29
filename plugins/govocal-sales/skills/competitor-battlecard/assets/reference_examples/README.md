# Reference examples — canonical Decidim battlecard

These four files are the canonical layout and design anchors for every battlecard this skill produces. They were hand-tuned and signed off by Wietse (Go Vocal CEO) on the Decidim/OSP deal in April 2026, and every new battlecard should look and feel identical to these, only with different content.

## What's here

| File | Language | Purpose |
|---|---|---|
| `Go_Vocal_vs_Decidim_Concept_Note.docx` | EN | Layout reference for the concept note in English. |
| `Go_Vocal_vs_Decidim_Comparison.xlsx`   | EN | Layout reference for the comparison spreadsheet in English. |
| `Go_Vocal_vs_Decidim_Note_Conceptuelle_FR.docx` | FR | Layout reference for the concept note in French, including the localised headings ("Pourquoi cette note", "L'enjeu", "Ce que nous proposons", "En résumé"). |
| `Go_Vocal_vs_Decidim_Comparatif_FR.xlsx` | FR | Layout reference for the spreadsheet in French. |

## How to use them

Before generating a new battlecard:

1. **Open the two reference files** that match the target language (if target is German, open an EN or FR reference — any reference shows the same layout, only the labels change).
2. **Scan the structure quickly** so the layout is fresh in mind: cover page with `GO VOCAL × {COMPETITOR}` label, title, italic subtitle, then "Why this note" → numbers band → five USPs (each: dark-purple number cell + lilac title strip, "The opportunity" in cherry, "What we offer" in cherry, bulleted features) → "The bottom line".
3. **Spreadsheet layout:** Overview tab with legend + six-tab map + cherry italic honesty note; then six product tabs with purple header row, lilac category strips, green/yellow/red status fills, alternating row shade.
4. **Do not invent new layouts.** The generator scripts in `scripts/` reproduce this layout from the brand tokens in `references/brand_tokens.md`. If a briefing JSON doesn't fit the layout, adjust the content — never the layout.

## If the generated output doesn't match

If the newly generated `.docx` or `.xlsx` doesn't visually match these references (fonts, colours, spacing, table widths, number band formatting), that's a regression in the generator scripts or a brand-token mismatch. Fix the scripts or tokens — don't post-edit the generated file by hand, because the next run will undo your edit.

## Content vs layout

These references are the **visual ground truth**. The **content** (which USPs get which opportunity paragraph, which rows appear in the spreadsheet) is competitor-specific and comes from the briefing JSON. See `assets/example_briefing_decidim.json` for the content that produced the EN references.
