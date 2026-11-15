---
type: idea
status: done
system:
- '[[ClaudeCode (VM)]]'
parent: '[[Build a Tier 3 guard mod for Claude Code]]'
completed: 2026-11-15
---

## Outcome

Done 2026-11-15 ([commit 3eaf1c3](https://github.com/aaronspriggs/spriggs-homelab/commit/3eaf1c30cb7f518eda5b346c0a3ba70f4bae7e88)), as step 3 of the [setup review](<Review and tune the Claude Code setup on the ClaudeCode VM.md>). The idea was extracted on 2026-10-23 after a Bash heredoc that wrote vault notes was held as a rulebook edit: its text named the rulebook and the command had a `>` redirect. The guard's Bash path check now holds a guarded path only where the command writes it (write verb before the path in the same simple command, redirect target, or interpreter write). It covers all four guarded paths, not just the rulebook. Details in the change note.

## Decisions

- **2026-11-15 (Aaron approved): narrow the rule rather than live with retries.** 6 of 15 recorded holds were reads, and Claude had started switching tools to get past them. The full reasoning and the accepted gaps are in the setup review's Decisions, step 3.

## Links

![[Changes.base#For this project]]
