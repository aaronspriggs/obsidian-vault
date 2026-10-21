---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[One-tap approval notifications (updates and similar)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/51413dd
notion_id: 3f97ae76-22ba-81ac-802a-ff598fcfbfa6
---

# Push rules: FYI / approval / problem / one-off; Snooze (2hr); overnight-only 09:00 report; Sunday weekly report

Aaron's rules so most pushes need no action. FYI pushes have no buttons; problems get Ack + Snooze (2hr); one-off problems Snooze only. 09:00 report = overnight only; new Sunday 09:00 weekly report lists everything still open. Rules in the 'Homelab alerting' runbook.

Aaron (2026-10-14): not every push should need an action. Rules agreed and written into the runbook "Homelab alerting: add or change a monitor or alert", section Push rules.
**Alert2** ([51413dd](https://github.com/aaronspriggs/spriggs-homelab/commit/51413dd)): button renamed Snooze (2hr). FYI event alerts (`vm_updated`, `truenas_warning`, `truenas_update`) set `actions: []` and the dashboard url; `truenas_warning` now passive (was active). One-off problems (`truenas_error`, `vm_update_failed`, `alert2.global_exception`) carry Snooze (2hr) only. Battery/offline alerts stay at no reminders (push once).
**`automation.homelab_alert_ack_snooze_on_tap`** rewritten: Ack = `alert2.ack` + confirmation. Snooze (2hr) = ack, confirm, wait 2 h (or until 09:00 if that's in quiet hours), stop if a condition alert cleared, else `alert2.unack` and re-push with the original buttons (Restart kept via `action_data.button`). Alert2's own snooze isn't used: it only mutes, never re-notifies (`SnoozeEnded` sends nothing, [entities.py](http://entities.py/)). Mode parallel. Gap: an HA restart during the wait drops the reminder.
**`automation.homelab_alerts_09_00_report`**: now only alerts that started or fired since 20:00 yesterday (still open / happened and cleared); Install pushes only for container updates whose Alert2 alert turned on overnight.
**New ****`automation.homelab_alerts_weekly_report_sunday_09_00`**: Sunday 09:00, lists open homelab problems (acked marked), Home Health battery/offline alerts and pending updates (container + `ha_update_approval`), all-clear push when empty. Test run 2026-10-14 15:51: 2 items (Living Room Fan Dimmer offline, water filter leak sensor battery low).
