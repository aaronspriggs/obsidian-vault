---
type: task
status: done
priority: medium
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[Uptime Kuma]]'
completed: 2026-09-29
notion_id: 3e77ae76-22ba-81b3-81b4-e469b5c51e53
---

# Monitoring: deeper servarr health checks (Sonarr/Radarr/Prowlarr health APIs)

Done 2026-09-29: Kuma JSON Query monitors Sonarr/Radarr/Prowlarr Health (errors only) are live and up. Their HA sensors are in homelab_watch with their own alert trigger in homelab_service_device_alerts. No live alert test (it would need a real app error); the message render was checked. Complements gluetun-watchdog, which covers VPN loss.

- Add Kuma **HTTP(s) – JSON Query** monitors on `/api/v3/health` (Sonarr, Radarr) and `/api/v1/health` (Prowlarr) with header `X-Api-Key: <key>`; the keys are entered in Kuma only. Expression `$count($[type="error"])`, expected `0`, so warnings like "update available" are ignored.
- Add the new status sensors to `homelab_watch` and `automation.homelab_service_device_alerts`.
- At the same time, reconcile with "Add health checks and autoheal to servarr stack" (gluetun-watchdog may already cover it).

## Changes

![[Changes.base#For this project]]
