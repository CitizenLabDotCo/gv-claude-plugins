# Bundled imagery manifest

Imagery lives **inside the skill** (here), not in any user's local files — extracted from a signed-off reference note so every run reuses the same Go Vocal house imagery. The example briefings reference these exact paths (relative to `assets/`).

## Bundled and ready (reused across every city)

### assets/brand/
| File | Used as | Source |
|---|---|---|
| `go_vocal_logo.png` | Cover logo (top-left) | reference note |

### assets/brand/icons/  — the "Go Vocal in numbers" row icons (in order)
| File | Stat |
|---|---|
| `icon1_csat.png` | Customer Satisfaction Score |
| `icon2_countries.png` | Countries we work in |
| `icon3_governments.png` | Governments we have worked with |
| `icon4_peoplepowered.png` | People Powered score |
| `icon5_projects.png` | Projects launched |
| `icon6_admins.png` | Monthly active admins |

### assets/product/  — USP screenshots (map 1:1 to the five USP themes)
| File | USP | What it shows |
|---|---|---|
| `usp1_formsync.png` | 1 (channels in one hub) | FormSync scanning a handwritten paper form |
| `usp2_sensemaking.png` | 2 (reporting / dashboard) | AI Sensemaking summary + Q&A |
| `usp3_dashboard.png` | 3 (cross-dept workflows) | Back-office dashboard / report overview |
| `usp4_map.png` | 4 (multilingual UX) | Map survey with resident pins |

## Per-run / optional (omitted entirely if not provided — no placeholder box)

| Slot | Where | How to fill |
|---|---|---|
| **City logo / seal** | cover, next to the Go Vocal logo | Per city. Drop the city's logo in and set `cover.city_logo.path`. Pair the Go Vocal logo with the city’s own seal/logo. |
| **USP 5 — Best practices & peer network** | USP 5 image | If the reference layout had **no** image for a USP, leave it out. Pull the **Inspiration Hub** figure from the product doc (V12) and drop it in, e.g. `product/usp5_inspiration_hub.png`. Flagged for validation. |

## Regenerate after changing assets
```bash
python scripts/generate_concept_note.py assets/example_briefing_johannesburg.json out.docx assets
```
