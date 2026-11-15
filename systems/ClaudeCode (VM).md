---
status: active
category: vm
ip: 192.168.1.156
runs_on:
- '[[TrueNAS SCALE (Big Boi)]]'
last_verified: 2026-11-15
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/claudecode-vm
notion_id: 3cf7ae76-22ba-81bc-9a3e-ed83c614d524
---

Claude Code Remote Control host (VM on Big Boi). SSH: ssh aspriggs@192.168.1.156 (key-only).

## Overview

Ubuntu Server VM on [Big Boi](<TrueNAS SCALE (Big Boi).md>) that gives Claude direct LAN access to the homelab. It hosts [Claude Code](<Claude Code (Remote Control service).md>) (the Remote Control service with its settings, hooks, mods and fix runs, in its own note since 2026-11-15), the clones of the KB vault and the code repo, and the timers and API helpers Claude works through. The disk isn't backed up: what matters is in the two GitHub repos and 1Password, and the VM is rebuilt from [Rebuild the ClaudeCode VM from scratch](<../runbooks/Rebuild the ClaudeCode VM from scratch.md>), in the order given by [Disaster recovery: rebuild order (index)](<../runbooks/Disaster recovery - rebuild order (index).md>).

## Access

- **SSH:** `ssh aspriggs@192.168.1.156`, key-only (`PasswordAuthentication no`). User aspriggs has sudo NOPASSWD. Authorized keys: aaronspriggs@Aarons-MacBook-Pro.local and aspriggs@mbp-017446; add more by appending to `~/.ssh/authorized_keys`.
- **Console:** SPICE on Big Boi (bound to 192.168.1.248, not 0.0.0.0), in VGA text mode.
- **Remote Control:** see the Claude Code note.

## Config

**VM definition** (read from the TrueNAS API 2026-11-15)

- Name `ClaudeCode`, autostart on. 1 vCPU × 2 cores × 1 thread (2 logical CPUs), CPU mode host passthrough, 8192 MB, UEFI, clock UTC.
- Disk: zvol `Big+Boi/vmstore/claudecode_disk`, 40 GiB, VirtIO.
- NIC: VirtIO on `br0`, MAC `00:a0:98:1e:c7:5c`. Trust Guest Filters must stay off; it doesn't work with bridge attachment.
- IP 192.168.1.156 comes from a UDM fixed-IP reservation on that MAC; the guest's netplan is plain DHCP. A rebuilt VM must reuse the MAC.

**Guest**

- Ubuntu Server 26.04.1 LTS, kernel 7.0.0-43 on 2026-11-15. Built from the cloud image with a cloud-init NoCloud seed, no installer: [Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE](<../runbooks/Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE.md>).
- Boots with `nomodeset`. `softdog` plus systemd `RuntimeWatchdogSec=2min` and `RebootWatchdogSec=5min` reboot the VM if PID 1 hangs. Files and deploy commands: repo `claudecode-vm/README.md`, "Deploy".
- Updates: enrolled in homelab-update, weekly on Sunday 04:30 America/Denver ([runbook](<../runbooks/homelab-update - weekly unattended VM updates (install, add a VM, troubleshoot).md>)). A reboot drops every Claude Remote Control session. Kuma monitors: `ClaudeCode VM` (ping) and `ClaudeCode VM Updates` (push).
- Installed beyond the base image: Node.js 24 (NodeSource LTS), `1password-cli` (1Password's apt repo), `python3-websocket` (for `truenas-api`), `shellcheck`, `make`, and `gitleaks` 8.30.1 in `/usr/local/bin` (upstream binary, not apt).

**Repos cloned here**

- KB vault at `~/obsidian-vault`: pushes with the deploy key `~/.ssh/id_ed25519_github_obsidian_vault` (write, that repo only) through the SSH alias `github-obsidian-vault`. Its pre-commit hook (`core.hooksPath .kb/hooks`) runs gitleaks and `.kb/check.py`. Aaron's reading copy is on his Mac at `~/Documents/Claude/obsidian-vault.nosync`, pulled from GitHub.
- Code repo at `~/homelab`: pushes with the deploy key `~/.ssh/id_ed25519_github_spriggs_homelab` (write, that repo only), mapped to `github.com` in `~/.ssh/config`. Layout, `deployed.tsv` and `make check`: [spriggs-homelab repo](<spriggs-homelab repo.md>).
- `~/kb-export`: the last Notion export (branch `kb-export`), kept as an archive. The export was retired on 2026-10-22 and its script and units were removed from the VM on 2026-11-15; they stay in the repo under `kb-export/`.

**Timers and helpers** (system units that run as aspriggs; no AI)

- `kb-sync-check.timer`, every 15 min: pushes the vault's state to the Kuma push monitor `KB Vault Sync`, which goes down when KB changes sit uncommitted or unpushed for over an hour. See repo `kb-sync-check/README.md`.
- `truenas-alert-relay.timer`, every 5 min: forwards TrueNAS alerts to HA. See [TrueNAS API access and alert relay](<../runbooks/TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM).md>).
- `plex-db-export.timer`, Sunday 23:00 America/Denver: `ssh plex sudo claude-maint plex-db-export`, the weekly Plex DB export for the B2 backup. See [Offsite backup to B2](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>).
- API helpers in `~/.local/bin` (not on the PATH of non-interactive shells, so call them by full path): `truenas-api`, `unifi-api`, `dockhand-api`, `arr-api`, `kuma-api`, `kuma-adopt`, `homelab-secret`; `scrypted-api` is in `~/.local/lib/scrypted-api`. The repo's `deployed.tsv` is the full list of deployed files.

