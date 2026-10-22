---
date: 2026-10-22
type: install
system:
- '[[ClaudeCode (VM)]]'
project: '[[Build a Tier 3 guard mod for Claude Code]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/25d963d
---

# Added the tier3-guard mod to Claude Code on the ClaudeCode VM

## What changed

New Claude Code plugin `tier3-guard`, deployed to `~/.claude/mods/tier3-guard`. `~/.claude/settings.json` gained an `env` block (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`, `CLAUDE_CODE_PLUGIN_DIRS=/home/aspriggs/.claude/mods/tier3-guard`) and is now versioned in the repo as `claudecode-vm/claude/settings.json`. All five files are in `deployed.tsv`.

## Why

Tier 3 in [STANDARDS.md](<../STANDARDS.md>) was enforced only by Claude following the rule. The guard enforces the parts a tool call shows: a held call is refused with a 4-hex code, and only Aaron's own typed `approve <code>` (terminal or Remote Control) lets that identical call run once, within 30 minutes. Rule lists and limits are in [the project note](<../projects/Build a Tier 3 guard mod for Claude Code.md>).

## How

Repo commit [25d963d](https://github.com/aaronspriggs/spriggs-homelab/commit/25d963d): source in `claudecode-vm/mods/tier3-guard`, 42 tests run with `claude plugin test claudecode-vm/mods/tier3-guard`. Installed with `install -D` per file, then `make check` clean.

## How to verify / roll back

Verify: `claude plugin test ~/homelab/claudecode-vm/mods/tier3-guard` passes. In a new session, ask Claude to run `ssh-keygen --help`: the call is refused with "Held by tier3-guard (code …)". A `claude -p` run on 2026-10-22 got code 7233 for that call, which shows the guard loads from settings alone. Sessions started before the change don't have it.

Roll back: remove the `env` block from `~/.claude/settings.json` (and from `claudecode-vm/claude/settings.json`), or delete `~/.claude/mods/tier3-guard`, then drop their lines from `deployed.tsv`. New sessions start without the guard. With the guard active, Claude's own edits to either path are held for Aaron's approval.
