---
type: task
status: backlog
priority: low
system:
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
- '[[Plex Media Server]]'
notion_id: 3087ae76-22ba-812f-9f4d-f98d31e4ce3e
---

# Verify/clean up plex_config dataset

Dataset at /mnt/Big Boi/BIGBOI/plex_config may be a leftover from when Plex ran as a TrueNAS app. Verify if still needed or safe to delete.

**2026-11-15 (checked through the TrueNAS API during the quarterly triage):** 260 MB, top level `Library/`, `Codecs/` and a `.DS_Store`, which is a Plex config directory from the TrueNAS-app days. The Plex VM mounts only `plex_content` and `plex_recordings`, and its own config lives on its zvol, so nothing running reads this dataset. Deleting it is a dataset change (Tier 3) and `truenas-api --write` has no dataset method, so it would be Aaron's click in the TrueNAS UI.
