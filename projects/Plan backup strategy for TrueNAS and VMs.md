---
type: project
status: active
priority: high
system:
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
next_step: '2026-11-17: both B2 tasks ran clean on 2026-11-15 (checked live). Aaron reads the real bucket size himself at https://secure.backblaze.com/b2_buckets.htm (bucket spriggs-bigboi-backup; expected about 4-5 GB): Claude has no B2 credentials, and the TrueNAS API can''t report the bucket''s size including old file versions. Phase 2 (rips to B2) waits for the Big Boi rebuild, when rips get their own dataset on the HDD pool (Aaron 2026-11-08).'
notion_id: 3087ae76-22ba-8115-9603-e15b0f8b9f21
---

## Goal

Design and implement a backup strategy that protects all irreplaceable data in the homelab against hardware failure, accidental deletion, and catastrophic loss (fire, theft, power surge). Acceptable recovery time is one week.

## Status (2026-11-15)

- **Layer 1, local snapshots: done.** Daily recursive snapshots of `Big Boi/vmstore` and `Big Boi/BIGBOI`, kept 30 days (verified live 2026-11-15). The `BIGBOI` task excludes `plex_content` and `plex_recordings`. S.M.A.R.T. tests run weekly (short) and monthly (long), verified 2026-10-15.
- **Layer 2 phase 1, offsite to B2: live since 2026-10-16.** Two nightly Cloud Sync tasks, `B2 offsite: BIGBOI` (01:00) and `B2 offsite: vmstore` (01:15), push to bucket `spriggs-bigboi-backup`, encrypted by TrueNAS, with B2 keeping prior versions 30 days. Both ended SUCCESS on 2026-11-15 (live). A restore was tested on 2026-10-16. What's covered and how to restore: [the B2 runbook](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>).
- **Bucket size.** Estimated 4.3 GB after one week and heading for about 10 GB, the edge of the free tier; the 2026-10-23 fix cut the nightly upload from about 225 MiB to 60–70 MiB, so the 30-day steady state should be 4–5 GB. These are estimates from TrueNAS job history, because Claude has no B2 credentials.
- **Left:** phase 2, the self-ripped discs.

Slimmed 2026-11-15: the March design in full and the phase 1 detail are in two change notes, linked under Plan.

## Plan

### Done

