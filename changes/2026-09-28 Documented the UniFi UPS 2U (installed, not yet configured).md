---
date: 2026-09-28
type: doc
system:
- '[[UniFi UPS 2U]]'
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Rack Infrastructure — UPS + Power Management]]'
notion_id: 3e97ae76-22ba-81ea-b7d2-c137dd8af5c4
---

# Documented the UniFi UPS 2U (installed, not yet configured)

New Systems page for the UPS 2U from HA/UniFi data (192.168.1.12, fw 1.6.1.413, up since 2026-08-04). TrueNAS UPS service confirmed stopped. Rack UPS project Deferred -> Backlog. truenas_admin recorded on the TrueNAS page.

## What

Aaron confirmed 2026-09-28 that the UPS 2U was bought and installed but not configured. Created its Systems page from live HA (UniFi integration) data, confirmed via the TrueNAS API that the UPS service is stopped with no driver, moved the rack UPS project from Deferred to Backlog with the remaining config work, and recorded the TrueNAS admin username (`truenas_admin`, no 2FA) on the TrueNAS page.

## Verify

`sensor.ups_2u_state` = connected; `truenas-api service.query` shows `ups` STOPPED.
