---
type: task
status: active
priority: low
system:
- '[[Home Assistant OS (VM)]]'
next_step: '2026-10-17: (1) half done: real Install worked for Sonarr/Radarr on 10-16; NZBGet/Prowlarr NetworkMode check is still open (tracked in the Trial HA Install task). (2) real Snooze re-push and (3) leak buttons still waiting on first real use.'
notion_id: 3f97ae76-22ba-818f-b59b-e4211a9a30dd
---

Follow-up from 'One-tap approval notifications' (Done 2026-10-14). Everything was tested with safe test pushes; these paths still need one real run: (1) a real container image update via Install or Update all: check new image, container healthy, and for NZBGet/Prowlarr that NetworkMode still matches Gluetun's ID (same checks as 'Trial HA Install (Dockhand update entities)', which this also completes); (2) a real Snooze (2hr) re-push after 2 h; (3) the leak alert's buttons on a real critical push, covered by the task 'Run a real end-to-end water leak test'.
