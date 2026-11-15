---
type: task
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
notion_id: 3ea7ae76-22ba-81b7-8976-e4717c208fe4
---

## Goal

A recurring pass with Aaron, about 15 minutes every three months, over what otherwise only piles up: the backlog and ideas, the untested runbooks, and Claude Code's memory. Came out of KB governance phase 5 (project closed 2026-09-29).

## Status

Last run: 2026-11-15, pulled forward as step 8 of the setup review ([change](<../changes/2026-11-15 Ran the first quarterly KB triage.md>)). Next due: February 2027. This note stays in the backlog between runs.

## Plan

Claude does the reading for steps 1 to 3 before asking Aaron anything, so his 15 minutes go to decisions. Measured 2026-11-15, that reading is about 13,000 tokens a run (42 backlog notes, 8,485 words; 3 memory files, 1,061 words).

1. **Backlog and ideas.** `~/obsidian-vault/.kb/check.py --projects` lists every not-done title by System. Claude reads each note with `status: backlog` (ideas are the ones with `type: idea`) and gives Aaron one line per note with a recommendation. He decides for each: keep, make active (it then needs a dated `next_step`), or drop (`status: deprecated` plus one line saying why; never deleted).
2. **Untested runbooks.** `~/obsidian-vault/.kb/check.py --health` lists them. Aaron picks which get tested before the next triage and which are left. The same report lists Systems to verify and over-size notes; those need no decision from him, Claude works them off as it touches each note.
3. **Memory fold.** Claude reads every file in its memory (`~/homelab/claudecode-vm/claude/memory/`). A rule that has settled (Aaron hasn't corrected it since it was written, and it fits one line) moves into [CLAUDE.md](https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/CLAUDE.md) as that line, and its memory file and its `MEMORY.md` entry are deleted, so each rule has one home. A procedure too long for one line stays in memory. In the same pass Claude checks CLAUDE.md's dated rules for any that no longer hold. Aaron sees the diff and approves it before the commit (`claudecode-vm: …`).
4. **Log it.** One change note (type doc) for the run, then update Status here.

## Decisions

- **2026-11-15: rewritten for the vault.** The 2026-09-29 version had Claude list "Deferred projects and Ideas from the local export" and skim `HEALTH.md`. The Notion export was retired on 2026-10-22, deferred was merged into backlog the same day, and `check.py --health` replaced `HEALTH.md`. The note keeps its name because notes are never renamed.
- **2026-11-15: the memory fold is a step here, not its own task.** CLAUDE.md → Memory names the quarterly triage as when it happens, a second recurring task would be one more thing to remember, and three memory files add about 1,500 tokens of reading.
- **2026-11-15: only untested runbooks go to Aaron from the upkeep lists.** Testing a runbook can need him or a disruption he has to agree to. Verifying a System is Claude's own work against the live system, and the rulebook already says when an over-size note gets slimmed.
- **2026-11-15, first run: the reading cost more than the 13,000 tokens estimated,** because checking notes against the live systems is what made the recommendations right (a DVR test already done, a snapshot deletion three weeks overdue, the cause of the Yu Yu Hakusho mix-up). Keep the live checks, but ask each tool for the field needed: one whole-file read of `configuration.yaml` cost more than the 42 notes together.
- **2026-11-15: "drop" can't be written yet.** Step 1 says a dropped note gets `status: deprecated`, and the rulebook's Lifecycle section says the same for any note, but its property table and `check.py` allow only active, blocked, backlog and done on project notes. Adding the value is a rulebook change (Tier 3); Aaron approved it the same day and the seven notes were dropped ([change](<../changes/2026-11-15 Allowed deprecated on project notes and dropped seven backlog notes.md>)).
