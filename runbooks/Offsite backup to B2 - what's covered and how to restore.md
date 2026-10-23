---
kind: recovery
status: active
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
last_tested: 2026-10-16
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/backup
notion_id: 3fb7ae76-22ba-8139-858b-e106825c83ca
---

# Offsite backup to B2: what's covered and how to restore

What the two TrueNAS Cloud Sync tasks send to Backblaze B2 nightly, and how to pull it back (single files or a full rebuild) and put each item back in place.

## When to use

Data on Big Boi is lost or corrupted beyond what the 30-day local ZFS snapshots can fix (pool loss, hardware loss, fire/theft), or a snapshot doesn't have what you need. For anything inside the last 30 days with the pool intact, restore from a ZFS snapshot first: it's faster.

## What's covered

Bucket `spriggs-bigboi-backup`, encrypted by TrueNAS (contents only; file names are visible). B2 keeps prior versions 30 days. Design and exact task settings: repo [`backup/README.md`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/backup/README.md).

| Bucket folder | Task (schedule) | Contents |
| --- | --- | --- |
| `/BIGBOI` | `B2 offsite: BIGBOI` (daily 01:00) | `Media Library` (personal photos/videos), `servarr` (only `overseerr/`, Seerr's live config, since 2026-10-16), `uptime-kuma`, `autokuma`, `plex_config` (old TrueNAS-app Plex config, not live) |
| `/vmstore/dockhand-stacks-backup` | `B2 offsite: vmstore` (daily 01:15) | Dockhand stack dirs, copied nightly 23:30 by the TrueNAS cron. Holds the **live** servarr app configs (gluetun, nzbget, prowlarr, sonarr, radarr), including each app's own `Backups/scheduled` zips. Skips `logs/` and Prowlarr's `Definitions/` (since 2026-10-23). Its raw `*.db` files are copied while the apps run and may be torn; use the staged copies instead. |
| `/vmstore/offsite-staging` | same, written by the task's pre-script just before upload | `truenas-config.tar` (config DB + secret seed), `dockhand.db.gz`  • `dockhand.encryption_key`, `kuma.db`, `sonarr.db` • `radarr.db` • `prowlarr.db` (consistent copies, since 2026-10-23), `plex-db.tar.gz` (Plex library + blobs DB and `Preferences.xml`, exported weekly Sunday 23:00) |

Not covered: `plex_content` (phase 2 for self-ripped discs), DVR recordings, VM disks (HA backs itself up to Google Drive; the Plex and ClaudeCode VMs are rebuilt from their runbooks).

## Prerequisites

- 1Password item **Backblaze B2 - truenas-bigboi** (Aaron's vault): keyID, applicationKey, **encryption password and salt**. Without the password and salt nothing in the bucket can be read.
- B2 web login (2FA in Proton Authenticator), for browsing versions.
- A TrueNAS install with a pool to restore into (or any machine with rclone, see step 6).

## Steps

1. If the credential is gone (fresh TrueNAS): Credentials → Backup Credentials → Cloud Credentials → Add, provider Backblaze B2, name `B2 truenas-bigboi`, keyID and applicationKey from 1Password, Verify.
2. Make an empty scratch folder in System → Shell: `mkdir -m 700 "/mnt/Big Boi/vmstore/restore"` (any path on the pool works).
3. Data Protection → Cloud Sync Tasks → on the task that holds the data, **Restore** (if the tasks are gone, Add a task with Direction PULL, Transfer Mode COPY, the bucket folder from the table, Remote Encryption on, Filename Encryption off, and the password and salt). Transfer Mode **COPY**, destination the scratch folder. The new task is created disabled. **Run Now**.
4. Put things back from the scratch folder, with the app stopped:
    - **TrueNAS config:** System → General Settings → Manage Configuration → Upload File → `truenas-config.tar`. TrueNAS reboots.
    - **Dockhand:** stop the `dockhand` app, `gunzip dockhand.db.gz`, replace `/mnt/.ix-apps/app_mounts/dockhand/data/db/dockhand.db` (delete the old `-wal`/`-shm` next to it), put `dockhand.encryption_key` back as `data/.encryption_key`, copy `dockhand-stacks-backup/*` into `data/stacks/`, start the app. Stack compose files are also in the repo `stacks/`.
    - **Servarr apps:** with the stack stopped, copy the app's dir from `dockhand-stacks-backup/Big Boi/servarr/<app>` back into the stack dir, then replace `<app>.db` with the staged `offsite-staging/<app>.db` and delete `<app>.db-wal`/`-shm` (Sonarr, Radarr, Prowlarr; the staged copy is from that night's 01:15 run, the raw one may be torn). Logs and Prowlarr's indexer definitions aren't backed up; Prowlarr re-downloads definitions on start. Fallback: start the app fresh and use its System → Backup → Restore with the newest `Backups/scheduled/*.zip` (weekly, so up to 7 days old).
    - **Uptime Kuma:** stop the stack, replace `BIGBOI/uptime-kuma/kuma.db` with the staged `kuma.db` (delete `kuma.db-wal`/`-shm`), start. AutoKuma recreates labelled monitors anyway.
    - **Plex:** on the Plex VM, `sudo systemctl stop plexmediaserver`, extract `plex-db.tar.gz`, copy the two `.db` files into `.../Plex Media Server/Plug-in Support/Databases/` and `Preferences.xml` into `.../Plex Media Server/`, delete the old `-wal`/`-shm`, `chown plex:plex` them, start Plex. The tar is reachable from the Plex VM if restored under `plex_recordings` (mounted at `/mnt/dvr`); otherwise scp it.
    - **Media Library / other files:** copy back to `BIGBOI`.
5. Delete the restore task and the scratch folder when done.
6. Without TrueNAS: rclone on any machine. Config: a `b2` remote (keyID, applicationKey), and a `crypt` remote on `b2:spriggs-bigboi-backup/vmstore` (or `/BIGBOI`) with `filename_encryption = off`, `directory_name_encryption = false`, password and salt from 1Password (entered via `rclone config`, which obscures them). Then `rclone copy crypt: ./restore`. To get an older version, use the B2 web UI's file versions or rclone's `--b2-versions`.

## Verify

The restore task ends SUCCESS with the expected file count. Compare sizes with the source if it still exists (Claude can do this over the TrueNAS API). Tested 2026-10-16: restore of `/vmstore` (1,124 files, 430 MiB) matched every original by size; only two symlinks were skipped by design (Follow Symlinks is off).

## Rollback

Restores land in a scratch folder, so nothing is overwritten until you copy files into place. Before copying over live data, take a manual ZFS snapshot of the target dataset (Claude can, via `truenas-api --write zfs.snapshot.create`).
