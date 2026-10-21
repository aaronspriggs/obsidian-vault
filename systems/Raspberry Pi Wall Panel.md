---
status: active
category: hardware
ip: 192.168.1.84
url: ssh://raspberrypidashboard@hadashboard
notion_id: 3087ae76-22ba-810d-8359-c33338d22fec
---

Raspberry Pi running TouchKio kiosk display. Shows HA dashboard on Official RPi Touch Display 2. MQTT connected to Home Assistant Mosquitto broker. Hardwired, static IP in UniFi.

## Overview

Raspberry Pi configured as a wall-mounted home automation dashboard. Runs TouchKio in kiosk mode displaying a dedicated Home Assistant Lovelace dashboard. Publishes touch activity and brightness control via MQTT.

## Hardware

- **Device:** Raspberry Pi (arm64)
- **Hostname:** hadashboard
- **IP Address:** 192.168.1.84
- **Connection:** Hardwired and PoE-powered from USW Pro Max 16 PoE port 6 (about 5 W); DHCP reservation in UniFi (verified 2026-09-28)
- **Linux User:** raspberrypidashboard
- **Display:** Official Raspberry Pi Touch Display 2 (LCD)
- **Touchscreen:** Goodix Capacitive TouchScreen (10-005d)
    - Input handlers: kbd mouse0 event4
    - Touch events validated via evtest
- **Backlight sysfs path:** /sys/class/backlight/10-0045
    - Files used: brightness, max_brightness

## Software

- **OS:** Debian trixie (arm64)
- **Kiosk app:** TouchKio (github: leukipp/touchkio)
- **MQTT clients:** mosquitto-clients 2.0.21-1
- **evtest:** 1.35-1+b1 (used for touch input validation)

## TouchKio Configuration

- **Config file:** ~/.config/touchkio/Arguments.json
- **MQTT broker:** mqtt://192.168.1.218:1883
- **MQTT user:** mqttdashboard
- **Dashboard URL:** [http://192.168.1.218:8123/wall-panel/0](http://192.168.1.218:8123/wall-panel/0)
- **Screensaver URL:** [http://192.168.1.218:8123/wall-panel/screensaver](http://192.168.1.218:8123/wall-panel/screensaver)
- **Note:** TouchKio requires a full restart (not just HA refresh) for kiosk mode changes to apply

## Brightness Control Bridge

- **Script:** /usr/local/bin/[wallpanel-brightness-mqtt.sh](http://wallpanel-brightness-mqtt.sh/)
- **Service:** /etc/systemd/system/wallpanel-brightness-mqtt.service
- **MQTT credentials config:** /etc/wallpanel-mqtt.conf (chmod 600)
- **Subscribes to:** wallpanel/brightness/set
- **Publishes state to:** wallpanel/brightness/state (retained)
- **Writes to:** /sys/class/backlight/10-0045/brightness

## Home Assistant Entities (via MQTT discovery)

- text.touchkio_hadashboard_page_url — page navigation control
- light.touchkio_hadashboard_display — display on/off
- number.wall_panel_brightness — brightness via MQTT bridge script

## Home Assistant side (moved from the HA OS page 2026-09-29; automations verified live)

- **Dashboard:** `wall-panel` (view 0) plus a `screensaver` view, shown in TouchKio kiosk mode. HA user **MQTT Dashboard** (non-admin, kiosk mode, menus hidden) is dedicated to the panel.
- **Helpers:** dim timer 60 s, screensaver timer 10 min.
- **Automations:**
    - `automation.wall_panel_wake_on_activity`: MQTT `wallpanel/activity` → display on, brightness 100% (gated to avoid spam), leave the screensaver view, restart both timers.
    - `automation.wall_panel_dim_after_60s_idle`: dim timer active → idle → 15% by day; display off 01:00–07:00.
    - `automation.wall_panel_screensaver_after_10m_idle`: screensaver timer active → idle → go to the screensaver view at 15% (skipped 01:00–07:00).
    - `automation.wall_panel_morning_wake`: 07:00 daily → display on at 15%.
    - `automation.wall_panel_start_idle_timers_on_ha_startup`: restarts the idle timers after an HA restart.
- **Gotcha:** trigger on the timer's state change (active → idle), not the `timer.finished` event, which proved unreliable.

## Open work

Screensaver content (including the photo slideshow idea) is under "Design HA wall panel screensaver content".
![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
