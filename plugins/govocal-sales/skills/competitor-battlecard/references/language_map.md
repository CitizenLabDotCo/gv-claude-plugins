# Language map — competitor HQ / primary market → output language

Use this to pick the `language` field in the briefing JSON. Scripts read that field and localise every heading, label, and legend.

## Supported output languages

The generator scripts ship label dictionaries for these five languages:
- `en` — English (default, international fallback)
- `fr` — French (France, Belgium-FR, Switzerland-FR, Quebec, Luxembourg)
- `nl` — Dutch (Netherlands, Belgium-Flemish)
- `de` — German (Germany, Austria, Switzerland-DE)
- `es` — Spanish (Spain, LatAm)

If a competitor's market doesn't fit any of these, default to English and add a note in `research_notes.md` that translation is needed.

## Mapping

| Competitor HQ / primary market | Output language |
|---|---|
| France | `fr` |
| Belgium (Wallonia, Brussels) | `fr` |
| Belgium (Flanders) | `nl` |
| Netherlands | `nl` |
| Germany, Austria, German-speaking Switzerland | `de` |
| Spain, Latin America | `es` |
| UK, Ireland, US, Canada (English), Australia, NZ | `en` |
| International / unclear | `en` |
| Other (Nordic, CEE, etc.) | `en` with a flag in research_notes.md |

## When to override

The user can override in the intake. Common reasons:
- Competitor HQ'd in one region but the live deal is in another (use the deal's language)
- French competitor but the client is the European Commission (use English)
- Dutch competitor but the client is a Flemish municipality vs a Walloon one

**When in doubt, confirm with the user** before generating. Translating a completed docx is more work than doing it right the first time.

## What each language specifically localises

The label dictionary in `scripts/localisation.py` covers:
- Cover / intro headings: "Why this note", "Go Vocal in numbers", "Where Go Vocal stands out", "The bottom line"
- USP labels: "The opportunity" / "What we offer"
- Spreadsheet headers: `#`, `Requirement`, `Go Vocal`, competitor name (untranslated), `Details`
- Legend: 🟢 "Fully supported", 🟡 "Partially supported", 🔴 "Not supported"
- Tab names: "Engagement Methods", "Back-Office & Workflows", "Analysis & Reporting", "UX & Frontend", "Technical & Infrastructure", "Support & Services"
- Category names inside tabs (e.g. "IDEATION / IDEAS BOX" → "IDÉATION / BOÎTE À IDÉES")
- The honesty note ("Written honestly: where {competitor} does something Go Vocal doesn't yet, we say so")

Body prose inside USP paragraphs — the "opportunity" text, feature descriptions — must be written in the target language by the briefing author. The scripts do not translate free text; they only localise fixed labels.
