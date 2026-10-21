---
date: 2026-10-07
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Uptime Kuma]]'
project:
- '[[Stop false-positive arr health alerts (Sonarr-Radarr-Prowlarr flapping)]]'
notion_id: 3f27ae76-22ba-81b9-ab5f-d0a76afecfd0
---

# Arr health alerts now need 30 min of errors before pushing

What: in `automation.homelab_service_device_alerts` (Tier 2, Aaron said go): the `app_health_error` trigger now has `for: 30 min`. The three arr health sensors moved out of `service_up` into a new `health_up` trigger, and the recovery branch only notifies for health_up when the error lasted 30+ min (UniFi stays at 5 min; services always). The alert text and description now say 30+ min. Why: about 32 pushes in 7 days from NZBgeek 429 rate-limit blips lasting 1–17 min. Note: `sensor.homelab_issue_count` still counts a health sensor while it's down, so the Home Health dashboard shows the blip; it just doesn't push. Verify: config hash 388693743da62395; read-back confirmed all edits. Roll back: the exact prior config (hash 4013236e272cfdf9) is saved on the ClaudeCode VM at ~/.local/state/homelab/ha-config-backups/automation.homelab_service_device_alerts.2026-10-07.4013236e272cfdf9.json; re-apply it with ha_config_set_automation.
