---
status: active
category: hardware
ip: 192.168.1.248
url: https://192.168.1.248:9443/
last_verified: 2026-09-28
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas
notion_id: 2ff7ae76-22ba-8153-8df1-d4ca673fae00
---

NAS + hypervisor (Big Boi). i9-9900, 64 GB, RAIDZ1 5x 4 TB SSD. Hosts HA, Plex and ClaudeCode VMs plus Dockhand.

## Overview

"Big Boi": the homelab's NAS and hypervisor, a 2U rackmount box running TrueNAS SCALE. It holds all primary storage, serves the Plex media over NFS/SMB, and runs the three VMs and the Dockhand app. Everything below verified live via the read-only API on 2026-09-28 unless dated otherwise.

## Access

- **Web UI:** [https://192.168.1.248:9443/](https://192.168.1.248:9443/) (hostname `truenas`, domain `local`). Admin user `truenas_admin` (UID 950, FULL_ADMIN; 2FA not configured as of 2026-09-28); password in 1Password item **"TrueNAS - Admin"**.
- **SSH:** user `aspriggs`.
- **Claude (read-only):** local user `claude-readonlyapi` (renamed from `claude` 2026-10-14; UID 3002, no password, nologin shell, no sudo) in a group with the Read-Only Administrator privilege. User-linked API key `claude-readonly`, **no expiry**, stored only on the ClaudeCode VM at `~/.config/homelab/truenas-api-key` (600). Client `~/.local/bin/truenas-api <method> '<json>'` ([repo: truenas/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas)). Write test (`alert.dismiss`) returns EACCES. Setup and rotation: [TrueNAS API runbook](<../runbooks/TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM).md>).
- **Claude (maintenance, since 2026-10-14):** local user `claude-maint` (no password, nologin), privilege "Claude Maintenance" (`READONLY_ADMIN`, `APPS_WRITE`, `VM_WRITE`, `SYSTEM_UPDATE_WRITE`, `POOL_SCRUB_WRITE`, and `SNAPSHOT_WRITE`/`SNAPSHOT_DELETE` since 2026-10-15). Key in 1Password **TrueNAS API Key (claude-maint)**, read at run time, never on disk. Used only via `truenas-api --write`, which allowlists app upgrade/restart, VM start/stop/restart, TrueNAS OS updates and manual snapshot create/delete (Tier 2; never `auto-*`, no rollback). Change-authority tiers apply unchanged. Same runbook.
- **API gotchas (25.04):** REST is deprecated; use JSON-RPC over `wss://192.168.1.248:9443/api/current`. A user-linked key is **auto-revoked if it's ever sent over plain HTTP**, so the client is hard-coded to WSS. Read-Only Administrator keys get 403 on legacy REST. Method names: `zfs.snapshot.query` (not `pool.snapshot.query`), `update.check_available`.

## Config

**Hardware**
- CPU Intel Core i9-9900 (8C/16T, since 2026-03-04); UHD 630 iGPU passed through to the Plex VM.
- RAM 64 GB (non-ECC), Corsair Vengeance LPX 2×32 GB DDR4-3600.
- Board ASRock Z390M-ITX/ac (Mini-ITX, LGA1151) in a MyElectronics 19" 2U Mini-ITX rack case (225 mm deep); PSU Corsair SF750 Platinum, 2018 model CP-9020186 (standard SFX, 125 × 63.5 × 100 mm; takes Corsair Type 4 modular cables only; 3 "Peripheral & SATA" modular sockets, shipped with 2× 4-connector SATA cables + 1× 3-connector Molex cable; SFX-L corrected 2026-10-11 per Aaron). 10 GbE card: 10Gtek Intel 82599EN SFP+, low-profile. (From the 2026-03 build notes; not readable via the API.)
- Boot: Patriot P300 128 GB NVMe.
- Network: `enp1s0` 10 GbE DAC to USW Pro Max 16 PoE SFP+ 2, bridged as `br0` (192.168.1.248, gateway/DNS 192.168.1.1). Onboard `eno1` and `enp2s0` are unplugged.
**Software:** TrueNAS SCALE 25.04.2.6 (Fangtooth), no update pending. Timezone `America/Denver` (set 2026-10-15; was `America/Los_Angeles`), so the snapshot tasks and the stack-backup cron below run on Mountain time. Up since 2026-07-05.
**Pool ****`Big Boi`**** (ONLINE, healthy):** one RAIDZ1 vdev of 5× Samsung 870 EVO 4 TB SATA SSD (sda–sde). 20.0 TB raw; 2.3 TB used, 13.5 TB available to datasets. Last scrub 2026-09-20, 0 errors. Only alert: NOTICE that ZFS feature flags can be upgraded; that upgrade is one-way (blocks rolling TrueNAS back), so leave it unless a release needs it.
**Datasets and zvols**

