---
date: 2026-10-22
type: config
system:
- '[[ClaudeCode (VM)]]'
- '[[Uptime Kuma]]'
- '[[Home Assistant OS (VM)]]'
- '[[spriggs-homelab repo]]'
project:
- '[[Migrate the KB from Notion to an Obsidian vault in git]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/22de8d0
---

# Moved the KB from Notion to the obsidian-vault repo (cutover)

## What changed

The homelab KB's source of truth moved from Notion to this vault (aaronspriggs/obsidian-vault, `~/obsidian-vault`). With Aaron's approval of the Tier 3 steps:

1. Final migration from live Notion (vault commit c50c609, 316 notes), then no more Notion writes.
2. KB Standards rewritten as [STANDARDS](<../STANDARDS.md>): Notion edit-safety, the weekly export and the Cowork split removed; never-rename, link and session-start health-check rules added; rulebook changes made Tier 3.
3. `claudecode-vm/CLAUDE.md` and Claude's memories point at the vault; `feedback_notion_is_source_of_truth` and `open_work_from_live_notion` replaced by `vault-is-source-of-truth`.
4. claude-fix runs: Notion tools replaced by Read on the vault, Write on `changes/`, and git add/commit/push of that one file; the servarr runbook is referenced by path. Deployed and listener restarted; dry run shows the new prompt.
5. kb-export retired: timer disabled, unit files left in place, out of `deployed.tsv`. New `kb-sync-check` (every 15 min) pushes to Kuma monitor 17, renamed `KB Vault Sync` (interval 1 h; AutoKuma ID still `kb-export`), down when vault changes sit uncommitted or unpushed for over an hour. Alert2's heartbeat entry for `sensor.kb_export_status` relabelled "KB vault sync" (written with ha-mcp, config check ok, `alert2.reload`).
6. Notion homepage and KB Standards prepended with a deprecation banner; nothing deleted. The homepage's overview, network facts and access table, which the converter skipped, moved into [Home](<../Home.md>).

Found on the way: Compose doesn't recreate a service when only an inline config's content changes, so the monitor rename didn't deploy. `stacks/uptime-kuma/render` now adds a `MONITORS_HASH` env var to AutoKuma (commit 7f851b1); the redeploy recreated only AutoKuma.

## Why

Notion fetches and its edit-safety round trips cost tokens on Aaron's Pro plan, the Free plan's limited history needed workarounds, and homelab work only happens on this VM now. Git gives full history and a validator enforces the standards on every commit. Decisions are on the [project](<../projects/Migrate the KB from Notion to an Obsidian vault in git.md>).

## How to verify / roll back

Verify: `~/obsidian-vault/.kb/check.py --health`; `systemctl list-timers kb-sync-check.timer`; Kuma monitor `KB Vault Sync` up; `make -C ~/homelab check` all ok. Roll back: Notion still holds every page as of the cutover; re-enable `kb-export.timer`, revert spriggs-homelab 22de8d0 and the memory changes, and remove the banners. Anything written to the vault after 2026-10-22 would need copying back by hand.
