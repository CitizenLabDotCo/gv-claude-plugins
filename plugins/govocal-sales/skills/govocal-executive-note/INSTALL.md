# Installing / updating this skill

This package **supersedes `competitor-battlecard`** — it keeps the competitive battlecard behaviour and adds the greenfield city executive note. It can't be hot-edited from a Cowork session, so install it yourself.

## Option A — replace the existing skill (recommended)
The competitive mode here is backward compatible (old Decidim-style briefings still render). Replace the `competitor-battlecard` skill in your plugin/marketplace with this `govocal-executive-note` folder, keeping the same `scripts/` and `assets/reference_examples/`.

## Option B — install side by side
Add `govocal-executive-note` as a new skill and leave `competitor-battlecard` in place. Triggers may overlap on "battlecard" phrasing; if so, narrow the old skill's description or retire it.

## Steps
1. In Claude (desktop) → **Settings → Capabilities**, open the relevant plugin/skill source.
2. Add/replace the skill with this folder (`SKILL.md` at its root).
3. Drop the real imagery into `assets/brand/` and `assets/product/` per `assets/MANIFEST.md`.
4. Ensure **Chivo** and **Libre Franklin** (Google Fonts) are installed on machines that open the `.docx`.

## Smoke test
```bash
pip install python-docx openpyxl --break-system-packages
# greenfield
python scripts/generate_concept_note.py assets/example_briefing_johannesburg.json /tmp/jhb.docx assets
# competitive (note + spreadsheet)
python scripts/generate_concept_note.py assets/example_briefing_decidim.json /tmp/dec.docx assets
python scripts/generate_spreadsheet.py  assets/example_briefing_decidim.json /tmp/dec.xlsx
```

## Trigger
Natural language: **"executive note for [city]"** → greenfield; **"executive note for [city] vs [competitor]"** / **"battlecard for [competitor]"** → competitive.
