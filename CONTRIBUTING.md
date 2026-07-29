# House rules — gv-claude-plugins

This repo is the **single source of truth** for Go Vocal's shared Claude skills. If a skill improvement isn't in this repo, it doesn't exist.

## The golden rule

**No skill edits outside the repo.** If you improve a skill locally, open a pull request the same day. A better version sitting only on your machine recreates the exact problem this repo was built to fix.

## How to make a change

1. **Make a branch** — never edit `main` directly. On github.com: open the file → pencil icon → GitHub will offer to create a branch when you commit. In Claude Code: just ask Claude to branch, edit, and open the PR for you.
2. **Edit the skill** — change the `SKILL.md` (and supporting files) inside the right plugin folder under `plugins/`.
3. **Open a pull request** — describe in one or two sentences *what* you changed and *why*.
4. **Someone else merges** — don't merge your own PR. Ellen (or another maintainer) reviews and clicks "Merge pull request".
5. **Done** — the corporate Cowork marketplace auto-syncs on merge. On your own Max account, pull the update with `/plugin marketplace update`.

## Versioning

We deliberately do **not** set a `version` field in `plugin.json`. Claude then uses the git commit as the version, so **every merged PR is automatically a new release** — nothing to bump, nothing to forget.

## Naming rules

- Plugin and skill folder names: **lowercase-with-hyphens** (`project-setup`, not `Project Setup`). Syncs fail otherwise.
- One skill = one folder under `skills/` with a `SKILL.md` inside.

## Adding a whole new plugin

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` (copy from `vibe-coding` and adjust name/description).
2. Add its skills under `plugins/<plugin-name>/skills/`.
3. Register it in `.claude-plugin/marketplace.json` — add an entry with `"source": "./plugins/<plugin-name>"`.
4. PR as usual.

## What does NOT belong here

Apps, artifacts, prototypes, client code. Plugins and skills only. Mixed content makes every merge trigger a sync and one bad file can knock out plugins for the whole team.
