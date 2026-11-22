---
date: 2026-11-22
type: config
system:
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Home Assistant (integrations and automations)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/3d38bd1
---

# Added low-water and filter alerts for the Master Bedroom humidifier

Aaron asked for a phone push when the Levoit Superior 6000S runs low on water, and a reminder to change its filter. Two Alert2 alerts in domain `home_health`, added to repo `ha/alert2.yaml` and applied with `ha_config_set_yaml` plus `alert2.reload` (no restart):

- `alert2.home_health_master_bedroom_humidifier_low_water` fires when `binary_sensor.master_bedroom_superior_6000s_low_water` has been `on` for 5 min: "💧 Master Bedroom humidifier is low on water".
- `alert2.home_health_master_bedroom_humidifier_filter_due` fires when `sensor.master_bedroom_superior_6000s_filter_lifetime` is at or below 10 %: "🔄 Master Bedroom humidifier filter is due". The message gives the current percentage.

Both follow the battery-low pattern. They are low priority with no reminders, so each pushes once with Ack / Snooze (2hr) / Open dashboard, held to 09:00 by quiet hours, and then appears in the Sunday weekly report until it clears. Each holds through `unavailable`/`unknown` while firing, so a missed VeSync cloud poll doesn't push a false recovery. Clearing sends a passive "✅ … is refilled" or "✅ … filter is replaced" push.

**Why usage-based for the filter:** the unit tracks its own filter life, which follows how hard it runs; a calendar reminder would come too early in light use and too late in heavy use. 10 % matches the Battery Notes threshold. The filter lifetime was 90 % when this was set up. HA has no filter-reset entity for this model, so after a wick change the filter life is reset in the VeSync app; the alert clears when the sensor reads above 10 % again.

Verify: both alerts loaded `off`, and both conditions evaluated false live; no Alert2 errors in the log after the reload. Roll back: remove the two alerts from `ha/alert2.yaml`, re-apply and `alert2.reload`.
