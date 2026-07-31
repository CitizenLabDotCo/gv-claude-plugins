# Survey design — question types & selection reference

**Read this whenever a drafted recipe contains a `native_survey` phase** (and when an `ideation` form needs richer fields). Its job is to stop the skill **defaulting to short-answer / single-choice**. The survey tool supports a wide palette of question types — pick each one from the *insight you're after* and the *respondent experience*, not from habit.

> **Provenance.** The `input_type` strings below are **confirmed from source** — `CustomField::INPUT_TYPES` in `back/app/models/custom_field.rb` (`master`, read directly from the repo). The full enum is:
> `checkbox, date, file_upload, files, html, html_multiloc, image_files, linear_scale, rating, multiline_text, multiline_text_multiloc, multiselect, multiselect_image, number, page, point, line, polygon, select, select_image, shapefile_upload, text, text_multiloc, topic_ids, cosponsor_ids, ranking, matrix_linear_scale, sentiment_linear_scale`.
> Config field names (e.g. `maximum`, `linear_scale_label_N_multiloc`, `maximum_select_count` / `minimum_select_count`, `random_option_ordering`, `dropdown_layout`, `ask_follow_up`, `min_characters` / `max_characters`, `include_in_printed_form`, `page_layout`, matrix statements) are taken from the same model's schema. Catalogue framing also from the support article "What are the different question types?" and the FormSync FAQ.

---

## Core principle: match the question to the insight

Default-to-text is the most common survey defect. Before writing a question, ask **"what am I trying to learn, and what does the resident have to do to tell me?"** Then pick the lightest question type that captures it cleanly. Diversify types across the form — a varied form holds attention and reduces straight-lining; a wall of identical questions kills completion.

| What you want to learn | Best question type | Why |
|---|---|---|
| Open exploration, the "why", unanticipated ideas | **Long answer** (short answer for a word/phrase) | Free text captures what you didn't think to ask. AI summarisation handles scale. Use sparingly — costly to analyse and to answer. |
| A single decision among known options | **Single choice** | Forces one clear pick; supports "Other", randomised order, dropdown for long lists. |
| All that apply from a set | **Multiple choice** | Captures combinations; randomise to cut order bias. |
| Preference between **visuals** (designs, logos, sites, layouts) | **Image choice** | Residents react to images far better than to text labels. Can cap how many they pick. |
| Agreement / intensity on a statement | **Linear scale** (e.g. 1–5) ✓ | Quantifies strength of opinion; trends and averages out of the box. |
| A quick emotional pulse / how people *feel* | **Sentiment scale** (emoji) ✓ | Low-effort, inclusive, great for low-literacy or quick gut-check; warmer than a number. |
| Quality / satisfaction with something | **Rating** (stars, up to 10) | Intuitive "how good was this" signal. |
| Priorities / trade-offs across items | **Ranking** | Reveals relative priority a scale can't — forces residents to choose what matters *most*. |
| Same set of items judged on the **same dimensions** | **Matrix** (rows × columns) | Compact way to rate many items consistently. ⚠ Least mobile-friendly — keep small. |
| A count, amount, age, € figure | **Number** | Clean numeric data; no free-text cleanup. |
| Evidence: a document, photo, plan | **File upload** (≤50MB, 1 file/question) | When the answer is an artefact, not words. |
| **Where** — a place, route, or zone | **Mapping** (Drop pin / Line / Polygon / Shapefile) | Spatial questions capture geometry; never ask "where?" as free text for a place-based question. |

### Use spatial questions whenever the ask is clearly spatial

If a question is about a **place, a route, or an area**, use the mapping question types — don't fall back to a text box:

- **Drop pin (`point`)** — a specific location ("mark the junction that feels unsafe", "where would you like a bench?").
- **Draw line (`line`)** — a route or path ("draw the cycle route you'd take", "trace the street that needs resurfacing").
- **Draw area / polygon (`polygon`)** — a zone ("outline the area that floods", "shade where the new park should go").

A text answer for a place-based question throws away the geometry and is far harder to act on. Pair a mapping question with `per_pin_followups` when you also need structured attributes per location. (Same map-config / coordinate rule as `references/ideation-views.md`.)

