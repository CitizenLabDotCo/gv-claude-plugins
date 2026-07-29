---
name: govocal-ui
description: Source-grounded GoVocal UI components for prototypes — real design tokens + copy-paste static-HTML primitives transcribed from the @citizenlab/cl2-component-library, plus a per-city ?theme= colour switcher. Consult when building or restyling any prototype so it matches the actual product, and use the tenant colour variables (never hardcode brand colours).
---

# GoVocal UI (source-grounded components)

The **fidelity layer**: tokens and components transcribed from the real product
code, so prototypes look like GoVocal — not an approximation. This skill is the
*exact how* (tokens + components); for generic design craft (typography, palette,
layout direction) pair it with `skills/frontend-design/`.

For the **product model** behind the UI — what a Project/Phase/Input/participation
method is, the exact terminology, roles, and asset specs (image dimensions, etc.) —
read **`GOVOCAL.md`** (repo root), the internal product-context brief + living
project brain. Match its vocabulary when labelling components.

## Source & provenance

- Repo: `CitizenLabDotCo/citizenlab` (public). Pinned at commit **`5d67730`**.
- Path: `front/app/component-library/` (published on npm as
  `@citizenlab/cl2-component-library`). React + styled-components + TypeScript.
- Tokens come from `utils/styleUtils.ts`; each component from `components/<Name>/`.
- **Licence:** CitizenLab Commercial License v2 — no production/self-hosting use.
  We reproduce *appearance* for design prototypes; we do **not** copy their `.tsx`
  source into anything we publish. Keep that boundary.

## What's here

