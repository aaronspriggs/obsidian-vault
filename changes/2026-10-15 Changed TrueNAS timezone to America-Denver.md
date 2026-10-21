---
date: 2026-10-15
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Fix TrueNAS timezone (America-Los_Angeles → America-Denver)]]'
notion_id: 3fa7ae76-22ba-817d-a36b-f405437855a0
---

# Changed TrueNAS timezone to America/Denver

Big Boi timezone America/Los_Angeles → America/Denver (Aaron, TrueNAS UI); snapshots and stack-backup cron now on Mountain time.

## What changed

The TrueNAS SCALE (Big Boi) timezone went from America/Los_Angeles to America/Denver.

## Why

The 00:00 snapshots were running at 01:00 Mountain, and the 23:30 stack-backup cron at 00:30 Mountain. Their order was still correct; this is a consistency fix.

## How

Aaron changed it in the TrueNAS UI: System → General Settings → Localization. Claude's `claude-maint` key can't change system settings.

## Verify / roll back

Verified 2026-10-15 via `truenas-api`: `system.general.config` and `system.info` report America/Denver. The snapshot tasks still run at 00:00, keep 30 days and are enabled. The cron job still runs at 23:30 and is enabled. The alert relay's next run exited 0. To roll back, set the timezone in the same UI field.
