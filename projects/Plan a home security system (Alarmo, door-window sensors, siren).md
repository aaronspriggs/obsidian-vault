---
type: project
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
next_step: '2026-10-28: ZWA-2 ordered (Aaron); when it arrives, Claude passes it through to the HA VM and adds Z-Wave JS. Still to buy: UP Siren PoE. Phase 0 (Alarmo + door zones) waits on Aaron''s go.'
---

## Goal

A home alarm built on Home Assistant: Alarmo as the alarm panel and the single source of armed state, the existing door sensors as zones, the Ring Keypad (2nd gen) at the front door as the main arm/disarm point, the phone as a second one, the Aqara U400 front-door lock tied in, and UniFi Protect for the siren and camera-based detection. First scoped 2026-09-27 (never written to the KB, recovered 2026-10-22); planned in detail 2026-10-27.

## Status / next step

2026-10-28: planning; the plan below now covers every workstream Aaron asked for (guardrails, garage, sitters, alerts, resilience, smoke/CO, testing). Alarmo install deferred by Aaron until later. ZWA-2 ordered; UP Siren PoE still to buy. The keypad is powered over PoE at the front door and waiting for a Z-Wave network; HA has no Z-Wave controller yet (only ZHA on the Sonoff ZBDongle-E).

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
| Garage overhead door | `cover.garage_door` | Meross MSG100HK (HomeKit model, bought 2022-07-19) via Meross LAN since 2026-10-30, still in Apple Home and the Meross app; door-state reliability not yet confirmed |
| Inner garage door lock | none | plain lock, rarely locked |
| Smoke/CO | `binary_sensor.g6_instant_smoke_alarm_detected` only | G6 Instant audio detection; no smoke/CO alarms in HA |
| Siren | none | |
| Alarmo | not installed | HACS `nielsfaber/alarmo` v1.10.19, plus `alarmo-card` |

## Plan

Grouped by workstream; numbers are a suggested order, not strict dependencies. Each step names who does it where it's Aaron's.

**A. Guardrails (before anything can disarm or unlock)**

