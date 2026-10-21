---
type: task
status: done
system:
- '[[Servarr Stack (Docker Compose)]]'
completed: 2026-03-05
notion_id: 31a7ae76-22ba-8162-9d42-d52275d4908f
---

## Problem

When Gluetun restarts, NZBGet and Prowlarr stay attached to the old network namespace and lose all connectivity. They need to be manually restarted with `sudo docker restart nzbget prowlarr` after any Gluetun restart.
`depends_on: service_healthy` only controls startup order — Docker does not re-trigger dependent containers when a dependency restarts.

## Goal

Automate restart of NZBGet and Prowlarr whenever Gluetun restarts or becomes unhealthy, without manual intervention.

## Options to Evaluate

1. **Gluetun-companion container** — lightweight sidecar that monitors Gluetun health and restarts dependents
2. **Docker health check on NZBGet/Prowlarr** — fail the health check when DNS/VPN is down, combined with `restart: unless-stopped`
3. **Shell script + cron** — poll Gluetun health endpoint and restart containers if unhealthy
4. **Dockhand scheduled task** — use Dockhand's Schedules feature to run a restart command on a health condition

## Notes

- Gluetun exposes a health endpoint at [http://172.39.0.2:9999/v1/openvpn/status](http://172.39.0.2:9999/v1/openvpn/status)
- NZBGet and Prowlarr use `network_mode: service:gluetun` so they cannot have their own healthchecks in compose
- Any solution must work within the Dockhand-managed stack
