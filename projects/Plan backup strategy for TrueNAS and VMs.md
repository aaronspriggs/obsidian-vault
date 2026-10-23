---
type: project
status: active
priority: high
system:
- '[[TrueNAS SCALE (Big Boi)]]'
next_step: '2026-10-23: B2 bucket estimated ~4.3 GB after one week, heading for ~10 GB at 30-day steady state (see Layer 2 status). Next: phase 2 (split rips out of plex_content/Movies); around 2026-11-16 Aaron reads the real bucket size in the B2 web UI to confirm it plateaued; nightly upload should now be ~60-70 MiB (fixed 2026-10-23).'
notion_id: 3087ae76-22ba-8115-9603-e15b0f8b9f21
---

Layer 1 (daily snapshots, 30-day retention) and S.M.A.R.T. verified 2026-10-15. Layer 2 phase 1 live 2026-10-16: two nightly Cloud Sync tasks to B2 (about 2.4 GB), restore tested; runbook written. Rips are mixed into plex_content/Movies (phase 2).

## Goal

Design and implement a backup strategy that protects all irreplaceable data in the homelab against hardware failure, accidental deletion, and catastrophic loss (fire, theft, power surge). Acceptable recovery time is one week.

## Status (2026-10-16)

Layer 1 is done and verified: the daily snapshots keep 30 days. S.M.A.R.T. is covered (see checklist). **Layer 2 phase 1 is live:** two Cloud Sync tasks push nightly to B2 bucket `spriggs-bigboi-backup` (`B2 offsite: BIGBOI` 01:00, `B2 offsite: vmstore` 01:15). First runs 2026-10-16: 2.0 GiB + 430 MiB, both SUCCESS; a test restore of `/vmstore` matched every file. How to restore: runbook [Offsite backup to B2: what's covered and how to restore](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>). **Bucket size check 2026-10-23** (from TrueNAS job history, `core.get_jobs` for `cloudsync.sync`; Claude has no B2 credentials, so this is an estimate, not B2's own number): first runs uploaded 2.42 GiB, and the seven nightly runs since added 1.58 GiB (BIGBOI ~20 MiB/night, vmstore ~205 MiB/night, 257 MiB on 10-23). With every prior version still inside the 30-day window, the bucket holds about 4.0 GiB (4.3 GB). At about 225 MiB/night of churn the 30-day steady state is roughly 2.45 GiB current + 6.6 GiB prior versions, about 9.8 GB, right at the 10 GB free tier; any overage costs under $0.01/month at $6.95/TB. About 71 MiB of the vmstore churn is the staged DBs and Plex export (real changes); the rest is `dockhand-stacks-backup`, which holds the live servarr configs (compose `./sonarr:/config` etc.). Traced 2026-10-23: of its 1,121 files (360 MiB), ~290 MiB is rotating `logs/*.debug.N.txt` that renumber on every rollover, and Prowlarr rewrites its 670 `Definitions/` files daily, so most of both re-upload nightly; only ~39 MiB (DBs, current logs) really changes. Also found: `sonarr.db`/`radarr.db`/`prowlarr.db` are copied raw by rsync while the apps run (WAL mode, e.g. a 3.9 MB `sonarr.db-wal` at copy time), so the raw copy may not be consistent; the apps' own weekly `Backups/scheduled` zips are consistent but up to 7 days old. `plex-db.tar.gz` is re-staged with a new mtime every night (plain `cp`), so its 26 MiB re-uploads on the six nights it hasn't changed. **Fixed the same day** (Aaron approved): the pre-script now `sqlite_copy`s the three *arr DBs into staging and uses `cp -p` for the Plex export, and the 23:30 rsync skips `logs/` and `Definitions/`; first run uploaded 24 files / 119 MiB. See [[2026-10-23 B2 vmstore sync stages consistent servarr DBs and skips logs]]. Left: phase 2 (rips).
**Sizes for Layer 2 (live, 2026-10-15):**
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

---

## Decisions (2026-10-15)

