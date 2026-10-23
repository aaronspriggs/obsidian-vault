---
type: task
status: backlog
priority: low
system:
- '[[HDHomeRun Flex 4K]]'
- '[[Home Health (HA dashboard + alerts)]]'
parent: '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
---

Extracted 2026-10-23 from the done alerting redesign; open since 2026-10-09 with no date (Aaron cut over to Alert2 without waiting for it). Take the HDHomeRun off the network long enough to pass the alert's debounce, confirm `alert2.homelab_hdhomerun_down` fires and pushes, then reconnect and confirm the recovery push. Needs Aaron at the device, with no one watching live TV.
