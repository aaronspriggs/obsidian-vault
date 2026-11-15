---
date: 2026-10-28
type: research
system:
- '[[Home Assistant OS (VM)]]'
project: '[[Plan a home security system (Alarmo, door-window sensors, siren)]]'
---

## What changed

No system changes. The U400 unlock-source test of 2026-10-27, the read of its Matter users on 2026-10-28, and the research on per-person unlock automations, the back slider, the garage opener, smoke and CO listeners, dispatch and cellular failover (2026-10-27 to 2026-10-31). Moved here on 2026-11-15 from the [project](<../projects/Plan a home security system (Alarmo, door-window sensors, siren).md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

Unlock-to-disarm depends on telling a fingerprint, Home Key or PIN unlock from the thumb turn, and Aaron asked for every DIY-alarm consideration to be planned.

## How

### Reference: U400 unlock sources (tested 2026-10-27)

Matter debug logging, LockOperation events (`operationSource` raw value → HA `changed_by`, set by [matter/lock.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/matter/lock.py)):

| Unlock | Raw source | `changed_by` | userIndex |
|---|---|---|---|
| Thumb turn (inside) | 0 | Unspecified | none |
| PIN code | 3 (credential type 3, #2) | Keypad | 1 |
| Fingerprint | 128 (Aqara vendor value; confirmed by a fingerprint-only re-test) | Unknown | none |
| Home Key (UWB approach and tap) | 10 (credential type 10, #0 and #1) | Aliro | 1 |
| Any lock | 0 | Unspecified | none |

HA sets the state to `unlocked` first and `changed_by` about 10 ms later, so automations trigger on the attribute, not the state. `Unknown` is also HA's default after a restart, so the first fingerprint unlock after a restart may not fire. Every lock event resets it to Unspecified, so repeats fire. HA drops `userIndex` (no user attribute or event entity), and fingerprints carry no user at all (similar gaps for the U200: [thread](https://community.home-assistant.io/t/aqara-u200-matter-integration/748813?page=5)). Codes and fingerprints stay managed in the Aqara app and Apple Home; HA got the lock by Matter multi-admin from Apple Home.

### Reference: U400 lock users and who-unlocked options (2026-10-28)

Who uses the front door (Aaron, 2026-10-28): fingerprints for Aaron, his wife and his mother-in-law; several pet sitters, each with their own PIN. So the method already splits household from sitters: fingerprint = household, PIN = mostly sitters (Aaron's own PIN too).

`matter.get_lock_users` (read 2026-10-28): 12 of 20 Matter users, all created by fabric 3 (Apple Home), names blank. User 1: Home Key + PIN #2 (Aaron; matches the test unlock). User 2: Home Key + PIN #1 (likely his wife). Users 3–12: one PIN each (likely the sitters, as Apple Home guests). Fingerprints aren't Matter credentials; Aqara manages them, which is why a fingerprint unlock carries no user.

Ways to name the PIN user:
- [ha-matter-lock-identity](https://github.com/alexbbt/ha-matter-lock-identity) (HACS custom): reads the existing users, adds an Operator sensor and an Unlock event per lock, names mapped by Matter user unique ID. Fits the Apple Home-managed codes as they are, but first released 2026-10-25, 0 stars.
- [Lock Code Manager](https://github.com/raman325/lock_code_manager) (HACS, 112 stars, Matter supported with write-only PINs): named slots, calendar schedules, `lock_code_manager_credential_used` events, but only for codes it creates, so the sitter codes would move from Apple Home into HA. It won't report Apple Home users or Home Key ([issue #1754](https://github.com/raman325/lock_code_manager/issues/1754), closed not planned 2026-10-27, redirected to a core feature request).
- Wait for HA core to expose `userIndex` (requested; see also [discussion #2611](https://github.com/orgs/home-assistant/discussions/2611)).

### Reference: per-person unlock automations in the community (2026-10-27)

Mostly built on Z-Wave locks, which report the code slot, often managed with [Keymaster](https://github.com/raman325/keymaster) (named slots, date/time windows, use limits, per-slot notifications; describes itself as Z-Wave). Common uses: guest/cleaner/sitter codes that push a notice and work only in a time window; disarm only for certain slots ([forum example](https://community.home-assistant.io/t/disarm-alarm-automation/190883)); arm when locked from outside on the keypad but not from the inside thumb turn ([2026-06 thread](https://community.home-assistant.io/t/best-way-to-handle-arming-disarming-security-alarm-with-door-lock/1012569), lock method rather than person). Per-person welcome scenes are usually driven by presence, not the lock. For the U400 over Matter, method is available and person isn't (see Phase 3), so: method for disarm/arm, phone presence for who; guest codes would be time-limited in the Aqara app.

### Reference: back slider options (2026-10-27)

The back door is a sliding glass door with a lever latch; the Aeotec Multipurpose on it reports open/closed and has an accelerometer (`binary_sensor.aeotec_multipurpose_sensor_back_door_accelerometer`). Commercial smart locks for sliders are few ([The Smart Cave](https://thesmartcave.com/sliding-door-smart-lock/)).

- **Know it's latched (cheap, local):** a second small Zigbee contact sensor mounted so the lever closes it when latched. HA then knows locked vs only closed; Alarmo can refuse or warn on arming, plus a night reminder. Not automated locking.
- **Accelerometer as a forced-entry zone:** use the existing sensor's accelerometer as an Away-only Alarmo zone, since a glass slider is more likely to be lifted, forced or broken than picked. Needs a sensitivity test.
- **Motorized open/close + lock:** [Smart Slydr (Lychee Things)](https://community.home-assistant.io/t/smart-slyder-sliding-door-patio-auto-open-close-and-lock/739702): locks like a deadbolt, but cloud-only (HACS custom integration, OAuth), slow, pricey, buggy app per its users (2024–2025).
- **Slider locks:** Lockly Guard (Wi-Fi/Bluetooth, [announced CES 2021](https://www.reviewed.com/smarthome/features/lockly-guard-smart-lock-sliding-doors)); Haven Connect with a sliding-door adapter (Wi-Fi or Z-Wave, [Tom's Guide](https://www.tomsguide.com/us/security-haven-lock-kickstarter,news-19616.html)). Current availability and HA support of both unverified.
- **Motorized multipoint door hardware:** replaces the door's lock hardware; reported $800–2,500 per panel ([Gladiator](https://gladiatorwindowanddoors.com/blogs/news/smart-door-hardware-sliding-glass-doors)).

### Plan steps as they stood, with their sources

**Garage overhead door (step 8).** Garage overhead door (Meross MSG100HK, in Apple Home and the Meross app; Aaron's regular way in). Integrate without leaving Apple Home: [Meross LAN](https://community.home-assistant.io/t/meross-lan-not-reliable/721313) (HACS, local; some users report wrong door state at times), else HomeKit Controller after removing it from Apple Home and re-exposing it through HA's HomeKit Bridge ([community setup](https://community.home-assistant.io/t/meross-smart-garage-door-opener-with-chamberlain-remote-apple-homekit-home-assistant-apple-carplay/636592)). Done 2026-10-30: `cover.garage_door` via Meross LAN ([change](<../changes/2026-10-30 Added the Meross garage door opener to HA via Meross LAN.md>)); check its state against the Home app before relying on it. Left-open alert done 2026-10-30 ([change](<../changes/2026-10-30 Garage door left-open alert with Close, Snooze and Ignore buttons.md>): 15 min, any hour, critical at night, Close door button). Still to do with Alarmo: alert on arming with it open, close it on Arm Away, and treat opening while armed as an entry with a longer delay (time to park and walk to the inner door).

**Professional dispatch (step 14).** Optional professional dispatch: Noonlight, $9.99/month after a free month, with an HA integration ([Konnected announcement](https://konnected.io/blogs/news/introducing-24-7-smart-home-monitoring-for-security-fire-with-noonlight), [noonlight-hass](https://www.github.com/konnected-io/noonlight-hass)) that exposes an alarm switch. Escalation idea: Alarmo triggered, no disarm within N minutes, then Noonlight. Ask the insurer whether DIY + Noonlight earns a discount.

**Internet failover (step 17).** Internet failover so pushes still go out: [UniFi 5G Backup](https://ifeeltech.com/blog/unifi-5g-backup-smb-review) ($99, PoE, launched 2026-05; needs a cellular data plan, cost unverified), or LTE Backup Pro ($279) / 5G Max ($399).

**Smoke and CO (step 19).** Smoke/CO: nothing in HA today except the G6 Instant's audio smoke detection. Option: [Ring Alarm Smoke & CO Listener](https://ring.com/products/alarm-smoke-co-listener), Z-Wave, about 3-year battery, sits inches from an existing alarm and hears its T3 smoke / T4 CO pattern (detects nothing itself). Z-Wave JS has a device config ([ring_smoke_co_listener.json](https://github.com/zwave-js/zwave-js/blob/master/packages/config/config/devices/0x0346/ring_smoke_co_listener.json), checked 2026-10-31; parameter 2 must be set to smoke & CO, default is smoke only). With interconnected alarms every listener fires at once, so one per floor is enough and none tells you where; or replace alarms with Z-Wave smoke/CO units. Hook them to the keypad's fire/CO siren and a critical push. Avoid UniFi's SuperLink smoke alarm: adopting it flips Protect to Global mode.

## How to verify / roll back

Nothing to roll back. The unlock-source table can be re-tested with Matter debug logging on and one unlock per method.
