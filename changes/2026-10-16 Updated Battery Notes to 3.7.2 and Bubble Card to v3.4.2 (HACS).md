---
date: 2026-10-16
type: upgrade
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
notion_id: 3fc7ae76-22ba-8169-a57a-c98a963a0b19
---

# Updated Battery Notes to 3.7.2 and Bubble Card to v3.4.2 (HACS)

Battery Notes 3.7.0 → 3.7.2, Bubble Card v3.4.1 → v3.4.2 via HACS, then an HA restart. Pre-update backup 5f6310ad. The Battery Notes unknown→unavailable change needed no config edits.

## What changed

- **Battery Notes 3.7.0 → 3.7.2** ([release notes](https://github.com/andrew-codechimp/HA-Battery-Notes/releases/3.7.2)): mostly bug fixes. Breaking change: sensors that used to show `unknown` now show `unavailable`.
- **Bubble Card v3.4.1 → v3.4.2** ([release notes](https://github.com/Clooos/Bubble-Card/releases/v3.4.2)): frontend-only fixes, including a memory leak on long-open dashboards (relevant to the wall panel) and an editor loop that appeared with HA 2026.10.

## Why

The updates were pending in HA. Aaron asked for a safety check and then approved installing both.

## How

Checked everything that reads Battery Notes or `battery_watch` sensors for `unknown`-only logic: Alert2 `home_health_device_offline` and `home_health_battery_low` in repo `ha/alert2.yaml`, the 11 template helpers, the `home-health` dashboard (Offline / Stale Devices auto-entities filter) and `automation.battery_low_notify` (already off). Every check treats `unknown` and `unavailable` the same, so no edits were needed. Then: maintenance mode on, partial backup `5f6310ad` ("Pre Battery Notes 3.7.2 + Bubble Card 3.4.2"), `ha_manage_updates` install for both, HA restart, maintenance mode off.

## Verify / roll back

After the restart both update entities report the new versions. All 40 Battery Notes entities loaded, and the only `unavailable` ones are `sensor.living_room_fan_dimmer_battery_plus` and its `_low` sensor, which were `unknown` before (the expected change). No Battery Notes errors in the system log. Remaining system-log errors at startup are unrelated: the known HomeKit "Kitchen" / `camera.kitchen` failure, and a legacy `systemmonitor` sensor platform entry that HA says to remove. Clients need a frontend cache clear (wall panel: hard refresh) to load the new Bubble Card. To roll back, redownload the previous version in HACS (Battery Notes also needs a restart); backup `5f6310ad` covers Battery Notes' migrated storage.
