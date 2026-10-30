---
date: 2026-10-30
type: config
system:
- '[[Home Assistant OS (VM)]]'
project: '[[Plan a home security system (Alarmo, door-window sensors, siren)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/c42ea4e
---

# Garage door left-open alert with Close, Snooze and Ignore buttons

Aaron forgets to close the garage door and wanted a reminder he can't sleep through, with a button to close it from the push. Built on the [Meross LAN integration](<2026-10-30 Added the Meross garage door opener to HA via Meross LAN.md>) added the same day.

## What changed

**Alert:** `alert2.home_health_garage_door_open` in repo [`ha/alert2.yaml`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml). Fires when `cover.garage_door` has been open, opening or closing for 15 min, reminds every 15 min, priority medium. Its own notifier, so it pushes at any hour instead of following the 20:00-09:00 quiet hours; time-sensitive by day and critical (sounds through silent and Focus) 22:00-06:00. Title "🚗 Garage door is open", reminders "Still open after <time>.", passive "✅ Garage door is closed again." when it closes. Buttons: Close door, Snooze 2hr, Ignore, with the subtitle "👆 Tap to Close door".

**Handler:** `automation.garage_door_alert_buttons_and_night_check` (UI automation). Close door runs `cover.close_cover` unless the door is already closed and re-pushes "⚠️ Garage door didn't close" if it isn't closed 90 s later. Snooze 2hr acks the alert and, 2 h later, unacks and re-pushes if the door is still open (capped at 21:00). Ignore acks it. The night failsafe: at 21:00, and whenever an ack has been in place 30 min between 21:00 and 06:00, an acked alert for an open door is unacked (Alert2's 15-min reminders resume) and re-pushed, so Ignore or Snooze can't carry it through the night. It doesn't use the shared `automation.homelab_alert_ack_snooze_on_tap`, which moves night reminders to 09:00 and words Ack for homelab problems.

## Why

Choices are Aaron's (2026-10-30): 15-min threshold, 15-min reminders, any hour with critical at night, and Close / Snooze 2hr / Ignore, where Ignore is for working in the yard or garage with the door open on purpose and "there should be failsafes built in so that I don't leave it open overnight". 21:00 as the start of "after hours" and the 30-min night limit on an ack were Claude's defaults.

## Notes

Long-press on the push still shows "Loading actions…": upstream [home-assistant/iOS#5881](https://github.com/home-assistant/iOS/issues/5881) is open and Companion 2026.10.3 (2026-10-29) doesn't mention a fix. The buttons work by tapping the push, as on every other actionable alert ([[Restore iOS notification action buttons once upstream fix ships (iOS 5881)]]). Known gap: an HA restart drops a pending 2 h snooze or 30-min ack timer; the 21:00 check still runs. `switch.garage_door_buzzerenable` is off, so the opener doesn't beep when Close door runs with nobody watching.
