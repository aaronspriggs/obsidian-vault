---
type: project
status: active
priority: medium
system:
- '[[ClaudeCode (VM)]]'
- '[[Claude Code (Remote Control service)]]'
next_step: '2026-11-15: steps 1 to 7 done. Next, in a fresh session: step 8 (slim the four largest project notes, then the backlog triage with Aaron, following the quarterly triage note). Step 8 also splits the Home Assistant OS and Big Boi System notes (Aaron, 2026-11-15).'
---

## Goal

Review the whole Claude Code setup on this VM (settings, hooks, the tier3-guard mod, CLAUDE.md, memory, the KB tooling and how projects are organized) and fix what costs tokens, hides information or has drifted. Aaron asked for it on 2026-11-15 and wants each step checked as it goes, with the reasoning written down so later sessions know what was done and why.

## Status (2026-11-15)

Steps 1 to 7 are done, each with a change note. Steps 1, 3, 4 and 5 were verified live in sessions started after their deploys; step 2 waits for the first session to pass 400k. Step 8 is open and gets its own fresh session, because long sessions are the main token cost (Aaron, 2026-11-15). This note was slimmed on 2026-11-15 under the new size rule; the longer working-out of steps 1 to 3 and the step 7 inventory are in its git history from that date.

## Findings (measured 2026-11-15)

