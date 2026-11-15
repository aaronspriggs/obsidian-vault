---
type: task
status: backlog
priority: low
system:
- '[[Plex Media Server]]'
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
---

From the quarterly triage of 2026-11-15 (Aaron's yes), out of what the Big Boi split change note left for him.

## Goal

Find out why the Plex VM's 32 GiB disk (`vmstore/Plex-9wert`) holds 148 GB of snapshots: 30 daily snapshots at about 5 GB of changed blocks a day. Then move whatever churns off the zvol or stop it, so the snapshots shrink by themselves as old ones expire.

## Plan

1. Read-only, Claude alone over SSH: where Plex's transcoder temp directory points, how large the Plex database backups and caches are and how often they are rewritten, and what else writes daily (`homelab-update`, logs, the weekly `plex-db.tar.gz` export).
2. Compare a few consecutive daily snapshots' `written` values through the TrueNAS API to confirm the daily figure and see whether it is steady or spiky.
3. Propose the smallest fix (for example the transcoder temp directory on tmpfs or on the `plex_recordings` share) and say what tier it is.

## Decisions

- **2026-11-15 (Aaron): leave the 30-day retention on `vmstore` alone.** The pool has 13.4 TB free and about 2.1 TB of media leaves it at the rebuild, so space isn't short, and shortening retention would be a snapshot-task change (Tier 3) that treats the symptom. Rejected for the same reason: excluding the Plex zvol from the snapshot task, which would leave the VM with no rollback.
