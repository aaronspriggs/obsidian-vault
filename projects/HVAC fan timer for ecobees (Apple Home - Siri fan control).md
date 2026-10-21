---
type: idea
status: backlog
priority: low
system:
- '[[Home Assistant OS (VM)]]'
parent: '[[Migrate thermostats from Nest to ecobee]]'
next_step: Revisit only if room temperatures drift; then confirm design with Aaron.
notion_id: 3fc7ae76-22ba-8161-9470-d2ff1d6da51e
---

# HVAC fan timer for ecobees (Apple Home / Siri fan control)

Deferred 2026-10-17 by Aaron: HVAC was recently cleaned and the added SmartSensors are balancing rooms better, so fan circulation may not be needed. Revisit if rooms drift out of balance. Tied to this: the disabled HomeKit Bridge entry (adda16eb555c193e2d447fe275c1b48c) is kept only in case this gets built; if the idea is dropped, delete that entry (Tier 3, ask Aaron).

## Goal

Run the HVAC fan on its own for a set time from Apple Home/Siri and HA, then return it to auto.

## Findings (2026-10-17)

- Apple Home shows no standalone fan control on the natively paired ecobee Premiums (Aaron checked).
- HA `climate.upstairs` / `climate.downstairs` have fan modes `auto`/`on` and `fan_min_on_time` (0 today).

## Design (from the parent project)

- HA automation: when fan mode goes to `on` from any source, set it back to `auto` after N minutes (duration in a helper). Cloud polling means detection lags ~1 min.
- Apple Home/Siri: fixed-duration scripts ("Fan 30 min", "Fan 1 hr") exposed through a HomeKit Bridge whose include filter lists only those scripts. Never leave a bridge's include filter empty: that exposes every entity.
- Simpler alternative to check first: ecobee's own fan minimum on-time (minutes per hour), set in the ecobee app or via `ecobee.set_fan_min_on_time`. Gives continuous circulation without any HA automation.
- Climate is household-critical: Tier 2.
