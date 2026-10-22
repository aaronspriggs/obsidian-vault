---
type: project
status: active
priority: medium
system:
- '[[ClaudeCode (VM)]]'
next_step: '2026-10-22: pilot reviewed OK in Obsidian on the Mac (~/Documents/Claude/obsidian-vault.nosync; embedded Bases views, links, properties all render). Next: cutover, pending Aaron''s yes on the Tier 3 steps.'
notion_id: 4007ae76-22ba-8150-91b0-e3d3cd9061bb
---

Move the homelab KB out of Notion into Markdown notes in the private repo aaronspriggs/obsidian-vault, written by Claude Code on the VM and viewed in Obsidian on the Mac. Notion stays the source of truth until cutover, then becomes a read-only archive.

## Goal

Replace Notion as the KB with a git-backed Obsidian vault: plain Markdown with flat frontmatter, git as history and backup, a pre-commit validator enforcing KB Standards, Obsidian on the Mac as the viewer. Cheaper on tokens (local grep/edit instead of MCP fetches) and removes the Free-plan edit-safety and weekly-export workarounds.

## Status / next step

2026-10-21: pilot converted locally in `~/obsidian-vault` (315 notes, 370 Notion API requests, gitleaks clean, validator clean after setting Priority Low on the two Backlog projects that had none: Yu Yu Hakusho episode fix (cosmetic) and centralized VM update management (homelab-update already covers weekly updates); Aaron delegated the call). Waiting on the GitHub repo and deploy key (key generated on the VM, SSH alias `github-obsidian-vault`). Then Aaron opens it in Obsidian on the Mac and checks links, properties and the embedded Bases views.

## Plan

1. Pilot: `.kb/migrate.py` (reuses kb-export's read-only token, Notion client and renderer) converts all four databases plus KB Standards; rerunnable. `.kb/check.py` validates schema, enums, links and unique names in the pre-commit hook beside gitleaks; `--health` replaces [HEALTH.md](http://health.md/).
2. Aaron reviews on the Mac; fix what doesn't render.
3. Cutover: freeze Notion writes, rerun migrate, commit, push.
4. Rewrite KB Standards as the vault's [STANDARDS.md](http://standards.md/) (Tier 3, ask first); update this VM's [CLAUDE.md](http://claude.md/), memories, `claudecode-vm/claude-fix-runbooks.json` (Notion tools + 5 runbook URLs), retire kb-export and repoint the Kuma "KB Export" monitor to an unpushed-changes check.
5. Mark the Notion KB deprecated/read-only (never delete).

## Decisions

- 2026-10-21: homelab work happens only through Claude Code on the VM; Cowork/[claude.ai](http://claude.ai/) no longer need KB access (Aaron).
- 2026-10-21: separate repo `aaronspriggs/obsidian-vault`, repo root = vault; push on every commit, no nightly job.
- 2026-10-21: readable filenames; Markdown links in note bodies (clickable on GitHub), wikilinks only in frontmatter relations; no renames after migration.
- 2026-10-21: Projects status Deferred merges into Backlog. Runbook Tags dropped; replaced by `kind` (setup, procedure, troubleshooting, recovery, reference) plus the System link.
- 2026-10-21: long-text properties (Notes, Details, Summary) move into the note body; reverse relations (Hosts, Sub-items, Projects→Changes, Systems→Runbooks) become embedded Bases views; Last Edited/Last Updated dropped in favour of git history.
- 2026-10-21: mobile access undecided; Mac clone with git pull for now. Headless Obsidian Sync is the option if phone capture is wanted later.

## Open questions

- Confirm in the pilot: Bases `system.contains(this)` filters in embedded views, and Obsidian resolving `[text](<path with spaces.md>)` links.
