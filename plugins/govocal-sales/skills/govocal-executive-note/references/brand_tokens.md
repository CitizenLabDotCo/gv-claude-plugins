# Go Vocal brand tokens

Everything the generator scripts need. Don't improvise new colours or fonts.

## Colours

| Token | Hex | Use |
|---|---|---|
| `DARK_PURPLE` | `#1E155D` | Body text, headings, number cells, spreadsheet table headers |
| `MEDIUM_PURPLE` | `#43369B` | Secondary text, subtitles, italic notes |
| `CHERRY` | `#FF3E52` | "The opportunity" / "What we offer" labels, honesty notes, accents. Use sparingly. |
| `LILAC_1` | `#F0EEFA` | USP title background, spreadsheet category row background |
| `LILAC_2` | `#E1DEF5` | Darker lilac for secondary accents |
| `WHITE` | `#FFFFFF` | Number cell text on dark purple |
| `ALT_ROW` | `#FAFAFA` | Alternating row shading in spreadsheet |
| `GREEN_FILL` | `#C8E6C9` | 🟢 status cell background |
| `YELLOW_FILL` | `#FFF3B0` | 🟡 status cell background |
| `RED_FILL` | `#F5C6CB` | 🔴 status cell background |

## Typography

- **Font family:** Chivo (all weights). Fallback to system sans-serif if unavailable.
- **Body:** 11pt, dark purple.
- **USP title:** 20pt, dark purple, on lilac background.
- **USP number:** 32pt bold, white, on dark purple background.
- **Section heading:** 22pt, dark purple.
- **Cover title:** 46pt, dark purple, line-height 1.05.
- **Cover subtitle:** 13pt italic, medium purple, line-height 1.4.
- **Spreadsheet header row:** 10pt bold white on dark purple, 32pt row height.
- **Spreadsheet body:** 9pt, dark purple, wrapped.
- **Spreadsheet category row:** 10pt bold dark purple on lilac.
- **Status emoji cells:** 14pt bold, centred.

## Emoji status legend

Always use these exact glyphs so the spreadsheet colour fills line up:
- 🟢 = fully supported natively, production-grade
- 🟡 = partially supported OR on the near-term roadmap OR unverified
- 🔴 = not supported today; typically requires external tools or custom work

## Sizing

A4 page, 2.2 cm margins. Columns in the spreadsheet: `#` 6, `Requirement` 40, status cols 8 each, detail cols 50 each.
