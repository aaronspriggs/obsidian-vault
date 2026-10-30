---
date: 2026-10-30
type: install
system:
- '[[Home Assistant OS (VM)]]'
project: '[[Plan a home security system (Alarmo, door-window sensors, siren)]]'
---

# Added the Meross garage door opener to HA via Meross LAN

The garage overhead door is now in HA as `cover.garage_door` (area Garage), through the HACS integration [Meross LAN](https://github.com/krahabb/meross_lan) (`krahabb/meross_lan`, domain `meross_lan`). The opener stays paired to the Meross app and Apple Home, so the Home app button Aaron uses keeps working without HA.

## What changed

Installed Meross LAN from HACS and removed the unused `albertogeniola/meross-homeassistant` v1.3.12 (`meross_cloud`), which had no config entry. Restarted HA with maintenance mode on. Added two `meross_lan` entries: a Meross cloud profile for Aaron's Meross app account (1Password `Homelab - Claude` → "Meross LOGIN"; region `us`, password not saved, cloud MQTT publish off, firmware checks off), used only to fetch the device key and deleted again the same day (below), and the device itself, a Meross MSG100HK (hardware 4.0.0, firmware 4.2.20, MAC 48:e1:e9:7b:53:44) at 192.168.1.40, which HA's DHCP discovery had found. The device entry talks to the opener directly over HTTP on the LAN.

Renamed `cover.smart_garage_door_…_garage` to `cover.garage_door` (name "Garage Door") and the problem sensor to `binary_sensor.garage_door_problem`, and put the device in the Garage area. The other entities (signal strength, refresh/reload buttons, DND light, buzzer switch, open/close duration numbers) keep their generated IDs. After setup the door read `closed`, signal 100%, problem `off`.

## Why

Decided 2026-10-30 in the security plan: Aaron opens and closes the door from the Home app regularly, so the opener must stay in Apple Home, and Meross LAN reaches it without unpairing, where HomeKit Controller would have made the Home app button depend on HA.

## Notes

Some users [report wrong door state at times](https://community.home-assistant.io/t/meross-lan-not-reliable/721313) with Meross LAN; compare `cover.garage_door` against the Home app for a few days before Alarmo or alerts rely on it. Aaron set a fixed IP (192.168.1.40) for it in UniFi the same day, confirmed via the UniFi API. `cover.garage_door` is exposed to Assist by default. Checked the same day: the only Assist pipeline has no speech-to-text and no wake word, there are no voice satellites, no HA Cloud (so no Alexa or Google), and the HomeKit Bridge is disabled, so only a logged-in HA user can reach it through Assist, someone who could press the button anyway. Left exposed; revisit if a voice satellite is added. Siri works through Apple Home's own Meross pairing, outside HA.

Aaron changed the Meross password after setup. The profile entry only contacts the Meross cloud for a device-list query at most once a day ([`const.py`](https://github.com/krahabb/meross_lan/blob/master/custom_components/meross_lan/const.py)), so its token couldn't be tested on demand, and it was only there to fetch the device key. Deleted the profile entry the same day (Aaron's call); the device entry keeps the key and still loaded with no errors afterwards, so nothing in HA talks to the Meross cloud now. If the opener is ever reset and re-paired in the Meross app its key changes: Aaron adds the Meross cloud profile back himself (Settings → Devices & Services → Meross LAN → Add entry → profile) to fetch the new key.
