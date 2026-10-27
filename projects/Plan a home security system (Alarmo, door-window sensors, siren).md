---
type: project
status: active
priority: low
system:
- '[[Home Assistant OS (VM)]]'
next_step: '2026-10-27: Aaron reads the label on the back of the Ring keypad (1st or 2nd gen) and answers the arming questions below; then Claude picks the Z-Wave controller.'
---

## Goal

A home alarm built on Home Assistant: Alarmo as the alarm panel, the existing door sensors as zones, the Ring keypad at the front door for arm/disarm, and a siren. Scoped in a Claude session on 2026-09-27 that was never written to the KB; recovered from that session's summary on 2026-10-22. Cost figures are that session's rough estimates, not quotes.

## Status / next step

2026-10-27: opened for planning. Aaron has a Ring keypad powered over PoE (PoE splitter) by the front door; it blinks green (charging, waiting for a network). It is a Z-Wave device, and HA has no Z-Wave controller (only ZHA on the Sonoff ZBDongle-E), so a Z-Wave stick is the first purchase. The keypad must not be paired to a Ring base station; "waiting for network" suggests it isn't, otherwise factory-reset it first.

What HA already has, checked live 2026-10-27:

| Piece | Entity | Notes |
|---|---|---|
| Front door | `binary_sensor.aeotec_multipurpose_sensor_front_door` | Aeotec Multipurpose (Zigbee, ZHA), reporting today; also has accelerometer and battery-low entities |
| Back door | `binary_sensor.aeotec_multipurpose_sensor_back_door` | same, area Dining Room |
| Garage entrance door | `binary_sensor.aeotec_multipurpose_sensor_garage_entrance_door` | same, area Downstairs; not the overhead garage door |
| Motion | `binary_sensor.aarons_office_ikea_motion_sensor_aarons_office_occupancy`, `binary_sensor.garage_ikea_motion_sensor_garage_occupancy` | IKEA Zigbee; possible interior zones for Away mode |
| UniFi Alarm Manager | `alarm_control_panel.dream_machine_pro_alarm_manager` | from the UniFi Protect integration, disarmed; Alarmo can arm it as an action so Protect's own alarm rules follow the house state |
| Siren | none | no `siren` entities |
| Alarmo | not installed | HACS `nielsfaber/alarmo` v1.10.19 available, plus `alarmo-card` |

## Plan

1. Phase 0: install Alarmo (HACS) and set up zones: the three doors as entry/exit with delay, motion as Away-only.
2. Phase 1: Z-Wave. Buy a Z-Wave controller, plug it into Big Boi on a USB extension, pass it through to the HA VM like the Zigbee dongle (passthrough binds to the bus/port path), add the Z-Wave JS integration, then include the Ring keypad with S2 security. Coordinate with the Big Boi rebuild: both USB dongles move when the case changes.
3. Phase 2: wire the keypad to Alarmo: codes and the Disarm/Home/Away buttons into Alarmo, Alarmo state back to the keypad's indicators and entry/exit beeps.
4. Phase 3: notifications (Companion app critical alerts, same as the leak alerts) and a siren (about $200–400 in the 2026-09-27 estimate).
5. Phase 4: more sensors if wanted (windows, about $400–600 in the estimate for a full set).
6. Phase 5: cameras moved from Nest to UniFi Protect (about $800–1,200), tracked as [Migrate cameras from Nest to UniFi Protect](<Migrate cameras from Nest to UniFi Protect.md>).
7. Phase 6: resilience (keypad battery, Z-Wave/Zigbee radios and HA all depend on Big Boi; UPS coverage).

## Decisions

- **2026-10-27:** keypad = Aaron's existing Ring keypad, PoE-powered by the front door, paired directly to HA over Z-Wave (no Ring base station or subscription).
- **2026-10-27:** first zones = the three existing Aeotec door sensors (front, back, garage entrance).

## Open questions

- Which keypad generation (label on the back)? HA support for the 2nd gen is much better documented; check the 1st gen before buying the stick.
- Who arms it, and how: keypad only, or also phones and presence (auto-arm when everyone leaves)?
- Windows: cover any, and which?
- Siren: indoor only, or outdoor too? Z-Wave or Zigbee?
- Budget?
