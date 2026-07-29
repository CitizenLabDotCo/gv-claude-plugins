#!/usr/bin/env python3
"""Confidentiality scanner for the gv-claude-plugins management plugin.

Flags content that should not land in the repo: credentials, embedded
financial figures, client-health data, and meeting/CRM deep links. Runs in CI
on every push (added lines only, so existing content is grandfathered) and
locally before adding a new skill.

Usage:
  python3 scripts/confidentiality_scan.py --range <before_sha>..<after_sha> [path ...]
  python3 scripts/confidentiality_scan.py --all [path ...]

Exit codes: 0 = clean, 1 = findings (check fails / flag raised), 2 = usage error.
"""
import re
import subprocess
import sys

# (label, severity, compiled regex) — severity is informational; any finding flags.
PATTERNS = [
    ("credential", "HARD", re.compile(
        r"sk-ant-|ghp_[A-Za-z0-9]{20,}|github_pat_|xox[bap]-|AKIA[0-9A-Z]{16}"
        r"|-----BEGIN [A-Z ]*PRIVATE KEY|Bearer [A-Za-z0-9._\-]{25,}")),
    ("financial figure", "SOFT", re.compile(
        r"[€£$]\s?\d[\d.,]*\s?[kKmM]?\b|\b\d[\d.,]*\s?[kKmM]?\s?(EUR|GBP|USD)\b")),
    ("revenue metric with number", "SOFT", re.compile(
        r"\b(MRR|ARR|ACV|eNPS|GRR|NRR|runway)\b[^\n]{0,40}\d")),
    ("client health/churn data", "SOFT", re.compile(
        r"Health\s*[🟢🟡🔴]|\bchurn(ed|ing)?\b[^\n]{0,60}\b[A-Z][a-z]+"
        r"|\b[A-Z][a-z]+[^\n]{0,60}\bchurn(ed|ing)?\b")),
    ("CRM/meeting deep link", "SOFT", re.compile(
        r"https?://[^\s)\]]*(planhat\.com|fireflies\.ai|gong\.io)[^\s)\]]*")),
    ("personal email address", "SOFT", re.compile(
        r"\b[\w.+-]+@(?!govocal\.com|citizenlab\.co|example\.com)[\w-]+\.[\w.]+\b")),
]


def scan_line(line):
    return [(label, sev) for label, sev, rx in PATTERNS if rx.search(line)]


def added_lines_from_diff(diff_range, paths):
    out = subprocess.run(
        ["git", "diff", "--unified=0", "--no-color", diff_range, "--"]
        + (paths or ["plugins", "README.md", ".claude-plugin"]),
        capture_output=True, text=True, check=True).stdout
    current_file, findings = None, []
    lineno = 0
    for raw in out.splitlines():
        if raw.startswith("+++ b/"):
            current_file = raw[6:]
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            lineno = int(m.group(1)) if m else 0
        elif raw.startswith("+") and not raw.startswith("+++"):
            for label, sev in scan_line(raw[1:]):
                findings.append((current_file, lineno, label, sev, raw[1:].strip()))
            lineno += 1
    return findings


def all_lines(paths):
    files = subprocess.run(
        ["git", "ls-files", "--"] + (paths or ["plugins"]),
        capture_output=True, text=True, check=True).stdout.split()
    findings = []
    for f in files:
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    for label, sev in scan_line(line):
                        findings.append((f, i, label, sev, line.strip()))
        except OSError:
            continue
    return findings


def main():
    args = sys.argv[1:]
    if args[:1] == ["--range"] and len(args) >= 2:
        findings = added_lines_from_diff(args[1], args[2:])
        scope = f"lines added in {args[1]}" + (f" under {' '.join(args[2:])}" if args[2:] else "")
    elif args[:1] == ["--all"]:
        findings = all_lines(args[1:])
        scope = "all tracked content"
    else:
        print(__doc__)
        return 2
    if not findings:
        print(f"Confidentiality scan clean ({scope}).")
        return 0
    print(f"⛔ Confidentiality scan flagged {len(findings)} line(s) ({scope}):\n")
    for f, ln, label, sev, text in findings:
        print(f"  {f}:{ln} [{sev} {label}] {text[:160]}")
    print("\nRemove or fictionalize the flagged content, or get an explicit"
          " owner decision before pushing (see CONTRIBUTING.md).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