Fixed by steps 1 to 5: the session hook never arrived whole (output over Claude Code's 10,000-character hook cap); sessions ran to about 967k before compacting; tier3-guard held reads (6 of 15 holds); the rulebook's Claude Code section predated the hook and `--map`; four memories restated CLAUDE.md while other rules lived only in memory.

The measurement behind the token decisions: 68 transcripts hold 4,916 main-thread requests that processed 1.16 billion tokens of context, 236k per request on average. 12 sessions account for 67%, 28 passed 200k and 11 passed 400k. In the 12 heaviest, 67% of what entered context was tool output, 26% tool input and about 7% conversation. The whole vault is about 230k tokens and the largest note about 10k.

Still open:

- **Large project notes and backlog (step 8).** Four open project notes are over the 2,000-word limit: Rebuild Big Boi (7,167), home security (3,660), backup strategy (3,112), patch panels (2,537). Backlog: 42 notes, 17 of them ideas.

Sound and left alone: `make check` clean, vault and repo pushed, memory symlinked into the repo, `truenas-api --write` has its own method allowlist.

## Plan

1. **Session hook fits the cap.** Done 2026-11-15, [change](<../changes/2026-11-15 Trimmed the session-start hook to fit the 10,000-character cap.md>).
2. **Session length.** Done 2026-11-15: sessions compact at 400k, [change](<../changes/2026-11-15 Set Claude Code sessions to compact at 400k tokens.md>).
3. **tier3-guard Bash matching.** Done 2026-11-15, [change](<../changes/2026-11-15 Narrowed the tier3-guard Bash rule to commands that write a guarded path.md>). Closed [this idea](<Stop tier3-guard holding Bash commands that only mention the rulebook.md>).
4. **CLAUDE.md rewrite.** Done 2026-11-15, [change](<../changes/2026-11-15 Rewrote CLAUDE.md and cut Claude Code memory from 14 files to 3.md>).
5. **Rulebook update** (Tier 3). Done 2026-11-15, [change](<../changes/2026-11-15 Updated the rulebook - Claude Code section and a size rule for project notes.md>).
6. **Drift sweep.** Done 2026-11-15, [change](<../changes/2026-11-15 Split the ClaudeCode System note and pointed the repo docs at the vault.md>): repo docs point at the vault, [the quarterly triage note](<Quarterly KB triage with Aaron (Deferred items and Ideas).md>) has the memory fold, and the ClaudeCode System note is split in two.
7. **Loose files.** Done 2026-11-15, [change](<../changes/2026-11-15 Deleted the loose files on the ClaudeCode VM and the retired kb-export copies.md>): all deleted on Aaron's yes, none versioned, plus the retired kb-export's deployed copies.
8. **Slim the four largest project notes, split the Home Assistant OS and Big Boi System notes, then the backlog triage** with Aaron (pulls the quarterly triage forward).

## Decisions

- **2026-11-15, step 1: trim the hook output rather than tell Claude to read the saved file.** The cap can't be raised, and an instruction to read the file would depend on the same remembering that failed with `--map`. Cut: the by-System list, which repeated open work, and the upkeep lists, now a count. Kept at full length: open work with next steps. The limit is enforced in code (8,500 characters in `check.py --session`). Rejected: splitting the output across several hooks. Cost accepted: a backlog project that names several Systems is listed under its first only.
- **2026-11-15, step 2: cap the context window instead of a warning hook.** Nothing compacted before about 967k because of a default, not a habit, and a documented setting fixes that without a script or relying on Claude to pass a warning on. Rejected: `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`, an environment switch for every model.
- **2026-11-15, step 2 (Aaron): 400k.** Replayed over the transcripts, a window of 150k gives 38% of the actual context tokens and 83 compactions, 200k 47% and 55, 300k 61% and 28, 400k 72% and 17 (in 11 sessions, at most 3 in one). Aaron has heavy iteration sessions and has gone into usage credits only 3 times, so the window's job is to stop runaway sessions, not to trim ordinary ones. It can be lowered later from experience.
- **2026-11-15, what compaction keeps** ([context window docs](https://code.claude.com/docs/en/context-window)): CLAUDE.md and memory (re-read from disk), up to five recently modified files, and the output of SessionStart hooks that match `compact`, which the KB hook does. The conversation is summarized, steered by the "Compact instructions" section in CLAUDE.md. Not documented: what happens to tool results and to tool schemas loaded through ToolSearch.
- **2026-11-15 (Aaron asked how much weight token spend should get): read in full, don't carry stale context.** Reading is cheap next to carrying (see the measurement above), and the Pi-hole miss of 2026-11-08 happened at request 14 of a fresh 96k session, from a truncated grep and a skipped lookup. So the rule in CLAUDE.md and the rulebook is to read what the task touches in full and save tokens by ending sessions at task boundaries. No Sonnet default: Aaron starts chats on Opus. He stays on Pro; Max ($100) only pays off if usage credits become regular.
- **2026-11-15, step 3: narrow the guard's Bash rule rather than leave it.** A false hold only costs a retry, but three times Claude answered one by switching tools, and a guard that teaches working around it is worse than a narrower one. A guarded path is now held where a write verb precedes it in the same simple command, where it is a redirect target, or where an interpreter writes it. Checked three ways: 89 tests; a replay over all 2,265 past Bash commands (6 held where the old rule held 22, nothing new let through); and each of the 16 released commands read to confirm it wrote no guarded path. Gaps accepted: a guarded path passed in a variable isn't caught; copying a guarded file out is still held. The guard backs up Claude's judgment; it isn't a wall against a command written to dodge it. The live check used a redirect that appends nothing, so a miss couldn't break the file that loads the guard (detail in the change note).
- **2026-11-15, step 4 (Aaron approved the diff): CLAUDE.md holds every settled rule, memory holds three procedures.** Four memories restated CLAUDE.md, `token_budget` contradicted the agreed rule, and a rule in two places drifts. Memory is now the inbox for new corrections, folded into CLAUDE.md at the quarterly triage. Cost: what loads every session grew from 1,559 to 1,959 words (about 500 tokens); on-demand memory shrank from 3,473 to 962 words. Rejected: stopping at about 9 files as first planned (six would each restate a line now in CLAUDE.md); a CLAUDE.md line for the ha-mcp gate (its memory index line already loads every session); moving the archive procedure to a runbook (it is Claude's behaviour, not a homelab procedure). Dropped on purpose: "pull before reading if Aaron edited on the Mac" (the hook pulls at session start), "run check.py before committing" (the pre-commit hook does), "batch writes".
- **2026-11-15, step 5 (Aaron approved the diff, Tier 3): the rulebook states the KB rules and points at CLAUDE.md for the procedure.** Rejected: copying CLAUDE.md's bullets in (the old section drifted exactly that way) and cutting the section to a bare link (Aaron reads the rulebook, and "read in full" is a KB rule). Size rule for open project notes: about 2,000 words, slimmed the next time the note is worked on. Project notes carry decisions, so they get more room than a System note (1,500). Rejected: 1,500 (also flags the 1,936-word UPS note, which hasn't been read for staleness) and 2,500. `check.py --health` lists over-size notes as a warning, never a commit error, so a long design session isn't blocked from committing.
- **2026-11-15, step 6, sweep: every README that named Notion, not only the two in the plan.** Nine more had a one-line Notion pointer, the same drift. Rejected: touching `kb-export/` (marked retired, describes the Notion export as history) and rewriting READMEs beyond the stale lines.
- **2026-11-15, step 6, split: a second System note for Claude Code, not a reference runbook.** What moved is current state, which a System note's skeleton fits and a runbook's steps don't, and a reference runbook would sit in "untested runbooks" for good. The line between the VM and the software on it is the one already used for Dockhand and Uptime Kuma on Big Boi. Rejected: trimming only (it reached about 1,500 and would be over again within weeks). Cost: one more System to verify, and five projects and three runbooks name both Systems. Old change notes stay under the VM.
- **2026-11-15, step 6, triage note: the memory fold is a step in it,** since CLAUDE.md → Memory names the triage as when it happens. Only untested runbooks go to Aaron from the upkeep lists. A run reads about 13,000 tokens.
- **2026-11-15, step 7 (Aaron: "yes and kb-export"): delete everything, version nothing.** Each item was superseded by the vault or git, or (the work brief) wasn't homelab material. Rejected: an archive folder in the repo (it is what `.archive/` was, and nothing read it in two months) and keeping the two skills in the repo (never used; the built-in `artifact-design` skill covers page design).
- **2026-11-15, a false hold on a note edit was not worked around.** The step 6 update of this note named the SSH authorized-keys file and was held; it waited for Aaron's yes and was retried unchanged, as CLAUDE.md says.
- **2026-11-15 (Aaron): the Home Assistant OS (1,720 words) and Big Boi (1,689) System notes are split in step 8,** not left until each is next worked on. He wants them "organized well and properly linked between everything": done the way the ClaudeCode split was, with the line of the split proposed to him first, every fact checked live and given one home, both notes on the Systems skeleton, and the projects, runbooks and other notes that point at a moved part relinked.

## Open questions

- Step 2 still needs its live check: the first session past 400k should compact, keep what the compact instructions list, and reload the KB block. Check then whether ToolSearch schemas need loading again.
- False holds from the guard's word rules, four on 2026-11-15: `keygenChangesKeys` matches `ssh-keygen` anywhere in a command (a `cat` of a change note, a heredoc editing this note), and the rule on `authorized_keys` does the same (a read-only check, a heredoc editing this note). The fix is to match both only where a simple command starts or names the file as an argument of a write: another Tier 3 guard change and deploy by Aaron. Recommended: bundle it with the next guard change; Aaron to say if he wants it sooner.
- Fix runs haven't run since 2026-10-17. Their tools were switched from Notion to the vault at the 2026-10-22 cutover and have only been through a dry run, so the first real tap is the test. [Verify one-tap actions on first real use](<Verify one-tap actions on first real use.md>) is the place to track it.
- Plan: settled for now, Aaron stays on Pro (2026-11-15). Revisit if usage credits become regular.