1. Propose a STANDARDS rule (Tier 3, Aaron's yes): Claude never unlocks a lock, disarms, or changes alarm zones/codes/automations unless Aaron explicitly asks in that session. Reason: ha-mcp's `ha_call_service` isn't gated, so this session can unlock the door and disarm.
2. Lock down other control paths: lock and Alarmo not exposed to Assist/voice; Alarmo requires a code to disarm from HA's UI; no Disarm button in any push. Once live, alarm and lock automations count as "safety and security" under STANDARDS change authority.

**B. Core alarm**

3. Alarmo (HACS, Tier 2) with modes Away and Home (night: perimeter only, no motion). Zones: front, back and garage entrance doors as entry/exit with delay; garage overhead door with a longer entry delay (step 9); back-door accelerometer and the IKEA motion sensors Away-only.
4. Z-Wave: ZWA-2 (ordered 2026-10-28) on Big Boi, on its cable outside the metal rack, USB passthrough to the HA VM like the Zigbee dongle (bus/port path), Z-Wave JS, include the keypad with S2. The keypad is the only Z-Wave node at first, so it must reach the stick directly (basement center to 1st-floor front door); if not, add a mains-powered Z-Wave repeater or plug. Re-map both dongles after [Rebuild Big Boi into a new case with an HDD pool for bulk media](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>).
5. Keypad: [Advanced Ring Keypad V2 Blueprint (Alarmo)](https://community.home-assistant.io/t/advanced-ring-keypad-v2-blueprint-for-home-assistant-alarmo/1010017) for state sync, codes, buttons, and panic buttons (police/fire/medical → siren + critical push, or dispatch if step 13 is adopted). Fallback: [Synchronize Ring Alarm Keypad v2 with Alarmo](https://community.home-assistant.io/t/synchronize-ring-alarm-keypad-v2-with-alarmo/349461).
6. Siren: [UniFi Protect Siren PoE](https://store.ui.com/us/en/products/up-siren-poe) ($109, 110 dB, PoE; Aaron to buy). HA's unifiprotect `siren` entity plays 5/10/20/30 s at a time ([siren.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/unifiprotect/siren.py), uiprotect `SirenDuration`), so an automation re-plays it every 30 s while Alarmo is `triggered` and stops it on disarm. Check right after adoption that Protect stays in Local mode (see Reference: UniFi Protect). Backup sounder: the keypad's alarm tones.

**C. Entry points and who's coming in**

7. Front door (U400, in HA since 2026-10-27): unlock by fingerprint (household), Home Key UWB/tap (household, most common entry) or PIN (sitters, plus Aaron's) disarms; PIN also pushes "front door unlocked with a code, alarm disarmed". Thumb turn and app unlocks never disarm. Trigger on `changed_by` changing to `Unknown` / `Aliro` / `Keypad` while unlocked (see Reference: U400 unlock sources). Arm Away locks it; arming with it unlocked warns.
8. Garage overhead door (Meross MSG100HK, in Apple Home and the Meross app; Aaron's regular way in). Integrate without leaving Apple Home: [Meross LAN](https://community.home-assistant.io/t/meross-lan-not-reliable/721313) (HACS, local; some users report wrong door state at times), else HomeKit Controller after removing it from Apple Home and re-exposing it through HA's HomeKit Bridge ([community setup](https://community.home-assistant.io/t/meross-smart-garage-door-opener-with-chamberlain-remote-apple-homekit-home-assistant-apple-carplay/636592)). Done 2026-10-30: `cover.garage_door` via Meross LAN ([change](<../changes/2026-10-30 Added the Meross garage door opener to HA via Meross LAN.md>)); check its state against the Home app before relying on it. Left-open alert done 2026-10-30 ([change](<../changes/2026-10-30 Garage door left-open alert with Close, Snooze and Ignore buttons.md>): 15 min, any hour, critical at night, Close door button). Still to do with Alarmo: alert on arming with it open, close it on Arm Away, and treat opening while armed as an entry with a longer delay (time to park and walk to the inner door).
9. Inner garage door: today a plain lock, rarely locked. Add a smart lock with the same disarm rules as the front door, so coming in through the garage disarms by fingerprint or Home Key at the inner door. A second U400 if the door has a deadbolt bore (same Matter, Home Key and fingerprint behavior, already tested); a lever-style lock otherwise (to research once the door hardware is known). Until then, disarm from the phone or the front keypad within the garage entry delay; a second Ring keypad by the inner door is the alternative.
10. Back slider: a second small Zigbee contact sensor on the lever so HA knows latched vs only closed (warn on arming, night reminder), and the existing accelerometer as an Away-only forced-entry zone after a sensitivity test. Motorized options are in Reference: back slider.
11. People: [Add Aaron's wife to Home Assistant (account, Companion app, person)](<Add Aaron's wife to Home Assistant (account, Companion app, person).md>) (Tier 3, Aaron helps). Mother-in-law uses her fingerprint, so she needs no HA account unless she should count for presence. Sitters: PIN disarm + push (step 7); naming them waits on a route in Reference: U400 lock users.
12. Sitter leaves: after a PIN disarm, once the door is locked from outside and there's no motion for N minutes, push "Sitter left, arm Away?" (or auto-arm; Aaron to choose). Needs a test of how the U400 reports a lock from the outside keypad.

**D. Alerts and response**

13. Alarm push: critical alert to Aaron and his wife (bypasses Do Not Disturb), with a camera snapshot once Protect cameras cover the doors (needs Protect Full access mode: local UniFi user, Tier 3). "Everyone left, arm Away?" push with an Arm button when both are away while disarmed (iOS long-press buttons are broken, tap-to-open works: [Restore iOS notification action buttons once upstream fix ships (iOS 5881)](<Restore iOS notification action buttons once upstream fix ships (iOS 5881).md>)).
14. Optional professional dispatch: Noonlight, $9.99/month after a free month, with an HA integration ([Konnected announcement](https://konnected.io/blogs/news/introducing-24-7-smart-home-monitoring-for-security-fire-with-noonlight), [noonlight-hass](https://www.github.com/konnected-io/noonlight-hass)) that exposes an alarm switch. Escalation idea: Alarmo triggered, no disarm within N minutes, then Noonlight. Ask the insurer whether DIY + Noonlight earns a discount.

**E. Resilience**

15. Protect as backup brain: mirror Alarmo's armed state into `alarm_control_panel.dream_machine_pro_alarm_manager` (Local mode) with Alarm Manager rules (person detection, siren, UniFi app push) that keep working if HA or Big Boi dies while armed.
16. Off-box dead-man check: pick up [Monitoring - off-box dead-man check (alert when Big Boi-HA goes silent)](<Monitoring - off-box dead-man check (alert when Big Boi-HA goes silent).md>) (backlog) as part of this.
17. Internet failover so pushes still go out: [UniFi 5G Backup](https://ifeeltech.com/blog/unifi-5g-backup-smb-review) ($99, PoE, launched 2026-05; needs a cellular data plan, cost unverified), or LTE Backup Pro ($279) / 5G Max ($399).
18. Power: Big Boi, UDM Pro and rack PoE switches are on the UPS ([Rack Infrastructure — UPS + Power Management](<Rack Infrastructure — UPS + Power Management.md>)); confirm the keypad's and siren's PoE ports are on a UPS-backed switch. Lock battery alert done 2026-10-27 (20% threshold).

**F. Coverage**

19. Smoke/CO: nothing in HA today except the G6 Instant's audio smoke detection. Option: [Ring Alarm Smoke & CO Listener](https://ring.com/products/alarm-smoke-co-listener), Z-Wave, pairs with Z-Wave JS, sits inches from each existing alarm, about 3-year battery; or replace alarms with Z-Wave smoke/CO units. Hook them to the keypad's fire/CO siren and a critical push. Avoid UniFi's SuperLink smoke alarm: adopting it flips Protect to Global mode.
20. Windows: Aeotec Multipurpose (Zigbee) on the 1st floor and maybe the basement, once Aaron counts them.
21. Cameras: Protect person detection (not animal, because of the pets) as Away-only zones, after [Migrate cameras from Nest to UniFi Protect](<Migrate cameras from Nest to UniFi Protect.md>). G6 Instant (Poppy's room): tie its privacy/recording to Alarmo state (Aaron to choose).

**G. Operations**

22. Monthly walk-test runbook: each door, latch sensor, keypad, siren, each disarm method, garage, pushes to both phones. Record `last_tested`.
23. When everything is built: change notes, a "Home alarm" System note (zones, codes kept in 1Password names only, automations), and the walk-test runbook.

## Decisions

- **2026-10-27:** keypad = Aaron's existing Ring keypad, PoE-powered by the front door, paired directly to HA over Z-Wave (no Ring base station or subscription).
- **2026-10-27:** first zones = the three existing Aeotec door sensors (front, back, garage entrance).
- **2026-10-27 (Aaron):** keypad is the 2nd gen, so the Alarmo blueprint path applies.
- **2026-10-27 (Aaron):** arm mainly at the keypad, also from the phone. When everyone leaves: a push offering to arm, not auto-arm.
- **2026-10-27 (Aaron):** indoor siren is enough; prefer UniFi PoE hardware for it. Chose the UP Siren PoE.
- **2026-10-28:** ZWA-2 ordered (Aaron).
- **2026-10-27:** Z-Wave stick = Home Assistant Connect ZWA-2 over the Zooz ZST39, for range from the basement rack to the 1st-floor front door.
- **2026-10-27 (Aaron):** budget isn't a constraint; priority medium.
- **2026-10-27 (Aaron):** include the Aqara U400 front-door lock. His wife counts for "everyone left" once she's in HA; their infant daughter doesn't.
- **2026-10-27:** siren via HA's native unifiprotect `siren` entity, not a Protect Alarm Manager webhook (the integration gained siren support; an [older forum thread](https://community.simon42.com/t/unifi-protect-poe-sirene/71929) saying it couldn't is out of date).
- **2026-10-28 (Aaron):** unlock-to-disarm covers fingerprint (household), Home Key UWB/tap (household, the most common entry) and PIN (sitters, with a push). Thumb turn and app unlocks never disarm.
- **2026-10-28 (Aaron):** plan all the DIY-alarm considerations (guardrails, sitter re-arm, pets, garage, smoke/CO, resilience, dispatch option, camera privacy, testing). Garage overhead is a regular entry, so it's in scope; a smart lock for the inner garage door is wanted if the alarm can drive it. Alarmo install waits.
- **2026-10-27 (Aaron confirmed):** Alarmo is the one alarm brain; Protect's Alarm Manager only follows it, so losing Protect's Local mode (see Reference) costs a convenience, not the alarm. Consequence: window sensors stay Aeotec Zigbee, and UniFi alarm hardware is limited to the siren and cameras, because adopting UniFi sensors, relays, fobs or an Alarm Hub flips Protect to Global mode.
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
- Sitter names: generic "code used" push for now, naming later (see Reference: U400 lock users)?
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

## Reference: U400 unlock sources (tested 2026-10-27)

Matter debug logging, LockOperation events (`operationSource` raw value → HA `changed_by`, set by [matter/lock.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/matter/lock.py)):

| Unlock | Raw source | `changed_by` | userIndex |
|---|---|---|---|
| Thumb turn (inside) | 0 | Unspecified | none |
| PIN code | 3 (credential type 3, #2) | Keypad | 1 |
| Fingerprint | 128 (Aqara vendor value; confirmed by a fingerprint-only re-test) | Unknown | none |
| Home Key (UWB approach and tap) | 10 (credential type 10, #0 and #1) | Aliro | 1 |
| Any lock | 0 | Unspecified | none |

HA sets the state to `unlocked` first and `changed_by` about 10 ms later, so automations trigger on the attribute, not the state. `Unknown` is also HA's default after a restart, so the first fingerprint unlock after a restart may not fire. Every lock event resets it to Unspecified, so repeats fire. HA drops `userIndex` (no user attribute or event entity), and fingerprints carry no user at all (similar gaps for the U200: [thread](https://community.home-assistant.io/t/aqara-u200-matter-integration/748813?page=5)). Codes and fingerprints stay managed in the Aqara app and Apple Home; HA got the lock by Matter multi-admin from Apple Home.

## Reference: U400 lock users and who-unlocked options (2026-10-28)

Who uses the front door (Aaron, 2026-10-28): fingerprints for Aaron, his wife and his mother-in-law; several pet sitters, each with their own PIN. So the method already splits household from sitters: fingerprint = household, PIN = mostly sitters (Aaron's own PIN too).

`matter.get_lock_users` (read 2026-10-28): 12 of 20 Matter users, all created by fabric 3 (Apple Home), names blank. User 1: Home Key + PIN #2 (Aaron; matches the test unlock). User 2: Home Key + PIN #1 (likely his wife). Users 3–12: one PIN each (likely the sitters, as Apple Home guests). Fingerprints aren't Matter credentials; Aqara manages them, which is why a fingerprint unlock carries no user.

Ways to name the PIN user:
- [ha-matter-lock-identity](https://github.com/alexbbt/ha-matter-lock-identity) (HACS custom): reads the existing users, adds an Operator sensor and an Unlock event per lock, names mapped by Matter user unique ID. Fits the Apple Home-managed codes as they are, but first released 2026-10-25, 0 stars.
- [Lock Code Manager](https://github.com/raman325/lock_code_manager) (HACS, 112 stars, Matter supported with write-only PINs): named slots, calendar schedules, `lock_code_manager_credential_used` events, but only for codes it creates, so the sitter codes would move from Apple Home into HA. It won't report Apple Home users or Home Key ([issue #1754](https://github.com/raman325/lock_code_manager/issues/1754), closed not planned 2026-10-27, redirected to a core feature request).
- Wait for HA core to expose `userIndex` (requested; see also [discussion #2611](https://github.com/orgs/home-assistant/discussions/2611)).

## Reference: per-person unlock automations in the community (2026-10-27)

Mostly built on Z-Wave locks, which report the code slot, often managed with [Keymaster](https://github.com/raman325/keymaster) (named slots, date/time windows, use limits, per-slot notifications; describes itself as Z-Wave). Common uses: guest/cleaner/sitter codes that push a notice and work only in a time window; disarm only for certain slots ([forum example](https://community.home-assistant.io/t/disarm-alarm-automation/190883)); arm when locked from outside on the keypad but not from the inside thumb turn ([2026-06 thread](https://community.home-assistant.io/t/best-way-to-handle-arming-disarming-security-alarm-with-door-lock/1012569), lock method rather than person). Per-person welcome scenes are usually driven by presence, not the lock. For the U400 over Matter, method is available and person isn't (see Phase 3), so: method for disarm/arm, phone presence for who; guest codes would be time-limited in the Aqara app.

## Reference: back slider options (2026-10-27)

The back door is a sliding glass door with a lever latch; the Aeotec Multipurpose on it reports open/closed and has an accelerometer (`binary_sensor.aeotec_multipurpose_sensor_back_door_accelerometer`). Commercial smart locks for sliders are few ([The Smart Cave](https://thesmartcave.com/sliding-door-smart-lock/)).

- **Know it's latched (cheap, local):** a second small Zigbee contact sensor mounted so the lever closes it when latched. HA then knows locked vs only closed; Alarmo can refuse or warn on arming, plus a night reminder. Not automated locking.
- **Accelerometer as a forced-entry zone:** use the existing sensor's accelerometer as an Away-only Alarmo zone, since a glass slider is more likely to be lifted, forced or broken than picked. Needs a sensitivity test.
- **Motorized open/close + lock:** [Smart Slydr (Lychee Things)](https://community.home-assistant.io/t/smart-slyder-sliding-door-patio-auto-open-close-and-lock/739702): locks like a deadbolt, but cloud-only (HACS custom integration, OAuth), slow, pricey, buggy app per its users (2024–2025).
- **Slider locks:** Lockly Guard (Wi-Fi/Bluetooth, [announced CES 2021](https://www.reviewed.com/smarthome/features/lockly-guard-smart-lock-sliding-doors)); Haven Connect with a sliding-door adapter (Wi-Fi or Z-Wave, [Tom's Guide](https://www.tomsguide.com/us/security-haven-lock-kickstarter,news-19616.html)). Current availability and HA support of both unverified.
- **Motorized multipoint door hardware:** replaces the door's lock hardware; reported $800–2,500 per panel ([Gladiator](https://gladiatorwindowanddoors.com/blogs/news/smart-door-hardware-sliding-glass-doors)).
