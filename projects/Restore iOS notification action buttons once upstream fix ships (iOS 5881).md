---
type: task
status: blocked
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
next_step: 'Wait for upstream long-press fix, then follow ''When a fix ships''. (Dockhand Restart test dropped: homelab_container_restart_on_tap was deleted 2026-10-23.)'
notion_id: 3e67ae76-22ba-8122-9734-d7553f58b8a6
---

# Restore iOS notification action buttons once upstream fix ships (iOS #5881)

Long-press buttons blocked on home-assistant/iOS#5881 (iOS 27.0 + Companion 2026.9.x–2026.10.1). Since 2026-10-14 the buttons work by tapping the notification (Companion 'show actions when tapped' on; authenticationRequired removed from Install and Shut Off Water). automation.companion_app_updated_re_test_notification_buttons pushes a reminder whenever the Companion app updates.

## Why blocked

Open upstream bug [home-assistant/iOS#5881](https://github.com/home-assistant/iOS/issues/5881) (related [#5823](https://github.com/home-assistant/iOS/issues/5823)): on iOS 27.0 with Companion 2026.9.x, notification action buttons show "Loading actions…" and never load, and taps never send `mobile_app_notification_action` to HA. Confirmed on Aaron's iPhone 2026-09-25: the Install test had 0 automation runs.
**Re-tested 2026-10-14 on Companion 2026.10.1:** still "Loading actions…". Upstream #5881 still open, last activity 2026-09-25; no fix mentioned in the 2026.9.3, 10.1 or 10.2 release notes.
**Partial workaround found 2026-10-14:** Companion setting (HA app → Settings → Companion app → Notifications) to show a notification's actions when it is tapped, added in 2026.9.3, off by default; Aaron turned it on. Tapping the notification opens an in-app sheet with the buttons, and a tap does fire `mobile_app_notification_action` (test #5: `automation.ha_updates_install_on_approval` traced and stopped at its condition as expected). **But the sheet hides actions with ****`authenticationRequired: true`** (test #4 showed only Release notes / Cancel). Affects Install (update approval) and the auth-gated leak button in `automation.water_leak_detected_notify`. The Dockhand Restart button has no auth flag, so it should work via the sheet.
**Applied 2026-10-14 (Aaron approved):** removed `authenticationRequired` from Install and Shut Off Water. Verified via the sheet: Install tap traced (stopped at condition); leak Dismiss ran the Dismiss branch. Buttons are usable by tapping; long-press remains broken until upstream fixes #5881, so this task stays Blocked for the long-press path. Dockhand Restart not yet tested via the sheet.

## Affected

- `automation.water_leak_detected_notify`: **Shut Off Water** / **Dismiss** buttons (handled by `automation.water_leak_notification_handle_actions`)
- `automation.ha_updates_ask_for_approval`: **Install** / **Release notes** buttons (handled by `automation.ha_updates_install_on_approval`)
- Alert2 container down/unhealthy pushes: **Restart** button (`CONTAINER_RESTART`, handled by `automation.homelab_container_restart_on_approval`). The older `DOCKHAND_RESTART` path and both its automations were deleted 2026-10-23.

## Temporary workarounds in place (2026-09-25)

- Tapping the leak alert opens **`switch.shutoff_valve`** instead of the wet sensor (Aaron approved), and the message says so. **Verified 2026-09-25:** a passive test push with the same `entity_id` opened the valve control on Aaron's phone.
- Tapping the update notice opens **`/config/updates`**: native Install with a "Create backup" option.
- The buttons were left in both payloads so they work again automatically once fixed.

## Tracking

- `automation.companion_app_updated_re_test_notification_buttons` sends a passive "HA app updated — ask Claude to re-test" push whenever `sensor.aarons_iphone_17_pro_app_version` changes.
- iOS updates aren't auto-detected. Re-test after a notable iOS 27.x update too.

## When a fix ships: re-test and restore

1. Send an **active** test push (a passive one didn't surface on 2026-10-14) with an `INSTALL_HA_UPDATE` button whose `action_data.entity_id` is a **non-pending** update (e.g. `update.home_assistant_core_update` when it's `off`). Long-press, confirm the buttons load, tap Install and approve with Face ID. Then confirm `automation.ha_updates_install_on_approval` got a trace that stopped at its condition (safely ignored).
2. Test the leak buttons the same way. **Tap Dismiss only.** Shut Off Water really closes the main valve, so only test it deliberately with Aaron present.
3. ~~Revert the leak tap target~~ Done 2026-10-14 differently: the leak push, the HA update push and Alert2 button pushes now carry **no** `url`/`entity_id`, because either one hides the tap sheet. Re-check whether that still holds once long-press works.
4. Delete `automation.companion_app_updated_re_test_notification_buttons`, mark this task Done, log to Changes, and update the HA System page Known Gaps.

## Changes

![[Changes.base#For this project]]
