# gv-claude-plugins

Go Vocal's internal plugin marketplace — the **single source of truth** for shared Claude skills.

## How it works

One repo, two distribution channels:

1. **Corporate account** (non-technical users): this repo is connected as a GitHub-synced plugin marketplace in Claude's Organization settings and syncs automatically. Users install via **Browse plugins** in Cowork — they never touch GitHub.
2. **Individual Max accounts** (vibe coders): connect the repo directly in Claude Code with `/plugin marketplace add CitizenLabDotCo/gv-claude-plugins`, install the plugins you want, and pull updates with `/plugin marketplace update`.

## Repo structure

```
.claude-plugin/
└── marketplace.json          ← the catalog: lists every plugin below
plugins/
├── govocal-coding/           ← one folder per plugin
│   ├── .claude-plugin/
│   │   └── plugin.json       ← plugin metadata
│   └── skills/
│       └── govocal-ui/
│           └── SKILL.md      ← one folder per skill
├── govocal-paas/
├── govocal-sales/
├── govocal-gs/
└── govocal-general/
CONTRIBUTING.md               ← house rules — read before editing
```

## The plugins

| Plugin | For | Skills |
|---|---|---|
| **govocal-coding** | Vibe coders building prototypes | govocal-ui, govocal-a11y, govocal-persona-critique, govocal-translate, participation-design, project-setup |
| **govocal-paas** | Participation-as-a-service delivery | govocal-metabase, project-library-finder, govocal-project-intake, govocal-project-setup, content-plan, strategic-project-planning |
| **govocal-sales** | Sales & bid teams | tender-review, govocal-executive-note, competitor-battlecard, intent-signals-radar |
| **govocal-gs** | Government Success | govocal-account-plan |
| **govocal-general** | Everyone | govocal-brand, product-expert |

> `vibe-coding` was renamed to `govocal-coding` (July 2026). If you had it installed, remove it and install `govocal-coding` instead.

## House rules (short version)

- **No skill edits outside this repo** — see [CONTRIBUTING.md](CONTRIBUTING.md).
- Push directly to `main` with a clear commit message — git history is our versioning, no review needed.
- Validate before pushing if you touched `marketplace.json` or multiple files.
- Names: lowercase-with-hyphens only.
- Plugins and skills only — no apps or artifacts.

Maintainers: Wietse, Jeroen, Irene, Rob · Owner: Ellen
