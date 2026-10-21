---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Migrate thermostats from Nest to ecobee]]'
notion_id: 3fc7ae76-22ba-818e-9c0c-cb6685a3abaf
---

# ecobees paired to Apple Home; 4 more SmartSensors added and assigned HA areas

Aaron paired both ecobees natively to Apple Home and added four SmartSensors: Dining Room (downstairs), Cheryls Office, Master Bedroom, Loft (upstairs). HA picked them up through the ecobee cloud integration; all show in each thermostat's active_sensors. Claude assigned the four new devices to the matching HA areas (dining_room, cheryls_office, master_bedroom, loft) via ha-mcp. Totals: upstairs 4 remote sensors + thermostat, downstairs 2 + thermostat.
