---
type: project
status: active
priority: low
system:
- '[[Home Assistant OS (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
next_step: '2026-10-27: Aaron buys a Home Assistant Connect ZWA-2 and the UP Siren PoE; meanwhile Claude installs Alarmo and sets up the three door zones (Phase 0).'
---

## Goal

A home alarm built on Home Assistant: Alarmo as the alarm panel, the existing door sensors as zones, the Ring keypad at the front door for arm/disarm, and a siren. Scoped in a Claude session on 2026-09-27 that was never written to the KB; recovered from that session's summary on 2026-10-22. Cost figures are that session's rough estimates, not quotes.

## Status / next step

2026-10-27: opened for planning; Aaron answered the scoping questions the same day (see Decisions). Aaron has a Ring keypad powered over PoE by the front door; it blinks green (charging, waiting for a network). It is a Z-Wave device, and HA has no Z-Wave controller (only ZHA on the Sonoff ZBDongle-E), so a Z-Wave stick is the first purchase. The keypad must not be paired to a Ring base station; "waiting for network" suggests it isn't, otherwise factory-reset it first.

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
2. Phase 1: Z-Wave. Buy a Z-Wave controller, plug it into Big Boi on a USB extension, pass it through to the HA VM like the Zigbee dongle (passthrough binds to the bus/port path), add the Z-Wave JS integration, then include the Ring keypad with S2 security. Any 700/800-series stick includes either keypad generation. Candidates, per [HA's adapter list](https://home-assistant.io/docs/z-wave/controllers/) and a [2026 comparison](https://computingforgeeks.com/best-zwave-800-stick-home-assistant/): Home Assistant Connect ZWA-2 (800 series, external antenna, best range) or Zooz ZST39 (same 800 chip and Long Range, about half the price, no external antenna). Range decides it: the keypad will be the only Z-Wave device (window sensors would be Zigbee), so there is no mesh and the stick, in the basement rack at the center of the house, has to reach the keypad one floor up at the front door directly. Pick: ZWA-2, on its cable outside the metal rack. If it still can't reach, add a mains-powered Z-Wave repeater or plug between them. Coordinate with [Rebuild Big Boi into a new case with an HDD pool for bulk media](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>): both USB dongles move when the case changes.
3. Phase 2: wire the keypad to Alarmo with an existing blueprint rather than custom automations: the [Advanced Ring Keypad V2 Blueprint (Alarmo)](https://community.home-assistant.io/t/advanced-ring-keypad-v2-blueprint-for-home-assistant-alarmo/1010017) syncs armed/arming/pending states to the keypad and maps its buttons, and the long-running [Synchronize Ring Alarm Keypad v2 with Alarmo](https://community.home-assistant.io/t/synchronize-ring-alarm-keypad-v2-with-alarmo/349461) thread is the fallback. Both target the 2nd gen.
4. Phase 3: phone and siren.
   - Phone arming: Alarmo card on an HA dashboard, plus an Alarmo actionable notification. When `person.aaron_spriggs` (and anyone else added) leaves home while disarmed, push "Everyone left, arm Away?" with an Arm button; never a Disarm button. iOS long-press buttons are broken (see [Restore iOS notification action buttons once upstream fix ships (iOS 5881)](<Restore iOS notification action buttons once upstream fix ships (iOS 5881).md>)), but tap-to-open works for actions without `authenticationRequired`, which an Arm button doesn't need.
   - Alarm push: Companion app critical alert on trigger, same as the leak alerts.
   - Siren: [UniFi Protect Siren PoE](https://store.ui.com/us/en/products/up-siren-poe) (UP-Siren-PoE, $109, 110 dB, all-weather, PoE). HA can't drive it directly: the UniFi Protect integration doesn't expose sirens ([simon42 thread](https://community.simon42.com/t/unifi-protect-poe-sirene/71929)). Route: a Protect Alarm Manager alarm with a webhook trigger and a siren action; Alarmo's triggered state calls an HA `rest_command` that POSTs to `https://192.168.1.1/proxy/protect/integration/v1/alarm-manager/webhook/<id>` with a Protect API key in `x-api-key` (pattern from a [Homey community post](https://community.homey.app/t/unifi-protect-alarm-trigger-from-homey-to-unifi-webhook-post/152543); key goes in 1Password and HA `secrets.yaml`). Unverified until it's installed: how to silence it from HA on disarm (siren duration in Alarm Manager vs a second webhook alarm), and whether `alarm_control_panel.dream_machine_pro_alarm_manager` must be armed for the webhook alarm to fire.
   - Backup sounder: the keypad itself can sound alarm tones (per the blueprint above).
5. Phase 4: window sensors, same Aeotec Multipurpose (Zigbee) as the doors, on the 1st floor and maybe the basement. Count and cost once Aaron counts the windows.
6. Phase 5: cameras moved from Nest to UniFi Protect (about $800–1,200), tracked as [Migrate cameras from Nest to UniFi Protect](<Migrate cameras from Nest to UniFi Protect.md>).
7. Phase 6: resilience (keypad battery, Z-Wave/Zigbee radios and HA all depend on Big Boi; UPS coverage).

## Decisions

- **2026-10-27:** keypad = Aaron's existing Ring keypad, PoE-powered by the front door, paired directly to HA over Z-Wave (no Ring base station or subscription).
- **2026-10-27:** first zones = the three existing Aeotec door sensors (front, back, garage entrance).
- **2026-10-27 (Aaron):** keypad is the 2nd gen, so the Alarmo blueprint path applies.
- **2026-10-27 (Aaron):** arm mainly at the keypad, also from the phone. When everyone leaves: a push offering to arm, not auto-arm.
- **2026-10-27 (Aaron):** indoor siren is enough; prefer UniFi PoE hardware for it. Chose the UP Siren PoE.
- **2026-10-27:** Z-Wave stick = Home Assistant Connect ZWA-2 over the Zooz ZST39, for range from the basement rack to the 1st-floor front door.

## Open questions

- Who else in the house should count for "everyone left"? Only `person.aaron_spriggs` is tracked in HA (2026-10-27).
- How many 1st-floor and basement windows?
- Where does the siren go, and which PoE port feeds it?
- Budget?
