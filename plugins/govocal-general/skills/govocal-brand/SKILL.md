---
name: govocal-brand
description: "Apply Go Vocal brand guidelines to any output. ALWAYS trigger this skill when:  - Creating or editing presentations, slide decks, pitch decks, or any storytelling artifact  - Producing docs, reports, memos, or written documents (Word, PDF, Notion) - Asked to do anything product marketing related (social media assets, logos, illustrations, icons, images/photos)  - Working on anything that will be shared externally or with clients - Creating or editing ANY Figma prototype, mockup, wireframe, or screen design - User says 'build in Figma', 'create a prototype', 'mock this up', 'design a screen', 'vibecoding', or similar"
---

# GoVocal Brand Guidelines

This skill governs how Claude applies Go Vocal's brand when producing any visual or document output.

---

## Two Paths: Documents vs. Design Tasks

### Path 1 — Written Documents (Claude builds it directly)

Use this path for:
- Written documents: reports, memos, proposals, one-pagers (`.docx`, `.pdf`)
- Any structured text content artifact

**Apply the typography and text color tokens below.** Claude builds these directly using the docx or pdf skills.

### Path 2 — Design Tasks (route to Google Slides)

Use this path for:
- **Presentations and slide decks** (`.pptx` or google slides_
- **Notion documents**
- Logos or brand visuals
- Illustrations or icons
- Anything involving images or photos

**Ask whether to build directly or use Notion, or Google Drive MCP connector instead **

### Path 3 — Figma Prototypes & Mockups (use Figma MCP)

Use this path for:
- Prototypes, wireframes, mockups, or screen designs
- Any request to "build in Figma", "design a screen", "mock this up", or "vibecode"
- UI flows, component explorations, or design specs

**Workflow:**
1. **Search the UI library first** — before creating anything, search the GoVocal design system for existing components:
   - File key: `wDuMbaS2c9Tollii7Kdtja` (🖌 UI library)
   - Use `search_design_system` with the file key above
   - Import matching components via `importComponentByKeyAsync` — never recreate from scratch
2. **Apply brand tokens** — use the typography and color tokens defined in this skill for any custom elements
3. **Ask which Figma file to work in** — unless the user specifies, ask whether to create a new file or use an existing one
4. **Confirm before writing** — briefly describe what you're about to build and wait for a go-ahead before calling `use_figma`

**Brand tokens to apply in Figma:**
- Primary text color: `#1E155D`
- Secondary/supporting text: `#43369B`
- Accent (links, icons, highlights): `#FF3E52`
- Background lilacs if needed: `#F0EEFA` (lightest) → `#695ACF` (darkest)
- Headings font: Chivo (fall back to Inter if unavailable)
- Body font: Libre Franklin (fall back to Inter if unavailable)

---

## Brand Tokens — Written Documents

### Typography

| Role | Font | Weight | Size |
|---|---|---|---|
| H1 | Chivo | Thin (100) | 40px |
| H2 | Chivo | ExtraLight (200) | 36px |
| H3 | Chivo | ExtraLight (200) | 36px |
| Intro text | Libre Franklin | Light (300) | 18px |
| Main / body text | Libre Franklin | Regular (400) | 16px |

> **Note on fonts**:
> - **Chivo** (headings) and **Libre Franklin** (all body text, including intro/lead paragraphs) are both Google Fonts.
> - Note to the user that both fonts must be installed on their machine for correct rendering in Word/PDF.
> - If Libre Franklin is unavailable, fall back to Inter or the system default sans-serif.
> - **Body text is always Libre Franklin** — never use Chivo for running body copy.

### Text Colors

| Name | Hex | Use |
|---|---|---|
| Dark purple | `#1E155D` | Primary text: all headings and body copy |
| Medium dark purple | `#43369B` | Secondary text: subheadings, captions, supporting copy |
| Cherry | `#FF3E52` | Icons, hyperlinks, and inline highlights only — never for running text |

### Color Reference (for awareness — applied in Canva for design tasks)

These colors exist in the palette and may be referenced by the user, but Claude does **not** apply them as backgrounds or layout fills in written documents:

| Name | Hex |
|---|---|
| Lilac 1 — ultra light | `#F0EEFA` |
| Lilac 2 — light | `#E1DEF5` |
| Lilac 3 | `#C3BDEC` |
| Lilac 4 — medium | `#968BDD` |
| Lilac 5 — medium dark | `#695ACF` |

### Text Color Application Rules

- **All headings (H1–H3)**: `#1E155D` (Dark purple)
- **Body and intro text**: `#1E155D` (Dark purple)
- **Subheadings / secondary hierarchy**: `#43369B` (Medium dark purple)
- **Links and icons**: `#FF3E52` (Cherry) only
- **Avoid**: Applying Lilac colors to text or backgrounds in written documents — those are for Canva design outputs only

---

## Sign-off — Official Letters Only

**Scope:** This sign-off block applies **only to official letters** authored by Wietse — formal correspondence to clients, partners, public officials, investors, and similar external recipients. Do **not** apply to emails, internal docs, memos, reports, proposals, or one-pagers.

**Format:**

| Line | Content | Font | Weight | Size |
|---|---|---|---|---|
| 1 | `Wietse Van Ransbeeck` | Caveat | Regular (400) | 24px |
| 2 | Role (localized) | Libre Franklin | Regular (400) | 14px |
| 3 | `Go Vocal` | Libre Franklin | Regular (400) | 14px |

**Role line — match the letter's language:**
- English → `Co-founder and CEO`
- French → `Co-fondateur et directeur général`
- Dutch → `Medeoprichter en CEO`

**Color:** All three lines use `#1E155D` (Dark purple).

**Notes:**
- **Caveat** is a Google Font (handwriting style). Note to the user that Caveat must be installed on their machine for correct rendering. Fallback: any handwriting/script system font; do not substitute a regular sans-serif.
- The signature name in Caveat replaces a handwritten signature — render it on its own line, slightly larger than the body, with no bold or italic.
- Keep the sign-off left-aligned, single-spaced, separated from the closing line ("Sincerely," / "Cordialement," / "Met vriendelijke groet,") by one blank line.

---

## Notes for Claude
- Always apply these tokens without being asked — brand consistency is the default, not an option.
- If the I ask for something "quick and rough", still apply brand colors and fonts — just simplify the structure.
- When routing to a third party, briefly explain to the user and ask for go ahead
- Go Vocal is always two words 
- Go Vocal's clients are: "municipalities" 
- Go Vocal's end-users are called: "residents"
