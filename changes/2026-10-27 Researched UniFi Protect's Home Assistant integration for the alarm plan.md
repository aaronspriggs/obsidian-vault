---
date: 2026-10-27
type: research
system:
- '[[Home Assistant OS (VM)]]'
- '[[UniFi (UDM Pro)]]'
project: '[[Plan a home security system (Alarmo, door-window sensors, siren)]]'
---

## What changed

No system changes. Research of 2026-10-27 on what Home Assistant's unifiprotect integration can do for the alarm, and the siren step with its 2026-11-11 re-check. Moved here on 2026-11-15 from the [project](<../projects/Plan a home security system (Alarmo, door-window sensors, siren).md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

Aaron prefers UniFi PoE hardware for the siren and wants camera detection in the alarm. The research decided that Alarmo is the alarm brain and Protect only follows it, because adopting UniFi alarm hardware can flip Protect's Alarm Manager to Global mode, where HA can't arm, disarm or read it.

## How

**What HA's unifiprotect integration exposes** ([docs](https://www.home-assistant.io/integrations/unifiprotect/)). Cameras (streams, snapshots), smart detections as binary sensors and event entities (`person`, `vehicle`, `animal`, `package`, `license_plate`, `face`), sirens, relays (switch outputs, binary-sensor inputs), UP-Sense sensors (contact, motion, leak, tamper and more), chimes, doorbell fingerprint and NFC events (`ulp_id`, `nfc_id`), and the Alarm Manager as `alarm_control_panel` plus an Alarm profile `select`. Our install is in API-key-only mode, which lacks buttons, media players, text, actions, media source and the proxy views (event thumbnails, clips, snapshot at a timestamp). Doorbell ring, NFC, fingerprint and vehicle events also need Full access. Full access needs a local UniFi OS user plus the API key (Tier 3: a new user). It's worth it once Protect cameras cover the doors, for snapshots in alarm pushes.

**Alarm Manager Local vs Global mode.** HA's Alarm Manager entities exist only in Local mode, and need Protect 7.2.105+ ([docs](https://www.home-assistant.io/integrations/unifiprotect/)). Protect switches itself to Global mode when sensors, relays, fobs or an Alarm Hub are adopted, and can drift back to Global after a reboot ([HA discussion #972](https://github.com/orgs/home-assistant/discussions/972)). In Global mode the public API can't arm, disarm or read the alarm. Whether adopting a Siren PoE counts isn't documented: Ubiquiti's list doesn't name sirens. Check `alarm_control_panel.dream_machine_pro_alarm_manager` right after adopting it. If it goes to Global and we still want Protect to follow Alarmo, the community [UniFi Protect Alarm Bridge](https://community.home-assistant.io/t/unifi-protect-alarm-bridge-arm-disarm-protects-global-alarm-manager-from-home-assistant/1026598) (posted 2026-09-28, HA 2026.9+, undocumented API, needs a local Super Admin account without MFA) restores arm/disarm; it's young and a security-sensitive credential, so it's a last resort. Profiles are a separate `select` by design; a core request to merge them was closed not planned ([core #172388](https://github.com/home-assistant/core/issues/172388)).

**Protect detections as alarm zones.** The community pattern ([Alarmo + UniFi smart detections thread](https://community.home-assistant.io/t/alarmo-unifi-protect-smart-notifications-as-a-sensor/456582)): Alarmo takes binary sensors only, so use the per-camera person-detected binary sensor directly (giving it a motion device class if Alarmo doesn't list it) or a template binary sensor. Use outdoor cameras in Away mode only, with a short trigger time; they're noisier than door contacts.

**Protect to HA.** Alarm Manager can call a custom webhook (GET, or POST with event details) on any of its triggers, e.g. a person in the backyard at night, into an HA webhook automation ([write-up](https://discussion.scottibyte.com/t/unifi-alarm-manager-using-webhooks/692)). The reverse also exists: an Alarm Manager alarm with a webhook trigger, POSTed with an `x-api-key` ([Homey example](https://community.homey.app/t/unifi-protect-alarm-trigger-from-homey-to-unifi-webhook-post/152543)). Neither is needed for the siren now that HA has a siren entity.

**Doorbell fingerprint/NFC.** On a Protect doorbell with a reader (G4 Doorbell Pro class), HA gets fingerprint events with a `ulp_id` per enrolled user (`unifiprotect.get_user_keyring_info` maps them; Full access only). Community use: [unlock a smart lock via fingerprint, with a reboot safety check](https://community.home-assistant.io/t/unifi-protect-doorbell-unlock-smart-lock-via-fingerprint-with-reboot-safety-check/1026908), which can also disarm the alarm; [a G4 Doorbell Pro NFC/fingerprint write-up](https://chrishansen.tech/posts/unifi_g4_doorbell_pro_part3/). Known gotcha: a doorbell reboot fired a false fingerprint-unlock ([core #132395](https://github.com/home-assistant/core/issues/132395)), hence the safety check.

**Other community tools.** [UniFi Protect Blueprints](https://community.home-assistant.io/t/unifi-protect-blueprints/362604) (detection notifications with an alarm-state condition and cooldown). [Protect Sentinel](https://community.home-assistant.io/t/add-on-protect-sentinel-overnight-unifi-protect-reports-sensitive-zone-alerts-and-critical-push-notifications/1026617), an add-on for overnight reports and "sensitive zone" critical pushes over MQTT (posted 2026-09-28, author-tested only). Both are optional, not part of the plan.

### The siren step as it stood (plan step 6, re-checked 2026-11-11)

Siren: [UniFi Protect Siren PoE](https://store.ui.com/us/en/products/up-siren-poe) ($109, 110 dB, PoE; Aaron to buy). HA's unifiprotect `siren` entity plays 5/10/20/30 s at a time ([siren.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/unifiprotect/siren.py), uiprotect `SirenDuration`), so an automation re-plays it every 30 s while Alarmo is `triggered` and stops it on disarm. Check right after adoption that Protect stays in Local mode (see Reference: UniFi Protect). Backup sounder: the keypad's alarm tones. Re-checked 2026-11-11: still the pick over a Z-Wave siren (Aeotec Siren 6) because it keeps working from Protect if HA dies (step 15) and runs on UPS-backed PoE; retailers list it as IP56 (indoor or outdoor), 802.3af, 5 W, no battery, and some brand it SuperLink, so the Global-mode check after adoption still matters.

## How to verify / roll back

Nothing to roll back. After adopting the siren, check `alarm_control_panel.dream_machine_pro_alarm_manager` still exists (Local mode).
