---
status: active
category: vm
ip: 192.168.1.218
runs_on:
- '[[TrueNAS SCALE (Big Boi)]]'
last_verified: 2026-11-15
notion_id: 2ff7ae76-22ba-8157-b627-faf6eaccb052
---

HAOS VM on Big Boi: the machine Home Assistant runs on, with its add-ons (Mosquitto, Scrypted, Matter Server) and its backups. HAOS 18.4 on 2026-11-15.

## Overview

Home Assistant OS in a VM on [Big Boi](<TrueNAS SCALE (Big Boi).md>). This note holds the machine: the VM definition, the operating system, the add-ons and the backups. What runs inside it (logins, Claude's ha-mcp access, integrations, automations, alerting) is in [Home Assistant (integrations and automations)](<Home Assistant (integrations and automations).md>), split out on 2026-11-15; changes before that date are all listed here, whichever half they were about. Checked on 2026-11-15 through the TrueNAS API and ha-mcp unless dated otherwise.

## Access

- **Console:** SPICE on Big Boi, port 5900 (web 5901), opened from the VM's page in the TrueNAS UI.
- **Shell:** the Terminal & SSH add-on's web terminal, in the HA sidebar. No authorized keys or password are set and its port 22 isn't mapped, so there is no network SSH, from the ClaudeCode VM included (ports 22 and 22222 are closed from it).
- **Add-on UIs:** Scrypted at `https://192.168.1.218:10443` or in the HA sidebar (ingress, port 11080); Studio Code Server in the sidebar.
- **Claude:** no shell. Add-ons, backups and updates go through ha-mcp (see the application note), Scrypted through `~/.local/bin/scrypted-api`, and the VM definition through `truenas-api` (reads; start, stop and restart with `--write`, Tier 2).

## Config

**VM definition (TrueNAS VM `HomeAssistant`):** 2 vCPU threads (1 core × 2 threads, host-passthrough), 4 GiB RAM, UEFI, autostart, clock UTC. Disk: VirtIO on the zvol `Big Boi/vmstore/haos_disk`; HA sees 125.3 GB with 14.4 GB used. NIC: VirtIO on `br0`, MAC 00:a0:98:61:a7:c1, fixed IP 192.168.1.218 in UniFi. USB passthrough of the Sonoff ZBDongle-E (Zigbee; TrueNAS shows it as "CP210x UART Bridge", Silicon Labs `10c4:ea60`, device `usb_1_5`) on a `qemu-xhci` controller.

**Versions:** HAOS 18.4, Supervisor 2026.11.0, kernel 6.18.58-haos, Docker 29.8.2. Core's version is in the application note. Re-check with ha-mcp rather than trusting this line.

**Add-ons (6, all running):**

| Add-on | Version | What matters |
| --- | --- | --- |
| Mosquitto broker | 7.1.3 | MQTT on 192.168.1.218:1883 (8883 closed). Logins are Home Assistant users (`auth_api`); the add-on defines no logins of its own and has no anonymous-access option. Watchdog off, auto-update off. Clients: TouchKio and the brightness bridge on the [wall panel](<Raspberry Pi Wall Panel.md>). Setup: [Mosquitto runbook](<../runbooks/Mosquitto MQTT Broker Setup & Credential Configuration.md>) |
| Scrypted | v0.147.0 | `09e60fb6_scrypted`, from the repository `https://github.com/koush/scrypted`. Bridges UniFi Protect cameras into Apple Home with HomeKit Secure Video; setup and state are in the [Scrypted project](<../projects/Scrypted — UniFi Camera HomeKit Bridge.md>). Host network, boot auto, watchdog on, auto-update off. Its HomeKit plugin runs its own mDNS responder next to HA's (worked on 2026-10-17). Watched by the Kuma monitor `Scrypted` (`sensor.scrypted_status`, labelled `homelab_watch`) |
| Matter Server | 9.3.0 | Matter and Thread devices need it |
| Studio Code Server | 7.2.0 | |
| Terminal & SSH | 10.6.0 | Auto-update on |
| Spotify Connect | 0.19.0 | Still running though the Spotify integration was removed on 2026-09-03; a candidate for removal |

**Sizing:** Scrypted's load lands on this VM, so resize it as UniFi cameras are added: 4 vCPU and 8 GiB before passing about 3 HomeKit Secure Video cameras.

**Updates:** HAOS isn't in homelab-update. OS, Core and add-on updates wait for Aaron's tap on the phone and install with a backup first; the flow, and which entities it covers, are in the application note under Update approvals.

**Backups:** native automatic backups, daily around 05:00 (last 2026-11-15 05:07), to `hassio.local` and to Google Drive through the native `google_drive` integration (since 2026-09-04). About 400 MB each, encrypted. Each holds the settings, the recorder database, all six add-ons with their data, and the `ssl` folder (no `share` or `media`; `ssl` wasn't included when last read on 2026-10-16). Scrypted's backup leaves out only plugin code and NVR storage (2026-10-17). Retention is 7 days locally and 30 on Drive (settings read 2026-10-16; ha-mcp can't read them, and the 39 backups listed today fit). The encryption key (emergency kit) is in 1Password (Aaron confirmed 2026-09-29). Restore: [Restore Home Assistant from backup](<../runbooks/Restore Home Assistant from backup (new VM or in place).md>). Setup: [native Google Drive backup](<../runbooks/Set up native Google Drive backup integration for Home Assistant (retire the add-on).md>).

## Dependencies

- Runs on [Big Boi](<TrueNAS SCALE (Big Boi).md>) and goes down with it, on a power cut too: TrueNAS shuts down 300 s after the UPS goes on battery, and what is still missing for a clean return is in [Rack Infrastructure — UPS + Power Management](<../projects/Rack Infrastructure — UPS + Power Management.md>).
- Zigbee needs the USB dongle passthrough; Matter and Thread need the Matter Server add-on. The Google Drive copy of the backups needs HA's grant on Aaron's Google account.
- What depends on it: [Home Assistant](<Home Assistant (integrations and automations).md>) itself, and through it [Home Health](<Home Health (HA dashboard + alerts).md>), the wall panel's dashboard and all homelab alerting. The wall panel's MQTT clients need Mosquitto. The cameras in Apple Home need Scrypted.

## Decisions

- **2026-02-15:** migrated from a physical machine to a TrueNAS VM.
- **2026-09-03 / 09-04:** retired the community Google Drive Backup add-on for HA's native backup with the `google_drive` integration; removed Nabu Casa as a backup target.
- **2026-10-17:** Scrypted runs as an HA add-on, not on Big Boi or in its own VM: HA is where everything else is bridged into HomeKit, it means less to maintain, and TrueNAS mDNS can stay on for Finder and Time Machine. Accepted trade-off: it shares this VM's resources and reboots.
- **2026-11-15:** this note was split along the line between the machine and the application ([change](<../changes/2026-11-15 Split the Home Assistant System note into the VM and the application.md>)). The machine changes a few times a year; integrations, automations and alerting change weekly.

## Open work

![[Projects.base#Open for this system]]

## Runs on this

![[Systems.base#Runs on this]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]

## Related

- Repo: [scrypted/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/scrypted) (`scrypted-api`).
- Creating the VM: [Creating an Appliance-Image VM (e.g. HAOS) on TrueNAS SCALE](<../runbooks/Creating an Appliance-Image VM (e.g. HAOS) on TrueNAS SCALE.md>).
