---
date: 2026-09-29
type: config
system:
- '[[Uptime Kuma]]'
- '[[Servarr Stack (Docker Compose)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[Monitoring - deeper servarr health checks (Sonarr-Radarr-Prowlarr health APIs)]]'
notion_id: 3ea7ae76-22ba-8165-83fd-e2f5b1901ed1
---

# Added Sonarr/Radarr/Prowlarr health-API monitors and HA alerts

3 Kuma JSON Query monitors on the arr /health APIs (errors only), added by Aaron. Claude reloaded the HA Kuma integration, labeled the sensors homelab_watch, and added an app_health_error trigger with its own message to homelab_service_device_alerts.

**Kuma (Aaron, UI):** Sonarr Health / Radarr Health `http://192.168.1.248:{8989,7878}/api/v3/health`, Prowlarr Health `:9696/api/v1/health`. Type HTTP(s) – Json Query, header `X-Api-Key` (keys only in Kuma), `$count($[type="error"])` == `0`, 60 s, 3 retries. All three up on creation, which confirms the keys are valid and there are no current errors.
**HA (Claude, ha-mcp):**
- Reloaded the Uptime Kuma config entry so the new monitors appear (they don't show up on their own). 188 entities afterwards.
- `sensor.{sonarr,radarr,prowlarr}_health_status` labeled `homelab_watch` (now 26).
- `automation.homelab_service_device_alerts`: new trigger `app_health_error` (to `down`) with its own push, "⚠️ Homelab: Sonarr reports an error … open System → Status"; the three sensors were added to the `service_up` recovery trigger.
**Tested:** title/recovery text rendered against the live entity names. No live alert fired (that needs a real app health error).
