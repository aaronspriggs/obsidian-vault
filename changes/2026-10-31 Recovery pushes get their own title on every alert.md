---
date: 2026-10-31
type: config
system:
- '[[Home Assistant OS (VM)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/3c948a2
---

# Recovery pushes get their own title on every alert

Aaron found the garage door's closed push confusing: iOS showed the alert's title, "🚗 Garage door is open", above "✅ Garage door is closed again." Every Alert2 condition alert had the same shape ("🖥️ NZBGet is down" over "✅ NZBGet is back up.").

## What changed

In repo [`ha/alert2.yaml`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml), each of the 12 condition alerts with a `done_message` now has a `title` template that switches on `notify_reason == 'StopFiring'` to the old recovery wording without the period (for example "✅ NZBGet is back up"), and its `done_message` is "No action needed.". The garage door alert got the same treatment first: "✅ Garage door is closed" / "No more reminders.". Converted by script from each alert's existing title and done_message, applied with `ha_config_set_yaml`, then `alert2.reload`: no `alert2_error`, generators unchanged (111 alert entities). The wording rule in the defaults comment and in the [alerting runbook](<../runbooks/Homelab alerting - add or change a monitor or alert (Kuma + Alert2).md>) is updated.

## Why

Alert2 sends `done_message` with the alert's `title`, and `title` accepts `notify_reason` ([Alert2 README](https://github.com/redstone99/hass-alert2#notification-templates)), so the recovery push can have its own title. `done_message` has no "how long it was on" variable, so the body stays a fixed line.