| File | What it is |
|---|---|
| `govocal-tokens.css` | Design tokens as CSS custom properties (`--gv-*`): full palette, type scale, radius (3px), shadows, focus, tenant colours. |
| `govocal-primitives.css` | **Shared atoms** (`.gv-btn`, `.gv-input`, `.gv-checkbox`, `.gv-badge`, `.gv-modal`, … + `.gv-sr-only`/`.gv-panel`/`.gv-wrap` utilities). Used by BOTH surfaces. Edit an atom HERE. |
| `govocal-ui.css` | **Front-office components** (header/nav, footer, card, hero, phase timeline, homepage + project-page blocks). `@import`s `govocal-primitives.css`, so linking `govocal-ui.css` pulls the atoms automatically. |
| `govocal-bo.css` | **Back-office** chrome (`.gv-bo-*`): app shell, sidebar, top-bar, tabs. The `.gv-bo` scope remaps `--gv-tenant-*` → GoVocal's fixed teal/navy BO palette, so the same primitives render in back-office colours. See `govocal-exports/BACK-OFFICE.md`. |
| `govocal-survey.css` + `govocal-survey.js` | The **survey field kit**: every input-form question type (rating, ranking, linear/sentiment scale, image-select, matrix, map, file/shapefile, …) + the page-by-page runner. `GVSurvey.field({type,…})` renders one widget; `GVSurvey.mount(el, FORM)` renders a whole survey. Built on the gv-* primitives; themeable. Demo: `components/survey-fields/`; used by the Input Form page. |
| `govocal-themes.js` | `?theme=` per-city colour + **font** switcher + on-screen picker + per-city logos. |
| `govocal-icons.js` | The real **GoVocal icon set** (curated subset transcribed verbatim from the repo + the admin sidebar glyphs + the live account menu; `GVIcons.names` is the live list — grows as we transcribe more, so don't hardcode a count). Drop in, then `<span data-gv-icon="vote-up"></span>` → inline `<svg class="gv-icon">` that inherits text colour + size. |
| `govocal-logo.svg` | The real **go·vocal** wordmark (footer “powered by” attribution). Muted grey; use as `<img>`. |
| `../../registry.json` | **The recall index (generated).** One lean entry per component + page: `kind` (snippet/widget) · `surfaces` · `category` · `status` · `file`. Scan this to pick — don't read the registries wholesale. |
| `../../registry/<name>.md` | **Per-component file (generated, on-demand).** Rendered canonical markup + props + classes + usage. Open only the one you need. |
| `../../tokens.json` | Machine-readable tokens (DTCG `$value`/`$type`/`{alias}`) + `../../tokens.allowlist.json` (legal `--gv-*` names; powers `npm run lint:prototype`). |
| `gallery.html` | Live demo of every primitive in every state, across all city themes. Open it to eyeball fidelity. |

## Library tiers — Primitives → Components → Pages (HARDWIRED)

The design system is a **normal, hardwired component system**, layered, with one
source of truth per layer and the review site showing a tab per tier:

1. **Primitives** (`/primitives/`, the `gallery.html`) — tokens (colour, type, shadow,
   radius, focus) and base `.gv-*` primitives (button, input, badge, card…). The atoms.
   Defined in `govocal-tokens.css` (token values) + `govocal-primitives.css` (the `.gv-*` atoms).
2. **Components** (`/components/`) — composed, section-level blocks assembled from
   primitives: **header/nav, footer, project-card + rail, hero, modal + login, phase
   timeline, survey fields, and the back-office app-shell + sidebar**. Each
   `components/<name>/` is a demo that **uses** `.gv-*` classes — it must not redefine
   them. Recall index: [`registry.json`](../../registry.json) → [`registry/<name>.md`](../../registry/).
3. **Pages** (`/pages/`) — whole screens built from components "dragged in". A page is
   **layout + content only**; it uses component/primitive classes, defines none, and
   authors no colour/border/shadow/type of its own. Source in `pages/<name>/`.

**The invariant (enforced by `npm run lint`):** primitives → components → pages are
linked in real time — every demo references the canonical assets via
`../../skills/govocal-ui/<asset>`; **no tier copies assets, redefines `.gv-*`, or
hardcodes visual values.** Fix a primitive and every component and page changes with
it, because nothing downstream holds a private copy or its own definition. If a
component needs a change that belongs to a primitive, **edit the primitive** (then
`npm run verify:all` — the ratchet confirms you improved it without regressing other
consumers). **Only deliberately FORKED prototypes are exempt** — the default is to LINK the
canonical assets (`../../../skills/govocal-ui/...`); a fork copies them and may
break, on purpose. `build.js` ships the canonical assets once to `dist/skills/govocal-ui/` so the
same relative path resolves on the live site.

**Recall flow when building a prototype (READ THIS FIRST):** you don't need every
component in context. The loop is: **scan `registry.json`** (lean — kind · surfaces ·
category · status) → **open just `registry/<name>.md`** for that one component's rendered
canonical markup + props → build → **`npm run lint:prototype -- <dir>`** (the full strict
conformance audit, `scripts/lint-strict.mjs`: hardcoded hexes vs tokens, inline presentation
styles, fake `.gv-*` classes, + advisory raw-px spacing). Heed `status: review` + `useInstead` (they
steer you off known traps, e.g. `voting` → `approval-voting`). Prototypes can pull from
any tier — a token, a component, or a whole page. Everything in the recall layer is
GENERATED (`npm run registry`) from the `GV`/`GVWidgets` registries, so it never drifts.

## Locked components (the Figma model) — pages compose INSTANCES, not copies

"Dragged in" (tier 3 above) has a **precise mechanism**, and it's the difference between
a page that tracks its components and one that silently drifts. Think Figma: an **instance**
is locked to its master; you **detach** it to edit freely.

- **Place a locked instance** — drop an empty host, the master fills it on load:
  ```html
  <div data-gv-instance="hero" data-gv-props='{"outTitle":"…","outLead":"…"}'></div>
  ```
  `GV.mountAll()` runs on `DOMContentLoaded` (and immediately for deferred scripts): for every
  `[data-gv-instance]:not([data-gv-detached])` it renders the master (`GV.render(name, props)`),
  then **stamps `data-gv-rendered` + `data-gv-hash`** on the host. Props are JSON in
  `data-gv-props` (single-quote the attribute so the JSON keeps its double quotes).
- **The review overlay on the live site (`Shift+C`) reads that stamp**: a composite
  inside a `[data-gv-rendered]` host whose live markup still hashes to the stamp → **LINKED**;
  the same markup hand-authored with no such host → **BESPOKE**; a stamped instance whose DOM was
  edited after mount → **MODIFIED**. Base primitives (rank 1: button, avatar, icon…) are
  hand-written by design and exempt → they read **BASE**, which is fine.
- **Break the link only on request.** `data-gv-detached` opts a host out of mounting →
  overlay shows **DETACHED**. Hand-authoring `.gv-*` markup is also a fork (it just reads
  BESPOKE). **Default to locked instances; fork only when the user explicitly says to break
  the link.**
- **One master per component.** The `GV.register(name)` component in `govocal-instances.js`
  is the single master a reference page links to. ⚠️ `GVWidgets.homepage`/`GVWidgets.project`
  blocks (`govocal-widgets.js`) are the page-**builder's** block set — `GVWidgets.*.mount`
  injects markup but **does NOT stamp provenance**, so a section mounted that way stays
  **BESPOKE**. Some sections currently exist in *both* registries and have drifted (e.g.
  `hero`, `spotlight`); collapse them to one master before locking. To link a reference page,
  use `data-gv-instance` (the `GV` path), not `GVWidgets.mount`.
- **The page-section catalog lives in `GVWidgets`, not only in `GV.register`.**
  `GVWidgets.homepage`/`.project` (in `govocal-widgets.js`) is the authoritative list of the
  sections a page is assembled from — it mirrors the product's homepage/project builder. Most
  sections already exist there as widgets, so **before concluding a section has "no master,"
  check the generated _Page-section catalog_ table in [`INSTANCES.md`](INSTANCES.md)**: it maps
  each widget (e.g. `areas` = "In your area", `finished-or-archived` = "Finished projects") to
  its GV master if one exists (✓ = lockable now) or flags it GVWidgets-only (— = still BESPOKE).
  **Locking** such a section = giving its widget a GV master that mirrors the GVWidgets block
  (same name → they merge under one registry entry, like `spotlight`), then hosting it with
  `data-gv-instance` — *not* inventing a new component.

So: a canonical page should be **empty hosts + props**, not typed `.gv-*` blocks. Hand-authored
canonical-class markup is a deliberate fork, not the default.

## When to use

Consult this skill when **building or restyling any prototype — always** (see
CLAUDE.md, "Building a prototype" and the skills table): prototypes should match
GoVocal's **real** look by default. Pair it with `skills/frontend-design/` for
generic design craft.

## How to use it in a prototype

> **Data-driven pages from one object — see [`MODEL.md`](MODEL.md).** A single model
> object (`{ blocks: [{type, data}] }`) drives a whole surface: `GVWidgets.project.mount(el, model)`
> renders a resident project page and `GVWidgets.homepage.mount(el, model)` a homepage, both
> with **no editor required**. The content builder, when present, edits a canvas that snapshots
> back into the same object — so editor and hand-authored model are interchangeable.

**Link the repo's assets — don't copy (unless forking).** Reference the design system
via the relative path so your prototype tracks the DS and themes correctly. From
`<opportunity>/prototypes/<name>/`, three `../` reach the repo root
(`govocal-ui.css` `@import`s `govocal-primitives.css`, so linking it pulls the atoms
automatically):

```html
<head>
  <link rel="stylesheet" href="../../../skills/govocal-ui/govocal-tokens.css" />
  <link rel="stylesheet" href="../../../skills/govocal-ui/govocal-ui.css" />
  <script src="../../../skills/govocal-ui/govocal-themes.js" defer></script>
  <script src="../../../skills/govocal-ui/govocal-instances.js" defer></script>
  <script src="../../../skills/govocal-ui/govocal-icons.js" defer></script>   <!-- if using icons -->
</head>
<body class="gv-root">
  …
  <span data-gv-icon="vote-up"></span>             <!-- decorative; auto aria-hidden -->
  <button class="gv-iconbtn" aria-label="Search"><span data-gv-icon="search"></span></button>
</body>
```

(Add `govocal-icons.js` only if you use icons; `govocal-cookies.js` on resident-facing
prototypes — see the cookie rule. The deploy repoints the relative path to
`dist/.../skills/`.) **Copy assets into the prototype folder only when you deliberately
fork** and need to diverge from the DS — then it stops tracking it.
`scripts/link-prototypes.mjs` (`npm run link-prototypes`) converts old copied assets
back to links.

Then build markup from `registry/<name>.md` (rendered canonical markup, per component).
**Use the tokens for every colour** —
especially the three city-configurable ones:

- `var(--gv-tenant-primary)` — the city's main brand colour (buttons, links, focus)
- `var(--gv-tenant-secondary)` — secondary brand colour
- `var(--gv-tenant-text)` — body text colour

Never hardcode a hex for brand colour; that's what breaks city theming.

> **THEMING CONTRACT (don't break this).** Per-city theming is EXACTLY four
> variables — `--gv-tenant-primary` / `-secondary` / `-text` + `--gv-font-family` —
> common to every component, and the only things `?theme=` / `govocal-themes.js`
> swap per city (tints/focus/states derive via `color-mix`). Therefore:
> 1. Components reference `var(--gv-tenant-*)` / `var(--gv-font-family)`, never a literal city hex.
> 2. **Never invent a new per-city token** (e.g. a frozen city green). If a value varies by
>    city it must BE one of the four; if it's the same across cities it's SYSTEM — use the
>    shared palette (`--gv-green-*`, `--gv-success`, greys, radii, type), which `?theme=` never touches.
> 3. A city hex may appear only in a source comment or a `govocal-themes.js` theme definition.
>
> The canonical statement lives at the top of the tenant block in `govocal-tokens.css`.

## City theming — `?theme=`

Each GoVocal city configures primary/secondary/text. The switcher lets you preview
a prototype across several city palettes:

- `?theme=0` GoVocal (default) · `1` Københavns Kommune · `2` Stadt Wien · `3` Engaged California
- Live picker renders bottom-right (swatches); it also rewrites the URL so a view
  is shareable. Disable with `<body data-gv-theme-picker="off">`.
- Templates are **real city tenants** (researched from each one's official brand):
  `1` Københavns Kommune (`#000C2E`), `2` Stadt Wien (`#FF1D2B`), `3` Engaged
  California (`#1C2745` + `#E79450`), plus `0` GoVocal default. Add one by appending
  `{id, name, primary, secondary, text, logo, font}` to `GV_THEMES`.
- **City logos:** a theme's `logo` (inline `<svg>` or `<img>`) renders into any
  `[data-gv-logo]` slot and swaps with the theme; a placeholder is generated until a
  real logo is set. Put `<a data-gv-logo>` in a header.
- **City fonts:** a theme's `font` drives `var(--gv-font-family)` (real tenant font
  name first, then a free stand-in; proprietary fonts fall back to Public Sans like
  the live sites). Build text with `font-family: var(--gv-font-family)`.
- **Faithful-but-flagged:** real brand colours are kept even when under AA — Stadt Wien's
  in-product `#FF1D2B` (near-pure Wien-Rot) is ~3.8:1 white-on-primary and the audit flags
  it (expected, accepted).

## Accessibility — WCAG 2.2 is a hardwired contract (read with `skills/govocal-a11y/`)

Accessibility is enforced like the spacing grid, not left to review. `npm run lint`
**INV-11** fails the build on the three regressions a system can prevent structurally
(tenant-coloured focus ring · literal `#fff` on a tenant fill · focus rule that drops
its indicator). The token + primitive rules below make the rest correct by construction.

- **Focus is a NEUTRAL system concern, never a skin.** The ring is a two-tone token
  set — a 2px near-black ring (`--gv-focus-outline`) offset out, plus a white halo
  (`--gv-focus-halo`) in the gap — so it clears 3:1 (1.4.11 / 2.4.13) against *any*
  background, brand or neutral. On dark surfaces (the BO navy sidebar) the scope flips
  `--gv-focus-color` to white. **Never** point a focus ring at `var(--gv-tenant-*)`
  (INV-11a) and **never** `outline:none` on `:focus` without a box-shadow replacement
  (INV-11c). Was a brand-coloured ring — it failed 3:1 on brand fills.
- **On-color, not `#fff`.** A control that fills with `var(--gv-tenant-primary|secondary)`
  sets `color: var(--gv-on-primary|secondary)` — never a literal white (INV-11b). The
  on-color token is white by default and flips to black/white by live contrast via
  `contrast-color()` where supported (Baseline 2026), so an arbitrary *light* city brand
  still yields a legible label (1.4.3). Under `.gv-bo` the on-color tokens are re-pinned
  to the fixed BO palette, so they don't compute against the wrong (city) colour.
- **Target size ≥ 24px (2.5.8 AA).** `--gv-target-min: 24px`; `.gv-btn` carries it as a
  floor, the checkbox box is 24px, the modal close 40px. Any **new** icon-only / standalone
  interactive control must reach a 24px hit area (pad it even if the glyph is smaller).
  44px is AAA/touch, not the AA bar.
- **Focus not obscured (2.4.11 AA).** Sticky chrome sets `--gv-scroll-offset` via `:has()`
  (FO header, BO content-builder topbar), feeding `scroll-padding-top`, so a keyboard-focused
  field is never hidden behind a sticky bar on scroll. New sticky chrome must do the same.
- **Don't signal by colour alone (1.4.1 A).** Checked checkboxes/toggles are **success
  green** + a check glyph (state isn't the brand hue alone); status pills carry text +
  icon. Any new state must pair colour with text/icon/shape.
- **Dragging alternative (2.5.7 AA).** Reorder / range / map-pin / voting controls must
  ship a non-drag path (buttons, numeric input, "move to" menu) — bake it into the API.
- **Don't block paste/autofill (3.3.8 AA)** on credential fields; set `autocomplete`.
- **Contrast of the default theme:** deep teal `#0E7C86` primary (4.95:1 white-on-primary,
  AA) + warm coral `#E2603A` secondary (brand accent — dark/large text if filled, ~3.5:1).
  Of the city templates, Copenhagen (1) and Engaged California (3) clear AA; Wien (2,
  `#FF1D2B`) is the flagged ~3.8:1 exception. Run `npm run audit` and report results; with
  the on-color token in place, a light city brand now self-corrects its button labels.

## Building & extending the library

> **Maintainer-only:** this pipeline needs `.env.capture` credentials and the local-only
> `govocal-exports/` captures — neither is distributed. Collaborators build FROM the
> library; extending it against live captures is Rob's workflow.

Everything above is about **consuming** the library in a prototype. This section is
the **contract for growing it** — the source-grounded pipeline that turns a live
GoVocal screen into a verified, reusable primitive/component/page. Follow it
whenever extending the library against the real product; don't eyeball screens into approximate CSS.

This section is the authoritative pipeline. BO build queue + live captures:
`govocal-exports/BACK-OFFICE.md`. The working agreement around the guards (lint /
registry / index): **CLAUDE.md** ("The design-system pipeline"). The `npm` scripts:

| Step | Command | What it does |
|---|---|---|
| **1. Capture** | `npm run capture -- <url> --name <slug> --probe "<real selectors>"` | Logs into the demo platform, dumps `page.png` · `dom.html` · `styles.json` · `meta.json`. `styles.json.digest` = every distinct visual treatment with **exact computed values** (read these, never eyeball the PNG); `--probe` pins selectors into `styles.json.probed` as verify checkpoints. |
| **2. Build** | — | Assemble from existing `.gv-*` primitives; map digest values to `--gv-*` **tokens** (don't hardcode a hex you can alias). New visual? decide *new variant vs base fix* — extend, don't mutate the base out from under existing users. |
| **3. Verify** | `npm run verify -- <built.html> --against <slug> --map "realSel=mineSel|…"` | Renders your build and **numerically diffs** computed styles vs the capture's probed checkpoints. Loop until ✓. Replaces "compare to the screenshot by eye." |
| **4. Register (ratchet)** | add to `govocal-exports/checkpoints.json`, then `npm run verify:all` | Once verified, pin the checkpoint. After a shared-CSS change run `verify:all` to see the blast radius (`--changed .gv-btn` scopes it). **Advisory during discovery** — red = review + re-capture, not a hard stop. |
| **5. Lint** | `npm run lint` | Must pass before you store. Enforces the hardwired layering: no library tier copies an asset, links locally, or redefines a `.gv-*`. |

Then store: register the renderer (`GV.register('<name>', …)` in `govocal-instances.js`,
or a widget block in `govocal-widgets.js`) — that's the single source of markup — and run
`npm run index` (regenerates `registry.json` + `registry/<name>.md` + `tokens.json`, then
`LIBRARY.md`). Put new styles in the right canonical file — shared atoms →
`govocal-primitives.css`, FO → `govocal-ui.css`, BO → `govocal-bo.css`. **Never hand-write
a catalog snippet** — the recall layer is generated from the registry, so it can't drift.

**Why the guards matter:** the layering is hardwired (one source of truth per layer, no
copies — `lint` keeps it that way), and primitives are *meant* to improve as you learn
the real UI. The ratchet (`verify:all`) shows you when a primitive change moved another
checkpoint so you change atoms knowingly. **Pages stay pure assembly** (components dragged
in, no page-authored colour/border/shadow) so primitive gains flow into them automatically.

## Refreshing from source (when GoVocal's design system moves)

1. Find the new commit SHA on `master` and update the pin here + in file headers.
2. Re-pull `front/app/component-library/utils/styleUtils.ts` and diff the token
   values into `govocal-tokens.css`.
3. Re-pull changed `components/<Name>/index.tsx` and reconcile the right canonical
   file (`govocal-primitives.css` for atoms, `govocal-ui.css`/`govocal-bo.css` for components).
4. Linked prototypes and library demos pick the change up automatically; re-copy only
   into deliberately FORKED prototypes that should adopt it.
5. Open `gallery.html`, screenshot it (webapp-testing), and `npm run audit`.

## Scope

v1 covers the focused primitives prototypes actually reach for: Button, Input/
Textarea, Title, Text, Checkbox, Radio, Toggle, Badge, StatusLabel, Spinner, Card,
Divider. The library has ~35 components; extend by transcribing more from source
following the same provenance discipline.
