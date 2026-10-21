---
type: project
status: done
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
completed: 2026-10-14
notion_id: 3f97ae76-22ba-8120-9bf0-c5b2a524bc50
---

Done 2026-10-14. One-tap actions on iOS pushes (tap the push, pick a button): container Install / Update all, container Restart, Ack / Snooze (2hr) / Open dashboard on Alert2 problems, leak Shut Off Water / Dismiss, HA update Install; push rules, overnight-only 09:00 report, Sunday weekly report, maintenance mode. Rules: runbook 'Homelab alerting', sections Push rules / Maintenance mode. Follow-ups: 'Verify one-tap actions on first real use'; TrueNAS approvals move to the TrueNAS write-access work.

## Why

Aaron wants to approve things like updates with one tap from the phone instead of opening a UI.

## Depends on

- [Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts](<Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts.md>) (active in another Claude Code thread). As of 2026-10-14 every homelab source goes through **Alert2** (YAML `alert2:` in the repo, quiet hours 20:00–09:00 via notifier template, 09:00 report). Deliberately native: HA update approvals (interactive workflow) and leak alerts (critical path). `homelab_container_restart_on_tap` (Dockhand Restart button) is scheduled for deletion ~10-21.
- Alert2 hooks to use: per-alert `data` carries the iOS payload (so `actions` can be added there), `alert2.ack` / `notification_control` actions, and `alert2_*` events. Handlers listen for `mobile_app_notification_action` as usual.
- The redesign put ack/snooze on the dashboard because buttons were assumed broken; with the tap sheet working, Ack/Snooze buttons on Alert2 pushes are now an option too.

## Constraints (from 2026-10-14 testing)

See [Restore iOS notification action buttons once upstream fix ships (iOS 5881)](<Restore iOS notification action buttons once upstream fix ships (iOS 5881).md>).
- Long-press buttons are broken upstream (iOS#5881). Buttons work by **tapping** the notification, which opens an in-app sheet; the Companion setting "show actions when tapped" must stay on.
- The sheet hides actions with `authenticationRequired: true`, so no Face ID-gated buttons for now. The sheet only opens in the unlocked app.
- **A push with buttons must have no ****`url`** (or `url: ""`). With a url, tapping just opens the app and the sheet never shows (tested 2026-10-14). Alert2's defaults set a dashboard url, so every Alert2 alert with buttons must override it with `url: ""`.
- Plain buttons are verified. Text-input and URI-from-sheet buttons are untested; test each the first time.
- Existing pattern to reuse: `automation.ha_updates_ask_for_approval` + `automation.ha_updates_install_on_approval` (handler re-checks the update is still pending before acting).

## Built

- **2026-10-14, container image updates.** Aaron picked this first and chose nightly snapshots as the safety net (no pre-update snapshot). Alert2 `homelab_container_update` alerts carry an **Install** button (`CONTAINER_UPDATE`); `automation.homelab_container_update_on_approval` re-checks the update is pending and installable, then runs `update.install` and reports ⏳/✅/⚠️. The 09:00 report sends one actionable push per pending update, since the 04:00 Dockhand check lands in quiet hours. Gluetun has a button-less alert (whole-stack deploy only). Safe tap test passed; first real install not yet seen. Repo [28da594](https://github.com/aaronspriggs/spriggs-homelab/commit/28da594).
- **2026-10-14, container Restart.** Restart button on container down/unhealthy alerts (Gluetun alerts restart the servarr stack), handled by `automation.homelab_container_restart_on_approval` (only while the alert is still firing). Live-tested with `gluetun-watchdog` stopped: worked once the url was blanked. Same fix applied to the container-update alert and the HA update approval push.
- **2026-10-14, leak alert.** Aaron put it on the standard: removed the valve-control tap (`entity_id`), so tapping shows Shut Off Water / Dismiss. Test push verified (Dismiss). Every actionable push now follows the same rules (no url/entity_id, no Face ID gate).
- **2026-10-14, Ack / Snooze 4h / Open dashboard** on every Alert2 firing push (defaults `data` template), handler `automation.homelab_alert_ack_snooze_on_tap`. Snooze tested end to end. Button rules now live in the runbook "Homelab alerting: add or change a monitor or alert" (section Buttons on alerts).
- **2026-10-14, push rules** (FYI / approval / problem / one-off), Snooze (2hr) as a real re-push, overnight-only 09:00 report, Sunday weekly report. Rules in the alerting runbook.
- **2026-10-14, maintenance mode** (mutes homelab pushes, 2 h auto-off, summary when it ends, dashboard toggle) and **Update all containers** on the weekly report.
- **Skipped (Aaron, 2026-10-14):** restart-proof Snooze reminders; HA rarely restarts and the weekly report is the backstop.

## Candidates not yet built

- TrueNAS app/system updates: needs a TrueNAS API key with write access (today read-only), a Tier 3 credential decision.

## Changes

![[Changes.base#For this project]]