| Path | Type | Used | Role |
| --- | --- | --- | --- |
| `Big Boi/vmstore` | filesystem | 187 GB | VM zvols (POSIX ACL, mode Discard); also holds `dockhand-stacks-backup/` |
| `vmstore/haos_disk` | zvol | 44 GB | Home Assistant OS VM disk (128 GiB) |
| `vmstore/Plex-9wert` | zvol | 77 GB | Plex VM disk |
| `vmstore/claudecode_disk` | zvol | 62 GB | ClaudeCode VM disk |
| `Big Boi/BIGBOI` | filesystem | 2.11 TB | Shared data (SMB share `BIGBOI`) |
| `BIGBOI/plex_content` | filesystem | 2.11 TB | Plex media library |
| `BIGBOI/plex_recordings` | filesystem | 0.8 GB | Plex DVR recordings |
| `BIGBOI/plex_config` | filesystem | 0.3 GB | Leftover from when Plex ran as a TrueNAS app; cleanup tracked in Open work |
| `Big Boi/ix-apps` | hidden | — | TrueNAS apps (Dockhand); not in any snapshot task (see Decisions) |

**Shares**
- NFS `/mnt/Big Boi/BIGBOI/plex_content`: read-only, hosts `192.168.1.116` only. Mounted on the Plex VM at `/mnt/media`.
- NFS `/mnt/Big Boi/BIGBOI/plex_recordings`: read-write, hosts `192.168.1.116` only. Mounted on the Plex VM at `/mnt/dvr`.
- SMB `BIGBOI`: the whole `/mnt/Big Boi/BIGBOI` dataset.
**Data protection**
- Periodic snapshot tasks, both recursive, daily 00:00, naming `auto-%Y-%m-%d_%H-%M`, keep 30 days (retention re-verified 2026-10-15): `Big Boi/vmstore`, and `Big Boi/BIGBOI` **excluding** `plex_content` and `plex_recordings`.
- Offsite (since 2026-10-16): Cloud Sync tasks to Backblaze B2 bucket `spriggs-bigboi-backup`, credential `B2 truenas-bigboi` (keys, encryption password and salt in 1Password **Backblaze B2 - truenas-bigboi**, Aaron's vault). `B2 offsite: BIGBOI` (daily 01:00: `Media Library`, `servarr`, `uptime-kuma`, `autokuma`, `plex_config`) and `B2 offsite: vmstore` (daily 01:15: `dockhand-stacks-backup` and `offsite-staging`). Both PUSH/SYNC, remote encryption on, filename encryption off. The vmstore task's pre-script ([repo: backup/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/backup)) stages the TrueNAS config, the Dockhand and Uptime Kuma DBs and the weekly Plex DB export (from `plex_recordings/.plex-db-export`) into `vmstore/offsite-staging`. Restore: [Offsite backup to B2 runbook](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>).
- Cron (root, daily 23:30): `rsync -a --delete --chmod=D700,F600 /mnt/.ix-apps/app_mounts/dockhand/data/stacks/ "/mnt/Big Boi/vmstore/dockhand-stacks-backup/"` copies Dockhand's stack dirs into snapshotted `vmstore`. These include the servarr `.env` with VPN secrets and the live gluetun, nzbget, prowlarr, sonarr and radarr configs (mounted `./<app>` relative to the stack). `BIGBOI/servarr` holds only `overseerr/` (Seerr's live config) since the stale copy was removed 2026-10-16; manual snapshot `BIGBOI@pre-servarr-cleanup-2026-10-16` keeps it. The Dockhand app still bind-mounts `BIGBOI/servarr` at `/stacks`, an unused install leftover.
- S.M.A.R.T. tests configured 2026-03-07.
- Rebuild from bare metal (config from the nightly `truenas-config.tar`): [Rebuild Big Boi (TrueNAS) from bare metal](<../runbooks/Rebuild Big Boi (TrueNAS) from bare metal.md>).
**Services enabled (2026-10-16):** SMB, NFS, SSH (password auth on, port 22), S.M.A.R.T., and UPS as a NUT client (mode SLAVE) of 192.168.1.12.
**Certificates:** web UI uses `truenas-cert` from the internal CA `truenas-ca` (RSA 4096, CN `truenas.local`, SANs 192.168.1.248 / truenas.local / [truenas.thespriggs.com](http://truenas.thespriggs.com/)), valid to 2035-03-15. The expired self-signed `truenas_default` was deleted 2026-09-26.
**ACLs:** datasets use the ACL model. Plex/app access = group `apps` gets traverse on `BIGBOI` and read + traverse on `plex_content`, applied recursively in the UI ACL editor. `chmod -R` on these datasets fails with "Operation not permitted"; use the UI.
**Path quirks (pool name has a space):**
- Shell: always quote, e.g. `"/mnt/Big Boi/..."`.
- Device paths: space becomes `+`, e.g. `/dev/zvol/Big+Boi/vmstore/haos_disk`.
- fstab/mount: escape as `\040`, e.g. `Big\040Boi`.
- VM images: import into a zvol rather than booting a qcow2: `qemu-img convert -O raw <image.qcow2> /dev/zvol/Big+Boi/vmstore/<zvol_name>`.
- `br0` must persist for VMs to reach the LAN. It rolled back once during "Test Changes" when first created; check VM connectivity after any network change.

## Dependencies

**Hosts (all autostart):**

| Guest | Kind | IP | vCPU threads / RAM | Notes |
| --- | --- | --- | --- | --- |
| [Home Assistant OS (VM)](<Home Assistant OS (VM).md>) | VM | 192.168.1.218 | 2 / 4 GiB | USB passthrough |
| [Plex Media Server](<Plex Media Server.md>) | VM | 192.168.1.116 | 16 / 12 GiB | iGPU (PCI) passthrough |
| [ClaudeCode (VM)](<ClaudeCode (VM).md>) | VM | 192.168.1.156 | 2 / 8 GiB | Claude Code Remote Control host |
| [Dockhand](<Dockhand.md>) | TrueNAS app | :3001 | — | 1.1.38 (2026-10-16); runs the `servarr` and `uptime-kuma` (:3002) stacks |

If Big Boi goes down, all of the above go down with it.

## Decisions

- **2026-02-06:** Pi-hole and nginx-proxy-manager removed as TrueNAS apps; if they come back, they go on a VM or separate hardware (see Open work).
- **2026-03-04:** upgrade limited to a CPU swap (i5-9400 → i9-9900, same board). No new case or board, and no discrete GPU: the UHD 630 handles Plex transcoding. If AV1 encode or local LLMs become real needs, rethink with a 16 GB+ low-profile card (e.g. Intel Arc Pro B50) rather than a media-only card. Details: Done project "Big Boi Server Upgrade — CPU Swap (i9-9900)".
- **2026-10-15 (Aaron):** two-tier storage *inside Big Boi*. Rebuild into a new case with an HDD pool for bulk media, while this SSD pool keeps VMs, containers, apps and configs. A possible offsite TrueNAS box would receive ZFS replication. This replaces the 2026-03-03 UniFi UNAS Pro plan. See [Rebuild Big Boi into a new case with an HDD pool](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>).
- **2026-09-26:** `ix-apps` isn't snapshotted; instead of snapshotting a TrueNAS-managed hidden dataset, the nightly rsync copies Dockhand's stacks into `vmstore`. `BIGBOI` was rejected as the destination because it's SMB-shared.
- **2026-09-28:** NFS exports have always been restricted to the Plex VM by `hosts` (the 2026-09-26 note only read `networks`); no change needed.
- **Open:** the media library (`plex_content`, `plex_recordings`) is excluded from snapshots and has no offsite copy; self-ripped discs are phase 2 of the backup strategy project.

## Related

- Runbooks: [Big Boi Reboot Checklist](<../runbooks/Big Boi Reboot Checklist.md>), [Creating a Cloud-Init Seeded Linux VM](<../runbooks/Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE.md>), [Creating an Appliance-Image VM (e.g. HAOS)](<../runbooks/Creating an Appliance-Image VM (e.g. HAOS) on TrueNAS SCALE.md>), [Plex VM NFS Mount Setup](<../runbooks/Plex VM NFS Mount Setup & Troubleshooting.md>), [TrueNAS read-only API and alert relay](<../runbooks/TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM).md>), [Offsite backup to B2](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>).
- Repo: [truenas/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas) (`truenas-api`, `truenas-alert-relay` + systemd timer, deployed on the ClaudeCode VM).

## Open work

![[Projects.base#Open for this system]]

## Runs on this

![[Systems.base#Runs on this]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