### Don't under-use the rich types

The most common failure is retreating to text and single-choice. **Be confident** reaching for:

- **Matrix (`matrix_linear_scale`)** when several items share one scale (e.g. rate satisfaction with five services on the same 1–5) — just keep it small for mobile.
- **Sentiment scale (`sentiment_linear_scale`)** for an inclusive, low-effort emotional read — great as an opener or a temperature check.
- **Image choice (`select_image` / `multiselect_image`)** whenever the choice is genuinely visual (designs, layouts, logos, street furniture, planting options). People respond to images far better than to text labels.

Use them wherever they fit the insight; the only constraints are mobile load (matrix) and image availability (image choice — see below).

### Image-choice images — flag if you can't produce them

Image-choice questions need a real image per option. The skill drafts the question and the option labels, but the **actual images must exist**. If you cannot generate or source suitable images for the options, **do not silently drop the image-choice question** — keep it, mark the images as needed, and **flag it in the GSM report** ("Things to review") so the admin supplies them before publish. Provide concrete suggestions (search terms, or a note to use the client's own design renders/photos) rather than leaving it blank. Treat this exactly like the imagery fallback rule in §4.

---

## Full catalogue (with config knobs)

All `input_type` values below are the exact strings from `CustomField::INPUT_TYPES`.

**Standard question types**

| Type | `input_type` | Key config (real field names) | Notes |
|---|---|---|---|
| Short answer | `text` | `min_characters` / `max_characters` | one line |
| Long answer | `multiline_text` | `min_characters` / `max_characters`; AI summarisation if enabled | use sparingly |
| Yes/No | `checkbox` | — | boolean toggle |
| Single choice | `select` | options; "Other"; `random_option_ordering`; `dropdown_layout` | one pick |
| Multiple choice | `multiselect` | options; "Other"; `random_option_ordering`; `dropdown_layout`; `select_count_enabled` + `minimum_select_count` / `maximum_select_count` | many picks |
| Single image choice | `select_image` | image options | pick one image |
| Multiple image choice | `multiselect_image` | image options; min/max selections | pick several images |
| Linear scale | `linear_scale` | `maximum` (**2–11**); per-point labels `linear_scale_label_1..11_multiloc`; `ask_follow_up` | agreement/intensity |
| Rating | `rating` | `maximum` (stars, 2–11) | satisfaction/quality |
| Sentiment scale | `sentiment_linear_scale` | scale + labels; `ask_follow_up` | quick feeling (emoji) |
| Matrix | `matrix_linear_scale` | matrix statements (rows) × a shared linear scale | mobile-unfriendly; keep short |
| Ranking | `ranking` | options to rank | priorities/trade-offs |
| Number | `number` | numeric bounds | numeric only |
| Date | `date` | — | date picker |
| File upload | `file_upload` (single) / `files` | one file/question | exports as URL |
| Image upload | `image_files` | image attachments | photos |
| Content / description block | `html_multiloc` | rich text — **collects no answer** | section text, not a question |

**Mapping question types (Map-Based Survey Toolbox)** — each collects **one input per map**; add multiple questions for multiple inputs. Configure each map's centre/zoom and optional GeoJSON/ESRI layers (same coordinate-lookup rule as `references/ideation-views.md`).

| Type | `input_type` | Captures |
|---|---|---|
| Drop pin | `point` | a location |
| Draw route / line | `line` | a path |
| Draw area / polygon | `polygon` | a zone |
| ESRI shapefile upload | `shapefile_upload` | uploaded geometry |

**Structural elements**

| Element | `input_type` | Use |
|---|---|---|
| Page break | `page` | split a long survey into pages/sections; `page_layout: default \| map` (a **map page** anchors mapping questions to one shared map) |

Every question can be **required or optional** (`required`), carries a title/description, and has an `include_in_printed_form` flag (per-question FormSync inclusion). Skip logic / branching is supported on the types whose strategy allows it.

---

## UX & structure rules (apply when drafting a survey)

1. **Diversify deliberately.** Mix open and closed, scales and choices. Don't ship a form of ten short-answer boxes. Variety sustains completion and yields richer data.
2. **Mind mobile.** Many residents answer on a phone. **Matrix** is the least mobile-friendly type — use it rarely and keep rows/columns few; otherwise prefer several linear-scale questions.
3. **Page the survey.** Use page breaks (`page`) to group related questions into short sections; a single long scroll depresses completion. Skip logic / branching can route respondents between sections.
4. **Randomise choice order** on single/multiple/image choice to reduce order bias (ties into the §6 bias checklist).
5. **Demographics = attach user-fields as the last page** (also §6). Don't hand-author demographic questions as survey questions. Instead **attach the platform demographic user-fields** by setting the survey permission's **`user_fields_in_form: true`** — this renders them as the **final page** of the survey, optional, after the substantive questions. Never lead with demographics. (See `references/project-config.md` → Demographic questions.)
6. **Right-size length to the archetype** (§4 form-length defaults). Reaching for breadth (large audience) → fewer, simpler questions; depth (co-design, small group) → richer mix.
7. **Open text earns its place.** One or two well-placed open questions (with AI summarisation) beat many. Each open question is a real analysis cost — justify it.
8. **One insight per question.** Split double-barrelled asks (§6). A matrix is the right tool when you genuinely need the *same* scale across items — not a shortcut to cram unrelated questions together.
9. **Spatial = mapping, not text.** If the answer is a place/route/zone, use a mapping question (and see the spatial guidance in §2b / `references/ideation-views.md`).

---

## Per-question configuration — always set `required` and option order

Two settings must be **deliberately configured on every question** — never left to chance.

### Required vs. optional (`required`)

Decide per question; don't accept the default blindly.

- **Default to optional.** Every required question is a chance for the resident to abandon the survey — keep the form forgiving.
- **Mark `required: true` only for the few questions essential** to the phase's purpose (the decision can't be made without them).
- **Always optional:** demographic questions, sensitive questions, and open-ended/long-text questions (forcing prose drives drop-off).
- State the required/optional split implicitly by setting `required` on each question in the payload — don't leave it unset.

