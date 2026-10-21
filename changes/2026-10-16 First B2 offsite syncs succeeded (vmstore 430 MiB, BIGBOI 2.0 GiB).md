---
date: 2026-10-16
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Plan backup strategy for TrueNAS and VMs]]'
notion_id: 3fb7ae76-22ba-81e3-ba6b-f7b5a6bf76c5
---

# First B2 offsite syncs succeeded (vmstore 430 MiB, BIGBOI 2.0 GiB); live servarr configs are in the Dockhand stack dir

Aaron ran both Cloud Sync tasks manually (Run Now). 'B2 offsite: vmstore': SUCCESS, 1124 files / 430 MiB; the pre-script worked on TrueNAS (staged dockhand.db.gz 38 MB from the 2.19 GB DB, kuma.db 8.6 MB, truenas-config.tar 0.8 MB, plex-db.tar.gz 27 MB, dockhand.encryption_key). 'B2 offsite: BIGBOI': SUCCESS, 4272 files / 2.0 GiB. Total about 2.4 GB, inside the 10 GB free tier. Finding: servarr's gluetun, nzbget, prowlarr, sonarr and radarr mount ./<app> relative to the Dockhand stack, so their live config is in /mnt/.ix-apps/app_mounts/dockhand/data/stacks/Big Boi/servarr/ (radarr.db modified today), not BIGBOI/servarr (radarr.db last modified 2026-03-05, a stale pre-Dockhand copy). Only overseerr uses BIGBOI/servarr. The live configs, including the apps' own weekly Backups/scheduled zips, are covered by the 23:30 cron copy into vmstore/dockhand-stacks-backup and the vmstore task. The stale BIGBOI/servarr app dirs are a cleanup candidate. Next: test restore.
