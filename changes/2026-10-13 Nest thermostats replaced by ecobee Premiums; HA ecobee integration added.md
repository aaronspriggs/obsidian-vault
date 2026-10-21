---
date: 2026-10-13
type: install
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Migrate thermostats from Nest to ecobee]]'
notion_id: 3f87ae76-22ba-81b3-aae6-e5102fd25765
---

# Nest thermostats replaced by ecobee Premiums; HA ecobee integration added

Aaron installed ecobee Smart Thermostat Premiums upstairs and downstairs (upstairs wiring Y1/G/W1/C/R, conventional 1H/1C) and added the ecobee cloud integration in HA (config entry 01M4VTY9KJYZH20GBZ8VPB8ZPZ, discovered via zeroconf, [ecobee.com](http://ecobee.com/) login). Entities: climate.upstairs / climate.downstairs (fan modes auto/on, presets home/away/sleep), air-quality/CO2/VOC/humidity/temp sensors, SmartSensors Poppys Room and Aarons Office. Not yet paired to Apple Home. Nest climate entities are now dead; HomeKit Bridge and dashboard cards still point at them until Phase 3 cutover.
