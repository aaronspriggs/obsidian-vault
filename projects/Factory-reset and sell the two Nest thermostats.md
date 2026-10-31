---
type: task
status: backlog
priority: low
system:
- '[[Home Assistant OS (VM)]]'
parent: '[[Migrate thermostats from Nest to ecobee]]'
next_step: 'Aaron: reset the second display the same way (Nest base fully wired with an ecobee''s wires), then put the ecobee back; Claude verifies it in HA.'
notion_id: 3fc7ae76-22ba-81eb-8c79-fa1b3b77479c
---

Aaron's task. Both removed from the Google Home app 2026-10-17. Off the wall, the Nest menu won't open, so the on-device reset (Settings → Reset → All settings) is blocked. The base-plate + USB idea doesn't work: the display's micro-USB port is covered when it's on the base, and an unwired base gives no power anyway (Aaron, 2026-10-31). To try instead: charge each display 30+ min on USB (a flat battery shows only a charging screen), then use the menu while still on USB. Fallback: HVAC breaker off, swap one ecobee off its wires for a Nest base, power on, reset both displays, put the ecobee back. Unofficial USB method (ResetToDefaults.dropbox file on the mounted drive) is from a JustAnswer thread, unverified. Wipe needed before selling: the device keeps the schedule and Wi-Fi password. 2026-10-31: USB alone doesn't work either. On USB the display stops at error E2 (its wiring check finds no power) and won't get past it, so it needs real 24V through a base. What worked (2026-10-31): Rh + C alone power the display, but it then shows 'Equipment detected' with the remembered Y1/W1 flagged red and won't skip past it. Only with every original wire moved onto the Nest base (G, C, Y1, Rh, W1) did it reach Settings → Reset. First unit reset that way.
