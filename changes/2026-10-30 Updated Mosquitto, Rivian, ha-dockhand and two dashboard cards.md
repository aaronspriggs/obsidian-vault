---
date: 2026-10-30
type: upgrade
system:
- '[[Home Assistant OS (VM)]]'
---

# Updated Mosquitto, Rivian, ha-dockhand and two dashboard cards

Claude installed all five pending HA updates at Aaron's request, under maintenance mode, then restarted Core; everything came back loaded.

## What changed

Mosquitto broker app 7.1.1 → 7.1.3 (with the pre-install app backup). Through HACS: Rivian (Unofficial) 1.5.3b0 → [2.0.0](https://github.com/bretterer/home-assistant-rivian/releases/2.0.0), ha-dockhand v1.10.2 → [v1.11.1](https://github.com/raetha/ha-dockhand/releases/v1.11.1), clock-weather-card v2.9.6 → [v3.0.1](https://github.com/pkissling/clock-weather-card/releases/tag/v3.0.0) and Wall Clock Card v3.17.4 → [v3.18.0](https://github.com/rkotulan/ha-wall-clock-card/releases/v3.18.0). Core restarted on 2026.10.4; the rivian, dockhand and mqtt entries are `loaded`, `sensor.rivian_battery_state_of_charge` reads 40.0 before and after, and `sensor.rivian_charging_speed` went from unknown to 0.0.

## Why

Routine updates. Before installing, Claude checked the two major bumps: no automation, script, scene or helper references a Rivian entity (the only consumer is the power-flow card on the default dashboard, numeric sensors whose IDs don't change), and no storage dashboard uses clock-weather-card, so its v3 config rewrite breaks nothing.

## Notes

Rivian 2.0.0 raised a `state_values_changed` repair (states are now lowercase); nothing in automations or helpers compares Rivian states, but YAML-defined template sensors weren't searched. ha-dockhand v1.11 turns a container's update entity on, with Install unavailable, for a newer tag behind an installable one, a moved digest pin, or an update held by Dockhand's minimum image age. Those will reach Alert2 update alerts, and `homelab_container_update_on_approval` calling `update.install` on them will fail; no container updates were pending to test against. `ha_manage_updates(backup=true)` is refused for HACS update entities, so only app updates take that flag.
