---
type: task
status: done
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
completed: 2026-10-15
notion_id: 3fa7ae76-22ba-81e5-94e2-c06740a9c371
---

Dockhand v1.0.49 → v1.0.53 (catalog 1.1.34 → 1.1.38) on 2026-10-15, after a recursive pre-upgrade snapshot of ix-apps/app_mounts. All checks passed.

## Outcome (Done 2026-10-15)

Dockhand TrueNAS app upgraded from **v1.0.49 (catalog 1.1.34) to v1.0.53 (1.1.38)**. The release notes for v1.0.50–v1.0.53 list no breaking changes or migrations; v1.0.52's ownership bug was reverted in v1.0.53.
**How:**
1. Homelab maintenance mode on.
2. Recursive snapshot `Big Boi/ix-apps/app_mounts@pre-dockhand-1.1.38` (covers `app_mounts/dockhand/data`, Dockhand's DB), taken by Claude with the new `SNAPSHOT_WRITE` role.
3. `truenas-api --write app.upgrade '["dockhand", {"app_version": "1.1.38"}]'` (job 301419, SUCCESS).
4. Verified, then maintenance mode off.
**Verified 2026-10-15:**
- App `RUNNING` v1.0.53_1.1.38, no further upgrade pending.
- `dockhand-api` works. Both stacks and all 11 containers are as before (10 running, the permissions helper exited as usual). Users are admin, claude and homeassistant.
- Update check (daily 04:00 UTC, notify-only) and image prune (weekly, dangling) settings were kept.
- The HA `dockhand` integration and Kuma's Dockhand monitor were back up within about a minute.
- No homelab Alert2 alerts active afterwards.

## Decisions

- **2026-10-15 (Aaron):** snapshot before upgrading, because Dockhand's DB isn't in any backup yet. Aaron granted `claude-maint` the `SNAPSHOT_WRITE` role so Claude can take it.

## Links

Follow-up: [Delete the pre-dockhand-1.1.38 snapshot after a quiet week](<Delete the pre-dockhand-1.1.38 snapshot after a quiet week.md>).

## Sub-items

![[Projects.base#Sub-items]]

## Changes

![[Changes.base#For this project]]
