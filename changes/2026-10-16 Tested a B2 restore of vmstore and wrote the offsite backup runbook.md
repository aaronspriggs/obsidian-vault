---
date: 2026-10-16
type: doc
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Plan backup strategy for TrueNAS and VMs]]'
notion_id: 3fb7ae76-22ba-8147-aba5-ecb0d2d8219d
---

# Tested a B2 restore of /vmstore and wrote the offsite backup runbook

Aaron created a PULL task 'B2 restore test' (id 3, COPY, from the vmstore task's Restore action, created disabled) into /mnt/Big Boi/vmstore/restore-test and ran it: SUCCESS, 1124 files / 430 MiB. Claude compared every file with the originals over the TrueNAS API: all 1124 match by size (incl. truenas-config.tar, dockhand.db.gz, plex-db.tar.gz, kuma.db); 2 originals absent, both Overseerr log symlinks from 2026-03-05 that Cloud Sync skips with Follow Symlinks off (targets were restored). Proves the stored encryption password and salt decrypt the bucket. Wrote runbook 'Offsite backup to B2: what's covered and how to restore' (System: TrueNAS, Plex). Cleanup done by Aaron the same day and verified via the API: only the two PUSH tasks remain, restore-test folder removed.
