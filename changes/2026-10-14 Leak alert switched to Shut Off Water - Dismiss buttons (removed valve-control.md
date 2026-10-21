---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[One-tap approval notifications (updates and similar)]]'
notion_id: 3f97ae76-22ba-81b1-9ad7-ddceb7a9b7e5
---

# Leak alert switched to Shut Off Water / Dismiss buttons (removed valve-control tap workaround)

Aaron approved. Removed entity_id: switch.shutoff_valve from automation.water_leak_detected_notify so tapping shows the buttons; message now 'Tap, then Shut Off Water'. Test push (active level, dummy shutoff) showed both buttons; Dismiss ran the handler at 15:20.

Aaron chose to put the leak alert on the one-tap standard. `automation.water_leak_detected_notify`: removed `entity_id: switch.shutoff_valve` (the 2026-09-25 tap-opens-the-valve workaround), because an `entity_id`/`url` makes the tap open a page and hides the button sheet. Message is now "{{ sensor_name }} is reporting wet. Tap, then Shut Off Water to close the main valve." Description rewritten (no more TEMPORARY note). Handler `automation.water_leak_notification_handle_actions` unchanged.
Verified with a test push of the same shape (active level instead of critical; Shut Off Water wired to a dummy action): both buttons showed, Dismiss ran the handler's Dismiss branch at 15:20. A real critical push is still covered by the open "Run a real end-to-end water leak test" task, updated to tap Dismiss.
