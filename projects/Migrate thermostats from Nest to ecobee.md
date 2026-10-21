---
type: project
status: done
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
completed: 2026-10-17
notion_id: 3f17ae76-22ba-8155-8e37-f22bdd7ae0a1
---

Done 2026-10-17: ecobees native in Apple Home, HA via ecobee cloud integration; Nest thermostats gone from Google and HA. Follow-ups are sub-items.

## Outcome

Done 2026-10-17. Both Nest thermostats replaced by ecobee Smart Thermostat Premiums (installed 2026-10-13). They're paired natively to Apple Home, and HA runs them through the ecobee cloud integration (entry 01M4VTY9KJYZH20GBZ8VPB8ZPZ) as `climate.upstairs` / `climate.downstairs`, with six SmartSensors in their HA areas. The wall-panel and `lovelace` climate cards point at the ecobees. The HomeKit Bridge that carried the Nest thermostats is disabled in HA and removed from Apple Home. Both Nests are removed from the Google Home app, and HA's Nest integration dropped their devices on its own, leaving only the cameras. Current config lives on the [Home Assistant OS (VM)](<../systems/Home Assistant OS (VM).md>) System page. Upstairs wiring was conventional 1H/1C on Y1/G/W1/C/R, with a C-wire present and no PEK needed.
Follow-ups (sub-items): fan timer (Deferred Idea; Apple Home has no standalone fan control), factory-reset and sell the Nests (Aaron's Backlog task), and Nest/GCP teardown (Blocked until the cameras move).

## Decisions

- **2026-10-06:** ecobee over Aqara W200. The W200 exposes only mode/setpoint/temp/humidity/occupancy over Matter; fan, presets, schedules and remote sensors stay in the Aqara app, which splits HVAC logic outside HA.
- **2026-10-06:** the driver is leaving Google/Nest entirely (custom GCP project, poor Apple/HA interoperability, Google neglecting Nest), not a thermostat feature gap.
- **2026-10-06:** two Premiums, not Premium + Enhanced (Aaron): a SmartSensor and air-quality sensing on both floors.
- **2026-10-06:** cameras stay on Nest for now (cost). The thermostat migration went ahead on its own; the Nest integration and GCP project stay until the camera migration.
- **2026-10-13:** pair natively to Apple Home and run HA through the ecobee cloud integration, instead of HA-only HomeKit Device + HomeKit Bridge (Aaron: cloud for HA is fine if both connections work). Reasons: HA's ecobee integration takes username/password since 2026.3 (no dev key; [HA docs](https://www.home-assistant.io/integrations/ecobee/)), and Apple Home keeps working when HA is down. Apple's Adaptive Temperature needs a Matter thermostat ([MatterAlpha](https://www.matteralpha.com/how-to/how-to-use-apple-home-adaptive-temperature-with-your-matter-thermostat)) and the Premium has no Matter ([ecobee product page](https://www.ecobee.com/en-us/smart-thermostats/smart-thermostat-premium/)), so it wasn't a factor. Costs accepted: about 1 min HA state lag, and HA control depends on ecobee's cloud.
- **2026-10-17:** fan timer deferred (Aaron): the HVAC was recently cleaned and the added SmartSensors balance the rooms better, so it may not be needed.
- **2026-10-17:** HomeKit Bridge disabled rather than edited (Aaron approved). Removing its two Nest entities would have left an empty include filter, which exposes every HA entity to Apple Home.

## Links

Changes: [ecobees installed, HA integration added](<../changes/2026-10-13 Nest thermostats replaced by ecobee Premiums; HA ecobee integration added.md>) (2026-10-13), [Apple Home pairing + SmartSensors](<../changes/2026-10-17 ecobees paired to Apple Home; 4 more SmartSensors added and assigned HA areas.md>), [dashboard cards repointed](<../changes/2026-10-17 Dashboard climate cards repointed from Nest to ecobee.md>), [HomeKit Bridge disabled](<../changes/2026-10-17 HomeKit Bridge (Nest thermostats) config entry disabled.md>), and [Nest thermostats removed](<../changes/2026-10-17 Nest thermostats removed from Google account; HA dropped their devices.md>) (2026-10-17). No repo commits: all changes were made in HA through ha-mcp.

## Sub-items

![[Projects.base#Sub-items]]

## Changes

![[Changes.base#For this project]]
