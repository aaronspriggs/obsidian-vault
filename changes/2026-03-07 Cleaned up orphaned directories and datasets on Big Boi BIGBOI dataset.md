---
date: 2026-03-07
type: fix
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 31c7ae76-22ba-8157-97ee-d9cef30dce61
---

# Cleaned up orphaned directories and datasets on Big Boi BIGBOI dataset

Audited `/mnt/Big Boi/BIGBOI/` during backup strategy planning session. Found and removed several orphaned directories.

## Deleted

- `bulk_storage/Movies` (86 GB) — confirmed duplicate of content already in `plex_content/Movies` (self-ripped Blu-rays)
- `plex_contentt/` — empty directory, typo duplicate of `plex_content`
- `vm_imports/` (576 MB) — contained `haos_ova-15.0.qcow2`, the original HA import image no longer needed since HA runs as a zvol
- `servarr/dockge/` — leftover data directory from Dockge, replaced by Dockhand
- `homelab-mcp` ZFS dataset — orphaned dataset from abandoned MCP server project, deleted via TrueNAS UI

## Kept

- `Media Library/` (757 MB) — contains irreplaceable personal photos and videos (`2025/`, `Ouray 2020/`). Flagged for offsite backup — currently unprotected.

## Result

BIGBOI directory now contains only: `Media Library`, `plex_config`, `plex_content`, `plex_recordings`, `servarr`. ~87 GB of pool space reclaimed.
