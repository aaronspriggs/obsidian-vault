---
type: project
status: active
priority: medium
system:
- '[[ClaudeCode (VM)]]'
next_step: '2026-11-15: steps 1 to 5 done. Next, in a fresh session: step 6 (drift sweep) and step 7 (loose files; deletes need Aaron''s yes). Step 8 (slim the four largest project notes, backlog triage with Aaron) gets its own session after that (Aaron, 2026-11-15).'
---

## Goal

Review the whole Claude Code setup on this VM (settings, hooks, the tier3-guard mod, CLAUDE.md, memory, the KB tooling and how projects are organized) and fix what costs tokens, hides information or has drifted. Aaron asked for it on 2026-11-15 and wants each step checked as it goes, with the reasoning written down so later sessions know what was done and why.

## Status (2026-11-15)

Steps 1 to 5 are done, each with a change note. Steps 1 and 3 were verified live in a session started after their deploys; step 2 waits for the first session to pass 400k; steps 4 and 5 take effect in the next session (new CLAUDE.md, three memory files, rulebook, over-size count in the session block). Steps 6 to 8 are open, because long sessions are the main token cost: 6 and 7 go in one fresh session and step 8 in its own after that (Aaron, 2026-11-15). This note was slimmed on 2026-11-15 under the new size rule; the longer working-out of steps 1 to 3 is in its git history before that date's last commit.

## Findings (measured 2026-11-15)

