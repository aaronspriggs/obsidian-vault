---
date: 2026-10-16
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
project:
- '[[Plan backup strategy for TrueNAS and VMs]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/a13c872
notion_id: 3fb7ae76-22ba-816a-bc06-f367cfc96f00
---

# Created B2 account and the two Cloud Sync tasks on Big Boi (B2 offsite: BIGBOI, B2 offsite: vmstore)

Aaron created the Backblaze B2 account, bucket spriggs-bigboi-backup (private, 30-day prior versions) and app key truenas-bigboi; key, encryption password and salt are in 1Password item 'Backblaze B2 - truenas-bigboi' (Aaron's vault). TrueNAS: cloud credential 'B2 truenas-bigboi'; task 1 'B2 offsite: BIGBOI' (path /mnt/Big Boi/BIGBOI, include Media Library, servarr, uptime-kuma, autokuma, plex_config, folder /BIGBOI, daily 01:00); task 2 'B2 offsite: vmstore' (path /mnt/Big Boi/vmstore, include dockhand-stacks-backup, offsite-staging, folder /vmstore, daily 01:15, pre-script = repo backup/[cloudsync-vmstore-prescript.sh](http://cloudsync-vmstore-prescript.sh/)). Both PUSH/SYNC, remote encryption on, filename encryption OFF (TrueNAS warns it's experimental in rclone; contents still encrypted, names visible in the bucket; commit 1a4b9d8), Take Snapshot off. Verified via cloudsync.query; make check confirms the pre-script matches the repo (deployed.tsv host 'cloudsync'). Aaron reinstalled claude-maint (3dfa8eb); plex-db-export rerun gives a 600 file. Neither task has run yet.
