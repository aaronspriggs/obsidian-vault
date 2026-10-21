---
date: 2026-10-15
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[HA tidy-up - ignore stale discovered integrations, rename generic Sonos entities]]'
notion_id: 3fa7ae76-22ba-81f0-b091-eeacdfe09839
---

# Named the kitchen Sonos stereo-pair speaker, added the Denon AVR-S970H, removed the Sonos One SL area

sonos_one_sl* → kitchen_sonos_pair* (media player hidden, device in Kitchen); denonavr S970H added by Aaron, entity media_[player.living](http://player.living/)_room_denon; area Sonos One SL deleted.

## What changed

- **"Sonos One SL" is the kitchen stereo pair's second speaker** (Aaron). Changes:
    - Device renamed to "Kitchen Sonos (Stereo Pair)" and moved to the Kitchen area.
    - Entities renamed `media_player.sonos_one_sl` → `media_player.kitchen_sonos_pair` (now hidden), and the `number`/`switch` siblings → `*.kitchen_sonos_pair_*`.
    - Its UniFi client device moved to the Kitchen: `device_tracker.sonoszp_3` → `device_tracker.kitchen_sonos_pair` and `sensor.sonos_one_sl_link_speed` → `sensor.kitchen_sonos_pair_link_speed`.
- **Deleted the now-empty area "Sonos One SL"** (Tier 3, approved by Aaron).
- **Denon AVR-S970H** added by Aaron from the discovery card. It's device "Living Room Denon" in the Living Room. Its entity was renamed `media_player.living_room_living_room_denon` → `media_player.living_room_denon`.

## Why

These finish the HA tidy-up task. The stereo-pair speaker looked stale because HA's Sonos integration exposes a pair only through its main speaker (`media_player.kitchen_sonos`).

## How

ha-mcp registry updates and an area delete. None of the old IDs had consumers (automations, scripts, scenes, helpers, dashboards, HomeKit filters).

## Verify / roll back

`media_player.kitchen_sonos` is idle and working. `media_player.kitchen_sonos_pair` is unavailable and hidden, which is expected while the pair exists. To roll back, use `ha_set_entity(new_entity_id=...)` and unhide.
