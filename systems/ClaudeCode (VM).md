---
status: active
category: vm
ip: 192.168.1.156
runs_on:
- '[[TrueNAS SCALE (Big Boi)]]'
last_verified: 2026-10-16
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/claudecode-vm
notion_id: 3cf7ae76-22ba-81bc-9a3e-ed83c614d524
---

Claude Code Remote Control host (VM on Big Boi). SSH: ssh aspriggs@192.168.1.156 (key-only).

## Overview

Ubuntu Server VM on TrueNAS SCALE (Big Boi) running Claude Code in Remote Control server mode. Gives Claude direct LAN access to homelab systems (starting with Home Assistant) for building automations and dashboards, reachable from any device via [claude.ai/code](http://claude.ai/code) or the Claude mobile app — no public exposure, no VPN required, since Remote Control only makes outbound connections to Anthropic's API.

## Host

- **Hypervisor:** TrueNAS SCALE (Big Boi) — 192.168.1.248
- **VM Name:** ClaudeCode
- **VM IP:** 192.168.1.156 (UDM fixed-IP reservation on the NIC's MAC `00:a0:98:1e:c7:5c`; guest netplan is plain DHCP, verified 2026-10-16). A rebuilt VM must reuse that MAC.
- **Rebuild:** the disk isn't backed up. See runbook [Rebuild the ClaudeCode VM from scratch](<../runbooks/Rebuild the ClaudeCode VM from scratch.md>) and [Disaster recovery: rebuild order (index)](<../runbooks/Disaster recovery - rebuild order (index).md>).

## VM Specs

- **CPU mode:** Host Passthrough
- **vCPUs:** 1 (2 cores, 1 thread) — 2 logical CPUs total
- **Memory:** 8192 MB
- **Bootloader:** UEFI
- **Disk:** /dev/zvol/Big+Boi/vmstore/claudecode_disk (40 GiB)
- **NIC:** VirtIO, bridged via br0 (Trust Guest Filters must stay OFF — incompatible with bridge attachment, unlike direct-interface attachment)
- **Display:** SPICE, bound to 192.168.1.248 (not 0.0.0.0). Guest boots with `nomodeset` (since 2026-09-27): the qxl DRM driver's TTM eviction fails, and fbcon writes on it deadlocked PID 1 during the 2026-09-27 update reboot. The console still works in VGA text mode.
- **Watchdog:** `softdog` kernel module + systemd `RuntimeWatchdogSec=2min` / `RebootWatchdogSec=5min`. If PID 1 hangs for 2 min, the kernel reboots the VM. softdog is loaded by `softdog.service` (explicit modprobe), not `modules-load.d`, because Ubuntu's kernel package blacklists watchdog drivers. Config in repo `claudecode-vm/` (commits 585a3f9, 147dd96).
- **System Clock:** UTC (Linux guest — HA and Plex VMs may differ, verify if it matters)

## Software

- **OS:** Ubuntu Server 26.04 LTS (Resolute Raccoon)
- **Provisioning method:** Cloud image + injected cloud-init NoCloud seed via qemu-nbd — no ISO/installer used. First VM on Big Boi built this way (HA and Plex both used different methods). See linked Runbook.
- **User:** aspriggs, sudo NOPASSWD, SSH key-only (password auth disabled)
- **Authorized SSH keys:** aaronspriggs@Aarons-MacBook-Pro.local, aspriggs@mbp-017446 (add more the normal way — append to ~/.ssh/authorized_keys, no need to touch cloud-init again)
- **Node.js:** installed via NodeSource LTS setup script
- **Claude Code:** native install (not npm-global — npm-global requires sudo to auto-update), v2.1.286 on 2026-10-16 (update with `claude update`, then `sudo systemctl restart claude-remote-control.service` to activate; the restart drops every attached session), binary at /home/aspriggs/.local/bin/claude. `~/.local/bin` isn't on the non-interactive shell PATH, so use the full path.
- **Working directory:** /home/aspriggs/homelab-agent (trusted workspace)

## Remote Control Service

- **Unit:** /etc/systemd/system/claude-remote-control.service
- **Runs as:** aspriggs, WorkingDirectory /home/aspriggs/homelab-agent
- **Command:** `~/.local/bin/claude-remote-control-start`, which sets HA_MCP_URL from 1Password and then runs `claude remote-control --name "ClaudeCode VM"`
- **Restart policy:** always
- **Gotcha:** first run requires answering an interactive "Enable Remote Control? (y/n)" consent prompt, which systemd can't supply (no TTY) — the service will crash-loop until this is accepted once by running the same command manually from the same working directory over SSH, after which the consent persists and systemd starts clean.
- **Mods (Claude Code plugins) over Remote Control** (tested 2026-10-22, Claude Code 2.1.286): hooks work, UI doesn't. A mod can block, hold or rewrite tool calls and prompts, and its slash commands can answer in text (`tier3-guard` relies on this). Panes, buttons, toasts and status-line entries don't render in the Desktop app or the iOS app: `/ui-test` reported "Surfaces drawing this session: none" on both. Re-check after Claude Code updates with repo `claudecode-vm/mods/ui-test`; see project "Use mod UI once Remote Control clients draw it".

## Access

- **SSH:** `ssh aspriggs@192.168.1.156`
- **Remote Control:** shows as "ClaudeCode VM" in the session list at [claude.ai/code](http://claude.ai/code) and in the Claude mobile app's Code tab

## MCP Connectors

- **Notion, Box, Gmail, Google Drive, Google Calendar** are *account-level* [claude.ai](http://claude.ai/) connectors tied to [spriggs.aaron@gmail.com](mailto:spriggs.aaron@gmail.com). They aren't configured locally: `~/.claude.json` `mcpServers` is empty. Since 2026-10-22 Notion only holds the read-only archive of the old KB. Remote Control sessions inherit whatever is enabled on the [claude.ai](http://claude.ai/) account, so add, remove or reauthorize them in [claude.ai](http://claude.ai/) connector settings, not on this VM. Notion was verified working on 2026-09-03. Gmail, Drive and Calendar currently show as needing auth.
- **Home Assistant (ha-mcp)** is the only locally configured MCP server, at project scope in `~/homelab-agent/.mcp.json` (pre-approved via `enabledMcpjsonServers` in `.claude/settings.local.json`; URL from 1Password). See the "Setting Up ha-mcp" runbook.

## Source of truth & local files

The KB vault is the single source of truth for homelab state (systems, projects, decisions, changes): private repo [aaronspriggs/obsidian-vault](https://github.com/aaronspriggs/obsidian-vault), cloned at `~/obsidian-vault`, rules in its [STANDARDS](<../STANDARDS.md>). It replaced Notion on 2026-10-22 ([migration project](<../projects/Migrate the KB from Notion to an Obsidian vault in git.md>)). Homelab work happens only through Claude Code on this VM; Aaron reads the vault in Obsidian on his Mac (clone at `~/Documents/Claude/obsidian-vault.nosync`, pulled from GitHub). This VM's disk isn't backed up, so every KB write is committed and pushed. Claude Code memory is limited to how Claude Code itself should behave; see the `CLAUDE.md` in /home/aspriggs/homelab-agent.

## Updates

Enrolled in **homelab-update** (weekly, Sun 04:30 America/Denver; see runbook). Verified 2026-09-28: Ubuntu 26.04.1, kernel 7.0.0-34 running, 0 packages upgradable. The first run on 2026-09-27 applied the backlog and rebooted, but the shutdown hung ~9.5 h on the qxl framebuffer until a manual hard reset (fixed with `nomodeset` + softdog; see the Changes entry). **The reboot drops all Claude Remote Control sessions**; `claude-remote-control.service` restarts at boot. After a hard reset it can register a new environment ID, and the Claude desktop app then files earlier sessions under "Other". They're still on disk and can be resumed. Monitored by Kuma (`ClaudeCode VM` ping, `ClaudeCode VM Updates` push).

## Homelab tools hosted here

- **TrueNAS read-only access:** `~/.local/bin/truenas-api` plus the key in `~/.config/homelab/truenas-api-key`. It needs apt `python3-websocket`, installed 2026-09-25.
- **`kb-sync-check.timer`** (since 2026-10-22; system unit, every 15 min, runs as aspriggs): pushes the vault's state to the Kuma push monitor `KB Vault Sync`, which goes down when KB changes sit uncommitted or unpushed for over an hour. Push URL in `~/.config/homelab/kb-sync-check-push-url` (600). No AI. See repo `kb-sync-check/README.md`.
- **KB vault** `~/obsidian-vault`: push via deploy key `~/.ssh/id_ed25519_github_obsidian_vault` (write, that repo only), SSH alias `github-obsidian-vault` in `~/.ssh/config`. Pre-commit hook (`core.hooksPath .kb/hooks`) runs gitleaks and `.kb/check.py`; the same script gives the session-start list (`--health`, open work first) and the link map Claude starts lookups from (`--map ["note"]`).
- **`kb-export.timer`**: retired 2026-10-22 (timer disabled, unit files left in place, out of `deployed.tsv`). The `~/kb-export` clone and branch keep the last Notion export as an archive.
- **`truenas-alert-relay.timer`** (system unit, every 5 min, runs as aspriggs): forwards TrueNAS alerts to HA. If this VM is down, TrueNAS alerts aren't forwarded; the Kuma push monitor catches that within 15 min. See runbook "TrueNAS read-only API access and alert relay (ClaudeCode VM)".
- **`plex-db-export.timer`** (since 2026-10-15; system unit, Sun 23:00 America/Denver, runs as aspriggs): `ssh plex sudo claude-maint plex-db-export`, the weekly Plex DB export for the B2 offsite backup. If it stops, the Big Boi Cloud Sync pre-script fails after 9 days and TrueNAS alerts. See repo `backup/` and runbook "Offsite backup to B2".
- **`claude-fix-listener.service`** (enabled 2026-10-16; bearer token and HA webhook ID in 1Password item `Claude Fix Listener`, read at listener start; Kuma HTTP monitor `Claude fix listener` on `/health`): `~/.local/bin/claude-fix serve` on port 8765, accepting `POST /fix {alert_id}` with a bearer token from HA (192.168.1.218) only. It starts a capped, tap-started `claude -p` fix run for allowlisted alert IDs (`~/.config/homelab/claude-fix-runbooks.json`): one at a time, 3 per 24 h, Sonnet, dontAsk with the runbook's tools only, outcome posted to an HA webhook. Runs logged in `~/.local/state/claude-fix/`. See repo `claudecode-vm/README.md` "Fix runs" and project "Claude access model" plan 5.
- **`tier3-guard` mod** (since 2026-10-22): a Claude Code plugin in `~/.claude/mods/tier3-guard`, loaded into every session, fix runs included, by `CLAUDE_CODE_PLUGIN_DIRS` and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` in the `env` block of `~/.claude/settings.json`. It holds detectable Tier 3 tool calls until Aaron types `approve <code>`, and always denies `--no-verify` and plain force pushes. Source and tests in repo `claudecode-vm/mods/tier3-guard`. See project "Build a Tier 3 guard mod for Claude Code".

## Secrets (1Password, since 2026-10-05)

- `1password-cli` (apt, 1Password's repo) and service account `claudecode-vm`, which can only **read** the vault `Homelab - Claude`; writes are refused. Its token in `~/.config/homelab/op-service-account-token` (600) is the only credential on disk for the wrappers. Revoking the service account in 1Password cuts all of them off at once.
- `~/.local/bin/homelab-secret "<item>/<field>"` reads one field. `dockhand-api` and `unifi-api` call it on every run (commit 5cdd365). Aaron adds and rotates the items; Claude can't.
- Still on local files because of the Families-plan rate limits (1,000 requests/day per account): the TrueNAS key (relay timer every 5 min), the now-unused kb-export Notion token (`~/.config/kb-export/`, read-only; still used by the vault's `.kb/migrate.py --dry-run`) and `/etc/homelab-update.conf`. The ha-mcp URL comes from 1Password item `HA-MCP URL` too (since 2026-10-06, commit b4b398d): `.mcp.json` expands `${HA_MCP_URL}`, set by the ExecStart launcher `~/.local/bin/claude-remote-control-start`. If 1Password is down, Remote Control starts without the HA tools.

## Outbound SSH from this VM

Verified 2026-09-29: only to Plex (`ssh plex`, user `claude`) and GitHub (deploy keys for spriggs-homelab and, since 2026-10-22, obsidian-vault). **Not** to TrueNAS (never set up; its host key isn't in `known_hosts`; Claude uses the read-only API instead), HA (the SSH add-on exposes no port; Claude uses ha-mcp), or the wall panel Pi (no key; tracked in Open work).

## Homelab code repo (since 2026-09-27)

- Private repo [aaronspriggs/spriggs-homelab](https://github.com/aaronspriggs/spriggs-homelab), cloned at `~/homelab`. It holds scripts, units, compose files and config templates for every host; KB runbooks link to it.
- Push access: deploy key `~/.ssh/id_ed25519_github_spriggs_homelab` (write, this repo only), mapped to `github.com` in `~/.ssh/config`. Git identity "Claude Code (ClaudeCode VM)".
- Tools: `gitleaks` 8.30.1 (`/usr/local/bin`, upstream binary, not apt), `shellcheck`, `make`. Run `make setup` once per clone to enable the pre-commit hook; `make check` reports drift between deployed files and the repo.
- `~/homelab-agent` (Claude's working dir) is not a repo checkout, but what in it can't be regenerated is versioned in `claudecode-vm/` (since 2026-10-16, commit dc9d2ae): `CLAUDE.md` (symlink), `.mcp.json`, `.claude/settings.local.json` (deployed copy) and Claude Code's auto-memory (`~/.claude/projects/-home-aspriggs-homelab-agent/memory` is a symlink to `claudecode-vm/claude/memory`; commit after each memory write).
- SSH into this VM is key-only (`PasswordAuthentication no`).

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
