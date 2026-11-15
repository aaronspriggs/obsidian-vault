---
date: 2026-11-15
type: doc
system:
- '[[ClaudeCode (VM)]]'
- '[[Claude Code (Remote Control service)]]'
- '[[spriggs-homelab repo]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/c3a9b0979825b8da4e17dffbce692ffbe3e97a8c
---

# Split the ClaudeCode System note and pointed the repo docs at the vault

## What changed

Step 6 of the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>), the drift sweep. Docs only; no behaviour changed.

- **Repo docs.** The root `README.md`, `claudecode-vm/README.md`, nine other READMEs and the `truenas-api` docstring named Notion pages for the why. They now name the vault note, by its current name. The root README's layout table gained `servarr/`, `scrypted/`, `ha/` and `bin/`. `claudecode-vm/README.md` gained the files added since October (`claude/settings.json`, `kb-session-context`, `mods/tier3-guard/`), no longer calls `settings.local.json` "not in the repo", and describes the fix runs' vault tools instead of the Notion ones. `kb-export/` was left alone: it is marked retired and describes the Notion export as history.
- **System note split.** [ClaudeCode (VM)](<../systems/ClaudeCode (VM).md>) was 1,948 words against the 1,500 limit. The machine stays there (VM definition, guest OS, repo clones, timers, helpers, secrets on disk, outbound SSH; 1,096 words). The software moved to a new note, [Claude Code (Remote Control service)](<../systems/Claude Code (Remote Control service).md>) (install, service, settings, compaction, session hook, tier3-guard, mod UI, MCP connectors, fix runs; 1,251 words). Both now follow the Systems skeleton. Five projects and three runbooks that are about Claude Code name both Systems.
- **Verified live while rewriting** (both notes `last_verified: 2026-11-15`): the VM definition through the TrueNAS API, OS and kernel, watchdog and `nomodeset`, enabled units and timers, SSH client config and authorized keys, the two settings files, the mods directory and `.mcp.json`. Everything matched. Corrected: kernel 7.0.0-43 (the note said 7.0.0-34, from 2026-09-28), and the list of helpers that read 1Password (also `arr-api`, `kuma-api`, `kuma-adopt`, `scrypted-api`, `truenas-api --write`).
- **Triage note.** [Quarterly KB triage with Aaron](<../projects/Quarterly KB triage with Aaron (Deferred items and Ideas).md>) described the Notion export and `HEALTH.md`. It now uses `check.py --projects` and `--health`, and has the memory fold that CLAUDE.md → Memory points at.
- **Stale lines fixed nearby.** [spriggs-homelab repo](<../systems/spriggs-homelab repo.md>): layout and `deployed.tsv` count (15 entries then, 40 now). [Home](<../Home.md>): Claude's access to TrueNAS (`claude-readonlyapi`, plus allowlisted writes as `claude-maint`) and to Dockhand and Kuma (`dockhand-api`, `kuma-api`; it said "no direct access"). The rebuild runbook's last step names both System notes.

## Why

The KB left Notion on 2026-10-22 and these files still sent a reader there. The System note was over the size rule and mixed two things that change at different rates: the VM changes a few times a year, Claude Code's setup changed five times on 2026-11-15 alone. Why a second System note and not a reference runbook is in the project's Decisions.

## How

Repo commit c3a9b09; `truenas-api` redeployed with `install -m 755`, `make check` 40 of 40 ok before and after. The rest is in this vault commit.

## Verify / roll back

Verify: `grep -rn -i notion ~/homelab --include=README.md` hits only `kb-export/`, the dated "replaced the Notion KB" lines and the fix-run history line; `~/obsidian-vault/.kb/check.py --health` lists six over-size notes, none of them ClaudeCode; `check.py --map "Claude Code (Remote Control service)"` lists its projects and runbooks. Found on the way and not fixed: no fix run has run since 2026-10-17, so the fix runs' vault tools (changed at the cutover) have only been through a dry run. Roll back: `git revert` the two commits; the new note would then be deprecated, not deleted.
