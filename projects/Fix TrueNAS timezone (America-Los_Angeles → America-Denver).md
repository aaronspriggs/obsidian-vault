---
type: task
status: done
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
completed: 2026-10-15
notion_id: 3e77ae76-22ba-8174-bccc-c1a2913c98b5
---

# Fix TrueNAS timezone (America/Los_Angeles → America/Denver)

Set to America/Denver by Aaron 2026-10-15; verified via API.

## Outcome (Done 2026-10-15)

Aaron set System → General Settings → Localization → Timezone to `America/Denver` in the TrueNAS UI. Claude's `claude-maint` key has no `SYSTEM_GENERAL_WRITE`, and granting it wasn't worth it for a one-off change.
Verified through the API on 2026-10-15:
- `system.general.config` and `system.info` both report `America/Denver`.
- The snapshot tasks for `Big Boi/vmstore` and `Big Boi/BIGBOI` run daily at 00:00 with 30-day retention, now on Mountain time.
- The cron job "Copy Dockhand stack definitions to vmstore" runs at 23:30 Mountain, so it still finishes before the snapshot.
- `truenas-alert-relay` reads the timezone on every run, and its first run after the change exited 0.

## Changes

![[Changes.base#For this project]]
