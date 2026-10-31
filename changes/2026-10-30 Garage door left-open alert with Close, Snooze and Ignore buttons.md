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

**Alert:** `alert2.home_health_garage_door_open` in repo [`ha/alert2.yaml`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml). Fires when `cover.garage_door` has been open, opening or closing for 15 min, reminds every 15 min, priority medium. Its own notifier, so it pushes at any hour instead of following the 20:00-09:00 quiet hours; time-sensitive by day and critical (sounds through silent and Focus) 22:00-06:00. Title "🚗 Garage door is open", reminders "Still open after <time>.", passive "✅ Garage door is closed" / "No more reminders." when it closes (its own title since 2026-10-31: with the shared title it read "Garage door is open / Garage door is closed again", which Aaron found confusing). Buttons: Close door, Snooze 2hr, Ignore, with the subtitle "👆 Tap to Close door".

**Handler:** `automation.garage_door_alert_buttons_and_night_check` (UI automation). Close door runs `cover.close_cover` unless the door is already closed and re-pushes "⚠️ Garage door didn't close" if it isn't closed 90 s later. Snooze 2hr acks the alert and, 2 h later, unacks and re-pushes if the door is still open (capped at 21:00). Ignore acks it. The night failsafe: at 21:00, whenever an ack has been in place 30 min between 21:00 and 06:00, and 2 min after an HA start in that window, an acked alert for an open door is unacked (Alert2's 15-min reminders resume) and re-pushed, so Ignore, Snooze or a restart can't carry it through the night. The alert's condition stays true while the cover is unavailable or unknown and the alert is already on (as the battery-low alerts do), so a Meross LAN poll miss or an HA restart can't send a false "closed again"; re-pushes then say HA can't reach the opener. It doesn't use the shared `automation.homelab_alert_ack_snooze_on_tap`, which moves night reminders to 09:00 and words Ack for homelab problems.

## Why

Choices are Aaron's (2026-10-30): 15-min threshold, 15-min reminders, any hour with critical at night, and Close / Snooze 2hr / Ignore, where Ignore is for working in the yard or garage with the door open on purpose and "there should be failsafes built in so that I don't leave it open overnight". 21:00 as the start of "after hours" and the 30-min night limit on an ack were Claude's defaults.

## Notes

Long-press: re-tested with a test push the same day, still "Loading actions…" on Companion 2026.10.2 (Aaron). Upstream [home-assistant/iOS#5881](https://github.com/home-assistant/iOS/issues/5881) is still open and the Companion 2026.10.3 release notes (2026-10-29) don't mention a fix; Aaron's phone runs 2026.10.2. Tap path verified the same day: Aaron tapped a test push and Close door, and the handler ran the Close door branch and stopped at "Already closed" (door was closed). The buttons work by tapping the push, as on every other actionable alert ([[Restore iOS notification action buttons once upstream fix ships (iOS 5881)]]).

Known gap: an HA restart during the day drops a pending 2 h snooze; the 21:00 check still catches it. End-to-end test the same day (Aaron left the door open): opened 16:32:33, alert fired and pushed 16:47:33 (exactly 15 min), Aaron tapped Close door 16:47:42, door closing then closed 16:47:57, alert off and the closed push sent at once. Not yet seen live: the 15-min reminder wording, the critical push at night, Snooze and Ignore on a firing alert, and the night failsafe.

`switch.garage_door_buzzerenable` is off, so the opener gives no warning beep when Close door runs with nobody watching it. The beep is the safety warning for an unattended close; Aaron chose to leave it off (2026-10-30).
