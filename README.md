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
└── vibe-coding/              ← one folder per plugin
    ├── .claude-plugin/
    │   └── plugin.json       ← plugin metadata
    └── skills/
        └── project-setup/
            └── SKILL.md      ← one folder per skill
CONTRIBUTING.md               ← house rules — read before editing
```

## House rules (short version)

- **No skill edits outside this repo** — see [CONTRIBUTING.md](CONTRIBUTING.md).
- Push directly to `main` with a clear commit message — git history is our versioning, no review needed.
- Validate before pushing if you touched `marketplace.json` or multiple files.
- Names: lowercase-with-hyphens only.
- Plugins and skills only — no apps or artifacts.

Maintainers: Wietse, Jeroen, Irene, Rob · Owner: Ellen
