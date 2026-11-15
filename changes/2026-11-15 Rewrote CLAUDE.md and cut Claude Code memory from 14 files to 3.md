---
date: 2026-11-15
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/ecd0f47f682989d4b63d32bbbec3c7e734a7de0e
---

# Rewrote CLAUDE.md and cut Claude Code memory from 14 files to 3

## What changed

`CLAUDE.md` (repo `claudecode-vm/CLAUDE.md`, symlinked into `~/homelab-agent`) is retitled "Claude Code on the ClaudeCode VM (homelab operations)" and now holds every settled rule about how Claude works here:

- "Read before answering" and "Token budget" became "Map first" (run `check.py --map` for every System a question touches, implied ones included) and "Read in full, then verify" (read every note the task touches in full, never cut a vault search with `head`).
- New section "Context and sessions": read what the task touches in full and don't carry stale context (Aaron, 2026-11-15); fresh session at task boundaries, ask tools for less, scripts for mechanical work, no self-starting Claude runs.
- New section "Memory": auto-memory is the inbox for new corrections; a rule that has settled is folded into CLAUDE.md at the quarterly KB triage and its memory file deleted.
- Folded in as one line each: look for an existing option before building, don't hand Aaron UI steps Claude can do, no Google connectors, ask once for Tier 3, guard and permission changes go through Aaron, maintenance mode, and the `~/.local/bin` PATH gap.

Memory went from 14 files to 3. Kept: `feedback_ha_mcp_approval_notifications` (trimmed from 571 to 299 words) and `feedback_harvest_sessions_before_archiving` (its links to deleted memories now point at CLAUDE.md). New: `feedback_remote_control_surfaces`, merging `mods_remote_control` and `artifact_tool_varies`. Deleted, with their rule now in CLAUDE.md: `vault_is_source_of_truth`, `kb_hygiene_every_write`, `map_before_answering`, `token_budget`, `research_existing_before_building`, `claude_owns_alerting`, `kb_is_for_claude`, `no_google_connectors`, `single_yes_for_tier3`, `maintenance_mode_before_disruptive_work`.

## Why

Four memories restated CLAUDE.md, `token_budget` still said to read sparingly after Aaron agreed the opposite, and rules that only lived in memory (Tier 3 approvals, maintenance mode) were background context rather than instructions. One home per rule stops that drift. Aaron reviewed the diff and approved it on 2026-11-15. Reasoning, costs and rejected options are in the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>), step 4.

## How

Repo commit ecd0f47. Nothing to deploy: CLAUDE.md and the memory directory are symlinks into the repo. Sessions started after the commit load the new file.

## Verify / roll back

`make check` clean after the commit; `~/homelab-agent/CLAUDE.md` shows the new title; the memory directory lists three files plus `MEMORY.md`. CLAUDE.md grew from 1,274 to 1,879 words; with the shorter memory index, what loads every session grew from 1,559 to 1,959 words. Roll back: `git revert ecd0f47` in `~/homelab` restores the old CLAUDE.md and all twelve deleted memory files.
