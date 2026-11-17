---
type: project
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Assistant (integrations and automations)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
next_step: '2026-11-17: the UP Siren PoE is bought and in hand (Aaron). ZWA-2 ordered 2026-10-28 (arrival not recorded); when it is here, Claude passes it through to the HA VM and adds Z-Wave JS. Aaron has unused Ring devices to include too (Hardware on hand). Phase 0 (Alarmo + door zones) waits on Aaron''s go, which he will give in a separate chat.'
---

## Goal

A home alarm built on Home Assistant: Alarmo as the alarm panel and the single source of armed state, the existing door sensors as zones, the Ring Keypad (2nd gen) at the front door as the main arm/disarm point, the phone as a second one, the Aqara U400 front-door lock tied in, and UniFi Protect for the siren and camera-based detection. First scoped 2026-09-27 (never written to the KB, recovered 2026-10-22); planned in detail 2026-10-27.

## Status (2026-11-15)

Planning. Built so far are the garage door in HA with its left-open alert (2026-10-30) and the lock's battery alert (2026-10-27, 20% threshold). The Alarmo install waits on Aaron's go. ZWA-2 ordered 2026-10-28 (arrival not recorded); UP Siren PoE in hand (Aaron, 2026-11-17). Slimmed 2026-11-15: the research is in two change notes, [UniFi Protect](<../changes/2026-10-27 Researched UniFi Protect's Home Assistant integration for the alarm plan.md>) and [the lock and entry points](<../changes/2026-10-28 Tested the Aqara U400's unlock sources and researched the alarm's entry points.md>).

What HA has, checked live 2026-11-15 (HA 2026.11.0):

| Piece | Entity | Notes |
|---|---|---|
| Front door | `binary_sensor.aeotec_multipurpose_sensor_front_door` | Aeotec Multipurpose (Zigbee, ZHA) |
| Back door | `binary_sensor.aeotec_multipurpose_sensor_back_door` | same; a sliding door, with `…_back_door_accelerometer` |
| Garage entrance door | `binary_sensor.aeotec_multipurpose_sensor_garage_entrance_door` | same; the inner door, not the overhead one |
| Motion | `binary_sensor.aarons_office_ikea_motion_sensor_aarons_office_occupancy`, `binary_sensor.garage_ikea_motion_sensor_garage_occupancy` | IKEA Zigbee; possible Away-only zones |
| Protect Alarm Manager | `alarm_control_panel.dream_machine_pro_alarm_manager` | disarmed, so Protect is in Local mode |
| Front door lock | `lock.aqara_smart_lock_u400` | Aqara U400 over Matter, shared from Apple Home 2026-10-27. No door state, no who-unlocked entity |
| Garage overhead door | `cover.garage_door` | Meross MSG100HK via Meross LAN; door-state reliability not yet confirmed |
| Inner garage door lock, siren, Alarmo, Z-Wave | none | |
| Smoke/CO | `binary_sensor.g6_instant_smoke_alarm_detected` only | G6 Instant audio detection |

## Plan

**A. Guardrails (before anything can disarm or unlock)**

1. Propose a STANDARDS rule (Tier 3, Aaron's yes): Claude never unlocks a lock, disarms, or changes alarm zones, codes or automations unless Aaron explicitly asks in that session. Reason: ha-mcp's `ha_call_service` isn't gated, so a session can unlock the door and disarm.
2. Lock down other control paths: lock and Alarmo not exposed to Assist/voice; Alarmo requires a code to disarm from HA's UI; no Disarm button in any push. Once live, alarm and lock automations count as "safety and security" under STANDARDS change authority.

**B. Core alarm**

3. Alarmo (HACS `nielsfaber/alarmo` plus `alarmo-card`, Tier 2) with modes Away and Home (night: perimeter only, no motion). Zones: front, back and garage entrance doors as entry/exit with delay; garage overhead door with a longer entry delay (step 8); back-door accelerometer and the IKEA motion sensors Away-only.
4. Z-Wave: ZWA-2 on Big Boi, on its cable outside the metal rack, USB passthrough to the HA VM like the Zigbee dongle (bus/port path), Z-Wave JS, include the keypad with S2. The keypad is the only Z-Wave node at first, so it must reach the stick directly (basement center to 1st-floor front door); if not, add a mains-powered Z-Wave repeater or plug. Both dongles get re-mapped in the [Big Boi rebuild](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>).
5. Keypad: [Advanced Ring Keypad V2 Blueprint (Alarmo)](https://community.home-assistant.io/t/advanced-ring-keypad-v2-blueprint-for-home-assistant-alarmo/1010017) for state sync, codes, buttons and panic buttons (police/fire/medical → siren + critical push, or dispatch if step 14 is adopted). Fallback: [Synchronize Ring Alarm Keypad v2 with Alarmo](https://community.home-assistant.io/t/synchronize-ring-alarm-keypad-v2-with-alarmo/349461).
6. Siren: [UniFi Protect Siren PoE](https://store.ui.com/us/en/products/up-siren-poe) ($109, 110 dB; in hand, Aaron 2026-11-17). HA's `siren` entity plays at most 30 s at a time, so an automation re-plays it every 30 s while Alarmo is `triggered` and stops it on disarm. Right after adoption, check Protect is still in Local mode (some retailers brand the siren SuperLink). Backup sounder: the keypad's alarm tones.

**C. Entry points and who's coming in**

7. Front door (U400): unlock-to-disarm as decided 2026-10-28; a PIN also pushes "front door unlocked with a code, alarm disarmed". Trigger on the attribute `changed_by` becoming `Unknown` (fingerprint), `Aliro` (Home Key) or `Keypad` (PIN), not on the state, which changes about 10 ms earlier; `Unknown` is also HA's default after a restart, so the first fingerprint unlock after one may not fire. Arm Away locks it; arming with it unlocked warns.
8. Garage overhead door (Aaron's regular way in). Done 2026-10-30: `cover.garage_door` ([change](<../changes/2026-10-30 Added the Meross garage door opener to HA via Meross LAN.md>)) and the left-open alert ([change](<../changes/2026-10-30 Garage door left-open alert with Close, Snooze and Ignore buttons.md>)). Still to do with Alarmo: alert on arming with it open, close it on Arm Away, and treat opening while armed as an entry with a longer delay (time to park and walk to the inner door).
9. Inner garage door (plain lock, rarely locked): add a smart lock with the front door's disarm rules: a second U400 if the door has a deadbolt bore, a lever-style lock otherwise (to research). Until then, disarm from the phone or the front keypad within the garage entry delay; the alternative is a second Ring keypad by the inner door.
10. Back slider: a second small Zigbee contact sensor on the lever so HA knows latched from only closed (warn on arming, night reminder), and the existing accelerometer as an Away-only forced-entry zone after a sensitivity test.
11. People: [Add Aaron's wife to Home Assistant](<Add Aaron's wife to Home Assistant (account, Companion app, person).md>) (Tier 3, Aaron helps). His mother-in-law uses her fingerprint, so she needs no HA account unless she should count for presence. Sitters each have a PIN (step 7). HA can't name who unlocked: it drops the Matter user, and fingerprints carry none; ways round that are in the entry-points change note.
12. Sitter leaves: after a PIN disarm, once the door is locked from outside and there's no motion for N minutes, push "Sitter left, arm Away?" or auto-arm (open question). Needs a test of how the U400 reports a lock from the outside keypad.

**D. Alerts and response**

13. Alarm push: critical alert to Aaron and his wife, with a camera snapshot once Protect cameras cover the doors (needs Protect Full access, i.e. a local UniFi user: Tier 3). "Everyone left, arm Away?" push with an Arm button when both are away while disarmed (iOS long-press buttons are broken, tap-to-open works: [iOS 5881](<Restore iOS notification action buttons once upstream fix ships (iOS 5881).md>)).
14. Optional professional dispatch: Noonlight, $9.99/month, through its HA integration; escalate when Alarmo is triggered and nobody disarms within N minutes. Ask the insurer about a discount.

**E. Resilience**

15. Protect as backup brain: mirror Alarmo's armed state into Protect's Alarm Manager, whose rules (person detection, siren, UniFi app push) keep working if HA or Big Boi dies while armed.
16. Off-box dead-man check: pick up [the backlog task](<Monitoring - off-box dead-man check (alert when Big Boi-HA goes silent).md>) as part of this.
17. Internet failover so pushes still go out: a UniFi cellular backup (5G Backup, $99 plus a data plan of unverified cost, is the cheapest). The Ting second WAN (its own project) would also give failover.
18. Power: confirm the keypad's and siren's PoE ports are on a UPS-backed switch ([UPS project](<Rack Infrastructure — UPS + Power Management.md>)).

**F. Coverage**

19. Smoke/CO: a Ring Smoke & CO Listener (Z-Wave) per floor next to an existing alarm, or Z-Wave smoke/CO units; set the listener's parameter 2 to smoke & CO. Hook them to the keypad's fire/CO siren and a critical push. Avoid UniFi's SuperLink smoke alarm: adopting it flips Protect to Global mode.
20. Windows: the 3 unused Ring contact sensors first, then Aeotec Multipurpose (Zigbee) on the 1st floor and maybe the basement, once Aaron counts them.
21. Cameras: Protect person detection (not animal, because of the pets) as Away-only zones, after [the Nest-to-Protect migration](<Migrate cameras from Nest to UniFi Protect.md>). The G6 Instant in Poppy's room could tie its recording to Alarmo state (open question).

**G. Operations**

22. Monthly walk-test runbook: each door, latch sensor, keypad, siren, disarm method, the garage, pushes to both phones.
23. When built: change notes and a "Home alarm" System note (zones, automations, codes by 1Password item name only).

## Hardware on hand (2026-10-31, Aaron)

Unused Ring Alarm Z-Wave devices, all to join the ZWA-2 network once Z-Wave JS is up (step 4): 1 Smoke & CO Listener (never set up), 3 contact sensors, 1 motion sensor. Z-Wave JS has [configs](https://github.com/zwave-js/zwave-js/tree/master/packages/config/config/devices/0x0346) for them. Any that were paired to a Ring base station need a factory reset or exclusion first. Include with S2 from each QR code. None repeat for the mesh (battery devices).

## Decisions

- **2026-10-27:** keypad = Aaron's existing Ring keypad (2nd gen, so the Alarmo blueprint applies), PoE-powered by the front door, paired directly to HA over Z-Wave: no Ring base station or subscription.
- **2026-10-27:** first zones = the three existing Aeotec door sensors (front, back, garage entrance).
- **2026-10-27 (Aaron):** arm mainly at the keypad, also from the phone. When everyone leaves: a push offering to arm, not auto-arm.
- **2026-10-27 (Aaron):** budget isn't a constraint; priority medium.
- **2026-10-27 (Aaron):** include the Aqara U400 front-door lock. His wife counts for "everyone left" once she's in HA; their infant daughter doesn't.
- **2026-10-27 (Aaron confirmed): Alarmo is the one alarm brain; Protect's Alarm Manager only follows it,** so losing Protect's Local mode costs a convenience, not the alarm. Consequence: window sensors stay Zigbee or Z-Wave, and UniFi alarm hardware is limited to the siren and cameras, because adopting UniFi sensors, relays, fobs or an Alarm Hub flips Protect to Global mode, where HA can't arm, disarm or read it.
- **2026-10-27 (Aaron): an indoor siren is enough, UniFi PoE preferred: the UP Siren PoE,** driven by HA's native `siren` entity, not a Protect Alarm Manager webhook (the integration gained siren support). Re-checked 2026-11-11: still the pick over a Z-Wave siren (Aeotec Siren 6), because it keeps working from Protect if HA dies and runs on UPS-backed PoE.
- **2026-10-27:** Z-Wave stick = Home Assistant Connect ZWA-2 over the Zooz ZST39, for range from the basement rack to the 1st-floor front door. Ordered 2026-10-28 (Aaron).
- **2026-10-28 (Aaron):** unlock-to-disarm covers fingerprint (household), Home Key UWB/tap (household, the most common entry) and PIN (sitters, with a push). Thumb turn and app unlocks never disarm.
- **2026-10-28 (Aaron):** plan all the DIY-alarm considerations (guardrails, sitter re-arm, pets, garage, smoke/CO, resilience, dispatch option, camera privacy, testing). The garage overhead door is a regular entry, so it's in scope; a smart lock for the inner garage door is wanted if the alarm can drive it. Alarmo install waits.
- **2026-10-30 (Aaron):** garage opener is a Meross MSG100HK (bought 2022-07-19). He rarely uses the CarPlay/Siri button (drives a Rivian) but opens and closes the door from the Home app regularly, so it stays paired to Apple Home and HA reaches it through Meross LAN, not HomeKit Controller.

## Open questions

- Inner garage door: does it have a deadbolt bore, or only a knob? Decides second U400 vs a lever-style lock.
- Smoke/CO: how many alarms, and are they hardwired and interconnected? Decides listeners vs replacing them.
- Noonlight dispatch: yes, no, or later?
- Cellular failover for the UDM Pro: yes, no, or later?
- Sitter leaving: push to arm, or auto-arm?
- Home mode at night (perimeter only)?
- G6 Instant in Poppy's room: record only while armed, or leave as is?
- Mother-in-law: count her for presence (needs an HA account), or fingerprint only?
- Sitter names: generic "code used" push for now, naming later?
- How many 1st-floor and basement windows?
- Where does the siren go, and which PoE port feeds it?
- Front door camera: when the doorbell moves to Protect, a model with a fingerprint/NFC reader would add disarm-at-the-door. Worth it?
