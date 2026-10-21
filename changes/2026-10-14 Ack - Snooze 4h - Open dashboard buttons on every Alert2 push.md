---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[One-tap approval notifications (updates and similar)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/512b937
notion_id: 3f97ae76-22ba-8144-8857-ff636f22223e
---

# Ack / Snooze 4h / Open dashboard buttons on every Alert2 push

Alert2 defaults data is now one template: firing pushes get Ack / Snooze 4h / Open dashboard (url blanked), recovery pushes keep the dashboard url. Handler automation.homelab_alert_ack_snooze_on_tap. Snooze tested end to end after a timezone fix.

**Change** ([512b937](https://github.com/aaronspriggs/spriggs-homelab/commit/512b937)): Alert2 `defaults.data` became a single template returning push level, tag, url (`""` while firing, dashboard otherwise), `action_data.alert` and `actions` = Ack (`ALERT_ACK`), Snooze 4h (`ALERT_SNOOZE`), Open dashboard (URI, home_health alerts go to `/home-health/overview`, others to `#homelab-all`). Restart alerts carry Restart / Ack / Snooze 4h. Battery alerts dropped their own tag/url (inherited now). Container update alerts keep Install only.
New `automation.homelab_alert_ack_snooze_on_tap`: Ack = `alert2.ack`; Snooze = `alert2.notification_control` with `enable: on`, `snooze_until` now+4h (Alert2 also acks), each with a passive confirmation on the alert's tag.
**Tests:** a URI button opens the dashboard from the sheet (test push). First Snooze tap failed: Alert2 rejects a `snooze_until` without timezone ("Internal error ... without timezone info", which fired `alert2.alert2_error` with the new buttons). Fixed with `isoformat()`; second test (`alert2.report` on `homelab.vm_updated`) snoozed it to 19:33 with no error. Test snooze cleared, `alert2_error` acked. Rules written into the runbook "Homelab alerting: add or change a monitor or alert", section Buttons on alerts.
