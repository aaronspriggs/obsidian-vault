---
date: 2026-11-09
type: fix
system:
- '[[Plex Media Server]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/5b91942
---

# Removed the dead Plex apt repo from the Plex VM; weekly updates working again

## What changed

Aaron removed `/etc/apt/sources.list.d/plexmediaserver.list`, `/usr/share/keyrings/plex.gpg` and `/etc/apt/apt.conf.d/52unattended-upgrades-plex` from the Plex VM and ran `homelab-update run` by hand. It succeeded: 16 Ubuntu packages, Plex 1.43.4.10903 → 1.43.5.11079, reboot from kernel 6.8.0-147 to 6.8.0-149, 7/7 checks passed. The repo dropped `plex-vm/apt/52unattended-upgrades-plex` and its `deployed.tsv` line, and the Plex system note and both Plex runbooks no longer mention the repo.

## Why

`https://downloads.plex.tv/repo/deb` stopped serving a Release file, so `apt-get update` failed and homelab-update quit at its first step on Oct 25, Nov 1 and Nov 8. With no successful run since Oct 18, the Kuma push monitor `Plex VM Updates` went down after its 8-day window and `alert2.homelab_plex_vm_updates_missed` fired "heartbeat missed" on 2026-11-09. The repo was already stale (stuck at 1.42.2) and unused: Plex updates come from `claude-maint upgrade-plex` via plex.tv's download API.

## How

See [homelab-update runbook](<../runbooks/homelab-update - weekly unattended VM updates (install, add a VM, troubleshoot).md>), Troubleshooting. The first try failed silently because Aaron's Mac was on a non-home VPN and couldn't reach 192.168.1.116; nothing reached the VM.
