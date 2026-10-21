---
type: project
status: done
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Home Assistant OS (VM)]]'
- '[[Plex Media Server]]'
- '[[Uptime Kuma]]'
completed: 2026-10-07
notion_id: 3e57ae76-22ba-81d2-91c1-c0e4418b510b
---

Homelab service monitoring with HA pushes, silent when nominal. Core live 2026-09-26; last add-on done 2026-10-07; closed 2026-10-15. Alerting now owned by the Alerting redesign (Alert2).

## Outcome (Done 2026-10-07)

Monitoring for the homelab services on and around Big Boi is live and silent when everything is nominal. It was built and tested 2026-09-24 to 2026-09-26. The last add-on, [Dockhand container alerts via ha-dockhand](<Monitoring - Dockhand container alerts to HA via ha-dockhand.md>), finished 2026-10-07. Current details live on the system pages: [Uptime Kuma](<../systems/Uptime Kuma.md>) (monitors are now code via AutoKuma) and [Home Health](<../systems/Home Health (HA dashboard + alerts).md>). The pieces are homelab-update (weekly unattended VM updates), the HA Core/OS approval push and the TrueNAS alert relay. How alerts are raised and pushed is now owned by the [Alerting redesign](<Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts.md>) (Alert2), which is retiring this project's original HA automations.
Follow-ups (own items): [Stop false-positive arr health alerts](<Stop false-positive arr health alerts (Sonarr-Radarr-Prowlarr flapping).md>), [Alerting redesign](<Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts.md>), [Off-box dead-man check](<Monitoring - off-box dead-man check (alert when Big Boi-HA goes silent).md>) (Idea). Deferred: [TrueNAS metrics to HA](<Monitoring - publish read-only TrueNAS metrics to HA (MQTT discovery).md>), [SSL certificate expiry monitoring](<SSL certificate expiry monitoring.md>).

## Decisions

- **2026-09-24 (Aaron): Uptime Kuma** on Big Boi via Dockhand, the common homelab pattern (Claude had first suggested HA-native checks; Gatus and Beszel were considered). **Kuma detects, HA notifies:** no Kuma-side notifications, HA dashboards stay the main view. Scope: everything. Alert on down/needs attention, on a missed heartbeat, and when an update was done on Aaron's behalf; silent otherwise.
- **2026-09-24: no off-box dead-man check** (Aaron). Accepted limitation: Kuma, HA and the alert path all run on Big Boi, so if Big Boi goes down nothing alerts. Raised again 2026-10-09 and kept as a later Idea (linked above).
- **2026-09-24: no Docker socket for Kuma** (the socket means root on TrueNAS). The same day's "no Dockhand API for Claude" was reversed 2026-09-30; see the Dockhand project.
- **2026-09-24:** Kuma monitors use 60 s interval, 3 retries (about 4 min to "down").
- **2026-09-25:** UniFi switches/APs are watched through HA's UniFi integration (`sensor.<device>_state`), not Kuma pings; only the UDM Pro stays in Kuma, because the integration dies with it. The spare USW Flex is excluded. The UniFi integration has no UPS battery/on-mains data.
- **2026-09-25: ****`homelab-update`** is one reusable service for every Debian/Ubuntu VM: apt full-upgrade, optional app update (Plex: `claude-maint upgrade-plex`), reboot if needed, host checks, HA webhook result, Kuma push heartbeat. Sundays, staggered.
- **2026-09-25: HAOS is excluded from unattended updates.** Supervisor auto-updates; Core/OS/apps get a daytime approval push (backup first). No Claude involvement.
- **2026-09-26: relay TrueNAS's own alerts** (WARNING+, app updates, plus a synthetic stale-snapshot check) through the read-only API instead of rebuilding checks, and **no full-admin TrueNAS integration in HA** (Aaron): HA shouldn't become an entry point to the whole homelab, and HA runs on TrueNAS, so an HA-triggered reboot would kill itself mid-action. The HACS options (tomaae, kayl-codes) were evaluated; kayl-codes needs a Full Admin key.

## Links

Build log (phases 1–5, monitor table, relay tests): KB export commit 4ac914e and the Changes entries from 2026-09-24 to 2026-09-26. Done phases: [deeper servarr health checks](<Monitoring - deeper servarr health checks (Sonarr-Radarr-Prowlarr health APIs).md>), [servarr autoheal / watchdog IP pin](<Add health checks and autoheal to servarr stack.md>), [Dockhand container alerts](<Monitoring - Dockhand container alerts to HA via ha-dockhand.md>).

## Sub-items

![[Projects.base#Sub-items]]

## Changes

![[Changes.base#For this project]]
