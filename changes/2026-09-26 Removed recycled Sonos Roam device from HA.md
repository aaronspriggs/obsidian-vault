---
date: 2026-09-26
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3e77ae76-22ba-81dc-96d7-e85f4bd49cb0
---

# Removed recycled Sonos Roam device from HA; completed Battery Notes setup for 19 devices

**Battery Notes:** Aaron added 19 of the discovered devices, and battery types auto-filled (details on the HA System page, Home Health section). He skipped the iPhone, the Front Door Google Nest (being replaced by UniFi) and the Sonos Roam.
**Sonos Roam removed:** the speaker died and was recycled. With Aaron's confirmation, Claude removed its HA device (Sonos integration, device id `d7ec8fbe…`, area `unnamed_room`) and its 11 entities: `media_player.unnamed_room`, `sensor.unnamed_room_battery`, `number.sonos_roam_balance`, bass/treble, and the touch/crossfade/loudness/status-light/microphone switches and sensors. **Pre-checks:** all entities were unavailable, none were in `battery_watch` or `homelab_watch`, and nothing referenced them in automations/scripts/scenes/helpers or on the default, wall-panel or home-health dashboards. **After:** no Roam entities remain, and the other Sonos players (`media_player.unnamed_room_2`/`_3`) are unaffected (paused/idle). If the Roam ever comes back on the network, the Sonos integration would simply re-discover it.
**Noticed:** the remaining Sonos players still have generic `unnamed_room_2`/`unnamed_room_3` entity IDs. Renaming them is an optional tidy-up and needs the safe-refactoring consumer check first.
