---
type: project
status: done
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Uptime Kuma]]'
parent: '[[Homelab health monitoring with Home Assistant alerts (silent when nominal)]]'
completed: 2026-10-23
notion_id: 3f47ae76-22ba-81e0-a282-dfc43d44bf3b
---

# Alerting redesign: one dispatcher, one detector per symptom, label-driven alerts

## Outcome

Started as Claude's 2026-10-09 review of the HA error and notification setup, after the arr health work added a second poller for endpoints Kuma already watched and one flapping source sent about 32 pushes in 7 days. Thirteen automations each pushed to the phone directly and re-implemented severity, tags, debounce, recovery rules and logbook on their own, with overlapping detectors and no inhibition, ack, snooze or push counts.

Done 2026-10-23. Every homelab alert source now runs on [Alert2](https://github.com/redstone99/hass-alert2), defined in [ha/alert2.yaml](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml): Kuma services, hosts and heartbeats (monitors are code via AutoKuma), UniFi devices, Dockhand containers and image updates, the TrueNAS relay, homelab-update reports and per-device battery-low alerts. Alerts are generated from the `homelab_watch` label, `supersedes` handles parent/child inhibition (Kuma unreachable over everything, Gluetun over Prowlarr and NZBGet), `delay_on_secs` debounces, and pushes go out 09:00–20:00 with a 09:00 report of anything that fired overnight and a Sunday weekly report. A native watchdog pushes directly if Alert2 stops loading. Ack and snooze live on the Home Health dashboard because iOS action buttons are broken upstream. Two things stay native on purpose: water leak alerts (critical, any hour) and the HA update-approval flow (an interactive workflow, not an alert). The five superseded automations were deleted 2026-10-23. Adding a monitor: [Homelab alerting - add or change a monitor or alert](<../runbooks/Homelab alerting - add or change a monitor or alert (Kuma + Alert2).md>).

Follow-ups: [Prune homelab alerts monthly from Alert2 fire counts](<Prune homelab alerts monthly from Alert2 fire counts.md>), [Force an HDHomeRun outage to test its Alert2 alert](<Force an HDHomeRun outage to test its Alert2 alert.md>).

## Decisions

- **2026-10-09 (Aaron): quiet hours 20:00–09:00.** Alerts in that window wait for the 09:00 report. Homelab alerts never use the iOS critical level. **Exception: water leak alerts** go out immediately at any hour at the critical level.
- **2026-10-09 (Aaron): leak alerts go to Aaron only.** No second recipient.
- **2026-10-09 (Aaron): off-box dead-man check deferred** to a later project. Big Boi down still means silence, since Kuma, HA and the push path all run on it (accepted 2026-09-24).
- **2026-10-09 (Claude, delegated by Aaron): adopt Alert2** instead of building ack, snooze, reminders, throttling and inhibition natively, which would have meant a hand-written alert manager in Jinja and helpers. Risk accepted: a single-maintainer HACS integration, mitigated by YAML config in the repo, the native watchdog, and leaks staying native.
- **2026-10-09 (Aaron): cut over without waiting for the HDHomeRun forced test.**

## Links

![[Changes.base#For this project]]
