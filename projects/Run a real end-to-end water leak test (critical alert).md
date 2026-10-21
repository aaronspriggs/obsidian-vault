---
type: task
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
next_step: Aaron wants to run it later (said 2026-10-14). Before the test, he confirms iPhone Settings → Notifications → Home Assistant → Critical Alerts is on. Then wipe a sensor, check the critical push, tap Dismiss.
notion_id: 3e77ae76-22ba-812f-8a4f-e2aa8128fe23
---

The leak alert path was fixed on 2026-09-25 (notify.send_message → [notify.mobile](http://notify.mobile/)_app_*) but has never fired for real. Needs Aaron present because it sends a critical, breakthrough alert.

- Wipe one Aeotec leak sensor (e.g. Kitchen Sink) with a damp cloth, with Aaron present.
- Expect a **critical** "💧 Water Leak Detected" push that breaks through silent mode. Tapping it shows **Shut Off Water** / **Dismiss** (since 2026-10-14). Tap **Dismiss**; **don't** tap Shut Off Water unless you intend to close the main valve. Confirm `automation.water_leak_notification_handle_actions` ran the Dismiss branch. This also checks the button sheet on a real critical push, which the 2026-10-14 test (active level) didn't cover.
- Check the `automation.water_leak_detected_notify` trace, that the Home Health hero banner and Water Leak section turn red, and that everything clears when the sensor dries.
- Log the result to Changes and the "Build out water leak sensor automations" project.
