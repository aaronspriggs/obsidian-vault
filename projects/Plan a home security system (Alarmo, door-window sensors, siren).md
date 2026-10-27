---
type: project
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
next_step: '2026-10-27: Aaron buys a Home Assistant Connect ZWA-2 and the UP Siren PoE, and checks whether the U400 is already in Apple Home or the Aqara app; Claude can start Phase 0 (Alarmo + door zones) on his go.'
---

## Goal

A home alarm built on Home Assistant: Alarmo as the alarm panel and the single source of armed state, the existing door sensors as zones, the Ring Keypad (2nd gen) at the front door as the main arm/disarm point, the phone as a second one, the Aqara U400 front-door lock tied in, and UniFi Protect for the siren and camera-based detection. First scoped 2026-09-27 (never written to the KB, recovered 2026-10-22); planned in detail 2026-10-27.

## Status / next step

2026-10-27: planning. Aaron answered the scoping questions (see Decisions) and asked for research on deep UniFi Protect integration (see Reference below). Hardware to buy: Z-Wave stick and UP Siren PoE. The keypad is powered over PoE at the front door and waiting for a Z-Wave network; HA has no Z-Wave controller yet (only ZHA on the Sonoff ZBDongle-E).

What HA already has, checked live 2026-10-27 (HA 2026.10.4):

