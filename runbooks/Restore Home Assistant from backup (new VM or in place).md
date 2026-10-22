---
kind: recovery
status: active
system:
- '[[Home Assistant OS (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 3fb7ae76-22ba-816a-81f2-da95dd0e0fee
---

Bring Home Assistant back from its daily encrypted backup (Google Drive, or local) after the HAOS VM or its config is lost. A full backup holds config, history DB and all apps (Matter fabric, Mosquitto), so a restore onto a fresh HAOS VM with the same MAC brings back everything except up to ~24 h of changes. Aaron runs the VM and onboarding steps; Claude verifies over ha-mcp.

## When to use

Home Assistant is lost or broken beyond fixing one object: the zvol `vmstore/haos_disk` is gone, HAOS won't boot, Big Boi was rebuilt, or a bad update or deletion needs a full rollback. Pick the narrowest path:
- **One automation, script, dashboard or helper is wrong:** roll that object back, not the whole instance.
- **Zvol intact, problem under 30 days old, VM won't boot:** roll back the daily `vmstore` snapshot of `haos_disk` in TrueNAS (with the VM stopped). It's the fastest option, and like a restore it loses everything since the snapshot.
- **HA boots but its config is broken:** Path A (restore in place).
- **VM or zvol gone:** Path B (new VM, restore during onboarding).
A restore is **Tier 3**: it discards everything since the backup and restarts HA, so Aaron confirms it every time. Expect about 1 hour for Path B. Desk-checked against the live instance and its TrueNAS definition on 2026-10-16; not yet test-restored.

## What a backup holds (verified 2026-10-16)

