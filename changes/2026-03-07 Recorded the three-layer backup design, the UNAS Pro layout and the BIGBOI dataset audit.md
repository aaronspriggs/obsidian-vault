---
date: 2026-03-07
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project: '[[Plan backup strategy for TrueNAS and VMs]]'
---

## What changed

No system changes. The backup design of 2026-03-05 (three layers, a two-node layout with a UNAS Pro), the BIGBOI dataset audit of 2026-03-07, and the action checklist with its check-offs through 2026-10-16. Moved here on 2026-11-15 from the [project](<../projects/Plan backup strategy for TrueNAS and VMs.md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

This is the full text behind the [2026-03-05 design session](<2026-03-05 Backup strategy research and design session.md>). The UNAS Pro parts (two-node architecture, Layer 3, its directory structure) were superseded on 2026-10-15 by the Big Boi rebuild with an HDD pool; the tiering by replaceability and Layers 1 and 2 stand.

## How

### Key Decisions (Documented 2026-03-05)

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

### Backup Strategy by Layer

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

### UNAS Pro Directory Structure (plan before populating)

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

### TrueNAS Data Protection — What Each Section Does

For reference (from the UI at Data Protection):

| Section | Purpose | Use for this strategy |
| --- | --- | --- |
| TrueCloud Backup Tasks | iXsystems managed cloud backup | Skip — use B2 directly instead |
| Cloud Sync Tasks | Push/pull datasets to cloud providers (B2, S3, R2, etc.) | ✅ Layer 2 — B2 offsite sync |
| Periodic Snapshot Tasks | ZFS on-pool snapshots on a schedule | ✅ Layer 1 — accidental deletion protection |
| Replication Tasks | ZFS send/receive to remote TrueNAS-compatible host | Future — if UNAS Pro runs TrueNAS |
| Rsync Tasks | File-level sync to any remote host | ✅ Layer 3 — Big Boi → UNAS Pro nightly |
| Periodic S.M.A.R.T. Tests | Drive health monitoring / early failure warning | ✅ Enable regardless — early warning system |

### Open Action Items

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

### Dataset Audit Findings (2026-03-07)

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

### What's Explicitly Not Backed Up (and Why)

| Data | Reason |
| --- | --- |
| Servarr-managed Plex media | Re-downloadable via Seerr — cost of B2 not justified |
| UNAS Pro full media library offsite | Too large for B2 at scale; RAID 6 provides local redundancy; content is mostly re-downloadable |
| HA config offsite | Already covered by automated Google Drive backup |

## How to verify / roll back

Nothing to roll back. Layer 1 and Layer 2 as built are described in the project note and the B2 runbook.
