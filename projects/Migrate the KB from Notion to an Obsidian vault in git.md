---
type: project
status: done
priority: medium
system:
- '[[ClaudeCode (VM)]]'
completed: 2026-10-22
notion_id: 4007ae76-22ba-8150-91b0-e3d3cd9061bb
---

## Outcome

Done 2026-10-22 (started 2026-10-21). The homelab KB moved out of Notion into this vault: the private repo [aaronspriggs/obsidian-vault](https://github.com/aaronspriggs/obsidian-vault), cloned at `~/obsidian-vault` on the ClaudeCode VM (written by Claude Code) and at `~/Documents/Claude/obsidian-vault.nosync` on Aaron's Mac (read in Obsidian; `.nosync` because iCloud syncs Documents). 316 notes were converted from live Notion by `.kb/migrate.py` (now refuses to rerun without `--force`). `.kb/check.py` enforces schema, enums, links and unique names in the pre-commit hook beside gitleaks, and `--health` replaces HEALTH.md. [STANDARDS](<../STANDARDS.md>) replaces Notion's KB Standards; this VM's CLAUDE.md, Claude's memories and the claude-fix runs point at the vault. kb-export is retired; kb-sync-check feeds the Kuma monitor KB Vault Sync. Notion's homepage and KB Standards carry a deprecation banner and the Notion KB is a read-only archive. Details: [the cutover change](<../changes/2026-10-22 Moved the KB from Notion to the obsidian-vault repo.md>).

## Decisions

- 2026-10-21: homelab work happens only through Claude Code on the VM; Cowork/claude.ai no longer need KB access (Aaron).
- 2026-10-21: separate repo `aaronspriggs/obsidian-vault` (repo root = vault), push on every commit, no nightly job.
- 2026-10-21: readable filenames; Markdown links in note bodies (clickable on GitHub), wikilinks only in frontmatter relations; no renames after migration.
- 2026-10-21: Deferred merged into Backlog; runbook Tags dropped for `kind` (setup, procedure, troubleshooting, recovery, reference) plus the System link.
- 2026-10-21: long-text properties moved into note bodies; reverse relations (hosts, sub-items, a project's changes, a system's runbooks) became embedded Bases views; last-edited dates come from git.
- 2026-10-21: the two backlog projects with no priority got Low (Aaron delegated the call).
- 2026-10-22: Notion's search API lags recent edits, so the migration queried each database directly.
- 2026-10-22: mobile access undecided; Mac clone pulled from GitHub for now. Headless Obsidian Sync is the option if phone capture is wanted later.

## Links

- Research behind the move: claude.ai doc "Obsidian for homelab and beyond" (2026-10-21).
- Vault commits: daa60f8 (pilot), ad66d47 (direct database queries), c50c609 (final migration).
- spriggs-homelab commits: [22de8d0](https://github.com/aaronspriggs/spriggs-homelab/commit/22de8d0) (cutover), [7f851b1](https://github.com/aaronspriggs/spriggs-homelab/commit/7f851b1) (AutoKuma render fix).
- Follow-up: [Revoke the unused kb-export Notion integration token](<Revoke the unused kb-export Notion integration token.md>).
