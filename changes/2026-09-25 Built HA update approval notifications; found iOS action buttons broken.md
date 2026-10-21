---
date: 2026-09-25
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3e67ae76-22ba-815f-a3a3-d873c4f72f39
---

# Built HA update approval notifications; found iOS action buttons broken upstream (iOS 27 + Companion 2026.9.1), added tap-to-open fallback

Built HA update approvals: the `ha_update_approval` label, `input_text.ha_update_in_progress`, and the automations `ha_updates_ask_for_approval`, `ha_updates_install_on_approval` and `ha_updates_report_after_restart`. Details are on the Home Assistant OS (VM) page, Update Approvals section.
**Test found an upstream bug.** A test push with an Install button (pointing at the non-pending Core update, so it was safe) showed "Loading actions…" on long-press and never loaded. The install automation had 0 runs, meaning no `mobile_app_notification_action` reached HA. The device is iOS 27.0 with Companion 2026.9.1, matching the open bug home-assistant/iOS#5881 (actionable notification buttons don't render or fire on iOS 27 + Companion 2026.9.x; no fix yet).
**Consequences:**
- The leak alert's Shut Off Water button currently can't close the valve. The alert still delivers (critical), and the valve is still controllable in the app.
- The HA update Install button doesn't work.
**Fallback applied:** the update notice now carries `url: /config/updates`, so tapping it opens HA's native Updates page (Install with a backup option). The Install button stays in place for when upstream fixes the bug.
**Open:** Aaron to decide whether tapping the leak alert should open the shutoff valve instead of the sensor. Re-test buttons after the next Companion/iOS update.
