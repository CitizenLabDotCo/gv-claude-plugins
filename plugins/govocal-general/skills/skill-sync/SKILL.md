---
name: skill-sync
description: Use when a locally edited skill needs pushing to a Go Vocal plugin repo, when checking whether local skill copies have drifted from the repos, or when pulling repo updates down — e.g. "push my updated X skill", "sync my skills", "skill drift check", "update my plugins".
---

# skill-sync

## Overview

The plugin repos are the **single source of truth** for shared skills (see each repo's CONTRIBUTING.md). Local edits must flow back the same day; installed plugins pull updates down. This skill is the sync procedure in both directions. Personal skills (not tracked in any repo) are out of scope — leave them local.

## The repos

Run `claude plugin marketplace list` to see which marketplaces this machine has. The org-wide one is `CitizenLabDotCo/gv-claude-plugins` (plugins: govocal-coding, govocal-paas, govocal-sales, govocal-gs, govocal-general). Restricted marketplaces may also be configured — treat them identically.

## Local skill stores — search ALL of them

A skill often exists in several places. Known stores:

| Store | Path | Notes |
|---|---|---|
| Claude Code personal | `~/.claude/skills/` | Entries may be **symlinks** into project folders (e.g. `~/Claude/GV-Prototypes/skills/`) — resolve with `ls -la` and treat the target as the real file |
| Project skill folders | e.g. `~/Claude/*/skills/` | Git repos or exports; may be stale mirrors |
| Claude desktop app | `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills/` | On-disk mirror of claude.ai skills; **can lag the cloud copy** — check mtimes and say so if stale |
| Installed plugins | `~/.claude/plugins/cache/`, `~/.claude/plugins/marketplaces/` | **Never edit these** — overwritten on every update; they are the repo's copy, not the user's |

**Authoritative copy = the one the user actually edited.** Newest mtime is a hint, not proof — if two non-identical copies exist outside the plugin cache, ask the user which edit is the real one before pushing anything.

## Push (local → repo)

1. Find every local copy of the skill across the stores above; resolve symlinks.
2. Find the target: locate the skill's folder in the marketplace clone(s) under `~/.claude/plugins/marketplaces/` — that tells you repo + plugin.
3. Clone or pull the repo into a scratch directory. `diff -r` the local copy against the repo copy.
4. **Empty diff → stop and report.** Nothing to push; the edit may only exist in the claude.ai cloud store (not visible on disk) or may already be pushed. Never create an empty or no-op commit.
5. Scan the changed files for secrets and personal data before committing — if the repo ships `scripts/confidentiality_scan.py`, run it on your range (`python3 scripts/confidentiality_scan.py --range origin/main..HEAD <plugin path>`) and resolve findings first.
6. Copy the changes in, run `claude plugin validate .` at the repo root, commit with a one-line "what + why" message, push to `main`.
7. Remind the user: teammates receive it via `claude plugin marketplace update`.

## Pull (repo → local)

1. `claude plugin marketplace update <marketplace-name>` refreshes all installed plugins. (The govocal-general plugin ships a session-start hook that does this automatically once a week; the manual command forces an immediate refresh.)
2. If a duplicate of a repo-managed skill still exists in `~/.claude/skills/`, a project folder, or the desktop store, flag it: it will drift. Recommend deleting the duplicate (with the user's OK) so the installed plugin is the only copy.

## Drift check (both directions)

For every skill in every configured marketplace repo: diff repo HEAD against each local copy found. Report a table — skill | status (in sync / local newer / repo newer / local-only / repo-only) | paths. **Never auto-push from a drift check**; report and let the user decide per skill.

## Rules

- Repo is the source of truth. Same-day pushback of local improvements.
- Personal skills stay local — do not push skills that aren't already tracked in a repo without the user explicitly asking.
- Never edit the plugin cache or marketplace clones.
- Empty diff = no commit. Ambiguous authoritative copy = ask, don't guess.
