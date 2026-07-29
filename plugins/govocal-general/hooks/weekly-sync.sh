#!/usr/bin/env bash
# Weekly auto-sync of the gv-claude-plugins marketplace.
# Ships with the govocal-general plugin: every machine that installs the plugin
# pulls the latest shared skills at most once every 7 days, at session start.
# Always exits 0 — a failed sync must never break a session.

STAMP="$HOME/.claude/.gv-plugins-last-sync"

# Synced within the last 7 days? Nothing to do.
if [ -f "$STAMP" ] && [ -n "$(find "$STAMP" -mtime -7 2>/dev/null)" ]; then
  exit 0
fi

command -v claude >/dev/null 2>&1 || exit 0

if claude plugin marketplace update gv-claude-plugins >/dev/null 2>&1; then
  touch "$STAMP"
  echo "gv-claude-plugins: weekly marketplace sync done — shared skills are up to date."
else
  echo "gv-claude-plugins: weekly marketplace sync failed (offline?); will retry next session."
fi
exit 0