Fixed by steps 1 to 5: the session hook never arrived whole (output over Claude Code's 10,000-character hook cap); sessions ran to about 967k before compacting; tier3-guard held reads (6 of 15 holds); the rulebook's Claude Code section predated the hook and `--map`; four memories restated CLAUDE.md while other rules lived only in memory.

The measurement behind the token decisions: 68 transcripts hold 4,916 main-thread requests that processed 1.16 billion tokens of context, 236k per request on average. 12 sessions account for 67%, 28 passed 200k and 11 passed 400k. In the 12 heaviest, 67% of what entered context was tool output, 26% tool input and about 7% conversation. The whole vault is about 230k tokens and the largest note about 10k.

Still open:

- **Docs drift (step 6).** Repo `README.md`, `claudecode-vm/README.md` and the `truenas-api` docstring still point at Notion. Three System notes are over the 1,500-word limit (ClaudeCode 1,948, Home Assistant OS 1,720, Big Boi 1,689). The quarterly triage note still describes the Notion export and `HEALTH.md`.
- **Unversioned files on a disk with no backup (step 7):** `~/rack-artifact/`, `~/work-claude-brief.md`, `~/homelab-agent/mockup*.html`, `out/gpu-plan/`, `.archive/`, `settings.local.json.bak`, two project skills never invoked.
- **Large project notes and backlog (step 8).** Four open project notes are over the 2,000-word limit: Rebuild Big Boi (7,167), home security (3,660), backup strategy (3,112), patch panels (2,537). Backlog: 43 notes, 17 of them ideas.

Sound and left alone: `make check` clean, vault and repo pushed, memory symlinked into the repo, `truenas-api --write` has its own method allowlist.

## Plan

1. **Session hook fits the cap.** Done 2026-11-15, [change](<../changes/2026-11-15 Trimmed the session-start hook to fit the 10,000-character cap.md>).
2. **Session length.** Done 2026-11-15: sessions compact at 400k, [change](<../changes/2026-11-15 Set Claude Code sessions to compact at 400k tokens.md>).
3. **tier3-guard Bash matching.** Done 2026-11-15, [change](<../changes/2026-11-15 Narrowed the tier3-guard Bash rule to commands that write a guarded path.md>). Closed [this idea](<Stop tier3-guard holding Bash commands that only mention the rulebook.md>).
4. **CLAUDE.md rewrite.** Done 2026-11-15, [change](<../changes/2026-11-15 Rewrote CLAUDE.md and cut Claude Code memory from 14 files to 3.md>).
5. **Rulebook update** (Tier 3). Done 2026-11-15, [change](<../changes/2026-11-15 Updated the rulebook - Claude Code section and a size rule for project notes.md>).
6. **Drift sweep:** the two READMEs and the `truenas-api` docstring; rewrite [the quarterly triage note](<Quarterly KB triage with Aaron (Deferred items and Ideas).md>) for the vault and add the memory fold that CLAUDE.md → Memory now points at; split the ClaudeCode System note.
7. **Loose files:** version or delete each; deletes need Aaron's yes.
8. **Backlog triage** with Aaron (pulls the quarterly triage forward) and slim the four largest project notes.

## Decisions

- **2026-11-15, step 1: trim the hook output rather than tell Claude to read the saved file.** The cap can't be raised, and an instruction to read the file would depend on the same remembering that failed with `--map`. Cut: the by-System list, which repeated open work, and the upkeep lists, now a count. Kept at full length: open work with next steps. The limit is enforced in code (`check.py --session` shortens next steps to fit 8,500 characters; the hook warns at 9,800). Rejected: splitting the output across several hooks. Cost accepted: a backlog project that names several Systems is listed under its first only.
- **2026-11-15, step 2: cap the context window instead of a warning hook.** Nothing compacted before about 967k because of a default, not a habit, and a documented setting fixes that without a script or relying on Claude to pass a warning on. Rejected: `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`, an environment switch for every model.
- **2026-11-15, step 2 (Aaron): 400k.** Replayed over the transcripts, a window of 150k gives 38% of the actual context tokens and 83 compactions, 200k 47% and 55, 300k 61% and 28, 400k 72% and 17 (in 11 sessions, at most 3 in one). Aaron has heavy iteration sessions and has gone into usage credits only 3 times, so the window's job is to stop runaway sessions, not to trim ordinary ones. It can be lowered later from experience.
- **2026-11-15, what compaction keeps** ([context window docs](https://code.claude.com/docs/en/context-window)): CLAUDE.md and memory (re-read from disk), up to five recently modified files, and the output of SessionStart hooks that match `compact`, which the KB hook does. The conversation is summarized, steered by the "Compact instructions" section in CLAUDE.md. Not documented: what happens to tool results and to tool schemas loaded through ToolSearch.
- **2026-11-15 (Aaron asked how much weight token spend should get): read in full, don't carry stale context.** Reading is cheap next to carrying (see the measurement above), and the Pi-hole miss of 2026-11-08 happened at request 14 of a fresh 96k session, from a truncated grep and a skipped lookup. So the rule in CLAUDE.md and the rulebook is to read what the task touches in full and save tokens by ending sessions at task boundaries. No Sonnet default: Aaron starts chats on Opus. He stays on Pro; Max ($100) only pays off if usage credits become regular.
- **2026-11-15, step 3: narrow the guard's Bash rule rather than leave it.** A false hold only costs a retry, but three times Claude answered one by switching tools, and a guard that teaches working around it is worse than a narrower one. A guarded path is now held where a write verb precedes it in the same simple command, where it is a redirect target, or where an interpreter writes it. Checked three ways: 89 tests; a replay over all 2,265 past Bash commands (6 held where the old rule held 22, nothing new let through); and each of the 16 released commands read to confirm it wrote no guarded path. Gaps accepted: a guarded path passed in a variable isn't caught; copying a guarded file out is still held. The guard backs up Claude's judgment; it isn't a wall against a command written to dodge it.
- **2026-11-15, step 3 live check: a write that adds nothing.** `printf '' >> ~/.claude/settings.json` instead of the planned `echo x >>`: the same redirect to the same path, but a miss would have changed nothing instead of breaking the file that loads the guard. It was held.
- **2026-11-15, step 4 (Aaron approved the diff): CLAUDE.md holds every settled rule, memory holds three procedures.** Four memories restated CLAUDE.md, `token_budget` contradicted the agreed rule, and a rule in two places drifts. Memory is now the inbox for new corrections, folded into CLAUDE.md at the quarterly triage. Cost: what loads every session grew from 1,559 to 1,959 words (about 500 tokens); on-demand memory shrank from 3,473 to 962 words. Rejected: stopping at about 9 files as first planned (six would each restate a line now in CLAUDE.md); a CLAUDE.md line for the ha-mcp gate (its memory index line already loads every session); moving the archive procedure to a runbook (it is Claude's behaviour, not a homelab procedure). Dropped on purpose: "pull before reading if Aaron edited on the Mac" (the hook pulls at session start), "run check.py before committing" (the pre-commit hook does), "batch writes".
- **2026-11-15, step 5 (Aaron approved the diff, Tier 3): the rulebook states the KB rules and points at CLAUDE.md for the procedure.** Rejected: copying CLAUDE.md's bullets in (the old section drifted exactly that way) and cutting the section to a bare link (Aaron reads the rulebook, and "read in full" is a KB rule). Size rule for open project notes: about 2,000 words, slimmed the next time the note is worked on. Project notes carry decisions, so they get more room than a System note (1,500). Rejected: 1,500 (also flags the 1,936-word UPS note, which hasn't been read for staleness) and 2,500. `check.py --health` lists over-size notes as a warning, never a commit error, so a long design session isn't blocked from committing.

## Open questions

- Step 2 still needs its live check: the first session past 400k should compact, keep what the compact instructions list, and reload the KB block. Check then whether ToolSearch schemas need loading again.
- False holds from the guard's `ssh-keygen` rule, seen twice on 2026-11-15: a `cat` of the change note "Narrowed the tier3-guard ssh-keygen rule…" and a heredoc that edited this note were held as "SSH keys", because `keygenChangesKeys` matches the word anywhere in a command, filenames and quoted text included. Both were worked around with the Read and Edit tools. The fix is to match it only where a simple command starts (start of line, after `;`, `&`, `|` or `sudo`): another Tier 3 guard change and another deploy by Aaron. Recommended: bundle it with the next guard change; Aaron to say if he wants it sooner.
- Plan: settled for now, Aaron stays on Pro (2026-11-15). Revisit if usage credits become regular.
