---
date: 2026-10-23
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project: '[[Plan backup strategy for TrueNAS and VMs]]'
---

## What changed

No system changes. The Layer 2 status as of 2026-10-23 with the one-week bucket estimate, the source sizes and provider prices of 2026-10-15, and the phase 1 plan with its steps as completed. Moved here on 2026-11-15 from the [project](<../projects/Plan backup strategy for TrueNAS and VMs.md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

The bucket estimate is what led to the same day's fix ([change](<2026-10-23 B2 vmstore sync stages consistent servarr DBs and skips logs.md>)), and that note points here for the detail.

## How

### Status as of 2026-10-23

Layer 1 is done and verified: the daily snapshots keep 30 days. S.M.A.R.T. is covered (see checklist). **Layer 2 phase 1 is live:** two Cloud Sync tasks push nightly to B2 bucket `spriggs-bigboi-backup` (`B2 offsite: BIGBOI` 01:00, `B2 offsite: vmstore` 01:15). First runs 2026-10-16: 2.0 GiB + 430 MiB, both SUCCESS; a test restore of `/vmstore` matched every file. How to restore: runbook [Offsite backup to B2: what's covered and how to restore](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>). **Bucket size check 2026-10-23** (from TrueNAS job history, `core.get_jobs` for `cloudsync.sync`; Claude has no B2 credentials, so this is an estimate, not B2's own number): first runs uploaded 2.42 GiB, and the seven nightly runs since added 1.58 GiB (BIGBOI ~20 MiB/night, vmstore ~205 MiB/night, 257 MiB on 10-23). With every prior version still inside the 30-day window, the bucket holds about 4.0 GiB (4.3 GB). At about 225 MiB/night of churn the 30-day steady state is roughly 2.45 GiB current + 6.6 GiB prior versions, about 9.8 GB, right at the 10 GB free tier; any overage costs under $0.01/month at $6.95/TB. About 71 MiB of the vmstore churn is the staged DBs and Plex export (real changes); the rest is `dockhand-stacks-backup`, which holds the live servarr configs (compose `./sonarr:/config` etc.). Traced 2026-10-23: of its 1,121 files (360 MiB), ~290 MiB is rotating `logs/*.debug.N.txt` that renumber on every rollover, and Prowlarr rewrites its 670 `Definitions/` files daily, so most of both re-upload nightly; only ~39 MiB (DBs, current logs) really changes. Also found: `sonarr.db`/`radarr.db`/`prowlarr.db` are copied raw by rsync while the apps run (WAL mode, e.g. a 3.9 MB `sonarr.db-wal` at copy time), so the raw copy may not be consistent; the apps' own weekly `Backups/scheduled` zips are consistent but up to 7 days old. `plex-db.tar.gz` is re-staged with a new mtime every night (plain `cp`), so its 26 MiB re-uploads on the six nights it hasn't changed. **Fixed the same day** (Aaron approved): the pre-script now `sqlite_copy`s the three *arr DBs into staging and uses `cp -p` for the Plex export, and the 23:30 rsync skips `logs/` and `Definitions/`; first run uploaded 24 files / 119 MiB. See [[2026-10-23 B2 vmstore sync stages consistent servarr DBs and skips logs]]. Left: phase 2 (rips).

### Sizes for Layer 2 (live, 2026-10-15) and prices

- Personal photos and videos: `BIGBOI/Media Library/` (`2025/`, `Ouray 2020/`), about 0.8 GB.
- Configs on the `BIGBOI` root: `servarr/`, `uptime-kuma/`, `autokuma/`, plus the `plex_config` dataset (0.3 GB). The `BIGBOI` dataset holds about 2 GB outside `plex_content`. `servarr/` holds only `overseerr/` (Seerr's live config) since 2026-10-16.
- `vmstore/dockhand-stacks-backup/` (about 355 MB): Dockhand stack dirs, including the servarr `.env` with the WireGuard key and the **live** gluetun, nzbget, prowlarr, sonarr and radarr configs (they mount `./<app>` relative to the stack).
- Plex database and metadata: inside the Plex VM at `/var/lib/plexmediaserver` on its 15 GB root LV (5.1 GB used in total, so a few GB at most). It's a zvol, so Cloud Sync can't reach it directly; it needs an export onto a dataset first. **Corrected 2026-10-15:** the `Databases` directory is world-readable (library DB 12 MB, blobs 25 MB, plus Plex's own dated backups every 3 days); only `Preferences.xml` is root/plex-only.
- TrueNAS system config: on the boot pool, so it needs a scheduled export onto a dataset.
- `plex_content` (2.11 TB): `Movies/`, `TV Shows/`, `downloads/`. Self-ripped Blu-rays are **mixed into** `Movies/` with Servarr content, so their size is unknown until they're identified.
Everything except the rips adds up to well under 10 GB.
**Prices checked 2026-10-15** ([Backblaze](https://www.backblaze.com/cloud-storage/pricing), [Cloudflare R2](https://developers.cloudflare.com/r2/pricing/), [Wasabi minimums](https://docs.wasabi.com/docs/how-does-wasabis-minimum-storage-duration-policy-work)):
- **B2:** $6.95/TB/month, first 10 GB free, no minimum storage duration, free egress up to 3× stored.
- **R2:** $15/TB/month, 10 GB free, no egress fees.
- **Wasabi:** $7.99/TB/month, with a 1 TB minimum charge and a 90-day minimum storage duration.

### Plan: Layer 2 phase 1 (2026-10-15)

**Aaron (B2 account and credentials, Tier 3):**
1. Create a Backblaze B2 account, with 2FA in Proton Authenticator.
2. Create a bucket, e.g. `spriggs-bigboi-backup`: Private, Default Encryption off (TrueNAS encrypts), Object Lock off.
3. Bucket Lifecycle Settings: "Keep prior versions for this number of days" = 30.
4. Create an application key `truenas-bigboi`: this bucket only, Read and Write, with "Allow List All Bucket Names" ticked. Save the keyID and applicationKey in a 1Password item (e.g. "Backblaze B2 - truenas-bigboi") in Aaron's own vault, not "Homelab - Claude".
5. Generate a TrueNAS remote-encryption password and salt, and store both in the same item. Without them a restore is impossible.
**Claude (steps 1–3 done 2026-10-15, commit **[**4d8fb33**](https://github.com/aaronspriggs/spriggs-homelab/commit/4d8fb33)**; design and exact task settings in repo ****`backup/README.md`****):** two tasks, `B2 offsite: BIGBOI` (01:00) and `B2 offsite: vmstore` (01:15), because the TrueNAS folder picker only multi-selects within one parent. The vmstore task's **pre-script** replaces the separate TrueNAS config cron and the Dockhand cron widening: it stages the TrueNAS config tar, consistent copies of `kuma.db` and `dockhand.db` (gzipped; it is **2.19 GB**, not a few MB) plus Dockhand's `.encryption_key`, and the Plex export into `vmstore/offsite-staging`, and fails the run (TrueNAS alert) if the Plex export is over 9 days old. Plex: `claude-maint plex-db-export` copies Plex's newest own backup and `Preferences.xml` to `plex_recordings/.plex-db-export` over the existing NFS mount; `plex-db-export.timer` on the ClaudeCode VM runs it Sunday 23:00 Mountain (enabled). `BIGBOI/plex_config` was last modified March 2025, so it's the old TrueNAS-app Plex config, not live data. Original steps:
1. Write the two exports into the repo (`~/homelab`) and add them to `deployed.tsv`:
    - a nightly TrueNAS config export (DB plus secret seed) onto a `vmstore` path;
    - a weekly (Sunday night) Plex DB export from the Plex VM onto a dataset. Reading `/var/lib/plexmediaserver` needs a new `claude-maint` subcommand on the Plex VM.
2. Widen the Dockhand nightly cron so it covers Dockhand's DB as well as `stacks/`. Today it rsyncs only `.../app_mounts/dockhand/data/stacks/`. This is a TrueNAS UI edit by Aaron; Claude provides the command.
3. Give Aaron the exact Cloud Sync task settings: PUSH, SYNC, nightly, remote encryption on, with the source paths from the phase 1 scope above. `claude-maint` has no cloud-sync rights, so Aaron enters them in the UI (Aaron's preference).
4. Run the first sync, do a test restore of a few files to a scratch path, and check the B2 bucket size after one week. **First sync and restore test done 2026-10-16; bucket size checked 2026-10-23 (see Layer 2 status).**
5. Write the runbook "Offsite backup to B2: what's covered and how to restore", and link it to the Big Boi page. **Done 2026-10-16.**

## How to verify / roll back

Nothing to roll back. Claude has no B2 credentials, so the bucket figures are estimates from TrueNAS job history (`core.get_jobs` for `cloudsync.sync`); the real size is in the B2 web UI.
