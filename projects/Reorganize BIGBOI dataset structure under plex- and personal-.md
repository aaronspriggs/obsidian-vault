---
type: project
status: backlog
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 31c7ae76-22ba-8181-a9af-ed735fb9c968
---

# Reorganize BIGBOI dataset structure under plex/ and personal/

Agreed structure finalized 2026-03-07. Do not execute until ZFS snapshots are configured on current layout.

## Goal

Reorganize the `BIGBOI` dataset directory structure to separate Plex content, personal content, and operational config into clearly named top-level groups. Makes backup targeting unambiguous and BIGBOI easier to reason about as it grows.

## Agreed Target Structure

```javascript
/mnt/Big Boi/
  vmstore/                    // ZFS dataset — DONE
    haos_disk
    Plex-9wert
  BIGBOI/                     // ZFS dataset
    plex/
      plex_content/           // existing ZFS dataset (zfs rename)
        Movies/               // Servarr-managed (stays)
        TV Shows/             // Servarr-managed (stays)
        rips/                 // NEW: self-ripped Blu-rays moved here
      plex_config/            // existing ZFS dataset (zfs rename)
      plex_recordings/        // existing ZFS dataset (zfs rename)
      downloads/              // NZBGet working dir (moved from inside plex_content)
    personal/
      home-videos/            // content from Media Library/
      drone/                  // DJI_0001.MP4 moved here
  apps/                       // NEW ZFS dataset (top-level, alongside BIGBOI)
    dockhand/
      servarr/                // servarr/ contents moved here from BIGBOI/servarr/
```
Design principles:
- `vmstore/` — all VM zvols
- `BIGBOI/` — Plex content and personal data
- `apps/` — all Docker app data; pattern is apps/dockhand/<stack-name>/. Future stacks follow same convention.

## Why

- `plex_content`, `plex_config`, and `plex_recordings` are scattered loosely under `BIGBOI` with no grouping — hard to reason about as BIGBOI grows
- `downloads/` inside `plex_content` means NZBGet's working dir gets snapshotted and backed up alongside media
- Self-ripped Blu-rays mixed with Servarr-managed content in `Movies/` makes selective B2 backup impossible
- `Media Library/` is an ambiguously named folder containing irreplaceable personal content
- A `personal/` top-level group makes backup targeting unambiguous

## Prerequisite

- ZFS snapshot tasks must be configured on current layout BEFORE starting this migration
- Take manual snapshots of all three datasets immediately before starting

## ZFS Operations Required

ZFS renames to move Plex datasets under a new `plex/` parent, plus create `apps/` at the pool level:
```bash
# Create new parent datasets
sudo zfs create "Big Boi/BIGBOI/plex"
sudo zfs create "Big Boi/apps"
sudo zfs create "Big Boi/apps/dockhand"

# Move Plex datasets
sudo zfs rename "Big Boi/BIGBOI/plex_content" "Big Boi/BIGBOI/plex/plex_content"
sudo zfs rename "Big Boi/BIGBOI/plex_config" "Big Boi/BIGBOI/plex/plex_config"
sudo zfs rename "Big Boi/BIGBOI/plex_recordings" "Big Boi/BIGBOI/plex/plex_recordings"
```
Then move the servarr directory contents (plain directory, no zfs rename needed):
```bash
mv "/mnt/Big Boi/BIGBOI/servarr" "/mnt/Big Boi/apps/dockhand/servarr"
```

## Downstream Impact — Everything That Breaks

| Component | What changes | How to fix |
| --- | --- | --- |
| TrueNAS NFS export | `plex_content` path changes | Update in TrueNAS UI: Shares → NFS |
| Plex VM fstab | NFS source path changes | SSH into Plex VM, update `/etc/fstab`, remount |
| Radarr | Movie root folder path | Radarr UI: Settings → Media Management → Root Folders |
| Sonarr | TV root folder path | Sonarr UI: Settings → Media Management → Root Folders |
| NZBGet | Download dir path | Update in compose.yaml or NZBGet UI |
| Plex library sources | Both Movies and TV Show library paths | Plex UI: Settings → Libraries → Edit |
| ZFS snapshot tasks | All three dataset paths change | Update or recreate snapshot tasks in TrueNAS Data Protection |
| Dockhand compose path | compose.yaml moves from BIGBOI/servarr/ to apps/dockhand/servarr/ | Update Dockhand stack path config to point to new location |
| Cloud Sync tasks (future) | B2 sync paths | Update when configuring B2 |

## Content Migration Required

- Move self-ripped content from `Movies/` into `plex_content/rips/` — identify manually (LOTR Extended Editions, Apollo 13, any other non-Servarr files)
- Move `DJI_0001.MP4` from `plex_content/Movies/` into `personal/drone/`
- Move `Media Library/` contents into `personal/home-videos/`
- Move `downloads/usenet/` from inside `plex_content/` up to `BIGBOI/plex/downloads/`
- Move `servarr/` directory from `BIGBOI/servarr/` to `apps/dockhand/servarr/`
- Update NZBGet download path to point to new location

## Execution Order

1. Take manual snapshots of all three datasets
2. Stop Plex VM
3. Stop all Servarr containers via Dockhand
4. Perform ZFS renames
5. Update NFS export in TrueNAS UI
6. Update Plex VM fstab and remount
7. Start Plex VM, verify media is accessible
8. Update Sonarr, Radarr, NZBGet paths (all now under apps/dockhand/servarr/)
9. Start Servarr stack
10. Update Plex library paths in Plex UI and scan
11. Move content (rips, DJI file, Media Library)
12. Update ZFS snapshot tasks
13. Verify everything end-to-end
14. Delete pre-migration snapshots once confirmed healthy

## Notes

- `plex/` will be a plain ZFS dataset (no special roles), just a container for the three child datasets
- `personal/` is a plain directory under BIGBOI, not a separate ZFS dataset — keep it simple unless backup targeting requires it
- `downloads/` inside `plex/` is also a plain directory, not a dataset
- `apps/` is a top-level ZFS dataset at the same level as `BIGBOI` and `vmstore`, not nested inside BIGBOI
- `servarr/` is a plain directory move (not a ZFS dataset) — no zfs rename needed, just mv
- Dockhand compose file path will change — update Dockhand config to point to new compose location
- Do NOT start this until snapshot tasks are running on the current layout
