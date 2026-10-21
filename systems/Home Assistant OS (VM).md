---
status: active
category: vm
ip: 192.168.1.218
url: http://192.168.1.218:8123/
runs_on:
- '[[TrueNAS SCALE (Big Boi)]]'
last_verified: 2026-09-29
notion_id: 2ff7ae76-22ba-8157-b627-faf6eaccb052
---

HAOS VM on Big Boi: home automation hub, MQTT broker, homelab alert endpoint. HAOS 18.3 (2026-09-29) / Core 2026.10.1 (2026-10-16). Claude access via ha-mcp (secret URL; OAuth blocked upstream).

## Overview

Home Assistant OS in a VM on Big Boi: the home automation hub (lights, climate, Zigbee sensors, water shutoff, media, EV/solar) and the MQTT broker for the wall panel. Also the alert endpoint for the homelab: TrueNAS, Uptime Kuma and the VM update jobs push into it. Verified live via ha-mcp 2026-09-29 unless dated otherwise.
Related pages: [Home Health](<Home Health (HA dashboard + alerts).md>) (dashboard + leak/battery/signal alerts), [Raspberry Pi Wall Panel](<Raspberry Pi Wall Panel.md>) (kiosk dashboard and its automations).

## Access

- **UI:** [http://192.168.1.218:8123/](http://192.168.1.218:8123/) (LAN only; remote via WireGuard). Owner account `aaronspriggs`, MFA via Proton Authenticator.
- **Shell:** Terminal & SSH add-on, web terminal only (in the HA sidebar). Its SSH port isn't exposed and no keys are set, so there's no network SSH, including from the ClaudeCode VM (verified 2026-09-29).
- **Claude:** ha-mcp (homeassistant-ai/ha-mcp 8.7.0 as of 2026-10-16, HACS integration `ha_mcp_tools`) on the direct-access secret URL, not OAuth, until anthropics/claude-code#89671 is fixed (Blocked task in Open work). Setup: [Setting Up ha-mcp](<../runbooks/Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>).
- **Other users:** `MQTT Dashboard` (non-admin, wall panel kiosk).
- **Nabu Casa:** still logged in with `remote_enabled: true`, but the subscription expired 2018-01-01, so nothing connects. Left in place on purpose (Aaron, 2026-09-24); don't flag or clean it up.

## Config

**VM (TrueNAS VM ****`HomeAssistant`****):** 2 vCPU threads (host-passthrough), 4 GiB RAM, UEFI, autostart. Disk zvol `Big Boi/vmstore/haos_disk` (128 GiB; 11.3 GB used inside HA). VirtIO NIC on `br0`, MAC 00:a0:98:61:a7:c1, DHCP reservation 192.168.1.218. USB passthrough of the Sonoff ZBDongle-E (Zigbee; TrueNAS shows it as "CP210x UART Bridge", Silicon Labs `10c4:ea60`, device `usb_1_5` on 2026-10-16), controller `qemu-xhci`. VM clock UTC. SPICE console on port 5900.
**Versions (2026-09-29):** HAOS 18.3 (stable), Core **2026.9.4** (2026.10.1 as of 2026-10-16, per backup metadata), Supervisor 2026.09.3, kernel 6.18.52-haos, Python 3.14.6, HACS 2.0.5 (26 repositories). Recorder: SQLite, 824 MiB, history since 2026-09-18. No repairs or persistent notifications open. Re-check versions with ha-mcp rather than trusting this line.
**Apps (add-ons; 6, all running as of 2026-10-17):** Terminal & SSH 10.5.0, Mosquitto broker 7.1.1, Matter Server 9.2.0, Studio Code Server 7.2.0, Spotify Connect 0.19.0 (still running though the Spotify integration was removed 2026-09-03; candidate for removal), and **Scrypted** v0.147.0 (`09e60fb6_scrypted`, installed 2026-10-17 from repository `https://github.com/koush/scrypted`).
**Scrypted (since 2026-10-17):** bridges UniFi Protect cameras into Apple Home with HomeKit Secure Video; why it runs here and the setup are on the [Scrypted project](<../projects/Scrypted — UniFi Camera HomeKit Bridge.md>). Host network on this VM: UI `https://192.168.1.218:10443`, or the HA sidebar via ingress (port 11080). Boot auto, watchdog on, auto-update off. Its HomeKit plugin runs its own mDNS responder next to HA's; verified working 2026-10-17 (`Scrypted FE0A` and HA's five accessories all announce `_hap._tcp` from .218). Its load lands on this VM, so **resize the VM as UniFi cameras are added** (plan: 4 vCPU / 8 GiB before passing ~3 HKSV cameras). Monitored by Kuma `Scrypted` (`sensor.scrypted_status`, labelled `homelab_watch`).
**MQTT:** Mosquitto on 192.168.1.218:1883. Auth through HA users (`auth_api: true`); the add-on has no anonymous-access option, so there's nothing to disable (verified 2026-09-04). Clients: TouchKio and the brightness bridge on the wall panel (user `mqttdashboard`). Setup: [Mosquitto runbook](<../runbooks/Mosquitto MQTT Broker Setup & Credential Configuration.md>).
**Integrations:** 71 config entries: 56 loaded, 3 retrying, 12 ignored discoveries.
- Home: ecobee (cloud; see Climate below), ZHA (Zigbee), Matter + Thread, Hue, Lutron Caseta, Govee (local), Dyson (Office, Bedroom), Rachio, Flo by Moen (water shutoff), Litter-Robot, Canon printer (IPP), Google Calendar.
- Energy and vehicles: Enphase Envoy (solar), ChargePoint, Rivian (unofficial).
- Media: Sonos, Google Cast, Apple TV (Living Room), Living Room TV (HomeKit controller), Radio Browser.
- Cameras: Nest (cameras only since the thermostats left it 2026-10-17) plus Nest cameras bridged via HomeKit (see Decisions). **UniFi Protect** (since 2026-10-20): entry "Dream-Machine-Pro", host 192.168.1.1, **API-key-only** mode (key in 1Password `Unifi Protect - HA API Key`), added from HA's discovery card. Despite the setup dialog's "limited feature set" warning it gives the G6 Instant 38 entities: `camera.g6_instant_high_resolution_channel`, motion and smart-detection binary sensors (person, vehicle, animal, audio types), `event.g6_instant_*` motion/smart/sound events, and detection switches. HomeKit for cameras is Scrypted's job, not this integration's. The discovered "Scrypted FE0A (Bridge)" HomeKit card is ignored on purpose: cameras pair to Apple Home individually.
- Homelab: UniFi Network, Uptime Kuma, System Monitor, ha-mcp, MQTT.
- HomeKit Bridge "Home Assistant - Homekit Bridge": **disabled 2026-10-17** and removed from Apple Home (it only carried the Nest thermostats; an empty include filter would expose every entity). Mobile app (Aaron's iPhone 17 Pro), [Met.no](http://met.no/) weather, Sun, Backup, Google Drive.
- Helpers: Battery Notes, 11 template sensors (Home Health and `sensor.homelab_issue_count`), a Water Usage utility meter.
- **Retrying (setup_retry) on 2026-09-29:** Denon AVR-S930H, PrusaLink `prusa-mk4`, and Bluetooth on the wall panel Pi. Probably devices that are off or gone; covered by the HA tidy-up task.
**Climate (since 2026-10-13):** two ecobee Smart Thermostat Premiums, `climate.upstairs` and `climate.downstairs` (separate HVAC systems), via the ecobee cloud integration ([ecobee.com](http://ecobee.com/) login, polled, about 1 min lag). Modes heat_cool/heat/cool/off, fan auto/on, presets home/away/sleep. SmartSensors: upstairs Poppys Room, Cheryls Office, Master Bedroom, Loft; downstairs Aarons Office, Dining Room (verified 2026-10-17). Apple Home pairs to the ecobees natively, not through HA; it has no standalone fan control. Dashboard cards: wall-panel bubble card (downstairs), two mushroom cards on `lovelace`. No automations use them.
**Alerting (since 2026-10-14):** homelab and Home Health alerts are Alert2 (HACS), defined in repo `ha/alert2.yaml` (`alert2:` key): Kuma services/heartbeats, UniFi devices, UniFi Protect cameras offline 5+ min (generator `homelab_camera_offline`, picks every Protect camera's high-resolution channel, so new cameras are covered after `alert2.reload`; since 2026-10-20), arr health, Docker containers (Dockhand), TrueNAS and VM-update reports, batteries. 20:00–09:00 quiet hours with a 09:00 report (`automation.homelab_alerts_09_00_report`), a native watchdog (`automation.homelab_alerts_alert2_watchdog`). Water leak alerts and the update-approval flow stay native. `truenas_alert_relay` and `homelab_vm_update_reports` are now webhook receivers that call `alert2.report`.
**Automations:** Home Health (leak notify and actions; see Home Health), wall panel (5; see Wall Panel), update approvals (3, below), alerting (report, watchdog, the two webhook receivers), garage lights (2), and `companion_app_updated_re_test_notification_buttons`. Turned off 2026-10-14, delete after a quiet week: `homelab_service_device_alerts` (off since 10-09), `homelab_container_alerts_dockhand`, `homelab_container_restart_on_tap`, `battery_low_notify`, `battery_watch_stale_unavailable_digest`.
**Update approvals (since 2026-09-25):** HAOS isn't in homelab-update. Entities labelled `ha_update_approval` (Core, OS, Matter Server, Studio Code Server, Mosquitto, Scrypted) get an "Update available" push, held to 09:00 if it arrives overnight. `ha_updates_install_on_approval` installs with `backup: true`, and `ha_updates_report_after_restart` reports the result after a Core/OS restart. Supervisor, Spotify Connect and Terminal & SSH auto-update. **Container image updates (since 2026-10-14):** Alert2 update alerts and the 09:00 report carry an Install button handled by `homelab_container_update_on_approval` (`update.install` on the ha-dockhand entity; Gluetun excluded, whole-stack deploy only). Long-press buttons are broken upstream (iOS#5881), but since 2026-10-14 the **Install** button works by tapping the notification (Companion setting "show actions when tapped" is on); tapping still also offers `/config/updates`. Aaron installed 2026.9.4 by hand.
**Backups (verified 2026-10-16 via backup diagnostics):** native automatic backups, daily around 05:00, to `hassio.local` (kept 7 days) and Google Drive (kept 30 days; native `google_drive` integration, since 2026-09-04). Scope: settings, recorder DB and all apps with their data (`include_all_addons: true`, re-checked 2026-10-17, so Scrypted is included; its manifest leaves out only plugin code and NVR storage); no `share`/`media`/`ssl` folders. About 430 MB each. Restore: [Restore Home Assistant from backup](<../runbooks/Restore Home Assistant from backup (new VM or in place).md>). Encrypted; the encryption key/emergency kit has been in 1Password since 2026-09-04 (confirmed by Aaron 2026-09-29). Runbook: [native Google Drive backup](<../runbooks/Set up native Google Drive backup integration for Home Assistant (retire the add-on).md>).

## Dependencies

- Runs on [TrueNAS SCALE (Big Boi)](<TrueNAS SCALE (Big Boi).md>); the VM goes down with it. On a power cut TrueNAS shuts down cleanly 300 s after the UPS goes on battery (NUT client of the UPS 2U, verified 2026-10-16), but that's untested end to end and Big Boi doesn't power back on by itself yet; see the rack UPS project.
- Zigbee depends on the USB dongle passthrough; Matter/Thread on the Matter Server add-on.
- Hosts [Home Health](<Home Health (HA dashboard + alerts).md>) and the wall panel's dashboard and MQTT broker.
- Receives alerts from the ClaudeCode VM (`truenas-alert-relay`, homelab-update reports) and Uptime Kuma.

## Decisions

- **2026-02-15:** migrated from a physical machine to a TrueNAS VM.
- **2026-09-03 / 09-04:** retired the community Google Drive Backup add-on for HA's native backup + `google_drive` integration; removed Nabu Casa as a backup target.
- **2026-09-24:** leave the lapsed Nabu Casa login in place.
- **2026-09-25:** Core/OS updates need an explicit approval from the phone, always with a pre-update backup; no Claude/MCP involvement.
- **2026-10-13:** thermostats moved from Nest to ecobee, paired natively to Apple Home with HA on the ecobee cloud integration; reasoning in [Migrate thermostats from Nest to ecobee](<../projects/Migrate thermostats from Nest to ecobee.md>).
- **2026-10-14:** dropped the Face ID gate (`authenticationRequired`) on Install and leak Shut Off Water: the Companion tap-to-show sheet hides gated actions, and it only opens in the unlocked app (Aaron approved).
- **2026-10-17:** Scrypted runs as an HA app (not on Big Boi or in its own VM): HA is where everything else is bridged into HomeKit, it means less to maintain, and TrueNAS mDNS can stay on for Finder and Time Machine. Accepted trade-off: it shares this VM's resources and reboots.
- **Cameras:** the Nest integration is unreliable; Nest cameras are to be replaced by UniFi Protect (Deferred idea). Until then the broken `camera.kitchen` and the failing HomeKit "Kitchen" bridge are known and deliberately left alone.

## Related

- Runbooks: [ha-mcp setup](<../runbooks/Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>), [HA MFA recovery](<../runbooks/Home Assistant MFA Recovery (TOTP Lockout).md>), [Mosquitto](<../runbooks/Mosquitto MQTT Broker Setup & Credential Configuration.md>), [Google Drive backup](<../runbooks/Set up native Google Drive backup integration for Home Assistant (retire the add-on).md>), [HA dashboard conventions and gotchas](<../runbooks/HA dashboard conventions and gotchas (reference).md>).
- History of the Home Health build and the wall panel: Changes entries from 2026-02-15 onward.

## Open work

![[Projects.base#Open for this system]]

## Runs on this

![[Systems.base#Runs on this]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
