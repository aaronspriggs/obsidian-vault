---
status: active
category: software
url: https://github.com/aaronspriggs/spriggs-homelab
last_verified: 2026-11-15
repo: https://github.com/aaronspriggs/spriggs-homelab
notion_id: 3ea7ae76-22ba-815a-8d16-f4555aa80c62
---

Private GitHub repo holding every homelab script, unit, compose file and config template. Clone at ~/homelab on the ClaudeCode VM; the retired Notion export stays on branch kb-export.

## Overview

The *how* of the homelab: every script, systemd unit, compose file and config template that gets deployed to a host. The KB vault ([aaronspriggs/obsidian-vault](https://github.com/aaronspriggs/obsidian-vault)) holds the *why* and links here. Created 2026-09-26.

## Access

- Private repo [aaronspriggs/spriggs-homelab](https://github.com/aaronspriggs/spriggs-homelab), owned by Aaron.
- ClaudeCode VM: clone at `~/homelab`; push via deploy key `~/.ssh/id_ed25519_github_spriggs_homelab` (write, this repo only), identity "Claude Code (ClaudeCode VM)".

## Config

- **Layout:** one directory per host or stack, each with a README: `claudecode-vm/` (`CLAUDE.md`, Claude Code settings and memory, session hook, `tier3-guard` mod, fix-run listener, systemd, grub), `homelab-update/`, `truenas/` (`truenas-api`, alert relay), `plex-vm/` (`claude-maint`), `stacks/` (servarr and uptime-kuma compose + `.env.example`), `servarr/` (`arr-api`), `dockhand/` (`dockhand-api`), `unifi/` (`unifi-api`), `uptime-kuma/` (`kuma-api`, `kuma-adopt`), `scrypted/` (`scrypted-api`), `ha/` (YAML applied through ha-mcp), `backup/` (B2 offsite), `kb-sync-check/`, `kb-export/` (retired), `bin/`, `Makefile`, `deployed.tsv`. The root README's table is the full list.
- **`deployed.tsv`** maps each repo file to where it's deployed (40 entries on 2026-11-15: 35 on the ClaudeCode VM, 4 on the Plex VM, 1 TrueNAS Cloud Sync pre-script). `make check` compares deployed copies with the repo; run it before and after changing anything deployed.
- **Secrets never committed:** hosts keep real values; the repo holds `*.example` templates. The pre-commit hook (enable with `make setup`) runs gitleaks and shellcheck; `.gitleaks.toml` adds rules for HA webhook IDs and Kuma push tokens. Don't bypass it with `--no-verify`.
- **Branch ****`kb-export`****:** orphan branch holding the last weekly Notion KB export (2026-10-18) and `HEALTH.md`, from its own clone at `~/kb-export`. Archive only since 2026-10-22; never merged into `main`.
- **Commits:** `<area>: <summary>`; each KB change note links its commit.
- **`~/homelab-agent`** (Claude's working dir) isn't a checkout, but what in it can't be regenerated is versioned in `claudecode-vm/`: see [Claude Code (Remote Control service)](<Claude Code (Remote Control service).md>), Settings.

## Dependencies

GitHub (hosting). Deploys to the ClaudeCode VM and the Plex VM; TrueNAS and Dockhand config is copied in by Aaron (read-only API can't read files).

## Decisions

- **2026-09-26:** one private repo; Notion is the why, the repo is the how. Ansible, Renovate/Dependabot and a docs site deferred until per-host work becomes a burden (see the idea "Evaluate centralized VM update management").
- **2026-09-27:** the KB export goes to an orphan branch here rather than a separate repo.
- **2026-10-22:** the KB itself moved out of Notion into its own repo, aaronspriggs/obsidian-vault, kept separate from this one so it can grow non-homelab notes and sync to devices without touching the deploy tree.

## Related

Project: "Homelab foundation: version-controlled repo" (Done). Repo README has the full conventions.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
