---
date: 2026-03-07
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 31c7ae76-22ba-81aa-b2f1-fd488840a5b4
---

# Configured ZFS Periodic Snapshot Tasks on Big Boi

Configured two ZFS Periodic Snapshot Tasks in TrueNAS Data Protection.

## Tasks Created

| Task | Dataset | Recursive | Exclude | Schedule | Retention |
| --- | --- | --- | --- | --- | --- |
| VM Snapshots | `Big Boi/vmstore` | Yes | None | Daily 00:00 | 30 days |
| Config Snapshots | `Big Boi/BIGBOI` | Yes | plex_content, plex_recordings | Daily 00:00 | 30 days |

## Coverage

- `vmstore` recursive covers both `haos_disk` (HA VM) and `Plex-9wert` (Plex VM)
- `BIGBOI` recursive covers `plex_config`, `servarr/`, and `Media Library/` — excludes large media datasets
- `plex_content` and `plex_recordings` intentionally excluded — re-downloadable media not worth snapshotting

## Notes

- These are current-layout snapshot tasks — paths will need updating after the BIGBOI restructure project is executed
- Layer 1 of the backup strategy is now complete (accidental deletion / corruption protection)
- Layer 2 (B2 offsite cloud sync) still to be configured
