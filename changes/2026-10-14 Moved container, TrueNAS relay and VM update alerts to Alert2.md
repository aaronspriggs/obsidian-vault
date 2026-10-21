---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/13a5caad6f932e35b4fd3cb97fa30434218db95d
notion_id: 3f97ae76-22ba-816f-a5dd-cf73b9c049a2
---

# Moved container, TrueNAS relay and VM update alerts to Alert2; morning report priority-aware

What (Tier 2, Aaron asked to keep going on the alerting migration): repo ha/alert2.yaml applied + alert2.reload. (1) Docker containers (ha-dockhand) replace automation.homelab_container_alerts_dockhand: alert2.homelab_gluetun_down (3 min, supersedes Kuma's prowlarr_down/nzbget_down and prowlarr_health since they share Gluetun's network), gluetun_unhealthy (5 min, supersedes prowlarr_health), <container>_container_down for containers Kuma can't see (gluetun_watchdog, autokuma), <container>_unhealthy for every other health-checked container (seerr, uptime_kuma, autokuma; pattern-based so new containers are covered), <container>_update for every image update (low, passive, no reminders, no push when cleared; 9 containers). Kuma owns reachability, so sonarr/radarr/etc. down comes from Kuma only. Tapping opens the container's (or servarr stack's) Restart button via url entityId:. (2) tracked: event alerts truenas_error (medium), truenas_warning (low, active), truenas_update (low, passive), vm_update_failed (medium), vm_updated (low, passive). automation.truenas_alert_relay and automation.homelab_vm_update_reports keep their webhooks and helpers but call [alert2.report](http://alert2.report/) instead of pushing; TrueNAS 'resolved' pushes dropped (logbook only). (3) 09:00 report: time-sensitive only if an unacked medium/high alert is open, else passive; wording 'Fired overnight'. (4) Watchdog message lists all covered sources. (5) [alert2.global](http://alert2.global/)_exception ignores aiohttp ClientConnectionResetError (a websocket client disconnect at 14:10 had pushed a time-sensitive alert for nothing). Turned off (not deleted): homelab_container_alerts_dockhand, homelab_container_restart_on_tap (its DOCKHAND_RESTART action button is no longer sent). Left native on purpose: HA update approval flow (interactive, tuned today), leak alerts. Test: [alert2.report](http://alert2.report/) homelab.vm_updated at 14:09 notified, no alert2_error. Verify: 92 alert2 entities; sensor.alert2generator_homelab_container_update = 9. Runbooks updated: TrueNAS relay, homelab-update.
