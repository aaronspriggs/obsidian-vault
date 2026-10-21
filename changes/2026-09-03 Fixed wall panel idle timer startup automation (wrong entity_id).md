---
date: 2026-09-03
type: fix
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d07ae76-22ba-817d-9d5f-d021c87b882a
---

# Fixed wall panel idle timer startup automation (wrong entity_id)

Health-checked the HA instance via ha-mcp and found the log warning "Referenced entities timer.wall_panel_dim/timer.wall_panel_screensaver are missing or not currently available" was real, but not what it looked like.

Root cause: the two timer helpers' actual entity_ids are `timer.timer_wall_panel_dim` and `timer.timer_wall_panel_screensaver` (doubled "timer" — someone had put the literal string "timer.wall_panel_dim" into the helper's Name field at creation time, which HA slugified into a doubled entity_id). `timer.wall_panel_dim`/`timer.wall_panel_screensaver` (no double prefix) never existed.

Three of the four wall-panel automations (Dim after 60s idle, Screensaver after 10m idle, Wake on Activity) already correctly referenced the real doubled entity_ids and were working fine. Only "Wall Panel - Start idle timers on HA startup" was wrong — it called timer.start on the non-existent short-form entity_ids, so the idle timers never actually started at boot. Practical impact was limited (Wake on Activity restarts the correct timers on first touch), but it was a real, silent failure since original setup.

Fixed via ha_config_set_automation: corrected the startup automation's two action targets to the real entity_ids. Also renamed both timer helpers' display names (Wall Panel Dim / Wall Panel Screensaver) via ha_config_set_helper, without touching entity_id, so no other consumer broke.

Found as part of a broader ha-mcp-driven health check of the HA instance (repairs, logs, unavailable entities, updates, area organization). Other findings from that check not yet actioned: Nabu Casa/HA Cloud subscription appears lapsed (likely cause of automatic backup upload failures since 2026-08-29), HomeKit "Kitchen" bridge broken (missing [camera.kitchen](http://camera.kitchen/)), Spotify needs reauth, AmpliFi integration fully dead (candidate for removal), rpi_power integration errors pointlessly on this virtualized install, duplicate Bedroom TV/Loft TV media_player entities, UniFi device_tracker sprawl, and three empty orphaned areas (bedroom, stairs, kitchen_sonos).
