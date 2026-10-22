---
status: active
category: software
url: https://github.com/aaronspriggs/spriggs-homelab
last_verified: 2026-09-29
repo: https://github.com/aaronspriggs/spriggs-homelab
notion_id: 3ea7ae76-22ba-815a-8d16-f4555aa80c62
---

Private GitHub repo holding every homelab script, unit, compose file and config template. Clone at ~/homelab on the ClaudeCode VM; the retired Notion export stays on branch kb-export.

## Overview

The *how* of the homelab: every script, systemd unit, compose file and config template that gets deployed to a host. The KB vault ([aaronspriggs/obsidian-vault](https://github.com/aaronspriggs/obsidian-vault)) holds the *why* and links here. Created 2026-09-26. Verified 2026-09-29: 13 commits on `main`, latest 80f0250 (2026-09-28).

## Access

- Private repo [aaronspriggs/spriggs-homelab](https://github.com/aaronspriggs/spriggs-homelab), owned by Aaron.
- ClaudeCode VM: clone at `~/homelab`; push via deploy key `~/.ssh/id_ed25519_github_spriggs_homelab` (write, this repo only), identity "Claude Code (ClaudeCode VM)".

## Config

- **Layout:** `claudecode-vm/` ([CLAUDE.md](http://claude.md/), systemd, grub), `homelab-update/`, `kb-export/` (retired), `kb-sync-check/`, `plex-vm/` (`claude-maint`), `stacks/` (servarr, uptime-kuma compose + `.env.example`), `truenas/` (`truenas-api`, alert relay), `unifi/` (`unifi-api`), `bin/`, `Makefile`, `deployed.tsv`.
- **`deployed.tsv`** maps each repo file to where it's deployed (15 entries: 13 on the ClaudeCode VM, 2 on the Plex VM). `make check` compares deployed copies with the repo; run it before and after changing anything deployed.
- **Secrets never committed:** hosts keep real values; the repo holds `*.example` templates. The pre-commit hook (enable with `make setup`) runs gitleaks and shellcheck; `.gitleaks.toml` adds rules for HA webhook IDs and Kuma push tokens. Don't bypass it with `--no-verify`.
- **Branch ****`kb-export`****:** orphan branch holding the last weekly Notion KB export (2026-10-18) and `HEALTH.md`, from its own clone at `~/kb-export`. Archive only since 2026-10-22; never merged into `main`.
- **Commits:** `<area>: <summary>`; each KB change note links its commit.
- **Not in the repo on purpose:** `~/homelab-agent` (Claude's working dir) except `CLAUDE.md`, which lives at `claudecode-vm/CLAUDE.md` and is symlinked back.

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
