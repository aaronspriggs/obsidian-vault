---
date: 2026-10-07
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Dockhand]]'
project:
- '[[Monitoring - Dockhand container alerts to HA via ha-dockhand]]'
notion_id: 3f27ae76-22ba-8145-9cd1-fab0ff969b10
---

# Added Dockhand container alerts with tap-to-restart in HA

What: Aaron connected ha-dockhand (Dockhand user `homeassistant`, token in 1Password 'Dockhand API token (Home Assistant)'; options: 60 s/600 s polling, update entities on, everything else off). Claude created `automation.homelab_container_alerts_dockhand`. It pushes a time-sensitive alert when gluetun, gluetun-watchdog, nzbget, prowlarr, radarr, seerr, sonarr or uptime-kuma isn't running for 5+ min, or a _health sensor is unhealthy for 5+ min. A passive recovery notice replaces it if the outage lasted 5+ min, and a passive notice goes out when Dockhand's 04:00 check finds a newer image. Tapping an alert opens the container's Restart button; for Gluetun it opens the servarr stack restart, because nzbget and prowlarr share its network and gluetun-watchdog restarts them. Claude also created `automation.homelab_container_restart_on_tap`, which presses that button when the push's Restart action is tapped; it stays dormant until iOS#5881 is fixed. Excluded: ix-dockhand containers. Checked: 'HA Updates — Ask for Approval' only acts on label `ha_update_approval`, so container updates can't reach its Install flow. Container updates do now appear in Settings → Updates and in `sensor.ha_pending_update_count`. Why: Dockhand step 3, and the first one-tap fix. Roll back: delete both automations; remove the Dockhand integration and HACS repo.
