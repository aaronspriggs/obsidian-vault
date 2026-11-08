---
date: 2026-11-08
type: config
system:
- '[[ClaudeCode (VM)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/d0a5794
---

# Added a SessionStart hook that loads KB health and all open projects

## What changed

Every interactive Claude Code session on the ClaudeCode VM now starts with the vault pulled and with `check.py --health`, a new `check.py --projects` listing (every active, blocked and backlog project title, grouped by System) and the last 5 KB commits already in context. The script is repo `claudecode-vm/kb-session-context`, deployed to `~/.local/bin/` and wired as a `SessionStart` hook in `~/homelab-agent/.claude/settings.local.json`. A memory rule was added the same day: run `--map` on every System a question touches before answering, and never truncate vault searches (repo commit f8c586c).

## Why

On 2026-11-08 Claude recommended a Pi-hole plan without seeing the existing backlog task [Set up Pi-hole for local DNS and ad-blocking](<../projects/Set up Pi-hole for local DNS and ad-blocking.md>): it skipped the `--map` step and its grep was cut off by `head`. Aaron said missed project and past-note details had happened a couple of times recently. Having every project title in context from the first message lets an existing project match before any search, without depending on Claude remembering the session-start step.

## How

Repo commit d0a5794 (script, settings, `deployed.tsv`). `--projects` is in `.kb/check.py` in this vault. About 10 KB, roughly 2.5k tokens per session. Fix runs (`claude-fix`) use `--setting-sources user,project`, so they don't load it.

## Verify / roll back

Verify: start a new session; the first context should begin with "# KB session context". Roll back: remove the `hooks` block from repo `claudecode-vm/claude/settings.local.json`, redeploy it, and commit.
