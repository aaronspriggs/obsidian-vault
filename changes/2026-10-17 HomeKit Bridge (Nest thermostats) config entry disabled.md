---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Migrate thermostats from Nest to ecobee]]'
notion_id: 3fc7ae76-22ba-81a9-9470-ebb1d254e58a
---

# HomeKit Bridge (Nest thermostats) config entry disabled

Phase 3 step 1, approved by Aaron. Disabled config entry adda16eb555c193e2d447fe275c1b48c ("Home Assistant - Homekit Bridge") via ha-mcp; now not_loaded, disabled_by user. It exposed only the two dead Nest climate entities, and emptying its include filter would have exposed every entity, so it was disabled instead of edited. Options at disable time, kept for rollback: mode bridge; filter include_entities [climate.downstairs_temperature, climate.upstairs_temperature], all other filter lists empty; entity_config for camera.downstairs_camera and camera.front_door (Google Nest, support_audio true, video_codec copy). Rollback: re-enable the entry (the Apple Home pairing is gone once Aaron removes the bridge there, so re-enabling would need a reset and re-pair). Delete later if the fan-timer Idea stays dead. Maintenance mode was on for the dashboard and bridge work and was turned off afterwards.
