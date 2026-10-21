---
date: 2026-10-15
type: upgrade
system:
- '[[Dockhand]]'
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Decide backup for the Dockhand TrueNAS app upgrade, then upgrade it]]'
notion_id: 3fa7ae76-22ba-81c2-9718-df9306e5f32c
---

# Upgraded Dockhand v1.0.49 → v1.0.53 (TrueNAS app 1.1.34 → 1.1.38)

Pre-upgrade snapshot app_mounts@pre-dockhand-1.1.38, then app.upgrade via claude-maint under maintenance mode; all checks passed.

## What changed

The Dockhand TrueNAS app went from v1.0.49 (catalog 1.1.34) to v1.0.53 (catalog 1.1.38).

## Why

TrueNAS flagged the upgrade on 2026-10-15. The release notes for v1.0.50–53 list no breaking changes or migrations, and v1.0.50 fixes image-prune timeouts.

## How

1. `input_boolean.homelab_maintenance_mode` on.
2. `truenas-api --write zfs.snapshot.create '[{"dataset": "Big Boi/ix-apps/app_mounts", "name": "pre-dockhand-1.1.38", "recursive": true}]'` created 3 snapshots, including `app_mounts/dockhand/data`.
3. `truenas-api --write app.upgrade '["dockhand", {"app_version": "1.1.38"}]'`: job 301419, SUCCESS.
4. Maintenance mode off.

## Verify / roll back

- **Verified:** app RUNNING v1.0.53_1.1.38. The API works. Stacks, the 11 containers, users and the update-check and image-prune settings were kept. The HA dockhand integration and Kuma's Dockhand monitor were up within about a minute. No homelab alerts active afterwards.
- **Rollback:** roll the app back in TrueNAS Apps, or (Tier 3, Aaron) `zfs rollback` the `pre-dockhand-1.1.38` snapshots of `app_mounts/dockhand` and `app_mounts/dockhand/data` with the app stopped.
- The snapshot is to be deleted after a quiet week (separate task).