### Option order — randomise by default (`random_option_ordering`)

For questions with **nominal** answer options (`select`, `multiselect`, `select_image`, `multiselect_image`), **set `random_option_ordering: true` by default.** Randomising removes primacy/order bias — residents otherwise over-pick whatever sits at the top.

**Keep a fixed order only when the order carries meaning or aids legibility:**

- **Ordinal / scale-like options** — "Never → Sometimes → Always", "Strongly disagree → Strongly agree", age or income bands. Shuffling these makes them unreadable.
- **Sequential options** — days, months, times, steps.
- **Long alphabetical lists** where residents scan to *find* their answer (e.g. pick your street/neighbourhood) — alphabetical order beats random for findability.
- **`Other` / `None of the above` / `Prefer not to say`** — pin these **last**, never shuffled into the middle (the platform already keeps an "Other" option last).

When you keep a fixed order, set `random_option_ordering: false` and it's worth a one-line note in the report why (e.g. "ordinal scale — fixed order"). Inherently-ordered types (`linear_scale`, `rating`, `ranking`, `matrix_linear_scale`) are scales, not nominal options — randomisation doesn't apply.

---

## Light emoji on answer options

A single leading emoji on a *concrete, iconic* answer option aids scannability and makes a survey feel a little more human — e.g. 🌳 Greenery and trees, 🚲 Separated cycling space, 🚶 Wider walking space, 🪑 A small green seating area, 🗑️ Waste and recycling, 🚚 Delivery and loading.

**Where to use them:** `select` / `multiselect` / `multiselect_image` / `ranking` / `matrix` options and rows, where each option maps cleanly to a recognisable icon.

**Rules:**

- **One emoji per option, leading the label** — never trailing, never more than one.
- **Applied consistently across all options in a question.** Don't emoji half of them; either every option in the question carries one or none do.
- **Skip options that have no obvious icon,** and skip "Other" / opt-out options.
- **Skip scale labels** (`linear_scale` / `sentiment_linear_scale`) and **open-text** questions — they don't take option emojis.
- **Skip entirely for formal / institutional-tone projects.**

