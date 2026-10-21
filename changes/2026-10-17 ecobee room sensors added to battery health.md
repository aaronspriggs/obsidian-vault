---
date: 2026-10-17
type: config
system:
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Home Assistant OS (VM)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/e78d34de7cbf75b4785c83c3f984c1fda8dbf317
notion_id: 3fc7ae76-22ba-814d-9f2b-f69113e5a5f2
---

# ecobee room sensors added to battery health; battery-low alerts survive Battery Notes reloads

4 ecobee room sensors added to Battery Notes (CR2032); battery_watch on all 6 ecobee temperature sensors; Lutron Aurora renamed Cheryl’s Office Dimmer; Alert2 battery_low holds through unavailable and names by device registry; Offline popup lists all battery_watch sensors.

## What changed

- **Battery Notes:** added Dining Room, Cheryls Office, Master Bedroom and Loft ecobee room sensors (1× CR2032, default threshold), matching Poppys Room and Aarons Office from 10-15. They get type, last-replaced date and a Battery replaced button only: the ecobee integration exposes no battery level.
- **Label ****`battery_watch`** on `sensor.{aarons_office,poppys_room,dining_room,cheryls_office,master_bedroom,loft}_temperature`, so each ecobee sensor has an `alert2.home_health_<room>_offline` alert (1 h unknown/unavailable).
- **Renamed the Lutron Aurora** (Hue, device `3a294e70…`) in HA from "Cheryl’s Office" to "Cheryl’s Office Dimmer": its alert names collided with the ecobee "Cheryls Office" sensor. Entity IDs unchanged; nothing referenced the old alert IDs.
- **Alert2 ****`home_health_battery_low`** (repo `ha/alert2.yaml`): the condition holds through `unavailable`/`unknown` while the alert is firing, and names/titles come from the device registry instead of Battery Notes' `device_name` attribute.
- **Dashboard ****`home-health`****:** Offline / Stale Devices popup now lists every `battery_watch` sensor that's unavailable/unknown, not only `device_class: battery` ones, so it matches `sensor.sensor_health_issue_count`.

## Why

Aaron asked whether the new ecobee sensors were covered (they weren't) and to clear the pending Battery Notes discoveries. Adding notes reloads Battery Notes, which blipped every low sensor to unavailable at 21:32 on 10-16: the softener's battery-low alert cleared, pushed "✅ None battery is OK again" (no `device_name` while unavailable), and an unavailable sensor generated `alert2.home_health_none_battery_low`. A first fix with split `condition_on`/`condition_off` was replaced the same night: those are edge-triggered, so a battery already low at load never fired.

## How

ha-mcp: Battery Notes `config_subentry` creates, `ha_set_entity` labels, `ha_set_device` rename, `ha_config_set_yaml` replace of `alert2:` (preview diff + config check), `alert2.reload`, dashboard JSON patch. Ecobee behavior checked against `homeassistant/components/ecobee/sensor.py` (dev): remote sensor value `unknown` → state unknown; thermostat disconnected → unavailable.

## Verify / roll back

After reload: 6 new `alert2.home_health_<room>_offline` entities (off), `cheryls_office_dimmer_offline/_battery_low` present, the old `cheryls_office_battery_low` and `none_battery_low` gone, softener battery-low alert back on with "At 0.5%. Replace with CR2450…". Not tested end to end: an ecobee sensor actually going `unknown` (needs a battery pulled). Known gap: if ecobee's cloud drops for 1 h+, all 6 offline alerts fire at once.
The 4 leftover Battery Notes discovery prompts cleared with an HA restart later on 2026-10-17 and weren't re-offered (discovery skips devices that already have a note; don't use Add on such a prompt, it may duplicate the note). The same restart confirmed the fix: the softener battery-low alert stayed on through the Battery Notes reload, with no "OK again" push and no Alert2 state changes logged.
Roll back: revert the commit and re-apply `alert2:`; `ha_set_device(name='')` restores the Aurora's Hue name; remove the label / delete the 4 subentries.
