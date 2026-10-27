---
type: project
status: active
priority: low
system:
- '[[Home Assistant OS (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
next_step: '2026-10-27: Aaron picks a Z-Wave stick (ZWA-2 or ZST39, see Plan) after saying how far the rack is from the front door; separately he reads the keypad generation off its back label.'
---

## Goal

A home alarm built on Home Assistant: Alarmo as the alarm panel, the existing door sensors as zones, the Ring keypad at the front door for arm/disarm, and a siren. Scoped in a Claude session on 2026-09-27 that was never written to the KB; recovered from that session's summary on 2026-10-22. Cost figures are that session's rough estimates, not quotes.

## Status / next step

2026-10-27: opened for planning. Aaron has a Ring keypad powered over PoE by the front door; it blinks green (charging, waiting for a network). It is a Z-Wave device, and HA has no Z-Wave controller (only ZHA on the Sonoff ZBDongle-E), so a Z-Wave stick is the first purchase. The keypad must not be paired to a Ring base station; "waiting for network" suggests it isn't, otherwise factory-reset it first.

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
2. Phase 1: Z-Wave. Buy a Z-Wave controller, plug it into Big Boi on a USB extension, pass it through to the HA VM like the Zigbee dongle (passthrough binds to the bus/port path), add the Z-Wave JS integration, then include the Ring keypad with S2 security. Any 700/800-series stick includes either keypad generation. Candidates, per [HA's adapter list](https://home-assistant.io/docs/z-wave/controllers/) and a [2026 comparison](https://computingforgeeks.com/best-zwave-800-stick-home-assistant/): Home Assistant Connect ZWA-2 (800 series, external antenna, best range) or Zooz ZST39 (same 800 chip and Long Range, about half the price, no external antenna). Range decides it: with one Z-Wave node there is no mesh, so the stick in the rack has to reach the front door directly. Coordinate with [Rebuild Big Boi into a new case with an HDD pool for bulk media](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>): both USB dongles move when the case changes.
3. Phase 2: wire the keypad to Alarmo with an existing blueprint rather than custom automations: the [Advanced Ring Keypad V2 Blueprint (Alarmo)](https://community.home-assistant.io/t/advanced-ring-keypad-v2-blueprint-for-home-assistant-alarmo/1010017) syncs armed/arming/pending states to the keypad and maps its buttons, and the long-running [Synchronize Ring Alarm Keypad v2 with Alarmo](https://community.home-assistant.io/t/synchronize-ring-alarm-keypad-v2-with-alarmo/349461) thread is the fallback. Both target the 2nd gen.
4. Phase 3: notifications (Companion app critical alerts, same as the leak alerts) and a siren (about $200–400 in the 2026-09-27 estimate).
5. Phase 4: more sensors if wanted (windows, about $400–600 in the estimate for a full set).
6. Phase 5: cameras moved from Nest to UniFi Protect (about $800–1,200), tracked as [Migrate cameras from Nest to UniFi Protect](<Migrate cameras from Nest to UniFi Protect.md>).
7. Phase 6: resilience (keypad battery, Z-Wave/Zigbee radios and HA all depend on Big Boi; UPS coverage).

## Decisions

- **2026-10-27:** keypad = Aaron's existing Ring keypad, PoE-powered by the front door, paired directly to HA over Z-Wave (no Ring base station or subscription).
- **2026-10-27:** first zones = the three existing Aeotec door sensors (front, back, garage entrance).

## Open questions

- Which keypad generation (label on the back)? The Alarmo blueprints found 2026-10-27 are for the 2nd gen; for a 1st gen only Ring's [Z-Wave technical manual](https://ring.com/support/articles/o8ty4/Ring-Alarm-Keypad-1st-gen-Z-Wave-Technical-Manual) turned up, so Phase 2 would be custom work.
- How far is the rack from the front door, through how many floors and walls? Decides ZWA-2 vs ZST39, and whether a Z-Wave repeater is needed.
- Who arms it, and how: keypad only, or also phones and presence (auto-arm when everyone leaves)?
- Windows: cover any, and which?
- Siren: indoor only, or outdoor too? Z-Wave or Zigbee?
- Budget?
