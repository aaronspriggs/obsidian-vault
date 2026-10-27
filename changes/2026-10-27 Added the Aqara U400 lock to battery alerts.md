---
date: 2026-10-27
type: config
system:
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Home Assistant OS (VM)]]'
project:
- '[[Plan a home security system (Alarmo, door-window sensors, siren)]]'
---

# Added the Aqara U400 lock to battery alerts

**What changed:** after Aaron shared the U400 to HA over Matter, it got a Battery Notes entry (type Rechargeable, low threshold 20% instead of the 10% default, since a flat front-door lock is a lockout), `battery_watch` on `sensor.aqara_smart_lock_u400_battery` and `battery_low_alert` on `binary_sensor.aqara_smart_lock_u400_battery_plus_low`, then `alert2.reload`. No repo change: the Alert2 generators in `ha/alert2.yaml` pick devices up by label.

**Verified:** `alert2.home_health_aqara_smart_lock_u400_battery_low` and `alert2.home_health_aqara_smart_lock_u400_offline` exist and are off. The battery read 22% at pairing, so the low alert will fire once it drops below 20% unless it's charged first.
