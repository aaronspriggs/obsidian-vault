---
type: task
status: done
priority: low
system:
- '[[Dockhand]]'
- '[[Home Assistant OS (VM)]]'
parent: '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
completed: 2026-10-07
notion_id: 3e77ae76-22ba-816d-93f5-ec463f018153
---

# Monitoring: Dockhand container alerts to HA via ha-dockhand

Phase of 'Homelab health monitoring'. Dockhand (v1.0.49) can notify on container state changes, Docker HEALTHCHECK failures, stack deploy results, image scan findings and newer image versions via Email/Webhook/MQTT; HA's Mosquitto is already running.

## Decision 2026-10-06 (Claude, under Aaron's go-ahead): ha-dockhand, not MQTT

Aaron accepted HA having more power (project "Claude access model", 2026-10-03), so the full-admin token objection is gone. ha-dockhand covers state, health and native update entities, and its per-container restart buttons can be the one-tap fix with no Claude session needed. Polling every 60 s plus a 5-minute "not running" grace also absorbs the deploy-recreate noise that the MQTT design had to work around. Code review of v1.10.2 (commit 1670e4c, 2026-09-24): no pip requirements; it only calls the configured Dockhand host via HA's aiohttp session, with no external URLs. Its writes are start/stop/restart, updates, limits and the auto-update/auto-deploy toggles; no delete, exec, user or settings calls. Container inspect runs only for stack-less containers and keeps only Memory/NanoCpus/PidsLimit/RestartPolicy, so env vars (e.g. the Gluetun key) never reach HA. Diagnostics redact `api_token`.

## Outcome (Done 2026-10-07)

ha-dockhand v1.10.2 is connected as the Dockhand user `homeassistant`. `automation.homelab_container_alerts_dockhand` alerts after 5 min down or unhealthy, sends a passive recovery notice, and sends a passive notice for newer images; tapping an alert opens the container's Restart button. `automation.homelab_container_restart_on_tap` handles the Restart action and stays dormant until iOS#5881 is fixed. **End-to-end test passed 2026-10-06 (Denver time):** gluetun-watchdog stopped via the Dockhand API at 18:06; it showed exited at 18:06:28; the alert fired at 18:11:28; Restart was pressed from the tap-through at 18:12:17; the recovery notice followed at 18:12:18. Not done: the containers aren't labeled `homelab_watch`, because `sensor.homelab_issue_count` would count `running` as an issue. Containers only report health if they have a HEALTHCHECK (see the servarr auto-heal project). Changes: "Installed ha-dockhand v1.10.2 via HACS" and "Added Dockhand container alerts with tap-to-restart in HA".

## Findings 2026-10-02 (Claude, read-only)

- **Live state:** Dockhand has no notification channels (`GET /api/notifications` = `[]`). Big Boi's update check is on, notify-only. Mosquitto add-on 7.1.1 has `logins: []` and customize off, so every MQTT client authenticates as an HA user. The Mosquitto runbook says the wall panel user is defined in the add-on config; that's no longer true.
- **Dockhand MQTT channel** (source v1.0.49, `src/lib/server/notifications/mqtt*.ts`): it's an Apprise-style URL, `mqtt://user:pass@host:1883/topic?qos=1`, one-shot publish, retain off by default. LAN IPs are allowed (only loopback and metadata are blocked). The JSON body is `title`, `message`, `type` (info/success/warning/error), `eventType`, `environmentId`, `environmentName`, `timestamp`. The container name only appears inside `message` (`Container "sonarr" die (image)`), and there's no exit code.
- **Event types are subscribed per environment.** The relevant ones: `container_exited` (die/kill), `container_oom`, `container_unhealthy`/`container_healthy`, `container_started`, `stack_deploy_failed`, `git_sync_failed`, `updates_detected`, `newer_version_available`. Dockhand suppresses die/kill events its own image updates cause (issue #68), but not stack redeploys (`--force-recreate`), so a deploy sends an exit for every container. A `dockhand.notify=false` label opts a container out.
- **Generic webhook channel (****`json://`****)** sends no `eventType`, so HA would have to parse titles. MQTT is the better fit.
- **raetha/ha-dockhand** (HACS, 42★, polls every 60 s): rich entities plus start/stop/restart/update and limit controls. It needs a `dh_` token, which is full admin on Free (accepted 2026-10-06, see the decision above). It polls state and fires no died/unhealthy events.

## Changes

![[Changes.base#For this project]]