**Secrets on disk** (names only; values in 1Password)

- `~/.config/homelab/op-service-account-token` (600): the token of the 1Password service account `claudecode-vm`, which can only read the vault `Homelab - Claude`. `homelab-secret "<item>/<field>"` reads one field with it, and the API helpers call it on every run (`truenas-api` only for `--write`). Aaron adds and rotates items. Revoking the service account cuts all of them off at once.
- Kept as local files because the Families plan allows 1,000 requests a day per account and these are read by timers: `~/.config/homelab/truenas-api-key`, `kb-sync-check-push-url`, `truenas-alert-relay.json` and `/etc/homelab-update.conf`.
- `~/.config/kb-export/notion-token`: read-only Notion token, unused except by the vault's `.kb/migrate.py --dry-run`. See [Revoke the unused kb-export Notion integration token](<../projects/Revoke the unused kb-export Notion integration token.md>).

**Outbound SSH** (checked 2026-11-15): only to Plex (`ssh plex`, user `claude`) and GitHub (the two deploy keys). Not to TrueNAS (never set up; Claude uses the API), not to HA (the SSH add-on exposes no port; Claude uses ha-mcp), and not to the wall panel Pi ([backlog task](<../projects/Give the ClaudeCode VM SSH access to the wall panel Pi.md>)).

## Dependencies

Runs on Big Boi (zvol on `vmstore`, see [Big Boi storage](<Big Boi storage (pool, datasets, shares, backups).md>); bridge `br0`) and needs the UDM for its address, GitHub for both repos, and 1Password for the helpers' credentials. What depends on it: Claude Code; TrueNAS alerts reaching HA (if the VM is down they aren't forwarded, and the relay's Kuma push monitor catches that within 15 min); the weekly Plex DB export (if it stops, Big Boi's Cloud Sync pre-script fails after 9 days and TrueNAS alerts).

## Decisions

- **2026-09:** built from a cloud image with a cloud-init seed instead of an installer, the first VM on Big Boi done that way.
- **2026-09-27:** `nomodeset` and the softdog watchdog, after the qxl framebuffer hung PID 1 for about 9.5 hours during an update reboot. softdog is loaded by a unit, not `modules-load.d`, because Ubuntu's kernel package blacklists watchdog drivers ([change](<../changes/2026-09-27 ClaudeCode VM - fix QXL shutdown hang (nomodeset) + softdog runtime watchdog.md>)).
- **2026-10-05:** helper credentials come from 1Password through one read-only service account; jobs on timers keep local files because of the plan's rate limit ([change](<../changes/2026-10-05 1Password CLI + read-only service account on ClaudeCode VM.md>)).
- **No disk backup:** the B2 offsite backup skips VM disks, so anything that can't be regenerated is committed to one of the two repos, and a rebuild is the recovery path.
- **2026-11-15:** the Claude Code half of this note moved to its own System note when the note passed 1,500 words.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]

## Related

Repo [claudecode-vm/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/claudecode-vm) (units, grub and watchdog config), [truenas/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas), [kb-sync-check/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/kb-sync-check), [backup/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/backup).
