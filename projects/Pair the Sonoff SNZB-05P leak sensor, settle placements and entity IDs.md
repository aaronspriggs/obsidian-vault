---
type: task
status: done
priority: low
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
parent: '[[Build out water leak sensor automations (notifications, alerts)]]'
completed: 2026-10-17
notion_id: 3fa7ae76-22ba-814d-997f-f7af3d8a7302
---

Closed 2026-10-17 as not needed. Aaron: every leak sensor he bought is an Aeotec and all are set up; there is no SNZB-05P (the KB entry was wrong). Live check 2026-10-17: 4 Aeotec leak sensors in HA (Dishwasher, Kitchen Sink, Utility Room, Water Filter and Softener). The optional entity-ID rename (binary_sensor.samjin_water, binary_sensor.basement_aeotec_water_leak_sensor_utility_room) was dropped: cosmetic only, friendly names are consistent.

## Outcome

Closed 2026-10-17 without work. No Sonoff SNZB-05P exists (Aaron, 2026-10-17); all four leak sensors are Aeotec and already paired, labelled and alerting.

## Decisions

- 2026-10-17: entity-ID normalization dropped. It's cosmetic, and renaming leak sensor IDs is Tier 2 with several consumers (leak alert, Alert2, Home Health dashboard, `sensor.leak_wet_count`).
