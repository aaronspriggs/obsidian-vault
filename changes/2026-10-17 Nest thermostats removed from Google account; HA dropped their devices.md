---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Migrate thermostats from Nest to ecobee]]'
notion_id: 3fc7ae76-22ba-8178-b37a-ca0917b5f400
---

# Nest thermostats removed from Google account; HA dropped their devices

Aaron removed both Nest thermostats from the Google Home app. HA's Nest integration then removed the Upstairs Temperature and Downstairs Temperature devices and their entities on its own, so no manual deletion was needed. Verified via ha-mcp: the Nest integration now has 4 devices (Driveway, Downstairs Camera, Front Door doorbell, Backyard), and no climate.*_temperature entities remain. Factory reset still pending (off the wall the menu won't open); tracked as Aaron's Backlog task for selling them.
