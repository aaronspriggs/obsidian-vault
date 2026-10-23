---
status: active
category: software
url: http://192.168.1.218:8123/home-health/overview
runs_on:
- '[[Home Assistant OS (VM)]]'
last_verified: 2026-10-17
notion_id: 3ea7ae76-22ba-81ff-9924-fe27308ed491
---

HA dashboard + alerts for house health: water leaks and shutoff, device batteries, Zigbee signal, stale sensors, HA updates. Quiet when everything is fine.

## Overview

The house-health layer built in Home Assistant: one dashboard plus the alerts behind it, covering water leaks and the whole-home shutoff valve, device batteries, Zigbee signal, stale/offline sensors, and pending HA updates. Built 2026-09-04, redesigned as a "status board" 2026-09-05. Split out of the [Home Assistant OS (VM)](<Home Assistant OS (VM).md>) page on 2026-09-29. Homelab/server monitoring (TrueNAS, Kuma, VMs) is separate: see "Homelab health monitoring with Home Assistant alerts" in Projects.

## Access

- Dashboard: [http://192.168.1.218:8123/home-health/overview](http://192.168.1.218:8123/home-health/overview) ("Home Health" in the sidebar). Alerts go to Aaron's iPhone via the Companion app.
- Claude edits it through ha-mcp. Dashboard conventions and gotchas: [HA dashboard conventions and gotchas (reference)](<../runbooks/HA dashboard conventions and gotchas (reference).md>).

## Config

**Dashboard layout (status board, since 2026-09-05)**
- **Hero banner:** full-width `mushroom-template-card`, red/green gradient via card_mod, driven by `sensor.home_health_issue_count` (wet leaks + critical batteries + offline sensors + weak signal; HA updates deliberately excluded as routine). Read 2 on 2026-09-29.
- **Water Leak & Shutoff:** one green "All sensors dry" line; turns red and names the sensor when `sensor.leak_wet_count` > 0. Valve, flow, pressure and usage tiles below. `column_span` = 4 so it fills its row.
- **Battery Levels / Signal Health:** native `distribution` card, plus a full-width `mushroom-chips-card` row whose chips open Bubble Card pop-ups (`#battery-healthy|low|critical`) listing devices via `custom:auto-entities`.
- **Sensor Health / HA System:** visibility-gated `mushroom-template-card`s that only appear when their count is above 0.
- Sections view, `max_columns` 4.
- HACS cards used: Mushroom, Bubble Card, auto-entities, card-mod.
**Labels (the single source for what's monitored)**
- `leak_sensor`: the 4 Zigbee leak sensors (dishwasher, kitchen sink, basement utility room, water filter/softener `binary_sensor.samjin_water`).
- `battery_watch` (30 entities): physical battery devices (door/window, IKEA motion, dimmers, freezer temp, leak sensors). Personal electronics (phone, Watch, Rivian) excluded on purpose. To monitor a new battery device, add the label. **ecobee room sensors (6, since 2026-10-17):** the ecobee integration exposes no battery entity, so the label sits on each sensor's `sensor.<room>_temperature`; ecobee reports a sensor it can't hear from as `unknown` (verified in `ecobee/sensor.py`), which the offline alert catches. They get offline alerts only, no low-battery alert (the ecobee app sends its own). The offline and battery-low alerts are named after the device, so every watched device needs a unique name.
- `battery_low_alert` (20, one per `battery_watch` device): the Battery Notes `binary_sensor.*_battery_plus_low` sensors that drive the low-battery push. Separate from `battery_watch` on purpose (the old stale digest would have flagged them). To monitor a new battery device: add it to Battery Notes, then put `battery_watch` on its battery sensor and `battery_low_alert` on its new `*_battery_plus_low` sensor.
- `signal_watch` (9): ZHA LQI sensors for the leak, door and freezer sensors (ZHA creates them disabled; they were enabled).
**Template helpers:** `sensor.home_health_issue_count`, `leak_wet_count`, `battery_attention_count`, `battery_critical_count` (<15%), `battery_warning_count` (15–30%), `battery_healthy_count`, `signal_weak_count` (LQI < 100), `signal_strong_count`, `sensor_health_issue_count`, `ha_pending_update_count` (all `update.*`, including ZHA device firmware). Thresholds live only in these helpers; cards reference them.
**Automations**
- `automation.water_leak_detected_notify`: `moisture.detected` on label `leak_sensor` → critical push naming the sensor; tapping it shows **Shut Off Water** / **Dismiss** (since 2026-10-14, see Decisions). Never triggered for real yet (end-to-end test tracked in Open work).
- `automation.water_leak_notification_handle_actions`: "Shut Off Water" (closes the valve) and "Dismiss" (logbook only) buttons. Working via tap since 2026-10-14; Dismiss verified with a test push.
- **Battery alerts are Alert2 (since 2026-10-14)**, domain `home_health`, config in repo `ha/alert2.yaml`: `alert2.home_health_<device>_offline` (one per `battery_watch` battery sensor, fires after 1 h unavailable/unknown) and `alert2.home_health_<device>_battery_low` (one per `battery_low_alert` sensor, Battery Notes threshold, 10 min delay). Named by device name from the device registry, not entity_id (several battery sensor entity_ids don't match their renamed devices, e.g. `sensor.kitchen_pendant_dimmer_battery` is the Backyard Dimmer). Battery-low alerts hold through `unavailable`/`unknown` while firing, so a Battery Notes reload (adding or reconfiguring a note) doesn't clear and re-fire them (since 2026-10-17). Low priority, no Alert2 reminders, 20:00–09:00 quiet hours: they push once (with Ack / Snooze (2hr) / Open dashboard buttons), then anything still open is listed in the Sunday 09:00 weekly report (`automation.homelab_alerts_weekly_report_sunday_09_00`). Push rules: runbook "Homelab alerting", section Push rules (since 2026-10-14). Adding a battery device: same labels as below, then `alert2.reload`.
- Deleted 2026-10-23 (off since 2026-10-14, replaced by Alert2's per-device battery-low alerts): `automation.battery_low_notify` and `automation.battery_watch_stale_unavailable_digest`. The digest's "silent 48 h+" check used `last_updated`, which only moves on value changes and resets on restart, so it flagged ~20 healthy sensors whenever HA ran 48 h without a restart. ZHA, Hue and Matter mark silent devices unavailable on their own, so there is no staleness check any more.
**Battery Notes** (HACS, andrew-codechimp/HA-Battery-Notes, 3.7.2 since 2026-10-16): 27 devices with battery type, a "Battery replaced" button and last-replaced date (CR2450: 8 Aeotec sensors; CR2032: 9 Hue dimmers + Lutron Pico, and the 6 ecobee room sensors, which get type and dates only since there's no level to read; 2×AAA: 2 IKEA motion; CR2477: freezer sensor). Since 3.7.2 its sensors show `unavailable` (not `unknown`) when their source is. Its own low threshold is 10% and drives the Alert2 battery-low alerts. iPhone, Front Door Nest and Sonos Roam deliberately ignored.
**Flo by Moen shutoff:** `switch.shutoff_valve`, plus flow, pressure, temperature, daily usage and system-mode sensors. Utility meter "Water Usage".

## Dependencies

Runs on Home Assistant OS (ZHA via the Sonoff ZBDongle-E, Flo, Companion app push). Critical alerts only bypass Do Not Disturb if the iPhone grants the Companion app **Critical Alerts** permission.

## Decisions

- **2026-09-04:** notify only, never auto-close the valve on a leak: a false positive would cut water to the whole house. The valve is closed by a deliberate tap.
- **2026-09-04:** Puppet add-on (for ha-mcp dashboard screenshots) declined: it opens an unauthenticated listener on a flat LAN. Visual checks stay manual. Revisit only with VLANs.
- **2026-09-05:** status-board design: compact signal always visible, detail only when something's wrong. A dashboard that's always colored gets ignored.
- **2026-10-14 (Claude, delegated by Aaron):** battery low/offline alerts moved to Alert2 under the same quiet hours and morning report as homelab alerts (Alerting redesign step 3). Leak alerts stay native and critical.
- **2026-10-17:** Lutron Aurora renamed in HA from "Cheryl's Office" to "Cheryl's Office Dimmer" (Hue bridge name unchanged) because it collided with the ecobee "Cheryls Office" sensor's alert name.
- **2026-09-25:** iOS notification action buttons are broken upstream (home-assistant/iOS#5881). Tapping the leak alert opens the valve control instead.
- **2026-10-14 (Aaron):** buttons work by tapping the push (Companion "show actions when tapped"), so the valve-control tap was removed and the leak push follows the one-tap standard: no `url`/`entity_id` (they hide the button sheet) and no Face ID gate. Long-press is still broken upstream.

## Related

- Runbook: [HA dashboard conventions and gotchas (reference)](<../runbooks/HA dashboard conventions and gotchas (reference).md>).
- Project history: "Build out water leak sensor automations"; Changes from 2026-09-04 and 2026-09-05.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
