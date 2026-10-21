---
kind: procedure
status: active
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[Dockhand]]'
last_tested: 2026-10-01
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks/servarr
notion_id: 30d7ae76-22ba-8124-a5e1-c2fe467362ea
---

Operate the servarr stack in Dockhand: start/stop, image updates and compose changes (with the Gluetun recreate checks), tracing a missing download, common failures.

## When to use

Day-to-day operation of the `servarr` stack on Big Boi: start/stop/restart, image updates, compose changes, and tracing a request that never showed up in Plex. For Gluetun stuck `exited` or "address already in use", use [Recovering Gluetun](<Recovering Gluetun - stuck exited - address already in use on restart.md>) instead. Stack layout, IPs and paths are on the [Servarr Stack](<../systems/Servarr Stack (Docker Compose).md>) page.

## Prerequisites

- Dockhand: [http://192.168.1.248:3001](http://192.168.1.248:3001/), stack **servarr**. This is the normal path for everything below.
- Claude: no shell on Big Boi, but full Dockhand API access via `dockhand-api` on the ClaudeCode VM (since 2026-10-01). It reads freely; writes (deploy, update, restart) only after Aaron approves the specific action in chat. See repo `dockhand/README.md`.
- For CLI work: `ssh aspriggs@192.168.1.248` (Aaron only). Every CLI command below assumes this is set first:
```bash
STACK="/mnt/.ix-apps/app_mounts/dockhand/data/stacks/Big Boi/servarr"
```
Never run compose against `"/mnt/Big Boi/BIGBOI/servarr/compose.yaml"`: it's a stale leftover.

## Steps

### Start, stop, restart, logs

In Dockhand, open the stack and use the stack or per-container buttons; logs are per container. CLI equivalents:
```bash
sudo docker compose -f "$STACK/compose.yaml" ps
sudo docker restart sonarr                  # one container
sudo docker logs --tail 50 -f nzbget
```
Restarting Gluetun on its own is fine: `gluetun-watchdog` restarts NZBGet and Prowlarr within 30 s once Gluetun is healthy again. Stopping the whole stack and starting it again is also fine. Anything that **recreates** Gluetun (image update, compose change, `--force-recreate`) needs the check in the next step.

### Update images or change the compose file

**Step 1.** For a compose change, edit the repo copy first ([stacks/servarr/compose.yaml](https://github.com/aaronspriggs/spriggs-homelab/blob/main/stacks/servarr/compose.yaml)), commit, then paste it into Dockhand's stack editor.
**Step 2.** Before anything risky, snapshot the stack dir:
```bash
sudo zfs snapshot -r "Big Boi/ix-apps/app_mounts@pre-servarr-$(date +%F)"
```
**Step 3.** In Dockhand, **Update** (pull + recreate) or **Deploy** the edited stack. Dockhand's Deploy / "Save and redeploy" runs `docker compose up -d --force-recreate`, which recreates **all 7 containers** even for a one-line change. Per [Finsys/dockhand#419](https://github.com/Finsys/dockhand/issues/419), still open as of 2026-09-29; not verified on v1.0.49. It doesn't pull images; expect about 1–2 min downtime while Gluetun comes back healthy. To recreate only the changed service, save in Dockhand without deploying, then `sudo docker compose -f "$STACK/compose.yaml" up -d <service>`: without `--force-recreate`, compose only rebuilds services whose config changed.
**Step 4.** Check that NZBGet and Prowlarr point at the *current* Gluetun container. If Gluetun was recreated but they weren't, they show `Up` but have no network:
```bash
sudo docker inspect gluetun --format '{{.Id}}'
sudo docker inspect nzbget prowlarr --format '{{.Name}} {{.HostConfig.NetworkMode}}'
# if container:<id> doesn't match gluetun's Id:
sudo docker compose -f "$STACK/compose.yaml" up -d --force-recreate nzbget prowlarr
```
**Step 5.** Check that Gluetun holds 172.39.0.2 and the watchdog .3 (pinned since 2026-09-29; this is a sanity check now):
```bash
sudo docker network inspect servarrnetwork --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
```
If anything other than `gluetun` has .2, follow [Recovering Gluetun](<Recovering Gluetun - stuck exited - address already in use on restart.md>).

### Image updates through the Dockhand API (Claude)

Dockhand checks for newer images daily at 04:00 (notify-only, since 2026-10-01). To apply them, after Aaron approves:
```bash
dockhand-api "/api/containers/pending-updates?env=1"     # what's flagged
dockhand-api --write POST "/api/stacks/servarr/deploy?env=1" '{"pull": true, "build": false, "forceRecreate": true}'
```
Never update **Gluetun** on its own: recreating it alone leaves NZBGet and Prowlarr on the old namespace. Since 2026-10-14 Gluetun has the label `dockhand.update=false`, so Dockhand/HA won't offer per-container Install for it. When Gluetun has an update, use the stack deploy. The other six containers can be updated one at a time. The deploy returns a job ID; the stack is back in about 40 s. Then do steps 4 and 5 through the API instead of SSH: compare `HostConfig.NetworkMode` of nzbget/prowlarr (`dockhand-api "/api/containers/<id>?env=1"`) with Gluetun's ID, and read the `servarrnetwork` IPs from `/api/containers?env=1`. First run 2026-10-01: all 7 images updated, checks passed, no alerts.

### Image updates from HA (trial pending)

HA's update entities `update.big_boi_containers_<name>` (ha-dockhand) can apply updates too. Install calls Dockhand's `POST /api/containers/batch-update-stream` for that one container (pull + recreate). Aaron can click it, tap **Install** on the container-update push (since 2026-10-14; handled by `automation.homelab_container_update_on_approval`), or Claude can call ha-mcp `ha_manage_updates(action="install", entity_ids=[...])`. Gluetun doesn't offer Install (label above). After installing NZBGet or Prowlarr, still do step 4. This hasn't been tried yet: the next update round is the trial, tracked in [Trial HA Install for container image updates](<../projects/Trial HA Install (Dockhand update entities) for container image updates.md>). Once that's done, record which method is the default here.

### Trace a request that never arrived

1. Seerr ([:5055](http://192.168.1.248:5055/)): is the request approved and "Processing"?
2. Sonarr ([:8989](http://192.168.1.248:8989/)) / Radarr ([:7878](http://192.168.1.248:7878/)) → Activity → Queue, then History. "Root folder not found" or import permission errors mean ownership drifted (see Common failures).
3. NZBGet ([:6789](http://192.168.1.248:6789/)): queue and History. A download sitting in `intermediate` is still downloading or unpacking.
4. On disk:
```bash
ls -la "/mnt/Big Boi/BIGBOI/plex_content/Movies/" "/mnt/Big Boi/BIGBOI/plex_content/TV Shows/" | tail -20
```
1. If the file is there but Plex doesn't show it, scan the library in Plex (it reads the share read-only over NFS).

### Common failures

- **NZBGet/Prowlarr UI unreachable:** usually Gluetun restarted and the watchdog hasn't caught up; wait a minute, then `sudo docker restart nzbget prowlarr`. If they show `Up` with 0 B memory, run step 4 of the update procedure.
- **Imports fail / "Root folder not found":** `sudo chown -R 3000:0 "/mnt/Big Boi/BIGBOI/plex_content/"`.
- **linuxserver container won't start (chmod errors):** `sudo zfs get aclmode "Big Boi/BIGBOI"` must be `passthrough`; if not, `sudo zfs set aclmode=passthrough "Big Boi/BIGBOI"`.
- **Gluetun unhealthy or no VPN:** `sudo docker logs --tail 100 gluetun`; check `WIREGUARD_PRIVATE_KEY` and `WIREGUARD_ADDRESSES` in `"$STACK/.env"` (values unquoted). A fresh key comes from the ProtonVPN account (1Password).

## Verify

```bash
sudo docker compose -f "$STACK/compose.yaml" ps --format '{{.Name}} {{.Status}}'   # 7 containers, gluetun and seerr (healthy)
sudo docker exec gluetun wget -qO- https://ipinfo.io/ip                            # a ProtonVPN IP, not the home WAN IP
```
All eight Uptime Kuma monitors (Sonarr, Radarr, Prowlarr, NZBGet, Seerr, plus Sonarr/Radarr/Prowlarr Health) should be up, which also clears any HA alert. After a restart, a Health monitor can sit in `pending` for about 5 minutes (Sonarr Health did on 2026-10-01) while the app re-runs its own health checks; that's normal unless it turns `down`. Run the ipinfo check by hand only, never in a healthcheck.

## Rollback

Compose: paste the previous version from the repo history into Dockhand and redeploy. Config dirs: copy back from the step 2 snapshot (find it with `sudo zfs list -t snapshot -r "Big Boi/ix-apps/app_mounts" | grep pre-servarr`, then browse that dataset's `.zfs/snapshot/` directory; the exact child-dataset layout under `app_mounts` hasn't been confirmed) or from the nightly copy in `"/mnt/Big Boi/vmstore/dockhand-stacks-backup/"`. Image: pin the previous tag in compose and redeploy.
