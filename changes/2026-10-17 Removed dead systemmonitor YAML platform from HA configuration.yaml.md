---
date: 2026-10-17
type: fix
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3fc7ae76-22ba-81e3-ae44-f2382501c11a
---

# Removed dead systemmonitor YAML platform from HA configuration.yaml

Deleted the `sensor:` key (only `- platform: systemmonitor`) that logged an error every boot; the UI System Monitor entry (imported from it) already has the same resources. Verified after a restart: error gone, sensors unchanged.

## What changed

Removed the top-level `sensor:` key from `/config/configuration.yaml`. It held only `- platform: systemmonitor` with its resource list, plus old commented-out `homekit:` lines and an orphaned `# Enable python scripts` comment. A `#Sensor List` comment line remains above `rest:`.

## Why

Every HA start logged "The systemmonitor platform for the sensor integration does not support platform setup, please remove it from your config". The System Monitor config entry (`648011db…`, source `import`, loaded) was imported from this block and already lists the same 23 resources, so the YAML did nothing.

## How

ha-mcp `ha_config_set_yaml` remove on `sensor` (preview diff, built-in backup, config check `ok`). Aaron approved the edit. `configuration.yaml` isn't in the repo (only `alert2:`, `rest:` and `rest_command:` fragments are), so there's no commit.

## Verify / roll back

Verified after an HA restart on 2026-10-17 (Aaron asked for it): the systemmonitor error is gone (the only startup error left is the known HomeKit "Kitchen" / `camera.kitchen` one), and System Monitor sensors report as before (e.g. `/config` disk 10.2%, memory 40.6%, CPU 10%). `sensor.processor_temperature` is `unavailable`, as it has been all week (no CPU temperature sensor in the VM), so that isn't from this change. Roll back: re-add the block from ha-mcp's YAML backup of `configuration.yaml`.
