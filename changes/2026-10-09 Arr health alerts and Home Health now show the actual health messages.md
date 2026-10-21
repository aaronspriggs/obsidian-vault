---
date: 2026-10-09
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Stop false-positive arr health alerts (Sonarr-Radarr-Prowlarr flapping)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/88223b5
notion_id: 3f47ae76-22ba-81fa-b34b-ee1fc2015aa9
---

# Arr health alerts and Home Health now show the actual health messages

What (Tier 2, Aaron said go): (1) New `rest:` block in HA configuration.yaml (repo ha/rest-arr-health.yaml) polls Sonarr/Radarr/Prowlarr /health on 192.168.1.248 every 5 min with keys from HA secrets.yaml (sonarr_api_key, radarr_api_key, prowlarr_api_key; Aaron added them). Six sensors: sensor.<app>_health_errors (count of type=error) and sensor.<app>_health_messages ('error: …' / 'warning: …' joined, max 250 chars, or OK). HA restarted for the new integration; config check passed; all six read 0/OK. (2) automation.homelab_service_device_alerts, app_health_error branch: a variables step pulls the message text; push title is now '<app> reports an error', body includes the messages, logbook too; tap opens /home-health/overview#homelab-all. Falls back to 'open <app> → System → Status' if the sensor is OK/unavailable. Hash 388693743da62395 → 0ab7c2836ee9d3fb. (3) Home Health dashboard: the red homelab-issue card appends the message after an arr health item, and the #homelab-all popup has a new 'Arr app health' markdown card. Why: alerts said only 'an error'; the cause (NZBgeek 429s, per the 10-07 findings) needed opening each app. Roll back: prior alert strings saved on the ClaudeCode VM at ~/.local/state/homelab/ha-config-backups/automation.homelab_service_device_[alerts.2026-10-09.388693743da62395.app](http://alerts.2026-10-09.388693743da62395.app/)_health_error-strings.json (remove the added variables step, restore those two strings and url /home-health/overview); remove the `rest:` key with ha_config_set_yaml and restart. Not yet tested end to end with a real error.
