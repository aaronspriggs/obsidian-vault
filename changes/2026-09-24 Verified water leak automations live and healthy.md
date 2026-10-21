---
date: 2026-09-24
type: research
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3e57ae76-22ba-8151-9480-d87d93dabfec
---

# Verified water leak automations live and healthy; found Water Filter/Softener sensor battery critically low

Checked live HA state against the "Build out water leak sensor automations" Project page and System page notes, since Aaron asked whether the notify-only automations were really done.
Confirmed live and matching docs: all 4 leak sensors reporting, and all 4 related automations (`water_leak_detected_notify`, `water_leak_notification_handle_actions`, `battery_low_notify`, `battery_watch_stale_unavailable_digest`) are `on`.
Confirmed still genuinely open (not stale checkboxes): Sonoff SNZB-05P not yet paired, and entity renames to the descriptive scheme not done.
New finding: Water Filter/Softener sensor (`binary_sensor.samjin_water`) battery has dropped from 3.5% (2026-09-04) to 0.5% (2.2V) as of today — escalated urgency on the System page's Known Gaps and the Project page. Updated both pages to reflect current numbers.
