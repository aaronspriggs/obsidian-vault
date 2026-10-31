---
date: 2026-10-31
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/a89dde3
---

# Alert quiet hours moved to 22:00, garage alert left out of the 09:00 report's cleared list

The 31 October 09:00 report listed "Garage door open" as fired and cleared. The door had been open from 20:42 to 20:57 the night before, and Aaron closed it from the push himself. That counted as overnight because the quiet hours and the report window started at 20:00. Aaron asked for the overnight window to start at 22:00 and said he didn't think he'd want things he cleared himself in the report.

## What changed

**Quiet hours are now 22:00–09:00 everywhere.** The report window and the quiet hours have to move together. If only the report moved, alerts firing between 20:00 and 22:00 would send no push and also never appear in the report. So Alert2 alerts now push live until 22:00. Five places changed:

- `defaults.notifier` in repo [`ha/alert2.yaml`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml). Applied with `ha_config_set_yaml` (an `add` merge of `defaults` only, a one-line diff), then `alert2.reload`.
- `automation.homelab_alerts_09_00_report`: the `report` window now starts at 22:00 the previous day.
- `automation.homelab_alert_ack_snooze_on_tap`: a snooze reminder that lands after 22:00 moves to 09:00.
- `automation.homelab_alerts_alert2_watchdog`: holds until 09:00 only after 22:00, and the wait timeout went from 14 h to 12 h.
- `automation.homelab_maintenance_mode`: sends its end-of-maintenance summary until 22:00.

The garage alert's own times (critical 22:00–06:00, 21:00 failsafe, Snooze capped at 21:00) are separate rules and are unchanged.

**The garage alert is left out of the report's fired-and-cleared list**, through a `live_only` list in the report's `report` variable. It still appears under "still open" if the door is open at 09:00. Between 22:00 and 09:00 it is the only Alert2 alert that both pushes (its own notifier, critical at night) and can be cleared from the push. Every other alert is silent in that window, so nothing else can be cleared by hand. In practice, then, "manually cleared" means the garage door.

## Verification

The new `report` template, rendered for the 31 October report window, no longer lists the garage alert. The notifier template renders a push at 21:00 and quiet at 22:30. After the reload, all 111 `alert2.*` entities were available. `ha_search` finds no other `20:00` or `hour >= 20` quiet-hour logic in automations or scripts.

## Notes

Revert: change `22:00` back to `20:00` in the five places above, and remove `live_only` from the report. The Home Health, HA OS and Homelab alerting notes and the TrueNAS runbook now say 22:00–09:00. Older change notes still say 20:00, which is correct for when they were written.
