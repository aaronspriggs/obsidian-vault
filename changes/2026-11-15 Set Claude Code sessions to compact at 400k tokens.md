---
date: 2026-11-15
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/24d7179260f6ebb0386ba2eaf2a53c97b260a7fd
---

# Set Claude Code sessions to compact at 400k tokens

## What changed

`"autoCompactWindow": 400000` in `~/homelab-agent/.claude/settings.local.json` (repo `claudecode-vm/claude/settings.local.json`), so a session's conversation is summarized when its context reaches 400k tokens. `CLAUDE.md` gained a "Compact instructions" section that tells the summary what to keep: Aaron's decisions and corrections with dates, questions and Tier 3 steps waiting on him, the state of the task in hand, and live-system findings not yet in the vault.

## Why

Nothing set a window before, so sessions ran on the models' 1M window and only compacted at about 967k ([model config](https://code.claude.com/docs/en/model-config)). 28 of 68 sessions passed 200k and 11 passed 400k, re-sending that context on every request; about 93% of it was tool input and output. Aaron chose 400k on 2026-11-15 over 200k and 300k: he has heavy iteration sessions and has gone into usage credits only 3 times, so the window should stop runaway sessions rather than trim ordinary ones. Replayed over the transcripts, 400k would have compacted 17 times, in 11 sessions, at most 3 times in one, for 72% of the actual context tokens. The reasoning and the other options are in the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>).

## How

Repo commit 24d7179, then `install -m 644 claudecode-vm/claude/settings.local.json ~/homelab-agent/.claude/settings.local.json`. The setting applies to every model; a per-model window saved with `/autocompact` or the `CLAUDE_CODE_AUTO_COMPACT_WINDOW` variable would override it, and neither is set. Fix runs don't load local settings and stay far below the window anyway.

## Verify / roll back

Not yet seen working: the first session to pass 400k should show a compaction, after which CLAUDE.md, memory and the KB session block are reloaded (the SessionStart hook matches `compact`). Check then that the summary kept what the instructions list, and whether tool schemas loaded through ToolSearch need loading again; the docs don't say. To change the size, edit the number (100000 to 1000000) and redeploy. Roll back: remove the key and redeploy.
