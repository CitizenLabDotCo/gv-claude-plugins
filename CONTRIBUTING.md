# House rules — gv-claude-plugins

This repo is the **single source of truth** for Go Vocal's shared Claude skills. If a skill improvement isn't in this repo, it doesn't exist.

## The golden rule

**No skill edits outside the repo.** If you improve a skill locally, push it here the same day. A better version sitting only on your machine recreates the exact problem this repo was built to fix.

## How to make a change

**Push directly to `main` — no review needed.** In Claude Code, just say:

> "Push my updated project-setup skill to gv-claude-plugins."

Claude Code handles the rest (commit, message, push). Or on github.com: open the file → pencil icon → edit → Commit changes (directly to `main`).

Rules of thumb:

1. **Write a clear commit message** — one line saying *what* changed and *why*. This is our change log; future-you will thank you. (When Claude Code writes it for you, glance at it before confirming.)
2. **Validate before pushing** if you touched more than one file or edited `marketplace.json`: ask Claude Code to run `claude plugin validate` on the plugin. A broken file can knock the plugins offline for the whole team until fixed.
3. **Big or risky change?** Use a quick self-merged PR instead (branch → PR → merge it yourself, no reviewer needed). This reliably triggers the corporate marketplace sync and gives teammates a chance to see what changed.
4. **After pushing**: your teammates get it with `/plugin marketplace update`. The corporate Cowork marketplace syncs automatically; if a direct push doesn't show up there, click "Update" on the marketplace in Organization settings → Plugins.

## Versioning & rollback

Every push is a permanent, dated snapshot — that's our versioning. To see or undo history: open any file on github.com → **History** → pick a version → **Revert** (or ask Claude Code to revert a commit).

We deliberately do **not** set a `version` field in `plugin.json`. Claude uses the git commit as the version, so **every push is automatically a new release** — nothing to bump, nothing to forget.

## Naming rules

- Plugin and skill folder names: **lowercase-with-hyphens** (`project-setup`, not `Project Setup`). Syncs fail otherwise.
- One skill = one folder under `skills/` with a `SKILL.md` inside.

## Adding a whole new plugin

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` (copy from `vibe-coding` and adjust name/description).
2. Add its skills under `plugins/<plugin-name>/skills/`.
3. Register it in `.claude-plugin/marketplace.json` — add an entry with `"source": "./plugins/<plugin-name>"`.
4. Validate, then push.

## What does NOT belong here

Apps, artifacts, prototypes, client code. Plugins and skills only. Every push can trigger a sync, and one bad file can knock out plugins for the whole team.
