---
date: 2026-10-09
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Uptime Kuma]]'
project:
- '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/8d3da5f
notion_id: 3f47ae76-22ba-81fc-b5de-e8729a5ce496
---

# Moved homelab service/device alerts to Alert2 (phone, quiet hours, 09:00 report)

What (Aaron: cut over without waiting for the HDHomeRun test): Alert2 defaults now push to [notify.mobile](http://notify.mobile/)_app_aarons_iphone_17_pro 09:00–20:00 only (notifier template renders 'null' otherwise); fire/reminder pushes are time-sensitive, done/summary passive; tag = alert entity id so the recovery replaces the alert; tap opens /home-health/overview#homelab-all. Added the KB Export Kuma heartbeat (label homelab_watch on sensor.kb_export_status; alert2.homelab_kb_export_missed). New native automations: automation.homelab_alerts_09_00_report (09:00 push of Alert2 alerts still on or fired since 20:00; silent if none) and automation.homelab_alerts_alert2_watchdog (pushes directly if alert2.homelab_kuma_unreachable is unavailable/missing 10 min, held to 09:00 at night). Turned OFF automation.homelab_service_device_alerts (not deleted). Test: [alert2.report](http://alert2.report/) on alert2.alert2_warning at 15:26 notified the phone without errors (Alert2 also sent a one-time v1.16 'data syntax' notice). Also fixed while doing this: kb-export had failed since 2026-10-04 because gitleaks read 'Verified via API: NZBGet/Prowlarr' in the 2026-10-01 servarr Changes entry as an API key (false positive); reworded that sentence and reran kb-export (OK, 228 pages); Kuma heartbeat back up 15:25. Roll back: automation.turn_on homelab_service_device_alerts, set the alert2 notifier back to persistent_notification (or remove the alert2 key) and alert2.reload, turn off the two new automations.
