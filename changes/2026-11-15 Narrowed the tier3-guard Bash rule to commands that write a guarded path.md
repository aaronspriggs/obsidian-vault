---
date: 2026-11-15
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
- '[[Stop tier3-guard holding Bash commands that only mention the rulebook]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/3eaf1c30cb7f518eda5b346c0a3ba70f4bae7e88
---

# Narrowed the tier3-guard Bash rule to commands that write a guarded path

## What changed

`tier3-guard` holds a Bash command for a guarded path (the rulebook, `.ssh/`, `.claude/mods`, `.claude/settings.json`) only where the command writes that path. Three shapes count: a write verb with the path later in the same simple command (`sed -i … PATH`, `cp x PATH`, `tee`, `mv`, `rm`, `install`, `git checkout`…), a redirect whose target is the path (`> PATH`, `>> "PATH"`), and an interpreter writing it (`open(PATH, 'w')`, `Path(PATH).write_text`). Until now any write anywhere in the command plus any mention of the path held the call. The Edit and Write tools are unchanged: they are held on the exact path, as before. The other Bash rules (force push, Dockhand DELETE, ZFS, 1Password, `ssh-keygen`) are unchanged.

## Why

6 of the 15 holds on record were reads or unrelated commands: a `for` loop that printed `settings.json`, a `find` over the mods directory, a heredoc whose text named the rulebook. Three times on 2026-11-15 Claude answered such a hold by switching tools, and a guard that teaches working around it is worse than a narrower one. Aaron approved the change on 2026-11-15. Reasoning, rejected options and accepted gaps are in the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>), step 3.

## How

Claude edited `hooks/register.ts` and `tests/guard.test.ts` in repo `claudecode-vm/mods/tier3-guard`. The auto mode classifier refused Claude's commit of its own guard, as on 2026-10-23, so Aaron ran the commit, push and `install -m 644` of `register.ts` into `~/.claude/mods/tier3-guard/hooks/` over SSH at 20:39 UTC (commit 3eaf1c3). Sessions started after that have the new rule.

## Verify / roll back

Verified 2026-11-15 in a session started after the deploy: `make check` all `ok`; `claude plugin test claudecode-vm/mods/tier3-guard` 89 pass; a `for` loop that printed `~/.claude/settings.json` followed by `python3 -c "print('<x>')"` ran without a hold; `printf '' >> ~/.claude/settings.json` (an append that adds nothing, used instead of `echo x >>` so a miss couldn't damage the file) was held. Before the deploy the rule was replayed over all 2,265 Bash commands in the transcripts: it holds 6 where the old rule held 22 and nothing the old rule let through.

Not caught, accepted: a guarded path passed in a variable or built from pieces and written elsewhere in the command. Still held though harmless: copying a guarded file out, and a script that quotes the guard's own patterns. Roll back: revert 3eaf1c3 and copy `register.ts` back; Aaron runs both, since the copy into `~/.claude/mods` is itself held.