| Piece | Entity | Notes |
|---|---|---|
| Front door | `binary_sensor.aeotec_multipurpose_sensor_front_door` | Aeotec Multipurpose (Zigbee, ZHA), reporting today |
| Back door | `binary_sensor.aeotec_multipurpose_sensor_back_door` | same, area Dining Room |
| Garage entrance door | `binary_sensor.aeotec_multipurpose_sensor_garage_entrance_door` | same, area Downstairs; not the overhead garage door |
| Motion | `binary_sensor.aarons_office_ikea_motion_sensor_aarons_office_occupancy`, `binary_sensor.garage_ikea_motion_sensor_garage_occupancy` | IKEA Zigbee; possible Away-only zones |
| Protect Alarm Manager | `alarm_control_panel.dream_machine_pro_alarm_manager` | unifiprotect, disarmed, so Protect is in Local mode today |
| Protect cameras | G6 Instant (Poppy's Bedroom) only | Front Door (doorbell), Driveway, Backyard, Downstairs are still Nest |
| Front door lock | none | Aqara U400 not in HA; Matter over Thread, and HA already has Matter Server + Thread |
| Presence | `person.aaron_spriggs` only | Aaron's wife isn't in HA yet: [Add Aaron's wife to Home Assistant (account, Companion app, person)](<Add Aaron's wife to Home Assistant (account, Companion app, person).md>) |
| Siren | none | |
| Alarmo | not installed | HACS `nielsfaber/alarmo` v1.10.19, plus `alarmo-card` |

## Plan

1. **Phase 0, Alarmo.** Install from HACS (Tier 2). Zones: the three doors as entry/exit with delay; motion Away-only. Alarmo card on a dashboard.
2. **Phase 1, Z-Wave.** Home Assistant Connect ZWA-2 on Big Boi, on its cable outside the metal rack, passed through to the HA VM like the Zigbee dongle (bus/port path). Z-Wave JS integration, then include the keypad with S2. The keypad is the only Z-Wave node, so it must reach the stick directly (basement center to 1st-floor front door); if not, add a mains-powered Z-Wave repeater or plug between them. Re-map both dongles after [Rebuild Big Boi into a new case with an HDD pool for bulk media](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>).
3. **Phase 2, keypad.** Wire it to Alarmo with the [Advanced Ring Keypad V2 Blueprint (Alarmo)](https://community.home-assistant.io/t/advanced-ring-keypad-v2-blueprint-for-home-assistant-alarmo/1010017): state sync (armed, exit delay, entry delay) to the keypad, buttons and codes to Alarmo. Fallback: the [Synchronize Ring Alarm Keypad v2 with Alarmo](https://community.home-assistant.io/t/synchronize-ring-alarm-keypad-v2-with-alarmo/349461) thread.
4. **Phase 3, lock.** Pair the U400 to HA over Matter (multi-admin from Apple Home or the Aqara app; it needs a Thread border router, which HA already sees). Use it in Alarmo: warn on arming if unlocked, lock on Arm Away. Don't auto-disarm on unlock until a paired U400 shows HA which method/user unlocked; [Selora's U400 page](https://selorahomes.com/devices/aqara/smart-lock-u400/) lists lock, settings and battery entities only, no door state and no unlock attribution, and codes/fingerprints stay in the Aqara app or Apple Home.
5. **Phase 4, phone and siren.**
   - Phone: Alarmo card; when everyone is away while disarmed, push "Everyone left, arm Away?" with an Arm button, never a Disarm button. iOS long-press buttons are broken ([Restore iOS notification action buttons once upstream fix ships (iOS 5881)](<Restore iOS notification action buttons once upstream fix ships (iOS 5881).md>)), but tap-to-open works for actions without `authenticationRequired`. "Everyone" needs Aaron's wife in HA first.
   - Alarm push: Companion app critical alert, same as the leak alerts, with a camera snapshot once Protect cameras cover the doors.
   - Siren: [UniFi Protect Siren PoE](https://store.ui.com/us/en/products/up-siren-poe) ($109, 110 dB, PoE). HA's unifiprotect integration gives each siren a `siren` entity with trigger, stop, volume and duration (works in API-key-only mode; default 5 s, indefinite not supported), per the [integration docs](https://www.home-assistant.io/integrations/unifiprotect/). Alarmo's triggered action turns it on with a long duration; disarm turns it off. Max duration unverified until it's installed. Backup sounder: the keypad's own alarm tones.
6. **Phase 5, Protect as part of the alarm** (see Reference): Protect person detections as Away-only zones; Alarmo arm/disarm mirrored to Protect's Alarm Manager so Protect's own alarm rules and recording follow it. Most of this waits for [Migrate cameras from Nest to UniFi Protect](<Migrate cameras from Nest to UniFi Protect.md>), since only the G6 Instant is on Protect.
7. **Phase 6, windows.** Same Aeotec Multipurpose (Zigbee) on the 1st floor and maybe the basement, once Aaron counts them.
8. **Phase 7, resilience.** The keypad battery covers power cuts at the door; HA, both radios, the UDM Pro and the PoE switches are on the UPS ([Rack Infrastructure — UPS + Power Management](<Rack Infrastructure — UPS + Power Management.md>)).

## Decisions

- **2026-10-27:** keypad = Aaron's existing Ring keypad, PoE-powered by the front door, paired directly to HA over Z-Wave (no Ring base station or subscription).
- **2026-10-27:** first zones = the three existing Aeotec door sensors (front, back, garage entrance).
- **2026-10-27 (Aaron):** keypad is the 2nd gen, so the Alarmo blueprint path applies.
- **2026-10-27 (Aaron):** arm mainly at the keypad, also from the phone. When everyone leaves: a push offering to arm, not auto-arm.
- **2026-10-27 (Aaron):** indoor siren is enough; prefer UniFi PoE hardware for it. Chose the UP Siren PoE.
- **2026-10-27:** Z-Wave stick = Home Assistant Connect ZWA-2 over the Zooz ZST39, for range from the basement rack to the 1st-floor front door.
- **2026-10-27 (Aaron):** budget isn't a constraint; priority medium.
- **2026-10-27 (Aaron):** include the Aqara U400 front-door lock. His wife counts for "everyone left" once she's in HA; their infant daughter doesn't.
- **2026-10-27:** siren via HA's native unifiprotect `siren` entity, not a Protect Alarm Manager webhook (the integration gained siren support; the [2025 forum thread](https://community.simon42.com/t/unifi-protect-poe-sirene/71929) saying it couldn't is out of date).
- **2026-10-27:** Alarmo is the one alarm brain; Protect's Alarm Manager only follows it. That way losing Protect's Local mode (see Reference) costs a convenience, not the alarm.

## Open questions

- Is the U400 already set up in Apple Home or the Aqara app, and does it have a Thread connection today?
- How many 1st-floor and basement windows?
- Where does the siren go, and which PoE port feeds it?
- Front door camera: when the doorbell moves to Protect, a model with a fingerprint/NFC reader (see Reference) would add disarm-at-the-door. Worth it?

## Reference: UniFi Protect integration research (2026-10-27)

**What HA's unifiprotect integration exposes** ([docs](https://www.home-assistant.io/integrations/unifiprotect/)). Cameras (streams, snapshots), smart detections as binary sensors and event entities (`person`, `vehicle`, `animal`, `package`, `license_plate`, `face`), sirens, relays (switch outputs, binary-sensor inputs), UP-Sense sensors (contact, motion, leak, tamper and more), chimes, doorbell fingerprint and NFC events (`ulp_id`, `nfc_id`), and the Alarm Manager as `alarm_control_panel` plus an Alarm profile `select`. Our install is in API-key-only mode, which lacks buttons, media players, text, actions, media source and the proxy views (event thumbnails, clips, snapshot at a timestamp). Doorbell ring, NFC, fingerprint and vehicle events also need Full access. Full access needs a local UniFi OS user plus the API key (Tier 3: a new user). It's worth it once Protect cameras cover the doors, for snapshots in alarm pushes.

**Alarm Manager Local vs Global mode.** HA's Alarm Manager entities exist only in Local mode, and need Protect 7.2.105+ ([docs](https://www.home-assistant.io/integrations/unifiprotect/)). Protect switches itself to Global mode when sensors, relays, fobs or an Alarm Hub are adopted, and can drift back to Global after a reboot ([HA discussion #972](https://github.com/orgs/home-assistant/discussions/972)). In Global mode the public API can't arm, disarm or read the alarm. Whether adopting a Siren PoE counts isn't documented: Ubiquiti's list doesn't name sirens. Check `alarm_control_panel.dream_machine_pro_alarm_manager` right after adopting it. If it goes to Global and we still want Protect to follow Alarmo, the community [UniFi Protect Alarm Bridge](https://community.home-assistant.io/t/unifi-protect-alarm-bridge-arm-disarm-protects-global-alarm-manager-from-home-assistant/1026598) (posted 2026-09-28, HA 2026.9+, undocumented API, needs a local Super Admin account without MFA) restores arm/disarm; it's young and a security-sensitive credential, so it's a last resort. Profiles are a separate `select` by design; a core request to merge them was closed not planned ([core #172388](https://github.com/home-assistant/core/issues/172388)).

**Protect detections as alarm zones.** The community pattern ([Alarmo + UniFi smart detections thread](https://community.home-assistant.io/t/alarmo-unifi-protect-smart-notifications-as-a-sensor/456582)): Alarmo takes binary sensors only, so use the per-camera person-detected binary sensor directly (giving it a motion device class if Alarmo doesn't list it) or a template binary sensor. Use outdoor cameras in Away mode only, with a short trigger time; they're noisier than door contacts.

**Protect to HA.** Alarm Manager can call a custom webhook (GET, or POST with event details) on any of its triggers, e.g. a person in the backyard at night, into an HA webhook automation ([write-up](https://discussion.scottibyte.com/t/unifi-alarm-manager-using-webhooks/692)). The reverse also exists: an Alarm Manager alarm with a webhook trigger, POSTed with an `x-api-key` ([Homey example](https://community.homey.app/t/unifi-protect-alarm-trigger-from-homey-to-unifi-webhook-post/152543)). Neither is needed for the siren now that HA has a siren entity.

**Doorbell fingerprint/NFC.** On a Protect doorbell with a reader (G4 Doorbell Pro class), HA gets fingerprint events with a `ulp_id` per enrolled user (`unifiprotect.get_user_keyring_info` maps them; Full access only). Community use: [unlock a smart lock via fingerprint, with a reboot safety check](https://community.home-assistant.io/t/unifi-protect-doorbell-unlock-smart-lock-via-fingerprint-with-reboot-safety-check/1026908), which can also disarm the alarm; [a G4 Doorbell Pro NFC/fingerprint write-up](https://chrishansen.tech/posts/unifi_g4_doorbell_pro_part3/). Known gotcha: a doorbell reboot fired a false fingerprint-unlock ([core #132395](https://github.com/home-assistant/core/issues/132395)), hence the safety check.

**Other community tools.** [UniFi Protect Blueprints](https://community.home-assistant.io/t/unifi-protect-blueprints/362604) (detection notifications with an alarm-state condition and cooldown). [Protect Sentinel](https://community.home-assistant.io/t/add-on-protect-sentinel-overnight-unifi-protect-reports-sensitive-zone-alerts-and-critical-push-notifications/1026617), an add-on for overnight reports and "sensitive zone" critical pushes over MQTT (posted 2026-09-28, author-tested only). Both are optional, not part of the plan.
