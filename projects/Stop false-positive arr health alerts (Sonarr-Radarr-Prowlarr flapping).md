---
type: task
status: done
priority: high
system:
- '[[Home Assistant OS (VM)]]'
- '[[Uptime Kuma]]'
parent: '[[Homelab health monitoring with Home Assistant alerts (silent when nominal)]]'
completed: 2026-10-15
notion_id: 3f27ae76-22ba-81a0-856d-e8751accc831
---

# Stop false-positive arr health alerts (Sonarr/Radarr/Prowlarr flapping)

~32 false pushes/week before; 0 from 2026-10-09 to 10-15 with the 30-min Alert2 delay. Cause: single-indexer (NZBgeek) blips, not a rate limit.

## Outcome (Done 2026-10-15)

Fixed by option 1. Since 2026-10-14 the arr health alerts live in Alert2 (`alert2.homelab_<app>_health`, repo `ha/alert2.yaml`): they fire only after 30 min of continuous error (`delay_on_secs: 1800`), only while the app itself is up, and the message names the cause from `sensor.<app>_health_messages`. **Result, 2026-10-09 to 2026-10-15:** no false pushes, against about 32 a week before. Alert2 fired three times, all during quiet hours, so nothing was pushed.
- **The cause is confirmed as indexer blips, not a rate limit.** The only sustained error was Sonarr on 2026-10-13, 05:26–06:01 Mountain: "All indexers are unavailable due to failures". NZBgeek is the only indexer, so any NZBgeek outage counts as an error. Prowlarr (checked 2026-10-15) has no `queryLimit` set and uses about 95–130 NZBgeek calls a day, with **0 failed queries or grabs since 2026-09-15** and no indexer status errors. So the planned "set queryLimit to Aaron's NZBgeek limit" step was dropped as unnecessary.
- Not yet seen: a real daytime push showing the message. The Alert2 runbook covers that; nothing to track here.
- Follow-up idea: [Add a second Usenet indexer](<Add a second Usenet indexer to Prowlarr.md>).

## Findings 2026-10-07 (Claude)

- **Source:** `automation.homelab_service_device_alerts`, trigger `app_health_error` (Kuma JSON-query monitors on the arr `/health` APIs) and its recovery branch. From 2026-09-30 to 2026-10-07: Sonarr went down 7 times, Radarr 7 and Prowlarr 2. Each produced a time-sensitive alert plus a recovery push, about 32 pushes in total. The other notifying automations fire roughly daily at most.
- **They flap together:** the three monitors go pending within a minute or two of each other (e.g. 2026-10-06 05:42, 12:10, 15:06 Denver). Every episode cleared by itself 1–17 min after the down push; the longest was Sonarr 2026-10-05 00:29→00:46.
- **Kuma timing:** pending→down takes 15 min, not the ~4 min the automation's note assumes (60 s × 3), so these monitors' interval or retries differ from the plain service monitors. Worth checking in Kuma.
- **Ruled out:** gluetun-watchdog restarts (only one, on 2026-10-01) and Gluetun tunnel drops (log shows only routine DoT reconnect warnings). Sonarr and Radarr don't use the VPN at all.
- **Likely cause (unconfirmed):** a shared upstream dependency, i.e. the indexers proxied through Prowlarr. With only one or two indexers, a short indexer outage makes 'all indexers unavailable', which the arrs report as an *error*, so the Kuma query fails. The only names in Gluetun's DNS warnings are `api.nzbgeek.info`. To confirm: read the health messages.

## Fix options

1. Alert only on sustained errors: `for: 30 min` on `app_health_error`, and recovery notices for health sensors only if they were down 30+ min. Every observed episode would have been silent. This edits household-relied alerting (Tier 2: save the config first).
2. Fix the cause if it's indexers: add a second indexer, or accept that indexer blips are warnings rather than errors (the Kuma query could ignore IndexerStatusCheck).

## Sub-items

![[Projects.base#Sub-items]]

## Changes

![[Changes.base#For this project]]
