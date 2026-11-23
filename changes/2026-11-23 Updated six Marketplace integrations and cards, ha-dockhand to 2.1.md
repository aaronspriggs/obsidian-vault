---
date: 2026-11-23
type: upgrade
system:
- '[[Home Assistant (integrations and automations)]]'
- '[[Dockhand]]'
- '[[Raspberry Pi Wall Panel]]'
---

# Updated six Marketplace integrations and cards, ha-dockhand to 2.1

Claude installed every pending Marketplace update through ha-mcp and restarted HA once, with maintenance mode on for the 30U cutover. Nothing else was pending: HA Core 2026.11.2, HAOS 18.4, Supervisor 2026.11.0 and every add-on current; UniFi firmware has nothing upgradable; TrueNAS 25.04.2.6 reports no update; the Dockhand app and all containers current.

## What changed

- ha-dockhand v1.11.3 → 2.1.0 ([2.0.0 notes](https://github.com/raetha/ha-dockhand/releases/tag/2.0.0), [2.1.0](https://github.com/raetha/ha-dockhand/releases/tag/2.1.0))
- kiosk-mode v15.0.0 → v16.0.0 ([notes](https://github.com/NemesisRE/kiosk-mode/releases/tag/v16.0.0))
- Power Flow Card Plus v0.4.1 → v0.6.1, Mushroom v5.2.3 → v5.3.0, Meross LAN v6.0.0 → v6.0.2, Wall Clock Card v3.18.1 → v3.18.2

Backup first: `595acb40` (automatic-backup settings, local and Google Drive, 442 MB). Before installing, Claude accepted the Marketplace's first-run warning for the `claude` user on Aaron's yes (the acceptance is per HA user, see [the ha-mcp upgrade note](<2026-11-23 Upgraded ha-mcp to 9.2.0.md>)).

Verified after the restart against a baseline taken before it: 11 container State sensors (all `running` except the one-shot `ix_dockhand_permissions_1`, `exited` as before), 11 container update entities (none on, `supported_features` 21 or 16 as before), 12 restart buttons, 43 Alert2 container alerts, none firing; container health all `healthy`; Meross LAN 11 entities, none unavailable; config check valid; the startup log has only the known items (HomeKit "Kitchen", rivian/dyson_local/chargepoint deprecations, a linkplay discovery warning for 192.168.1.244); the only repair is the Nest one from 2026-11-09.

## Why

Aaron asked for everything pending to be updated. ha-dockhand 2.0 has breaking changes; none reach this install: polling intervals were the defaults (60/600/86400 s), images, volumes, networks and schedules are off, no automation or dashboard reads the removed attributes or the environment binary sensors that became switches, and the update attributes the Alert2 container alerts read (`supported_features`, `installed_version`, `latest_version`, `newer_version`, `pinned_digest_moved`, `update_held_hours`) are still documented in 2.x. ha-dockhand-cards isn't installed. kiosk-mode 16's one change: on Core 2026.11 `hide_dialog_camera_actions` hides the camera dialog's two-way-audio button instead of the old snapshot button.

## Notes

Rollback: Marketplace → the repository → Redownload → the previous version, then restart HA; or restore `595acb40`. ha-dockhand 2.x keeps 1.11.x downgradable. The wall panel needs a TouchKio restart to load the new kiosk-mode and card versions.
