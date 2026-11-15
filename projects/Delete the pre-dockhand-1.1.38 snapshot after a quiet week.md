---
type: task
status: done
system:
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
- '[[Dockhand]]'
completed: 2026-11-15
parent: '[[Decide backup for the Dockhand TrueNAS app upgrade, then upgrade it]]'
notion_id: 3fa7ae76-22ba-8179-b361-d0f2a6807d42
---

## Outcome

Deleted on 2026-11-15 at the quarterly triage (Tier 2, Aaron's yes; [change](<../changes/2026-11-15 Ran the first quarterly KB triage.md>)): the three `pre-dockhand-1.1.38` snapshots on `Big Boi/ix-apps/app_mounts`, `app_mounts/dockhand` and `app_mounts/dockhand/data`, taken 2026-10-15 before the Dockhand upgrade. Dockhand had run on 1.1.38 for a month. In the same pass the three older `pre-dockhand-update-2026-09-26` snapshots on the same datasets and `BIGBOI@pre-servarr-cleanup-2026-10-16` went too. Each `truenas-api --write zfs.snapshot.delete` returned true, and a query afterwards finds no `pre-*` snapshot. The manual snapshots left on the pool are TrueNAS's own (`1.1.4`, `1.1.34`, `ix-apps-backup-system-update--2026-01-19`).

## Links

![[Changes.base#For this project]]
