---
type: project
status: done
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
completed: 2026-10-15
notion_id: 3c87ae76-22ba-8169-ad75-f5dd135bfb73
---

Leak alerts live 2026-09-04 (fixed 2026-09-25); closed 2026-10-15 with leftovers split into their own items.

## Outcome (Done 2026-10-15)

Leak alerting is live on ZHA (Sonoff ZBDongle-E). Four Aeotec/Samjin sensors carry the `leak_sensor` label: Dishwasher, Kitchen Sink, Utility Room and Water Filter/Softener. `automation.water_leak_detected_notify` sends a critical push naming the wet sensor. `automation.water_leak_notification_handle_actions` handles its **Shut Off Water** button (closes the Flo valve `switch.shutoff_valve`) and its **Dismiss** button. The battery and offline watchdogs started here and grew into whole-home monitoring, which now runs on Alert2 (see the [Alerting redesign](<Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts.md>)). Entity inventory: the Home Assistant OS (VM) and Home Health system pages. Verified live 2026-10-15: all four sensors dry and both automations on.
Follow-ups (own items): [Replace the Water Filter/Softener sensor battery](<Replace battery in Water Filter-Softener leak sensor.md>), [Run a real end-to-end leak test](<Run a real end-to-end water leak test (critical alert).md>), [Pair the SNZB-05P, settle placements and entity IDs](<Pair the Sonoff SNZB-05P leak sensor, settle placements and entity IDs.md>), [Standalone non-networked leak alarm](<Add a standalone non-networked leak alarm at the highest-risk spot.md>) (Idea).

## Decisions

- **2026-09-04 (Aaron): notify-only, no auto-shutoff.** The Flo valve closes only when Shut Off Water is tapped, so a false positive can't cut water to the whole house. Revisit if an alert is ever missed.
- **2026-09-04:** ZHA, not Zigbee2MQTT. Alerts go out as critical mobile pushes through the Companion app.
- **2026-09-04 (Aaron):** battery and stale-sensor watching was broadened from the leak sensors to every battery device (label `battery_watch`) plus the Home Health dashboard.

## Links

Changes from 2026-09-04 to 2026-09-25 (the leak alert build, and the notify-service fix on 2026-09-25).

## Sub-items

![[Projects.base#Sub-items]]

## Changes

![[Changes.base#For this project]]
