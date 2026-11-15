---
status: active
category: software
runs_on:
- '[[TrueNAS SCALE (Big Boi)]]'
last_verified: 2026-11-15
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/backup
---

Big Boi's storage: the SSD pool `Big Boi`, its datasets and VM disks, the NFS and SMB shares, snapshots, the nightly offsite sync to Backblaze B2, and disk health checks.

## Overview

The storage side of [Big Boi](<TrueNAS SCALE (Big Boi).md>): one ZFS pool of five SSDs that holds the VM disks, the shared data and the Plex media, with its shares and its data protection. The box itself (hardware, network, TrueNAS, logins and API access, the guests) is in Big Boi's note. A second pool of HDDs for bulk media is planned in [Rebuild Big Boi](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>). Split from Big Boi's note on 2026-11-15; changes before that date are listed under Big Boi. Checked on 2026-11-15 through the read-only API unless dated otherwise.

## Access

- **Aaron:** the TrueNAS UI's Storage, Shares and Data Protection pages (login in Big Boi's note), and the SMB share `BIGBOI` at `smb://192.168.1.248/BIGBOI`.
- **Plex VM:** the two NFS exports below; it is the only host allowed.
- **Claude:** reads through `truenas-api` (`pool.query`, `pool.dataset.query`, `zfs.snapshot.query`, `pool.snapshottask.query`, `cloudsync.query`). With `--write` it can create and delete manual snapshots (Tier 2; the allowlist is in Big Boi's note). Pool, dataset and snapshot-task changes, rollbacks and VM disk operations are Tier 3.
- **Backblaze B2:** bucket `spriggs-bigboi-backup`, TrueNAS credential `B2 truenas-bigboi`. The keys, the encryption password and the salt are in the 1Password item **Backblaze B2 - truenas-bigboi** (Aaron's vault, not Claude's).

## Config

**Pool `Big Boi`** (ONLINE, healthy): one RAIDZ1 vdev of 5× Samsung 870 EVO 4 TB SATA SSD (`sda`–`sde`). 20.0 TB raw, 2.95 TB allocated; datasets use 2.44 TB and have 13.40 TB available. A scrub is scheduled weekly on Sunday at 00:00 and runs when the last one is 35 days old; the last finished on 2026-10-25 with 0 errors. TrueNAS shows a NOTICE that the pool's ZFS feature flags can be upgraded. That upgrade is one-way and blocks rolling TrueNAS back, so leave it unless a release needs it.

**Datasets and zvols** (decimal units; "used" includes snapshots)

| Path | Type | Used | Role |
| --- | --- | --- | --- |
| `Big Boi/vmstore` | filesystem | 320 GB | VM disks (POSIX ACL); also the directories `dockhand-stacks-backup/` and `offsite-staging/` |
| `vmstore/haos_disk` | zvol, 128 GiB | 52 GB (35 GB snapshots) | [Home Assistant OS VM](<Home Assistant OS (VM).md>) disk |
| `vmstore/Plex-9wert` | zvol, 32 GiB | 188 GB (148 GB snapshots) | [Plex VM](<Plex Media Server.md>) disk |
| `vmstore/claudecode_disk` | zvol, 40 GiB | 73 GB (13 GB snapshots) | [ClaudeCode VM](<ClaudeCode (VM).md>) disk |
| `Big Boi/BIGBOI` | filesystem | 2.11 TB | Shared data (NFSv4 ACL), SMB share `BIGBOI` |
| `BIGBOI/plex_content` | filesystem | 2.11 TB | Plex media library; servarr downloads into it |
| `BIGBOI/plex_recordings` | filesystem | 0.9 GB | Plex DVR recordings, and the weekly Plex database export |
| `BIGBOI/plex_config` | filesystem | 0.3 GB | Left from when Plex ran as a TrueNAS app (`Library/`, `Codecs/`; nothing mounts it, checked 2026-11-15); [cleanup](<../projects/Verify-clean up plex_config dataset.md>) is in the backlog |
| `Big Boi/ix-apps` | hidden | — | TrueNAS apps (Dockhand); in no snapshot task (see Decisions) |

`BIGBOI` also holds plain directories: `Media Library` (personal photos and videos), `servarr` (only `overseerr/`, Seerr's live config, since 2026-10-16), `uptime-kuma` and `autokuma`.

**Shares**

- NFS `/mnt/Big Boi/BIGBOI/plex_content`: read-only, host 192.168.1.116 only; the Plex VM mounts it at `/mnt/media`.
- NFS `/mnt/Big Boi/BIGBOI/plex_recordings`: read-write, host 192.168.1.116 only; mounted at `/mnt/dvr`. Mount setup: [Plex VM NFS runbook](<../runbooks/Plex VM NFS Mount Setup & Troubleshooting.md>).
- SMB `BIGBOI`: the whole `/mnt/Big Boi/BIGBOI` dataset.

**ACLs:** apps and Plex get in through the group `apps`, which has traverse on `BIGBOI` and read plus traverse on `plex_content`, applied recursively in the UI's ACL editor. `chmod -R` on these datasets fails with "Operation not permitted"; use the UI.

**Snapshots:** two periodic tasks, both recursive, daily at 00:00, named `auto-%Y-%m-%d_%H-%M`, kept 30 days: `Big Boi/vmstore`, and `Big Boi/BIGBOI` without `plex_content` and `plex_recordings`. 208 snapshots exist. Manual ones still held: only TrueNAS's own on `ix-apps` (`1.1.4`, `1.1.34` and `ix-apps-backup-system-update--2026-01-19`). The three `pre-dockhand-1.1.38`, the three `pre-dockhand-update-2026-09-26` and `BIGBOI@pre-servarr-cleanup-2026-10-16` were deleted on 2026-11-15.

**Offsite (since 2026-10-16):** two Cloud Sync tasks push to B2, both PUSH/SYNC with remote encryption on and filename encryption off: `B2 offsite: BIGBOI` daily at 01:00 and `B2 offsite: vmstore` daily at 01:15. Both succeeded on 2026-11-15. The vmstore task runs a pre-script (repo [backup/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/backup)) that stages the TrueNAS config and the app databases into `vmstore/offsite-staging`. What each task uploads and how to restore it: [Offsite backup to B2 runbook](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>).

**Stacks copy:** a root cron job, daily at 23:30, rsyncs Dockhand's stack directories from `ix-apps` into `vmstore/dockhand-stacks-backup/`, so they are snapshotted and go offsite; they include the servarr `.env` with the VPN secrets and the live app configs. The command is in the repo's [truenas/README.md](https://github.com/aaronspriggs/spriggs-homelab/blob/main/truenas/README.md) and matched the live job on 2026-11-15 (it excludes `logs/` and `Definitions/`).

**Disk health:** S.M.A.R.T. tests on all disks: SHORT weekly on Sunday at 00:00, LONG monthly on the 1st at 01:00.

**Path quirks (the pool name has a space):**

- Shell: always quote, `"/mnt/Big Boi/..."`.
- Device paths: the space becomes `+`, `/dev/zvol/Big+Boi/vmstore/haos_disk`.
- fstab and mount: escape it as `\040`, `Big\040Boi`.

## Dependencies

Lives on Big Boi's five SATA SSDs and goes down with the box. The offsite sync needs the internet and Backblaze B2. What depends on it: the three VMs' disks, Plex's media and recordings over NFS, the servarr stack's downloads and Seerr's config, [Dockhand](<Dockhand.md>)'s stack copy, and every restore in the [disaster recovery index](<../runbooks/Disaster recovery - rebuild order (index).md>).

## Decisions

- **2026-09-26:** `ix-apps` isn't snapshotted. Instead of snapshotting a hidden dataset that TrueNAS manages, the nightly rsync copies Dockhand's stacks into `vmstore`. `BIGBOI` was rejected as the destination because it is SMB-shared.
- **2026-09-28:** the NFS exports have always been restricted to the Plex VM by `hosts` (a 2026-09-26 note had only read `networks`); nothing to change.
- **2026-10-16:** offsite is Backblaze B2 for the small irreplaceable set, encrypted by TrueNAS; scope and reasons are in [Plan backup strategy for TrueNAS and VMs](<../projects/Plan backup strategy for TrueNAS and VMs.md>).
- **Open:** the media library (`plex_content`, `plex_recordings`) is left out of snapshots and has no offsite copy; the self-ripped discs are phase 2 of that project.
- **2026-11-15:** split from Big Boi's note ([change](<../changes/2026-11-15 Split the Big Boi System note into the box and its storage.md>)). Storage is where the open backup, dataset and rebuild work lands; the box's own facts rarely change.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]

## Related

- Repo: [backup/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/backup) (the Cloud Sync pre-script and the weekly Plex database export timer) and [truenas/README.md](https://github.com/aaronspriggs/spriggs-homelab/blob/main/truenas/README.md) (the stacks cron).
- Rebuilding the pool's host: [Rebuild Big Boi (TrueNAS) from bare metal](<../runbooks/Rebuild Big Boi (TrueNAS) from bare metal.md>).
