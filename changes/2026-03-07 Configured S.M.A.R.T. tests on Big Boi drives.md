---
date: 2026-03-07
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 31c7ae76-22ba-81fa-bca4-d726cdb1702d
---

# Configured S.M.A.R.T. tests on Big Boi drives

Configured two S.M.A.R.T. test schedules in TrueNAS Data Protection.

## Tests Created

- **Weekly Short** — All disks, SHORT test, weekly Sundays at 00:00
- **Monthly Long** — All disks, LONG test, 1st of every month at 01:00

## Notes

- TrueNAS rejected Monthly schedule for the LONG test due to conflict with SHORT test running on the same schedule (first Sunday = day 1 conflict). Used custom cron `0 1 1 * *` to run on the 1st of the month at 1am instead.
