---
date: 2026-10-15
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[HA tidy-up - ignore stale discovered integrations, rename generic Sonos entities]]'
notion_id: 3fa7ae76-22ba-8100-ab91-c0a2542d97d3
---

# Renamed Sonos entities, cleaned up HA areas and discovered integrations, removed dead Denon entry

Sonos unnamed_room_* → poppys_room_* / cheryls_office_*; areas Unnamed Room and Poppy's Room deleted; 5 discoveries ignored; 2 Battery Notes added; Denon S930H entry removed.

## What changed

- **Renamed 21 Sonos entities.** Poppy's Era 100 SL: `media_player.unnamed_room_2` → `media_player.poppys_room`, plus `binary_sensor`/`number`/`switch` siblings, all `unnamed_room_*_2` → `poppys_room_*`. Cheryl's One SL: `media_player.unnamed_room_3` → `media_player.cheryls_office`, plus siblings → `cheryls_office_*`, including the `button` and the doubled `unnamed_room_cheryls_office_*` switches.
- **Device areas.** Sonos Era 100 SL and the Hue "Poppy's Room" group → Poppy's Bedroom. Sonos One SL "Cheryl's Office" and its UniFi client device (MAC 38:42:0b:1f:31:a6) → Cheryl's Office.
- **Deleted areas "Unnamed Room" and "Poppy's Room"** (both empty after the moves). Tier 3, approved by Aaron 2026-10-15.
- **Ignored discoveries:** Android TV Remote (Living Room, Loft, Bedroom TVs), WiiM Garage, Withings.
- **Battery Notes subentries added:** ecobee Room Sensors "Poppys Room" and "Aarons Office", 1× CR2032 each.
- **Removed the denonavr config entry for the AVR-S930H**, which was in setup_retry with its entity unavailable. Aaron replaced it with an AVR-S970H. Tier 3, approved 2026-10-15.

## Why

This is the HA tidy-up task (from the 2026-09-26 review). Aaron chose what to add or ignore and approved the deletes.

## How

All through ha-mcp: entity and device registry updates, `config_entries/ignore_flow`, a Battery Notes `config_subentry`, area removal, and the config entry delete. Before renaming or deleting, I checked automations, scripts, scenes, helpers, dashboards and HomeKit Bridge filters for the old entity IDs and area IDs. Nothing referenced them.

## Verify / roll back

The old entity IDs return nothing in `ha_search`, and the new ones resolve. To roll back the renames, use `ha_set_entity(new_entity_id=...)` back to the old IDs. Ignored integrations can be restored from Settings → Integrations → Ignored. Deleted areas would need to be recreated. The Denon S930H entry comes back by re-adding the integration, but the receiver is gone.
