---
type: task
status: done
priority: low
system:
- '[[Home Assistant OS (VM)]]'
completed: 2026-10-15
notion_id: 3e77ae76-22ba-81c4-b7b5-f985e697f8ce
---

# HA tidy-up: ignore stale discovered integrations, rename generic Sonos entities

From the 2026-09-26 review of Settings → Integrations → Discovered.

## Outcome (Done 2026-10-15)

- **Sonos entity IDs:** `media_player.unnamed_room_2` → `media_player.poppys_room` (Era 100 SL) and `media_player.unnamed_room_3` → `media_player.cheryls_office` (One SL), plus all their sibling entities (`*_bass`, `*_treble`, `*_loudness`, ...; 21 entities in all). Nothing referenced the old IDs: no automations, scripts, scenes, helpers or dashboards, and HomeKit doesn't include them. Devices moved to the Poppy's Bedroom and Cheryl's Office areas.
- **Areas:** deleted "Unnamed Room" and "Poppy's Room" (Aaron, 2026-10-15). The Hue "Poppy's Room" group and the UniFi client for Cheryl's Sonos were moved out first. Poppy's Bedroom is the single area for that room now.
- **Discovered integrations:** Ignored Android TV Remote (Living Room, Loft, Bedroom TVs), WiiM Garage and Withings (Aaron, 2026-10-15; reversible from Settings → Integrations → Ignored). Left visible on purpose: NUT (UPS data, later in the [UPS project](<Rack Infrastructure — UPS + Power Management.md>)) and UniFi Protect (camera migration).
- **Battery Notes:** added the two new ecobee Room Sensors (Aaron's Office, Poppy's Room), 1× CR2032 each.
- **Denon:** Aaron replaced the AVR-S930H with an AVR-S970H. The dead S930H config entry was removed (nothing referenced `media_player.denon_avr_s930h`). Aaron added the discovered S970H on 2026-10-15. It's device "Living Room Denon" in the Living Room, entity `media_player.living_room_denon` (renamed from HA's doubled `living_room_living_room_denon`).
- **Kitchen stereo pair:** the device that was called "Sonos One SL" (MAC 38:42:0b:7d:38:4a, 192.168.1.171, wired to Pro Max port 9) is the second speaker in the kitchen stereo pair (Aaron, 2026-10-15). HA controls the pair only through `media_player.kitchen_sonos` (wired, Pro Max port 8), so this speaker's media player is always unavailable. Its 13.4.1 firmware is just the last value HA recorded before the pair was made. Renamed the device to "Kitchen Sonos (Stereo Pair)" and moved it to the Kitchen. Entities are now `*.kitchen_sonos_pair*`; `media_player.kitchen_sonos_pair` is hidden. Its UniFi client device (`device_tracker.kitchen_sonos_pair`) also went to the Kitchen, and the empty "Sonos One SL" area was deleted (Aaron approved).

## Decisions

- **2026-10-15:** keep the stereo-pair speaker's device and hide its media player rather than delete it. Sonos would recreate it, and it comes back to life if the pair is split.
- **Note:** UniFi also lists Cheryl's Office One SL (.205) under Pro Max port 9, even though it's wired to the upstairs USW Flex 2.5G port 1 (100 Mbps, no client shown there). The likely cause is Sonos bridging its traffic over SonosNet. It's harmless, so ignore it when reading UniFi client ports for Sonos.

## Changes

![[Changes.base#For this project]]
