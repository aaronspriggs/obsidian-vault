---
date: 2026-11-15
type: fix
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/6a98107ae9c018ce3c50133b2e3868e9cc2e68ea
---

# Trimmed the session-start hook to fit the 10,000-character cap

## What changed

The SessionStart hook (`kb-session-context`) now prints `check.py --session`, a new mode in this vault's `.kb/check.py`: open work with next steps, stalled projects, gaps, a count of systems to verify and untested runbooks, and every backlog title once under its first System. With the header and the last 5 commits the block is 6,924 characters (was 11,354). `CLAUDE.md` describes the new block and says what an "Output too large" preview means.

## Why

Claude Code caps hook stdout at 10,000 characters and replaces longer output with a 2,000-character preview and a file path; nothing raises the cap ([hooks reference](https://code.claude.com/docs/en/hooks)). The hook's output was 10,025 characters on the day it was added (2026-11-08) and grew from there, so all 13 sessions since got the preview. It ended partway through open work, and the backlog list, the reason the hook was built, never reached context. `CLAUDE.md` said the block was already in context, so nothing prompted Claude to read the saved file. Found during the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>), which records why trimming was chosen over the alternatives.

## How

Repo commit 6a98107 (hook script, `CLAUDE.md`); `.kb/check.py` in this vault. `--session [budget]` shortens next steps (120, 80, 50 characters, then none) until the block fits the budget (8,500 by default) and prints a warning if it still doesn't. The hook cuts itself with a warning at 9,800 characters. `--health`, `--projects` and `--map` are unchanged.

## Verify / roll back

Verify: `~/.local/bin/kb-session-context | wc -m` is under 10,000 (6,924 on 2026-11-15), and a new session starts with the whole block, ending in "Newest KB commits", with no "Output too large" line. Not yet checked in a new session. Roll back: `git revert 6a98107` in `~/homelab`, `install -m 755 claudecode-vm/kb-session-context ~/.local/bin/`; the `--session` mode can stay.
