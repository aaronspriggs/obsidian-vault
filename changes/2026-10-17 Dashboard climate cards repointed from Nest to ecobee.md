---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Migrate thermostats from Nest to ecobee]]'
notion_id: 3fc7ae76-22ba-81ba-9e43-f4eda7c950ca
---

# Dashboard climate cards repointed from Nest to ecobee

Phase 3 step 2 via ha-mcp JSON patch (with test ops). wall-panel views[0].sections[0].cards[2] (bubble-card climate): climate.downstairs_temperature → climate.downstairs. lovelace views[0].cards[0] (mushroom-climate): climate.downstairs_temperature → climate.downstairs; views[0].cards[1]: climate.upstairs_temperature → climate.upstairs. Rollback: patch the entity back to the old ID; no other card keys changed. Re-ran ha_search for both old IDs: no automations, scripts, scenes or helpers reference them. HomeKit Bridge left unchanged (see project).