1. Layer 1 snapshot tasks ([2026-03-07](<../changes/2026-03-07 Configured ZFS Periodic Snapshot Tasks on Big Boi.md>)); 30-day retention confirmed over the API on 2026-09-25.
2. S.M.A.R.T. tests ([2026-03-07](<../changes/2026-03-07 Configured S.M.A.R.T. tests on Big Boi drives.md>)). TrueNAS 25.04's `smart.test.results` fails schema validation for the SATA SSDs, so pass/fail history can't be read over the API; a failure still surfaces as a TrueNAS alert through the relay.
3. `ix-apps` can't be given a snapshot task, so a nightly cron copies Dockhand's stack directories into `vmstore/dockhand-stacks-backup`, which is snapshotted and synced ([2026-09-26](<../changes/2026-09-26 Added nightly Dockhand stack backup cron (→ vmstore, snapshotted).md>)).
4. B2 phase 1: staging pre-script, Plex DB export and task design ([2026-10-15](<../changes/2026-10-15 B2 offsite phase 1 - staging pre-script, Plex DB export and Cloud Sync task.md>)); account and tasks created ([2026-10-16](<../changes/2026-10-16 Created B2 account and the two Cloud Sync tasks on Big Boi (B2 offsite.md>)); first syncs ([2026-10-16](<../changes/2026-10-16 First B2 offsite syncs succeeded (vmstore 430 MiB, BIGBOI 2.0 GiB).md>)); restore test and runbook ([2026-10-16](<../changes/2026-10-16 Tested a B2 restore of vmstore and wrote the offsite backup runbook.md>)).
5. Orphaned directories from the 2026-03-07 dataset audit removed ([2026-10-16](<../changes/2026-10-16 Removed the stale pre-Dockhand servarr copy from BIGBOI-servarr (kept.md>)).
6. One-week bucket check ([estimate, source sizes, prices and the phase 1 steps as completed](<../changes/2026-10-23 Estimated the B2 bucket size after one week and recorded the Layer 2 sizes and phase 1 steps.md>)) and the fix it led to ([2026-10-23](<../changes/2026-10-23 B2 vmstore sync stages consistent servarr DBs and skips logs.md>)).

The original three-layer design, the UNAS Pro layout, the dataset audit and the action checklist are in [this change note](<../changes/2026-03-07 Recorded the three-layer backup design, the UNAS Pro layout and the BIGBOI dataset audit.md>).

### Phase 2: self-ripped discs to B2 (waits for the Big Boi rebuild)

Rips are mixed into `plex_content/Movies` with Servarr content. During the [rebuild](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>)'s media move they get their own `rips` dataset on the HDD pool and their own Cloud Sync task. Until then they have no snapshot and no offsite copy. [Reorganize BIGBOI dataset structure under plex- and personal-](<Reorganize BIGBOI dataset structure under plex- and personal-.md>) (backlog) is the related groundwork.

Sized 2026-11-08 (`du --apparent-size` on the Plex VM's `/mnt/media`, Radarr `/api/v3/movie`): `Movies/` is 872 GiB in 16 folders plus 2 loose files; `TV Shows/` 1.1 TiB; `downloads/` 1.3 GiB. Radarr manages only 5 movies (315 GB: Anaconda, The Super Mario Galaxy Movie, Back to the Future I–III). The other 11 folders, 616 GB, are the likely rips (about 56 GB each, UHD remux size): D&D Honor Among Thieves, Ex Machina, Ford v Ferrari, Inception, Marty Supreme, Ocean's Eleven, LOTR Fellowship and Return of the King (Extended), The Martian, Weird, Zombieland. Loose files: `Apollo 13 1995 HDRip h264.mp4` (a download) and `DJI_0001.MP4` (a personal drone clip, to move to Media Library). At $6.95/TB/month, 616 GB is about $4.30/month, plus about $0.39/month per further UHD disc.

## Decisions

- **2026-03-05: protection is tiered by how replaceable the data is.** Irreplaceable: self-ripped discs, home videos, computer backups, the TrueNAS config, VM configs and compose files, Plex metadata and watch history. Re-downloadable but painful: Servarr-managed media, which doesn't go to B2 because re-requesting through Seerr is possible and the cost isn't justified. Already backed up: Home Assistant, by its own automated Google Drive backup.
- **2026-03-05: three layers.** Layer 1, ZFS snapshots on the pool, against deletion, corruption and operator error. Layer 2, B2, against losing the box. Layer 3, a UNAS Pro as a local rsync target for the VM disks and configs, with the UNAS Pro also the bulk storage node. Layer 3 and the UNAS Pro layout were replaced on 2026-10-15 (long-term line below).
- **2026-03-05: rips and Servarr content need separate directories,** or a backup task can't pick out the irreplaceable part. Carried into phase 2 as the `rips` dataset.
- **2026-10-15 (Aaron): provider is Backblaze B2.** $6.95/TB/month, first 10 GB free, no minimum duration ([pricing](https://www.backblaze.com/cloud-storage/pricing)). Rejected: Box, although Aaron has an unlimited account and Cloud Sync supports it, so that backup volume won't trip usage flags on an account he relies on; Cloudflare R2, about twice the price per TB; Wasabi, a 1 TB minimum charge and 90-day minimum duration.
- **2026-10-15 (Aaron): phase 1 scope.** Media Library, the `BIGBOI` app configs, `vmstore/dockhand-stacks-backup` with Dockhand's own DB, a nightly TrueNAS config export and a weekly Plex DB export, all synced nightly. VM disks aren't sent: HA backs itself up, and the Plex and ClaudeCode VMs are rebuilt from runbooks.
- **2026-10-15: two tasks and one pre-script.** Two because the TrueNAS folder picker only multi-selects within one parent. The vmstore task's pre-script stages the config export and consistent database copies, and fails the run (a TrueNAS alert) if the Plex export is over 9 days old; that replaced a separate cron. Aaron enters Cloud Sync settings in the UI, since `claude-maint` has no cloud-sync rights (his preference). Settings: repo [`backup/README.md`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/backup/README.md).
- **2026-10-15 (Aaron), long term: B2 stays limited to the small irreplaceable set.** Bulk media lives on the HDD pool of the rebuilt Big Boi, and its offsite copy, if any, is ZFS replication to a box Aaron owns, never paid cloud (14 TB on B2 would be about $97/month).
- **2026-10-23 (Aaron approved): stage consistent copies of the three *arr databases and skip `logs/` and Prowlarr's `Definitions/`.** The raw copies were taken while the apps ran in WAL mode and could be torn, and rotating logs made up most of the nightly upload.
- **2026-11-08 (Aaron): re-ripping is an acceptable worst case, but back the rips up to B2 if the storage is affordable.** No offsite box (rebuild project). Phase 2 stays planned and waits for the rebuild.

## Open questions

- Aaron to confirm the 11 likely rips.
- The real bucket size, from the B2 web UI.
- Whether `plex_content` gets snapshots before the rebuild; today it has none, by the task's exclusion.

## Changes

![[Changes.base#For this project]]
