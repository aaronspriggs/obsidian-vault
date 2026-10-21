---
date: 2026-09-24
type: research
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3e57ae76-22ba-8153-9e7d-cf602d05f072
---

# Found bug: battery_low_notify automation has never fired (battery.became_low trigger doesn't work on numeric-only battery sensors)

Investigated why Aaron never got a low-battery push for `binary_sensor.samjin_water`'s battery sensor (`sensor.samjin_water_battery`, now at 0.5%, down from 3.5% on 2026-09-04).
`ha_get_automation_traces` on `automation.battery_low_notify` shows `last_triggered: null`, `trace_count: 0` — the automation has never fired, for any device, since it was created 2026-09-04.
Confirmed this isn't specific to one sensor: checked every entity carrying the `battery_watch` label live. Three dimmers (`sensor.kitchen_pendant_dimmer_battery`, `sensor.kitchen_cabinets_battery`, `sensor.living_room_dimmer_battery`) are all at 20% — inside the dashboard's own 15–30% "Low" band — and `sensor.samjin_water_battery` is at 0.5% (deep "Critical"). None triggered a notification.
Likely root cause: the automation's trigger (`battery.became_low`, a device-automation trigger, targeting the `battery_watch` label) is designed for entities backed by a genuine low-battery diagnostic (a `binary_sensor` with `device_class: battery`), not a raw numeric percentage `sensor`. These Zigbee/dimmer devices only expose the numeric `sensor.*_battery` entity, so the "became low" edge the trigger watches for likely never fires. By contrast, `automation.battery_watch_stale_unavailable_digest` (template-based, not a device trigger) does work — it already caught the Living Room Fan Dimmer going unavailable on its first run.
Not fixed yet — Aaron asked to log it and hold off on the fix for now. Proposed fix when we get to it: replace the `battery.became_low` device trigger with a `numeric_state` trigger per `battery_watch`-labeled sensor, using the same 15%/30% thresholds already centralized in `sensor.battery_critical_count` / `sensor.battery_warning_count` / `sensor.battery_healthy_count` from the dashboard work.
