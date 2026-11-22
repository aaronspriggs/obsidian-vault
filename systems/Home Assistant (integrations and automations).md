---
status: active
category: software
url: http://192.168.1.218:8123/
runs_on:
- '[[Home Assistant OS (VM)]]'
last_verified: 2026-11-15
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/ha
---

Home Assistant itself: logins, Claude's ha-mcp access, integrations, automations, update approvals and the Alert2 homelab alerting. Core 2026.11.0 on 2026-11-15.

## Overview

Home Assistant Core and its configuration, running on the [Home Assistant OS VM](<Home Assistant OS (VM).md>). It is the home automation hub (lights, climate, Zigbee sensors, water shutoff, media, EV and solar) and the homelab's single alert endpoint: TrueNAS, Uptime Kuma, Dockhand and the VM update jobs report into it, and it pushes to Aaron's iPhone only when something needs attention. The machine (VM definition, add-ons, MQTT broker, backups) is in the VM's note; [Home Health](<Home Health (HA dashboard + alerts).md>) and the [wall panel](<Raspberry Pi Wall Panel.md>) have their own. Split from the VM's note on 2026-11-15; changes before that date are listed under the VM. Checked live through ha-mcp on 2026-11-15 unless dated otherwise.

## Access

- **UI:** [http://192.168.1.218:8123/](http://192.168.1.218:8123/), LAN only; from outside through the UDM Pro's WireGuard VPN.
- **Users** (ha-mcp can't list them; as recorded): owner `aaronspriggs` with TOTP in Proton Authenticator (lockout: [MFA recovery runbook](<../runbooks/Home Assistant MFA Recovery (TOTP Lockout).md>)); `MQTT Dashboard`, non-admin, the wall panel's kiosk and MQTT login (2026-09-29); `claude`, a local-only admin made for ha-mcp's OAuth sign-in and otherwise unused. Persons today: `person.aaron_spriggs`, `person.claude`.
- **Phones:** the Companion app on Aaron's iPhone 17 Pro and iPad.
- **Claude:** ha-mcp 9.1.2 (custom integration `ha_mcp_tools` from homeassistant-ai/ha-mcp, which carries the server too; v9.2.0 is available). Claude Code connects on the direct-access secret URL (1Password item `HA-MCP URL`), not OAuth, until anthropics/claude-code#89671 is fixed: [Switch ha-mcp auth to Home Assistant sign-in (OAuth)](<../projects/Switch ha-mcp auth to Home Assistant sign-in (OAuth).md>). Setup: [Setting Up ha-mcp](<../runbooks/Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>).
- **Nabu Casa:** still logged in with `remote_enabled: true`, but the subscription expired 2018-01-01, so nothing connects. Left on purpose; don't flag or clean it up.

## Config

**Versions and size:** Core 2026.11.0 (2026.11.1 available), Python 3.14.10. 1,520 entities, 5 dashboards, 14 scenes, no scripts. Recorder: SQLite, 857 MiB, history since 2026-10-30. One repair is open (Nest `legacy_pubsub_topic`, since 2026-11-09); no persistent notifications.

**Store:** HACS became the built-in Marketplace in Core 2026.11. 22 repositories are installed: 9 integrations, 12 dashboard cards and one theme. Five integrations with no config entry (Amplifi, Raspberry Pi GPIO, Raspberry Pi GPIO PWM, Stream Deck, Dyson Cloud) were removed on 2026-11-15. Still odd: the store lists two repositories for the one folder `custom_components/dyson_local`, `libdyson-wg/ha-dyson` (the code on disk, with its own cloud module) and the older `shenxn/ha-dyson`; left alone, because removing the stale entry through the store could delete the folder both point at. Dyson VOC and NO₂ come only as the `*_volatile_organic_compounds_index` and `*_nitrogen_dioxide_index` sensors (a low-is-good index, not µg/m³); the old raw entities were orphans and were removed on 2026-11-22.

**Integrations:** 85 config entries: 63 loaded, 18 ignored discoveries, 1 disabled, and 2 retrying (PrusaLink and Bluetooth on the wall panel Pi). PrusaLink fails with "Cannot connect" even while the MK4 is printing: on 2026-11-17 the printer answered PrusaLink at 192.168.1.177 (Wi-Fi, no DHCP reservation; the UDM resolves `prusa-mk4` there), so the entry, unchanged since it was added on 2025-01-07, most likely holds an old IP. The entry has no reconfigure option, so the fix is to delete it and add it again.

- Home: ecobee, ZHA (Zigbee, 9 devices), Matter and Thread, Hue, Lutron Caseta, Govee (local), Dyson (Office, Bedroom), VeSync (Levoit Superior 6000S, since 2026-11-22), Rachio, Flo by Moen (water shutoff), Litter-Robot, Canon printer (IPP), Google Calendar. Garage door: Meross LAN (`krahabb/meross_lan`, local HTTP to the Meross opener at 192.168.1.40, fixed IP) gives `cover.garage_door`; there is no Meross cloud entry.
- Energy and vehicles: Enphase Envoy (solar), ChargePoint, Rivian (unofficial).
- Media: Sonos, Google Cast, Apple TV, Living Room TV (HomeKit controller), Denon AVR, Radio Browser.
- Cameras: **UniFi Protect** (entry "Dream-Machine-Pro", host 192.168.1.1, API-key-only mode since 2026-10-20, key in 1Password `Unifi Protect - HA API Key`) gives the G6 Instant 38 entities, among them `camera.g6_instant_high_resolution_channel`, motion and smart-detection sensors and events. Nest carries cameras only since the thermostats left it on 2026-10-17.
- HomeKit: HA exposes six single accessories to Apple Home (four Nest cameras, "Kitchen" and the Office Floor Lamp). The bridge "Home Assistant - Homekit Bridge" is disabled (see Decisions).
- Homelab: UniFi Network, Uptime Kuma, Dockhand (`raetha/ha-dockhand`), System Monitor, ha-mcp, and MQTT (26 entities) on the VM's Mosquitto broker.
- Other: Met.no weather, Sun, Backup and Google Drive (the backup target; backups are in the VM's note).
- Helpers: Battery Notes (126 entities), 11 template sensors (Home Health and `sensor.homelab_issue_count`), the `sensor.water_usage` utility meter, 4 input helpers and 3 timers.

**Climate (since 2026-10-13):** two ecobee Smart Thermostat Premiums, `climate.upstairs` and `climate.downstairs` (separate HVAC systems), through the ecobee cloud integration (polled, about 1 min lag). Modes heat_cool, heat, cool, off; fan auto or on; presets home, away, sleep and away_indefinitely. SmartSensors: upstairs Poppys Room, Cheryls Office, Master Bedroom, Loft; downstairs Aarons Office, Dining Room. The upstairs thermostat (CO₂, VOC, humidity) is in the hallway outside the Master Bedroom. The Master Bedroom has an HVAC return near its door, which is left cracked for the cats, so the thermostat largely reads master-bedroom air (Aaron, 2026-11-22). The Master Bedroom also has a Levoit Superior 6000S humidifier (LEH-S602S-WUS, firmware 1.0.04), in HA since 2026-11-22 through the core `vesync` integration (cloud polling, Aaron's VeSync login) as `humidifier.master_bedroom_superior_6000s`, with humidity, temperature, mist level, low-water, tank-lifted, filter-life and display/child-lock/auto-off/drying switches. Its own sensor reads high: at 07:21 on 2026-11-22 it said 58 % at 60.4 °F while the Bedroom Dyson said 46 % at 67.6 °F and the ecobee room sensor 66.0 °F. The same moisture at a 7 °F lower temperature works out to about 59 %, so it is reading cool air at the unit rather than the room. Read room humidity from the Dyson. Poppy's room has a Canopy humidifier with no HA integration and no humidity sensor. Apple Home pairs to the ecobees natively, not through HA, and has no standalone fan control. No automation uses them.

**Alerting (since 2026-10-14):** homelab and Home Health alerts are [Alert2](https://github.com/redstone99/hass-alert2) v1.23.2, defined in the repo's [ha/alert2.yaml](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml): 59 `alert2.homelab_*` and 49 `alert2.home_health_*` entities covering Kuma services and heartbeats, UniFi devices, Protect cameras offline for 5 min (a generator, so a new camera is covered after `alert2.reload`), arr health, Dockhand containers, TrueNAS and VM-update reports, and batteries. Quiet hours are 22:00–09:00, with a report at 09:00 and a weekly one on Sunday. `input_boolean.homelab_maintenance_mode` mutes every homelab alert. Water-leak alerts and the update approvals stay native automations. How to add or change one: [Homelab alerting runbook](<../runbooks/Homelab alerting - add or change a monitor or alert (Kuma + Alert2).md>).

**Automations (26):**

- Alerting (7): `homelab_alerts_09_00_report`, `homelab_alerts_weekly_report_sunday_09_00`, `homelab_alerts_alert2_watchdog`, `homelab_alert_ack_snooze_on_tap`, `homelab_maintenance_mode`, and the webhook receivers `truenas_alert_relay` and `homelab_vm_update_reports`, which call `alert2.report`.
- Approvals from a notification (8): three `ha_updates_*` (below), `homelab_container_update_on_approval`, `homelab_container_update_all_on_approval`, `homelab_container_restart_on_approval`, and `homelab_claude_fix_run_on_tap` with `homelab_claude_fix_run_result` (fix runs are in the [Claude Code note](<Claude Code (Remote Control service).md>)).
- House (11): water leak notify and its actions (Home Health), five `wall_panel_*` (wall panel note), two for the garage lights, `garage_door_alert_buttons_and_night_check`, and `companion_app_updated_re_test_notification_buttons`.

**Update approvals (since 2026-09-25):** update entities labelled `ha_update_approval` (Core, OS, Matter Server, Studio Code Server, Mosquitto, Scrypted) get an "Update available" push from `ha_updates_ask_for_approval`; one that appears between 21:00 and 09:00 waits for the 09:00 batch. On Aaron's tap `ha_updates_install_on_approval` installs with `backup: true` and notes the install in `input_text.ha_update_in_progress`, and `ha_updates_report_after_restart` reports the result once Core or the OS is back. Supervisor and Terminal & SSH carry no label and update themselves. Container images work the same way through the Dockhand integration's update entities (Gluetun excluded: whole-stack deploy only). Long-press action buttons are broken upstream ([project](<../projects/Restore iOS notification action buttons once upstream fix ships (iOS 5881).md>)); tapping the notification shows the actions, because the Companion setting "show actions when tapped" is on (2026-10-14).

## Dependencies

Runs on the [Home Assistant OS VM](<Home Assistant OS (VM).md>), which supplies the Zigbee dongle, the Matter Server and the MQTT broker. ecobee, Nest, Google Calendar and the Companion app's push notifications need the internet. What depends on it: [Home Health](<Home Health (HA dashboard + alerts).md>), the [wall panel](<Raspberry Pi Wall Panel.md>)'s dashboard, [Uptime Kuma](<Uptime Kuma.md>)'s alert delivery, the alert relay and update reports posted from the [ClaudeCode VM](<ClaudeCode (VM).md>), and [Claude Code](<Claude Code (Remote Control service).md>)'s HA tools and fix runs.

## Decisions

- **2026-09-24 (Aaron):** leave the lapsed Nabu Casa login in place.
- **2026-09-25:** Core and OS updates need an explicit approval from the phone, always with a backup first; Claude and ha-mcp aren't involved.
- **2026-10-09:** Alert2 instead of a hand-built alert manager; reasons in [the alerting redesign](<../projects/Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts.md>). The five automations it replaced were deleted on 2026-10-23.
- **2026-10-13:** thermostats moved from Nest to ecobee, paired natively to Apple Home with HA on the cloud integration; reasons in [Migrate thermostats from Nest to ecobee](<../projects/Migrate thermostats from Nest to ecobee.md>).
- **2026-10-14 (Aaron approved):** no Face ID gate (`authenticationRequired`) on Install or on the leak alert's Shut Off Water: the Companion tap-to-show sheet hides gated actions, and it only opens in the unlocked app.
- **2026-10-17:** the HomeKit bridge was disabled and removed from Apple Home. It only carried the Nest thermostats, and an empty include filter would expose every entity.
- **2026-10-20:** HomeKit for UniFi cameras is Scrypted's job, not the Protect integration's. The discovered "Scrypted FE0A (Bridge)" card is ignored on purpose, because cameras pair to Apple Home one by one.
- **Cameras:** the Nest integration is unreliable, and its cameras are being replaced by UniFi Protect ([project](<../projects/Migrate cameras from Nest to UniFi Protect.md>)). Until then the failing HomeKit "Kitchen" accessory is known and left alone.
- **2026-11-15:** split from the VM's note ([change](<../changes/2026-11-15 Split the Home Assistant System note into the VM and the application.md>)).

## Open work

![[Projects.base#Open for this system]]

## Runs on this

![[Systems.base#Runs on this]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]

## Related

- Repo [ha/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/ha): the YAML that ha-mcp applies (`alert2.yaml`, `rest-arr-health.yaml`, `rest-command.yaml`).
- Dashboards: [HA dashboard conventions and gotchas](<../runbooks/HA dashboard conventions and gotchas (reference).md>).
