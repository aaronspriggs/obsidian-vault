---
kind: troubleshooting
status: active
system:
- '[[Raspberry Pi Wall Panel]]'
notion_id: 3087ae76-22ba-819f-969f-cdd280c3f12f
---

Troubleshooting guide for the Raspberry Pi wall panel — covers MQTT auth issues, automation trigger gotchas, display off vs brightness 0, and kiosk mode behavior.

## Overview

Key gotchas and fixes for the RPi wall panel (hadashboard) brightness control, screensaver automations, and kiosk mode behavior.

## Kiosk Mode Not Applying

- **Symptom:** Menus still visible after configuring kiosk mode
- **Fix:** TouchKio requires a **full restart**, not just a Home Assistant refresh

## MQTT Brightness Service Failing ("not authorised")

- **Symptom:** wallpanel-brightness-mqtt.service repeatedly restarting; Mosquitto rejecting connection
- **Fix:** Credentials must be sourced from /etc/wallpanel-mqtt.conf (chmod 600)
    - Do not rely on credential extraction from TouchKio config at runtime

## Automation Timer Not Firing

- **Symptom:** Dim or screensaver automation never triggers despite timer finishing
- **Cause:** timer.finished event trigger is unreliable in Home Assistant
- **Fix:** Use state trigger instead:
    - from: active
    - to: idle
    - This is reliable and preferred over the event-based trigger

## Display Off vs Brightness 0

- **Important:** Setting brightness to 0% does NOT turn the display off
- **Fix:** Use light.turn_off on light.touchkio_hadashboard_display to truly power off the panel
- Used during overnight hours (1am-7am) after 60 seconds of idle

## Touch Causing Dashboard Reload

- **Symptom:** Every touch navigates back to main URL, causing reload/flash
- **Fix:** Add condition to URL-set action so it only fires when currently on screensaver URL
    - Do not unconditionally set page URL on every touch event

## Unknown Entity in Automation

- **Symptom:** Timer start actions show 'Unknown entity' and timers never start
- **Fix:** Re-select the correct timer entities in the automation GUI editor

## Script Syntax Error

- **Symptom:** [wallpanel-brightness-mqtt.sh](http://wallpanel-brightness-mqtt.sh/) fails with bash syntax error
- **Diagnosis:** Run bash -n /usr/local/bin/[wallpanel-brightness-mqtt.sh](http://wallpanel-brightness-mqtt.sh/)
- **Fix:** If 'done' was accidentally appended, remove last line with:
    ```javascript
    sed -i '$d' /usr/local/bin/wallpanel-brightness-mqtt.sh
    ```
    Then revalidate with bash -n

## Screensaver Rotation Abandoned

- Rotating screensaver via URL changes causes HA logo + spinner briefly — distracting
- Decided against rotation; using dimming + overnight display off for burn-in protection instead
