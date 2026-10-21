---
date: 2026-10-14
type: config
system:
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Home Assistant OS (VM)]]'
project:
- '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/bb46cb401ea6a87ae36fbcbc5510cb90ad0fa0d1
notion_id: 3f97ae76-22ba-818c-9c4c-eeed5fb58252
---

# Moved battery low/offline alerts to Alert2; dropped 48 h stale check; fixed quiet-hours notifier

Why: Aaron asked why the 09:00 'Sensor Health Check' push listed 20+ devices. automation.battery_watch_stale_unavailable_digest flagged any battery_watch entity whose last_updated was 48 h+ old; last_updated only changes when the value changes and resets on every HA restart, so stable sensors (battery at 100%, dry leak sensors) all tripped once HA ran 48 h without a restart (2026-10-13: 21 items, 20 of them '91h since last report' = the 10-09 restart). Only real item: Living Room Fan Dimmer unavailable since at least 10-05. Separately, the Water Filter and Softener leak sensor has been at 0.5% battery (Battery Notes low = on) since at least 10-05 and battery_low_notify last fired 09-29, so nothing reminded Aaron. What (Tier 2, Aaron said go ahead): (1) Alert2 alerts in domain home_health (repo ha/alert2.yaml): generator home_health_device_offline over battery_watch sensor.* (20 alerts, unavailable/unknown for 1 h) and home_health_battery_low over battery_low_alert Battery Notes sensors (20 alerts, 10 min delay). Named by device name, since several battery sensor entity_ids don't match their renamed devices. Priority low, iOS 'active', no Alert2 reminders; the 09:00 report is the daily reminder. No 'silent for N hours' check: ZHA, Hue and Matter mark devices unavailable themselves. (2) automation.homelab_alerts_09_00_report now includes domain home_health; title no longer says 'Homelab'. (3) automation.battery_low_notify and automation.battery_watch_stale_unavailable_digest turned off (not deleted). (4) Quiet-hours notifier template rendered 'null', which Alert2 treats as an unknown notifier, raising alert2_error for every held notification (why 'alert2_error' appeared in the 10-12/10-13 morning reports). Now renders '[]' (empty list, per Alert2 source notifierTemplateToList). Verify: 40 alert2.home_health_* entities; alert2.home_health_aeotec_water_leak_sensor_water_filter_and_softener_battery_low and alert2.home_health_living_room_fan_dimmer_offline on; no new alert2_error after 20:00. Roll back: turn the two automations back on, remove the two home_health generators and alert2.reload. Leak alerts stay native (unchanged).
