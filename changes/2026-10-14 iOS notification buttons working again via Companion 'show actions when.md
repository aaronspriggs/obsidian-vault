---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Restore iOS notification action buttons once upstream fix ships (iOS 5881)]]'
notion_id: 3f97ae76-22ba-81e4-bf35-d3ce8f4264b6
---

# iOS notification buttons working again via Companion 'show actions when tapped'; removed Face ID gate from Install and Shut Off Water

Companion 2026.10.1 still shows 'Loading actions…' on long-press (iOS#5881). Workaround: HA app → Settings → Companion app → Notifications → show actions when tapped (on). The in-app sheet hides authenticationRequired actions, so that flag was removed from Install and Shut Off Water.

Re-tested the actionable notification buttons after the Companion app updated to 2026.10.1. Long-press still shows "Loading actions…" ([home-assistant/iOS#5881](https://github.com/home-assistant/iOS/issues/5881) is still open).
**Workaround found:** Companion 2026.9.3 added a setting to show a notification's actions when it is tapped (HA app → Settings → Companion app → Notifications). It's off by default; Aaron turned it on. Tapping a notification then opens an in-app sheet with the buttons, and taps do reach HA as `mobile_app_notification_action`.
**Catch:** the sheet hides actions with `authenticationRequired: true`. Test #4 showed only Release notes / Cancel; test #5 without the flag showed Install, and the tap ran `automation.ha_updates_install_on_approval`, which stopped at its pending-update condition as expected.
**Change (Aaron approved):** removed `authenticationRequired` from Install in `automation.ha_updates_ask_for_approval` and from Shut Off Water in `automation.water_leak_detected_notify`. The sheet only opens inside the app, which needs the phone unlocked, so Face ID added little. The residual risk is that a locked phone could tap these from the lock-screen long-press menu once that's fixed upstream; the effects are bounded (install with backup, close main valve).
**Verified:** a leak test push (Shut Off Water wired to a dummy action) showed both buttons; Dismiss ran `automation.water_leak_notification_handle_actions` via the Dismiss branch (logbook only).
