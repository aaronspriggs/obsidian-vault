---
type: task
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
---

## Goal

Remove the read-only Notion integration `kb-export` and its token in `~/.config/kb-export/` now that the KB lives in the vault and kb-export is retired (2026-10-22).

## Status / next step

Not started. Wait until the Notion archive is no longer needed for cross-checks: the token is only used by `.kb/migrate.py --dry-run`. Revoking it is a security change (Tier 3), and *Aaron* removes the integration in Notion's settings; Claude then deletes the local token file and `~/.config/kb-export/kb-export.json`.