- **Provider: Backblaze B2** (Aaron). Box was considered because Aaron already has an unlimited Box account and TrueNAS Cloud Sync supports it. Aaron rejected it so backup volume won't trip Box usage flags on an account he relies on. R2 costs about 2× B2 per TB. Wasabi has a 1 TB / 90-day minimum.
- **Phase 1 scope** (Aaron): Media Library, the `BIGBOI` app configs (`servarr/`, `uptime-kuma/`, `autokuma/`, `plex_config`), `vmstore/dockhand-stacks-backup` (widened to include Dockhand's own DB), a nightly TrueNAS config export and a **weekly** Plex DB export. All sync to B2 nightly, encrypted by TrueNAS, with B2 keeping prior versions for 30 days. Expected cost is $0–0.10/month (first 10 GB free). VM disks aren't sent: HA backs itself up, and the Plex and ClaudeCode VMs are rebuilt from runbooks.
- **Phase 2:** self-ripped Blu-rays, once they're split out of `plex_content/Movies`, at $6.95/TB/month.
- **Long term** (Aaron): B2 stays limited to the small irreplaceable set. Bulk media lives on a future HDD pool in a rebuilt Big Boi, and its offsite copy (if any) is ZFS replication to an offsite TrueNAS box, never paid cloud. This **supersedes the UNAS Pro architecture and Layer 3 below**. See [Rebuild Big Boi into a new case with an HDD pool](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>).

## Plan: Layer 2 phase 1 (2026-10-15)

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

## Key Decisions (Documented 2026-03-05)

### What counts as irreplaceable

Not all data needs equal protection. The strategy is tiered by replaceability:
- **Irreplaceable** — self-ripped Blu-rays/DVDs, home videos, personal computer backups, TrueNAS system config, VM configs and compose files, Plex metadata/watch history. These cannot be recreated from a download service.
- **Re-downloadable but painful** — Servarr-managed media (movies and TV acquired via Overseerr/NZBGet). Losing this means re-requesting through Seerr — possible but takes weeks.
- **Already backed up** — Home Assistant config (automated Google Drive backup, already running).

### Architecture: Two-node setup (current + future)

**Current state (Big Boi only):**
Big Boi holds everything — VMs, configs, Servarr stack, and the full Plex media library on its SSD RaidZ1 array.
**Future state (Big Boi + UNAS Pro):**
When the SSD pool approaches ~80% utilization, the Plex media library migrates to a UNAS Pro 7-bay NAS. Big Boi becomes the compute/config node; UNAS Pro becomes the bulk storage node. The UNAS Pro is also planned to hold home videos, personal rips, and computer backups — making it a general household bulk storage tier, not just a Plex overflow drive.
This two-node architecture is important because it means the UNAS Pro is a **primary storage node**, not available to double as a backup target for Big Boi.

### The mixed-content problem

The Plex library is not purely re-downloadable. It contains:
- Servarr-managed content (re-downloadable via Seerr)
- Self-ripped Blu-rays and DVDs (irreplaceable)
These need to be kept in **separate directory structures** on the UNAS Pro from day one, so backup tasks can target only the irreplaceable content. Mixing them together makes selective backup impossible without backing up everything.

---

## Backup Strategy by Layer

### Layer 1 — ZFS Snapshots on Big Boi (implement now)

**What it protects against:** Accidental deletion, file corruption, ransomware, operator error.
**What it does NOT protect against:** Pool failure, hardware loss, fire/theft.
**Cost:** Free. Built into TrueNAS.
Configure Periodic Snapshot Tasks in TrueNAS Data Protection for:
- VM datasets (HA disk, Plex VM disk)
- Config datasets (servarr compose, plex_config)
- Recommended schedule: daily snapshots, 30-day retention

### Layer 2 — Backblaze B2 Cloud Sync (implement now)

**What it protects against:** Everything including catastrophic loss. Offsite copy survives fire, theft, hardware failure.
**Cost:** ~$0.01–0.02/month for configs. Scales with ripped content size — budget ~$6/TB/month. At 1–2TB of rips/home videos, that's $6–12/month.
Configure Cloud Sync Tasks in TrueNAS Data Protection to push to a B2 bucket:

| Dataset / Path | Frequency | Notes |
| --- | --- | --- |
| TrueNAS config export | Weekly | Small XML, use Settings → General → Save Config automation |
| Servarr compose.yaml + env files | On change / daily | `/mnt/Big Boi/BIGBOI/servarr/` |
| Plex config/metadata | Nightly | Plex database, preferences, metadata — not media files |
| Personal rips directory (UNAS Pro, future) | Nightly | Irreplaceable content only — separate path from Servarr downloads |
| Home videos (UNAS Pro, future) | Nightly | Irreplaceable |
| Computer backups (UNAS Pro, future) | Nightly | Irreplaceable |

Servarr-managed media (re-downloadable) does **not** go to B2.

### Layer 3 — UNAS Pro as Backup Target for Big Boi (future, when UNAS Pro arrives)

**What it protects against:** Big Boi hardware failure — fast local restore without waiting for B2 download.
**Cost:** Disk space on UNAS Pro (no additional hardware needed).
Use TrueNAS Rsync Tasks to push nightly from Big Boi to UNAS Pro:
- HA VM disk image
- Plex VM disk image
- Servarr configs
This gives a local copy of Big Boi's critical data that can restore within hours rather than days. Note: the UNAS Pro itself has no offsite backup for its media content (by design — see decisions above). Only the irreplaceable subdirectories get pushed to B2.

---

## UNAS Pro Directory Structure (plan before populating)

When the UNAS Pro is purchased, structure it before putting content on it:
```javascript
/media/
  /movies/              ← Servarr-managed (re-downloadable, no B2)
  /tv/                  ← Servarr-managed (re-downloadable, no B2)
  /rips/                ← Self-ripped content (B2 backup)
/personal/
  /home-videos/         ← Irreplaceable (B2 backup)
  /computer-backups/    ← Irreplaceable (B2 backup)
/bigboi-backups/        ← Rsync target from Big Boi (VM disks, configs)
```
Plex libraries should be configured with separate source paths for `/media/movies` + `/media/tv` vs `/media/rips` so rips can have a distinct library if needed.

---

## TrueNAS Data Protection — What Each Section Does

For reference (from the UI at Data Protection):

| Section | Purpose | Use for this strategy |
| --- | --- | --- |
| TrueCloud Backup Tasks | iXsystems managed cloud backup | Skip — use B2 directly instead |
| Cloud Sync Tasks | Push/pull datasets to cloud providers (B2, S3, R2, etc.) | ✅ Layer 2 — B2 offsite sync |
| Periodic Snapshot Tasks | ZFS on-pool snapshots on a schedule | ✅ Layer 1 — accidental deletion protection |
| Replication Tasks | ZFS send/receive to remote TrueNAS-compatible host | Future — if UNAS Pro runs TrueNAS |
| Rsync Tasks | File-level sync to any remote host | ✅ Layer 3 — Big Boi → UNAS Pro nightly |
| Periodic S.M.A.R.T. Tests | Drive health monitoring / early failure warning | ✅ Enable regardless — early warning system |

---

## Open Action Items

- [x] Enable Periodic S.M.A.R.T. Tests on Big Boi drives. **Verified 2026-10-15:** weekly SHORT (Sunday 00:00) and monthly LONG (1st, 01:00) on all disks, `smartd` running and enabled, no SMART alerts. TrueNAS 25.04's `smart.test.results` fails schema validation for the SATA SSDs, so pass/fail history can't be read over the API. Failures would still surface as TrueNAS alerts through the relay. The NVMe boot drive has no test results.
- [x] Configure ZFS Periodic Snapshot Tasks for VM and config datasets. **Found already in place (2026-09-24, from Aaron's screenshot):** `Big Boi/vmstore` and `Big Boi/BIGBOI`, both recursive, daily at 00:00, naming `auto-%Y-%m-%d_%H-%M`, enabled, last state FINISHED. **Confirmed via the TrueNAS API 2026-09-25:** retention is **30 days** on both tasks (matches the plan), and the Plex VM disk is `vmstore/Plex-9wert` (covered). **Two gaps:**
    - (1) The `BIGBOI` task **excludes ****`plex_content`**** and ****`plex_recordings`**, so self-ripped and irreplaceable media isn't snapshotted. Decide whether to snapshot `plex_content` (rips) or rely on Layer 2 cloud sync for irreplaceable subfolders.
    - (2) **`Big Boi/ix-apps`**** has no snapshot task.** It holds Dockhand's stack definitions (servarr + uptime-kuma compose files); last snapshot 2026-01-19 (automatic, during a TrueNAS update). **Addressed 2026-09-26:** `ix-apps` can't be selected in the snapshot task UI, so a nightly TrueNAS cron job copies Dockhand's stack definitions into `vmstore/dockhand-stacks-backup` (unshared, snapshotted 30 days). See the TrueNAS page, Cron jobs. The HA disk was moved there in March, but the Plex disk path isn't documented.
- [x] Create cloud storage account and bucket: Backblaze B2, `spriggs-bigboi-backup` (2026-10-16).
- [x] Configure Cloud Sync Task: configs and Plex metadata → cloud (two tasks, 2026-10-16).
- [x] Back up `Media Library/` offsite: in `B2 offsite: BIGBOI` since 2026-10-16.
- [x] Check the B2 bucket size on 2026-10-23 (expect under 10 GB, the free tier): ~4.3 GB estimated, ~10 GB at steady state (2026-10-23).
- [x] Clean up orphaned directories on BIGBOI dataset. **Done 2026-10-16:** everything in the 2026-03-07 audit below is gone (re-checked via the API: no `bulk_storage/`, `plex_contentt/`, `vm_imports/`, `homelab-mcp` dataset or `servarr/dockge/`), and the stale pre-Dockhand copy in `servarr/` was removed (manual snapshot `BIGBOI@pre-servarr-cleanup-2026-10-16`). The `plex_config` leftover is tracked on the TrueNAS page.
- [ ] When UNAS Pro arrives: plan directory structure before populating
- [ ] When UNAS Pro arrives: configure Rsync Task: Big Boi critical data → UNAS Pro nightly
- [ ] When UNAS Pro arrives: configure Cloud Sync Task: irreplaceable UNAS Pro content → cloud

---

## Dataset Audit Findings (2026-03-07)

**Re-checked 2026-10-15:** `bulk_storage/`, `plex_contentt/` and `vm_imports/` are gone from the `BIGBOI` root. What's there now: `plex_content`, `plex_config`, `plex_recordings`, `Media Library`, `servarr`, `uptime-kuma`, `autokuma`, `.DS_Store`. The table below is the original 2026-03-07 audit.
Actual BIGBOI directory layout differs from what was documented. Findings from `ls` and `du` inspection:

| Directory | Size | Status | Action |
| --- | --- | --- | --- |
| `Media Library/` | 757 MB | ⚠️ Irreplaceable — personal photos/videos (`2025/`, `Ouray 2020/`) | Keep — add to B2 backup scope immediately |
| `bulk_storage/Movies` | 86 GB | Likely duplicate of `plex_content/Movies` (self-ripped Blu-rays) | Verify then delete |
| `plex_contentt/` | 0 | Empty typo directory | Delete |
| `vm_imports/` | 576 MB | Old HA OVA import image (`haos_ova-15.0.qcow2`), no longer needed | Delete |
| `homelab-mcp` dataset | ~0 | Orphaned ZFS dataset from abandoned MCP server project | Delete in TrueNAS UI |

Also noted: `servarr/dockge/` directory is a Dockge leftover — safe to delete after confirming nothing active references it.

---

## What's Explicitly Not Backed Up (and Why)

| Data | Reason |
| --- | --- |
| Servarr-managed Plex media | Re-downloadable via Seerr — cost of B2 not justified |
| UNAS Pro full media library offsite | Too large for B2 at scale; RAID 6 provides local redundancy; content is mostly re-downloadable |
| HA config offsite | Already covered by automated Google Drive backup |

## Changes

![[Changes.base#For this project]]
