---
date: 2026-10-09
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Uptime Kuma]]'
project:
- '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/1448f42
notion_id: 3f47ae76-22ba-8109-9b82-fa0ae3ca9560
---

# Added Alert2 pilot for homelab service and device alerts

What: Aaron added `alert2` as an extra YAML key in the HA-MCP File & YAML Tools options, so ha-mcp can write it. Claude wrote an `alert2:` block to configuration.yaml (repo ha/alert2.yaml; config check ok) and ran alert2.reload (no restart needed). It creates 27 alerts named alert2.homelab_*, matching automation.homelab_service_device_alerts: 13 Kuma service monitors (**down) and 7 UniFi devices (**_offline, 5 min delay) generated from the homelab_watch label, 3 Kuma heartbeats (**_missed), 3 arr health alerts from the rest: sensors (*_health, 30 min delay, only while the app is up), and kuma_unreachable (5 min). Pilot notifier is persistent_notification only (collapse_and_dismiss), so no pushes and no duplicates; the old automation is unchanged and still pushes. Added a custom:alert2-overview card at the top of the Home Health #homelab-all popup. Verify: sensor.alert2generator_homelab** counts 13/3/7/3; all alerts off; alert2.alert2_error never fired. Found: the KB Export Kuma push monitor has no homelab_watch label, so neither the old automation nor the pilot watches it. Roll back: remove the alert2 key with ha_config_set_yaml, alert2.reload, and remove the card.
