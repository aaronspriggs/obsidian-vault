---
type: task
status: active
priority: high
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
next_step: '2026-10-17: still at 0.5% (verified live). Aaron swaps the CR2450, using one from a different pack since the last one lasted only from 2026-08-28. Then press ''Battery replaced'' (button.aeotec_water_leak_sensor_water_filter_and_softener_battery_replaced). alert2.home_health_aeotec_water_leak_sensor_water_filter_and_softener_battery_low should clear; if it drains fast again, check the sensor''s LQI. Then the end-to-end leak test can run.'
notion_id: 3e57ae76-22ba-814b-aaae-cd66a7721bc5
---

# Replace battery in Water Filter/Softener leak sensor

binary_sensor.samjin_water (Aeotec, basement, Water Filter and Softener): battery at 0.5% since 2026-09-24 (3.5% on 2026-09-04). Takes a CR2450 (Battery Notes). The low-battery alert is working: alert2.home_health_aeotec_water_leak_sensor_water_filter_and_softener_battery_low is on (verified 2026-10-17). The old battery_low_notify automation is being retired by the alerting redesign.
