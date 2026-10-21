---
kind: troubleshooting
status: active
system:
- '[[Servarr Stack (Docker Compose)]]'
last_tested: 2026-07-11
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks/servarr
notion_id: 39a7ae76-22ba-81fb-95df-d041b644e248
---

# Recovering Gluetun: stuck exited / "address already in use" on restart

Gluetun won't start because gluetun-watchdog took its pinned IP 172.39.0.2, or NZBGet/Prowlarr point at a recreated Gluetun. Start Gluetun alone, then the rest; force-recreate NZBGet/Prowlarr after any Gluetun recreate.

## When to use

Gluetun shows `exited`, or is stuck in `Created` mid-restart, and `sudo docker start gluetun` fails with `Error response from daemon: Address already in use`. NZBGet and Prowlarr are down with it (they live in Gluetun's network namespace); Sonarr, Radarr and Seerr are unaffected. Also use it when NZBGet/Prowlarr show `Up` in Dockhand but are unreachable after Gluetun was recreated.

## Why it happens

Gluetun has a pinned IP, **172.39.0.2**, because Sonarr and Radarr reach NZBGet at that address. Until 2026-09-29 `gluetun-watchdog` had **no fixed IP**. While Gluetun was detached (crashed, mid-recreate), Docker treated .2 as free, and if the watchdog started first it could be given .2; Gluetun then couldn't start (reproduced 2026-07-11). The watchdog is now pinned to 172.39.0.3, which should prevent this. If it happens anyway, something else unpinned was added to `servarrnetwork`, or the pin was lost from the compose file.
Separately, `network_mode: service:gluetun` is resolved to a fixed container ID when NZBGet and Prowlarr are created. If Gluetun is **recreated** (new ID), they keep pointing at the dead namespace: they show `Up`, report about 0 B memory and have no network until they're force-recreated. A plain stop/start of Gluetun keeps its ID and is safe.

## Prerequisites

`ssh aspriggs@192.168.1.248` (Aaron; Claude has no shell on Big Boi), then:
```bash
STACK="/mnt/.ix-apps/app_mounts/dockhand/data/stacks/Big Boi/servarr"
sudo docker compose -f "$STACK/compose.yaml" config --services   # expect 7: gluetun gluetun-watchdog nzbget prowlarr sonarr radarr seerr
```
Only use the Dockhand stack file above; `"/mnt/Big Boi/BIGBOI/servarr/compose.yaml"` is a stale leftover.

## Steps

**Step 1.** Diagnose:
```bash
sudo docker inspect gluetun --format '{{.State.Status}} exit={{.State.ExitCode}} err="{{.State.Error}}"'
sudo docker network inspect servarrnetwork --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
```
If anything other than `gluetun` holds 172.39.0.2, that's the conflict.
**Step 2.** Stop everything unpinned, start Gluetun alone and wait for healthy:
```bash
sudo docker stop gluetun-watchdog nzbget prowlarr
sudo docker start gluetun
sleep 20; sudo docker inspect gluetun --format '{{.State.Status}} {{.State.Health.Status}}'   # repeat until "running healthy"
```
**Step 3.** Bring the rest back:
```bash
sudo docker start nzbget prowlarr gluetun-watchdog
```
**Step 4.** If Gluetun was recreated at any point, or NZBGet/Prowlarr fail with "No such container", force-recreate them:
```bash
sudo docker inspect gluetun --format '{{.Id}}'
sudo docker inspect nzbget prowlarr --format '{{.Name}} {{.HostConfig.NetworkMode}}'
# if container:<id> doesn't match:
sudo docker compose -f "$STACK/compose.yaml" up -d --force-recreate nzbget prowlarr
```

## Verify

Rerun the `network inspect` from step 1: `gluetun` holds .2. NZBGet ([:6789](http://192.168.1.248:6789/)) and Prowlarr ([:9696](http://192.168.1.248:9696/)) load, and their Uptime Kuma monitors are up.

## Rollback

Nothing here changes config; stopping and starting containers is safe to repeat.

## Background

- Incidents: Gluetun exited 2026-06-16, unnoticed until 2026-07-10; recurred 2026-07-11 during a Dockhand image update. Aaron recalls (2026-09-25, not certain) that the first one followed a power outage and an unclean restart of Big Boi, which points at startup ordering rather than Dockhand.
- **Durable fix applied 2026-09-29:** `gluetun-watchdog` pinned to 172.39.0.3 (commit c3c791d). Verified after a full Dockhand redeploy: gluetun .2, watchdog .3, NZBGet/Prowlarr attached to the new Gluetun ID. The "stale Gluetun ID" half of this runbook still applies to any Gluetun recreate done outside a full-stack deploy.
- Stack layout and IPs: [Servarr Stack](<../systems/Servarr Stack (Docker Compose).md>). Routine operation: [Managing the Servarr Docker Stack](<Managing the Servarr Docker Stack.md>).
