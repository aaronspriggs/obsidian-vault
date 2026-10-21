---
status: active
category: docker
ip: 192.168.1.248
port: 3001
url: http://192.168.1.248:3001
runs_on:
- '[[TrueNAS SCALE (Big Boi)]]'
last_verified: 2026-09-28
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks
notion_id: 31b7ae76-22ba-811e-b9dc-c0d98edf62e2
---

## Overview

**Current version (verified 2026-10-15):** Dockhand **v1.0.53**, TrueNAS catalog package 1.1.38 (upgraded from v1.0.49 / 1.1.34 on 2026-10-15; see [the upgrade task](<../projects/Decide backup for the Dockhand TrueNAS app upgrade, then upgrade it.md>)), no update pending. TrueNAS shows it as `v1.0.49_1.1.34`. Updates appear in TrueNAS Apps and are visible to Claude via the read-only TrueNAS API (`app.query` → `upgrade_available`). **Stack definitions** live in `/mnt/.ix-apps/app_mounts/dockhand/data/stacks/` on the hidden `Big Boi/ix-apps` dataset, which has **no recurring snapshot task** (not selectable in the UI). **Covered since 2026-09-26** by a nightly TrueNAS cron job (23:30) that rsyncs the stacks into `/mnt/Big Boi/vmstore/dockhand-stacks-backup/` (root-only, not shared), which the daily `vmstore` snapshot keeps for 30 days. To restore a stack, copy its folder back from the backup or from a `vmstore` snapshot. Still take a manual recursive snapshot of `Big Boi/ix-apps/app_mounts` before risky changes. Since 2026-10-15 Claude can do this: `truenas-api --write zfs.snapshot.create '[{"dataset": "Big Boi/ix-apps/app_mounts", "name": "<name>", "recursive": true}]'`. Claude deletes it afterwards with `zfs.snapshot.delete` (Tier 2, one snapshot per call). Dockhand's own DB (`app_mounts/dockhand/data`) isn't in the nightly copy yet; that's planned in the backup project. Managed stacks: `servarr`, `uptime-kuma`.
Dockhand is the Docker stack management UI for Big Boi. It replaced Dockge in March 2026 (v1.1.4) after Dockge was found to not reliably resolve `${ENV_VAR}` substitution in compose files, causing missing bind mounts across the servarr stack.
Installed via the TrueNAS community app catalog (not manually via Docker run).

## Access

- **URL:** [http://192.168.1.248:3001](http://192.168.1.248:3001/)
- **Host:** TrueNAS SCALE (Big Boi) — 192.168.1.248
- **Managed stacks:** `servarr` (Gluetun, NZBGet, Prowlarr, Sonarr, Radarr, Seerr, gluetun-watchdog) and `uptime-kuma` (:3002)
- **Authentication: on since 2026-10-01** (before that there was no login, so anyone on the LAN had full control of Docker on Big Boi). Users (checked 2026-10-15): `admin` (Aaron), `claude` (Claude's API token; created 2026-10-01) and `homeassistant` (the ha-dockhand integration). Credentials in 1Password. Free edition: every user is a full admin, so there are no roles. API tokens (`dh_…`) are per user, created from Profile (click the avatar) → API tokens → Generate token, shown once and stored hashed. Still plain HTTP, so logins and tokens cross the LAN unencrypted; tracked in [Serve Dockhand over HTTPS and review its settings](<../projects/Serve Dockhand over HTTPS and review its settings.md>).
- Uptime Kuma's Dockhand monitor stayed up after auth was enabled (checked 2026-10-01).

## Key Details

- Installed as a TrueNAS community catalog app
- Connects to Docker via Unix socket: `/var/run/docker.sock`
- TrueNAS `apps` user (UID 568) was added to the `docker` group (GID 999) to allow catalog app access to the socket
- Compose files live in Dockhand's stacks dir: `/mnt/.ix-apps/app_mounts/dockhand/data/stacks/Big Boi/<stack>/compose.yaml` (verified 2026-09-27; an older note here said `/mnt/Big Boi/BIGBOI/servarr/compose.yaml`). Per-app config dirs (`./sonarr` etc.) sit alongside. A stray `servarr/compose.yaml.bak-20260711` is also there; it's safe to delete.
- **Repo copies:** [`stacks/`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks) in `aaronspriggs/spriggs-homelab` holds both compose files plus `servarr/.env.example` (variable names only). The real `.env` holds the WireGuard private key and never leaves TrueNAS. Git is the source of truth: Claude commits there, then deploys through the Dockhand API and checks drift against the deployed file. The procedure is in the [stacks README](https://github.com/aaronspriggs/spriggs-homelab/blob/main/stacks/README.md). Both stacks are Dockhand `internal` stacks; Git stacks are a [Deferred Idea](<../projects/Move the servarr and uptime-kuma stacks to Dockhand Git stacks.md>).
- Bind-mount **paths** are hardcoded (e.g. `/mnt/Big Boi/BIGBOI/plex_content:/data`), but servarr still uses `${VAR}` substitution from `.env` for `PUID`/`PGID`/`TZ` and the Gluetun VPN settings (verified 2026-09-27). The Overseerr service is now `seerr` (`ghcr.io/seerr-team/seerr`), with config still at `/mnt/Big Boi/BIGBOI/servarr/overseerr`.
- Compose changes go through the repo and an API deploy, not the Dockhand editor (decided 2026-09-30).

## Known behaviour

- A deploy (editor "Save and redeploy", or the API without `forceRecreate: false`) runs `docker compose up -d --force-recreate`, which recreates every container in the stack ([Finsys/dockhand#419](https://github.com/Finsys/dockhand/issues/419)). The repo deploy passes `forceRecreate: false`.
- The stack editor saves the file to disk *before* validating it, so a YAML error leaves a broken compose file in place until it's fixed.
- Relative compose paths like `./sonarr` resolve against the stack directory, so moving a stack's directory silently gives the apps empty configs (the 2026-03 incident). servarr still uses relative paths.
- Update detection has two parts: a per-environment schedule (Settings → Environments → <env> → Update check), which is on for Big Boi and notify-only as of 2026-10-15, and a global setting (Settings → General → Newer version tags) that decides how versions are read, which matters for pinned tags like `uptime-kuma:2`.
- Keep `FEAT_API_DOCS` off: it serves `/api/docs` unauthenticated.
- **Image prune** (Big Boi, on since 2026-10-15): weekly, cron `0 3 * * 0` in the environment's UTC timezone, `dangling` mode, so only untagged leftovers from updates are removed. API: `GET`/`POST /api/environments/1/image-prune`. PUT returns "settings not found" until the row exists. Before this was on, 21 old images (7.4 GB) had built up.

## Why Dockhand Over Dockge / Portainer

Dockge was rejected because it does not reliably resolve `${DATA_PATH}` in bind mounts, silently dropping `/data` volumes from containers. Portainer was considered but has been moving key features behind paid tiers. Dockhand was chosen for its polished UI, inline CPU/RAM/GPU per-container stats, and open BSL license appropriate for homelab use.

## Related

- See **Servarr Stack** system page for full stack configuration
- See **Managing the Servarr Docker Stack** runbook for day-to-day operations

## Open work

![[Projects.base#Open for this system]]

## Runs on this

![[Systems.base#Runs on this]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
