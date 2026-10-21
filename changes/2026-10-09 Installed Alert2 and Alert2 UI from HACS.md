---
date: 2026-10-09
type: install
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
notion_id: 3f47ae76-22ba-8180-bac9-e0ab807d5c76
---

# Installed Alert2 and Alert2 UI from HACS

What (Tier 2, Aaron said yes): HACS downloads of Alert2 v1.22 (redstone99/hass-alert2, integration) and Alert2 UI v1.22 (redstone99/hass-alert2-ui, card; HACS registered /hacsfiles/hass-alert2-ui/alert2.js as a dashboard resource). HA Core restarted (Tier 1), then the integration was added through its config flow (entry 01M4H57RRN26NYKEDNBMWRT1PN). Only Alert2's built-in alerts exist (alert2.alert2_error, alert2_warning, alert2_global_exception); no homelab alerts are defined yet, and nothing pushes from it. Why: Alerting redesign, step 1. Verify: ha_search 'alert2' shows those entities and binary_sensor.alert2_ha_startup_done on. Roll back: remove the Alert2 config entry, then remove both repos in HACS and restart.