This mirrors the light-emoji guidance for project and phase copy (Process Design rule 8): purposeful and sparing, never decorative.

---

## Offline participation (FormSync) compatibility

Paper participation matters (§2b). Not every question type round-trips through FormSync, so factor it in when a survey is meant to reach offline residents:

- **Supported on paper (FormSync 2.0):** short/open text, multiple choice (A/B/C lettering), linear scale & rating, yes/no, image selection, **matrix**, **ranking**, star ratings, demographic questions (printed as the last page). Skip logic prints as instructions.
- **NOT supported on paper:** all **mapping / spatial** questions (print but answers won't upload) and **file / image upload** (excluded from the PDF).

> Drafting consequence: if the intake stresses offline reach, lean on the supported types for the core questions and treat mapping / file-upload as online-only extras. Note this trade-off in the GSM report. Each question also carries an `include_in_printed_form` flag controlling whether it appears on the printed form.

---

## Payload shape (survey questions)

Extend each `native_survey` phase's `form_questions` with the richer types. Field names mirror the `CustomField` model. Generic shape:
```json
{
  "input_type": "text | multiline_text | checkbox | select | multiselect | select_image | multiselect_image | linear_scale | rating | sentiment_linear_scale | matrix_linear_scale | ranking | number | date | file_upload | image_files | html_multiloc | point | line | polygon | shapefile_upload | page",
  "title_multiloc": { "en": "..." },
  "description_multiloc": { "en": "..." },
  "required": false,
  "random_option_ordering": true,
  "dropdown_layout": false,
  "include_in_printed_form": true,
  "config": {
    "options": ["..."],
    "allow_other": false,
    "select_count_enabled": false,
    "minimum_select_count": null,
    "maximum_select_count": null,
    "maximum": 5,
    "linear_scale_labels": { "1": "...", "5": "..." },
    "ask_follow_up": false,
    "matrix_statements": ["..."],
    "min_characters": null,
    "max_characters": null,
    "image_options": [ { "label": "...", "image": "url/description" } ],
    "page_layout": "default",
    "per_pin_followups": ["...for point/line/polygon questions..."]
  },
  "bias_check": "passed | flagged: leading | flagged: double-barreled | ..."
}
```
- Populate only the keys the chosen `input_type` needs. `maximum` (2–11) drives the linear-scale/rating range; `linear_scale_labels` map to `linear_scale_label_N_multiloc`; `matrix_statements` are the matrix rows; `page_layout: map` makes a page a shared map for its mapping questions.
- **Set `required` and `random_option_ordering` on every question** (see "Per-question configuration" above): default `required: false` (mark required only the essential questions; demographics / open-text always optional), and `random_option_ordering: true` for nominal options unless a fixed order aids legibility (ordinal scales, sequential, long alphabetical — and always keep "Other" / opt-out last).
- Run every question through the §6 bias checklist before returning.

---

## GSM report hooks
- **Decisions (§7 #3):** when the form uses a non-trivial type (matrix, ranking, sentiment, mapping, image choice), name it and the insight it serves — shows the GSM the question design was deliberate, not defaulted.
- **Things to review (§7 #4):** flag (a) any **matrix** question for mobile load, (b) **mapping / file-upload** questions if the project wants offline reach (won't FormSync), and (c) **image-choice questions whose images couldn't be generated** — list which questions need images and suggest sources, so the admin supplies them before publish.

## Source
- **`input_type` enum + config fields (authoritative):** `CustomField::INPUT_TYPES` and schema in [`back/app/models/custom_field.rb`](https://github.com/CitizenLabDotCo/citizenlab/blob/master/back/app/models/custom_field.rb) (`master`).
- Catalogue framing: [Notion support — "What are the different question types?"](https://app.notion.com/p/2419663b7b2680658e15d538874a1b82).
- Offline support: [Notion FAQ — "Which question types are supported in FormSync"](https://app.notion.com/p/3419663b7b26813289b5ef276fab4bc0).
