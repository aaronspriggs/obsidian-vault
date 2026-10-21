---
type: task
status: done
priority: medium
system:
- '[[Servarr Stack (Docker Compose)]]'
completed: 2026-09-29
notion_id: 30d7ae76-22ba-81e8-9425-f71a277359a1
---

Done 2026-09-29: gluetun-watchdog pinned to 172.39.0.3 (commit c3c791d) and deployed through Dockhand. Verified after a full-stack recreate. Health checks: Gluetun has its own; gluetun-watchdog restarts NZBGet/Prowlarr when Gluetun is unhealthy; Kuma watches all UIs. App-level checks continue in 'Monitoring: deeper servarr health checks'.

## Changes

![[Changes.base#For this project]]
