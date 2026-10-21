---
date: 2026-09-29
type: fix
system:
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Home Assistant OS (VM)]]'
project:
- '[[Fix battery_low_notify automation (has never fired)]]'
notion_id: 3ea7ae76-22ba-81d1-b372-ec7ffcd550f5
---

# Fixed battery low alerts and the daily sensor health digest

battery_low_notify now triggers on Battery Notes low binary sensors (new label battery_low_alert); both battery automations switched to [notify.mobile](http://notify.mobile/)_app_aarons_iphone_17_pro. Tested end to end. No repo commit: HA automations live in HA config.

**Why:** `automation.battery_low_notify` had never fired. `battery.became_low` only acts on battery-class binary sensors, and label `battery_watch` held only numeric `sensor.*_battery` entities (plus leak binary sensors). Separately, both battery automations called `notify.send_message` with a nested `data` payload (push/tag), which HA rejects: the daily digest had errored every run since at least 2026-09-25 ("not a valid option at 'data'").
**What changed (via ha-mcp):**
- New label `battery_low_alert` on the 18 Battery Notes `binary_sensor.*_battery_plus_low` entities. Kept separate from `battery_watch` because the stale digest would flag these sensors as silent (they only update when the battery reports), and the count helpers read `battery_watch`.
- `battery_low_notify`: trigger target label `battery_low_alert`; action `notify.mobile_app_aarons_iphone_17_pro`; message now names the battery type from Battery Notes (e.g. "Kitchen Cabinets is at 20%. Replace with CR2032."). Percentage comes from the device's own battery sensor, because Battery Notes' `battery_plus` sensor is briefly unavailable when the integration reloads.
- `battery_watch_stale_unavailable_digest`: same notify service fix.
**Verified:** digest run manually, `finished` with no error (it pushed about the Sonoff freezer sensor and Living Room Fan Dimmer being unavailable). Low alert tested by raising Kitchen Cabinets' Battery Notes threshold to 25% (the device is at 20%): the automation fired and pushed, then the threshold went back to default (0 = global 10%) and the sensor returned to `off`.
**Behavior to know:** any Battery Notes reload (HA restart, reconfiguring a device) re-fires the alert for devices that are still low. The push `tag` replaces the earlier notification, so it doesn't stack.
**Gap:** Living Room Hue and Bedroom Hue (both `battery_watch`) aren't in Battery Notes, so they have no low sensor and no low alert. Tracked as a Backlog task.
