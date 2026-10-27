---
type: project
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
next_step: '2026-10-27: Aaron buys a Home Assistant Connect ZWA-2 and the UP Siren PoE, (U400 is now in HA); Claude can start Phase 0 (Alarmo + door zones) on his go.'
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
| Front door lock | `lock.aqara_smart_lock_u400` | Aqara U400, shared from Apple Home to HA over Matter 2026-10-27. Entities: lock, actuator, auto-relock time (300 s), wrong-code limit, operating mode, battery (22% on pairing), firmware. No door state, no who-unlocked entity |
| Presence | `person.aaron_spriggs` only | Aaron's wife isn't in HA yet: [Add Aaron's wife to Home Assistant (account, Companion app, person)](<Add Aaron's wife to Home Assistant (account, Companion app, person).md>) |
| Siren | none | |
| Alarmo | not installed | HACS `nielsfaber/alarmo` v1.10.19, plus `alarmo-card` |

## Plan

1. **Phase 0, Alarmo.** Install from HACS (Tier 2). Zones: the three doors as entry/exit with delay; motion Away-only. Alarmo card on a dashboard.
2. **Phase 1, Z-Wave.** Home Assistant Connect ZWA-2 on Big Boi, on its cable outside the metal rack, passed through to the HA VM like the Zigbee dongle (bus/port path). Z-Wave JS integration, then include the keypad with S2. The keypad is the only Z-Wave node, so it must reach the stick directly (basement center to 1st-floor front door); if not, add a mains-powered Z-Wave repeater or plug between them. Re-map both dongles after [Rebuild Big Boi into a new case with an HDD pool for bulk media](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>).
3. **Phase 2, keypad.** Wire it to Alarmo with the [Advanced Ring Keypad V2 Blueprint (Alarmo)](https://community.home-assistant.io/t/advanced-ring-keypad-v2-blueprint-for-home-assistant-alarmo/1010017): state sync (armed, exit delay, entry delay) to the keypad, buttons and codes to Alarmo. Fallback: the [Synchronize Ring Alarm Keypad v2 with Alarmo](https://community.home-assistant.io/t/synchronize-ring-alarm-keypad-v2-with-alarmo/349461) thread.
4. **Phase 3, lock.** The U400 is already in Apple Home and the Aqara app (Aaron, 2026-10-27), so add HA as another Matter controller rather than re-pairing. On Aaron's iPhone: Home app, the lock, Settings, Turn On Pairing Mode, copy the setup code; then HA Companion app, Settings, Devices & services, Add device, Add Matter device, and enter the code. Commissioning from the iPhone uses Apple's Thread border routers. Apple Home and the Aqara app keep working; codes and fingerprints stay managed there. Use it in Alarmo: warn on arming if unlocked, lock on Arm Away. Aaron wants a code or fingerprint unlock to disarm (2026-10-27). HA's Matter lock sets `changed_by` from the DoorLock LockOperation event's operation source (Keypad, Biometric, Manual, Remote, Aliro and so on; [matter/lock.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/matter/lock.py)); Tested live 2026-10-27 with Matter debug logging (LockOperation events, `operationSource` raw value → HA `changed_by`):

   | Unlock | Raw source | `changed_by` | userIndex |
   |---|---|---|---|
   | Thumb turn (inside) | 0 | Unspecified | none |
   | PIN code | 3 (credential type 3, #2) | Keypad | 1 |
   | Fingerprint | 128 (Aqara vendor value; confirmed by a fingerprint-only re-test) | Unknown | none |
   | Home Key (UWB approach and tap) | 10 (credential type 10, #0 and #1) | Aliro | 1 |
   | Any lock | 0 | Unspecified | none |

   HA sets the state to `unlocked` first and `changed_by` about 10 ms later, so the disarm automation triggers on the `changed_by` attribute changing to `Keypad` or `Unknown` while unlocked, not on the state. `Unknown` is also HA's default after a restart, so the first fingerprint unlock after a restart may not fire; handle that edge when building it. Every lock event resets it to Unspecified, so repeats fire. Home Key doesn't disarm (Aaron asked for code and fingerprint only; revisit). HA drops `userIndex`, so per-user limits (e.g. excluding guest codes) would need custom work; any PIN disarms. Not built yet: it waits for Alarmo (Phase 0). Aaron wants per-person handling (several people have fingerprints and Home Key, 2026-10-27). What the lock sends: PIN and Home Key carry `userIndex` (and credential index), but HA's Matter lock drops it, keeping only `changed_by` ([lock.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/matter/lock.py) has no user attribute or event entity); fingerprint arrives as vendor source 128 with no user at all, so the U400 firmware doesn't identify fingerprint users over Matter (similar gaps reported for the U200 in [this thread](https://community.home-assistant.io/t/aqara-u200-matter-integration/748813?page=5)). Options: infer the person from whose phone just arrived home (Companion app presence), or get `userIndex` into HA for PIN/Home Key (upstream change or a small listener on the Matter Server); fingerprint identity would need Aqara to add it. Earlier note: don't auto-disarm on unlock other than these sources; [Selora's U400 page](https://selorahomes.com/devices/aqara/smart-lock-u400/) lists lock, settings and battery entities only, no door state and no unlock attribution, and codes/fingerprints stay in the Aqara app or Apple Home.
5. **Phase 4, phone and siren.**
   - Phone: Alarmo card; when everyone is away while disarmed, push "Everyone left, arm Away?" with an Arm button, never a Disarm button. iOS long-press buttons are broken ([Restore iOS notification action buttons once upstream fix ships (iOS 5881)](<Restore iOS notification action buttons once upstream fix ships (iOS 5881).md>)), but tap-to-open works for actions without `authenticationRequired`. "Everyone" needs Aaron's wife in HA first.
   - Alarm push: Companion app critical alert, same as the leak alerts, with a camera snapshot once Protect cameras cover the doors.
   - Siren: [UniFi Protect Siren PoE](https://store.ui.com/us/en/products/up-siren-poe) ($109, 110 dB, PoE). HA's unifiprotect integration gives each siren a `siren` entity with trigger, stop, volume and duration (works in API-key-only mode; default 5 s, indefinite not supported), per the [integration docs](https://www.home-assistant.io/integrations/unifiprotect/). A single play is capped at 5, 10, 20 or 30 s (uiprotect `SirenDuration`; [siren.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/unifiprotect/siren.py) rejects other values), so an automation re-plays it every 30 s while Alarmo is `triggered` and stops it on disarm. uiprotect's public `Siren` model covers both wired (`ucp4`) and SuperLink (`lora`) sirens, so the PoE model should appear; confirm after adoption. Backup sounder: the keypad's own alarm tones.
6. **Phase 5, Protect as part of the alarm** (see Reference): Protect person detections as Away-only zones; Alarmo arm/disarm mirrored to Protect's Alarm Manager so Protect's own alarm rules and recording follow it. Most of this waits for [Migrate cameras from Nest to UniFi Protect](<Migrate cameras from Nest to UniFi Protect.md>), since only the G6 Instant is on Protect.
7. **Phase 6, windows.** Same Aeotec Multipurpose (Zigbee) on the 1st floor and maybe the basement, once Aaron counts them.
8. **Phase 7, resilience.** The keypad battery covers power cuts at the door. Big Boi (HA and both radios), the UDM Pro and the rack PoE switches are on the UPS ([Rack Infrastructure — UPS + Power Management](<Rack Infrastructure — UPS + Power Management.md>)); check which switch feeds the keypad and the siren.

## Decisions

- **2026-10-27:** keypad = Aaron's existing Ring keypad, PoE-powered by the front door, paired directly to HA over Z-Wave (no Ring base station or subscription).
- **2026-10-27:** first zones = the three existing Aeotec door sensors (front, back, garage entrance).
- **2026-10-27 (Aaron):** keypad is the 2nd gen, so the Alarmo blueprint path applies.
- **2026-10-27 (Aaron):** arm mainly at the keypad, also from the phone. When everyone leaves: a push offering to arm, not auto-arm.
- **2026-10-27 (Aaron):** indoor siren is enough; prefer UniFi PoE hardware for it. Chose the UP Siren PoE.
- **2026-10-27:** Z-Wave stick = Home Assistant Connect ZWA-2 over the Zooz ZST39, for range from the basement rack to the 1st-floor front door.
- **2026-10-27 (Aaron):** budget isn't a constraint; priority medium.
- **2026-10-27 (Aaron):** include the Aqara U400 front-door lock. His wife counts for "everyone left" once she's in HA; their infant daughter doesn't.
- **2026-10-27:** siren via HA's native unifiprotect `siren` entity, not a Protect Alarm Manager webhook (the integration gained siren support; an [older forum thread](https://community.simon42.com/t/unifi-protect-poe-sirene/71929) saying it couldn't is out of date).
- **2026-10-27 (Aaron confirmed):** Alarmo is the one alarm brain; Protect's Alarm Manager only follows it, so losing Protect's Local mode (see Reference) costs a convenience, not the alarm. Consequence: window sensors stay Aeotec Zigbee, and UniFi alarm hardware is limited to the siren and cameras, because adopting UniFi sensors, relays, fobs or an Alarm Hub flips Protect to Global mode.

## Open questions

- Per person: what should differ? E.g. household disarms everything, a guest/cleaner code disarms but pushes a notice, someone else never disarms.
- Back slider (lever latch): which option (see Reference: back slider)?

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

## Reference: per-person unlock automations in the community (2026-10-27)

Mostly built on Z-Wave locks, which report the code slot, often managed with [Keymaster](https://github.com/raman325/keymaster) (named slots, date/time windows, use limits, per-slot notifications; describes itself as Z-Wave). Common uses: guest/cleaner/sitter codes that push a notice and work only in a time window; disarm only for certain slots ([forum example](https://community.home-assistant.io/t/disarm-alarm-automation/190883)); arm when locked from outside on the keypad but not from the inside thumb turn ([2026-06 thread](https://community.home-assistant.io/t/best-way-to-handle-arming-disarming-security-alarm-with-door-lock/1012569), lock method rather than person). Per-person welcome scenes are usually driven by presence, not the lock. For the U400 over Matter, method is available and person isn't (see Phase 3), so: method for disarm/arm, phone presence for who; guest codes would be time-limited in the Aqara app.

## Reference: back slider options (2026-10-27)

The back door is a sliding glass door with a lever latch; the Aeotec Multipurpose on it reports open/closed and has an accelerometer (`binary_sensor.aeotec_multipurpose_sensor_back_door_accelerometer`). Commercial smart locks for sliders are few ([The Smart Cave](https://thesmartcave.com/sliding-door-smart-lock/)).

- **Know it's latched (cheap, local):** a second small Zigbee contact sensor mounted so the lever closes it when latched. HA then knows locked vs only closed; Alarmo can refuse or warn on arming, plus a night reminder. Not automated locking.
- **Accelerometer as a forced-entry zone:** use the existing sensor's accelerometer as an Away-only Alarmo zone, since a glass slider is more likely to be lifted, forced or broken than picked. Needs a sensitivity test.
- **Motorized open/close + lock:** [Smart Slydr (Lychee Things)](https://community.home-assistant.io/t/smart-slyder-sliding-door-patio-auto-open-close-and-lock/739702): locks like a deadbolt, but cloud-only (HACS custom integration, OAuth), slow, pricey, buggy app per its users (2024–2025).
- **Slider locks:** Lockly Guard (Wi-Fi/Bluetooth, [announced CES 2021](https://www.reviewed.com/smarthome/features/lockly-guard-smart-lock-sliding-doors)); Haven Connect with a sliding-door adapter (Wi-Fi or Z-Wave, [Tom's Guide](https://www.tomsguide.com/us/security-haven-lock-kickstarter,news-19616.html)). Current availability and HA support of both unverified.
- **Motorized multipoint door hardware:** replaces the door's lock hardware; reported $800–2,500 per panel ([Gladiator](https://gladiatorwindowanddoors.com/blogs/news/smart-door-hardware-sliding-glass-doors)).
