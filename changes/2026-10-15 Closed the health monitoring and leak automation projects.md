---
date: 2026-10-15
type: doc
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[Homelab health monitoring with Home Assistant alerts (silent when nominal)]]'
- '[[Build out water leak sensor automations (notifications, alerts)]]'
notion_id: 3fa7ae76-22ba-818c-b3e9-f3a99fb9b821
---

# Closed the health monitoring and leak automation projects

KB close-out pass. Both pages collapsed to Outcome / Decisions / Links; leak leftovers split into two new Backlog items.

## What changed

- **Homelab health monitoring** → Done, `Date Completed` 2026-10-07. That's when its last open item, the Dockhand container alerts, finished. The page is collapsed to Outcome / Decisions / Links, and it points to the Alerting redesign as the current owner of alerting.
- **Water leak sensor automations** → Done 2026-10-15, collapsed the same way. The open scope items became their own Backlog items: "Pair the Sonoff SNZB-05P leak sensor, settle placements and entity IDs" (Task) and "Add a standalone non-networked leak alarm" (Idea).

## Why

Both projects were Active with stale or empty next steps. The remaining work was either finished elsewhere or was separate follow-up work, which KB Standards says belongs in its own item.

## How

Checked against live HA on 2026-10-15 before closing. All four leak sensors are present and dry, both leak automations are on, the SNZB-05P isn't paired, and the entity IDs haven't been renamed. Pre-edit page copies were saved to the session scratchpad. The weekly export (spriggs-homelab `kb-export` branch) is the restore path.

## Verify / roll back

Both pages were re-fetched after the edit and their content checked. To roll back, set Status back to Active and restore the body from the previous kb-export commit.