Automatic backups run daily around 05:00 to `hassio.local` (kept 7 days) and Google Drive account `spriggs.aaron@gmail.com` (kept 30 days), about 430 MB each, encrypted. Contents: HA settings (`.storage`, YAML, automations, dashboards, HACS custom components including ha-mcp and Alert2), the recorder DB, and **all apps with their data**: Mosquitto, Matter Server (the Matter fabric, so Matter devices don't need recommissioning), Terminal & SSH, Studio Code Server, Spotify Connect. Not included: the `share`, `media` and `ssl` folders (unused), and the VM definition itself (below). Expect to lose up to ~24 h of history and any changes since the backup. Check with Claude: `ha_get_integration` on the `backup` entry with diagnostics shows `include_all_addons: true`, `include_database: true`.

## Prerequisites

- **HA backup encryption key** (emergency kit), 1Password, Aaron's vault. Without it no backup can be restored.
- Google account login (for Drive) and the HA owner login `aaronspriggs` with its MFA (Proton Authenticator); [Home Assistant MFA Recovery (TOTP Lockout)](<Home Assistant MFA Recovery (TOTP Lockout).md>) if MFA is lost.
- Path B: Big Boi up, TrueNAS shell with sudo, the Sonoff ZBDongle-E plugged into Big Boi.
- **Never run two HA instances on the LAN at once.** If the old VM still exists, stop it and turn off its autostart. Keep its zvol until the new instance passes Verify.

## Path A: restore in place

1. Turn on maintenance mode first if HA is up enough (`input_boolean.homelab_maintenance_mode`), so the restart doesn't alert.
2. *Aaron*: Settings → System → Backups → pick the newest backup from **before** the problem (Drive keeps 30 days) → Restore → full restore, enter the encryption key if asked. HA restarts; allow 10-20 minutes. Claude can do the same with `ha_manage_backup(scope="snapshot", action="restore", restore_database=true)` after an explicit yes naming the backup and what is lost.
3. Go to Verify.

## Path B: new VM and restore

1. **Get the backup** (*Aaron*, on the Mac). In Google Drive, open the `Home Assistant` folder the integration writes to (or search for "Automatic backup") and download the newest `.tar`. It stays encrypted; it's unreadable without the key.
2. **VM** (*Aaron*). Follow [Creating an Appliance-Image VM (e.g. HAOS) on TrueNAS SCALE](<Creating an Appliance-Image VM (e.g. HAOS) on TrueNAS SCALE.md>) with the current stable HAOS `haos_ova` image and these settings, which match the live VM: name `HomeAssistant`, zvol 128 GiB (`vmstore/haos_disk`, or `haos_disk2` if the old zvol still exists), CPU Host Passthrough, 1 vCPU / 2 cores / 1 thread, 4096 MB, UEFI, **clock UTC** (HAOS keeps its RTC in UTC), autostart on, disk VirtIO, VirtIO NIC on `br0` with **MAC ****`00:a0:98:61:a7:c1`**, Trust Guest Filters off, SPICE display, and a **USB passthrough** device: controller `qemu-xhci`, device "CP210x UART Bridge" (Silicon Labs `10c4:ea60`, the ZBDongle-E; it was `usb_1_5` on 2026-10-16, but the name follows the host's USB numbering, so pick it by product). The MAC carries the UDM fixed IP 192.168.1.218, which the wall panel (MQTT, dashboard), the ClaudeCode VM (alert relay and update webhooks, ha-mcp), Uptime Kuma and the HomeKit bridge all use. If the MAC can't be reused, move the UDM reservation to the new MAC before starting the VM.
3. **Onboarding restore** (*Aaron*). Start the VM and open [http://192.168.1.218:8123](http://192.168.1.218:8123/). The first boot downloads Core and can show "Preparing Home Assistant" for up to 20 minutes. Choose **Restore from backup** → **Upload backup** → the `.tar` → enter the encryption key → full restore. HA restores Core to the backed-up version, then restarts into the old instance; allow another 10-20 minutes.
4. **Log in** as `aaronspriggs` (MFA as before). Settings → System → Repairs: re-authenticate any cloud integration that asks (a restore replays tokens that may have rotated since).
5. **Reconnect Claude** (Claude, or *Aaron* if no session is open): the ha-mcp config entry and its secret URL come back with the backup, so the 1Password item doesn't change. `sudo systemctl restart claude-remote-control` on the ClaudeCode VM to rediscover the tools. If ha-mcp had to be set up again, follow [Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code](<Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>) and Aaron updates the 1Password item.
6. When the new instance passes Verify, *Aaron* deletes the old VM and, after a quiet week, the old zvol.

## Verify

Claude, over ha-mcp, unless marked:
- `ha_get_overview`: version is the backed-up one (2026.10.1 as of this writing) and the entity count is close to before (about 830).
- `ha_get_system_health(include="repairs")`: no new repairs. `ha_get_integration`: nothing in `setup_error`; the only `setup_retry` entries are the known ones (Denon, PrusaLink, wall panel Bluetooth).
- `ha_get_system_health(include="zha_network")`: Zigbee devices report LQI/RSSI and recent `last_seen`. If ZHA can't open the radio, the USB passthrough is wrong (step 2).
- `ha_get_app(source="installed")`: all 5 apps started. Matter devices are available.
- Wall panel: dashboard loads and MQTT clients reconnect (Mosquitto log shows `mqttdashboard`).
- Alerting: the next `truenas-alert-relay` run turns Kuma `TrueNAS Alert Relay` green; Kuma's Home Assistant monitor is green; a test push reaches Aaron's iPhone (*Aaron* confirms).
- Backups: the `backup` diagnostics show `automatic_backups_configured: true` with Google Drive in `agent_ids`. Run `backup.create_automatic` once and check the new backup lists both `hassio.local` and `google_drive.*` (see [Set up native Google Drive backup integration for Home Assistant (retire the add-on)](<Set up native Google Drive backup integration for Home Assistant (retire the add-on).md>)).
- *Aaron*: Apple Home still sees the HomeKit Bridge accessories.
- Log the restore as a change note; update the Home Assistant OS (VM) System note (HAOS/Core versions, zvol name).

## Rollback

Path A: restoring discards what was there, so take a manual backup first if the broken instance has anything worth keeping, and restore that to go back. Path B doesn't touch the old VM or zvol while they exist: stop the new VM, start the old one (same MAC, never both). After a restore you can restore a different (older) backup the same way.
