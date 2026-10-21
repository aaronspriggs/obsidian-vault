---
status: active
category: docker
ip: 192.168.1.248
runs_on:
- '[[Dockhand]]'
last_verified: 2026-09-29
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks/servarr
notion_id: 30d7ae76-22ba-8119-9063-fb6430982534
---

7-container media automation stack on Big Boi, managed in Dockhand: Gluetun (VPN), NZBGet, Prowlarr, Sonarr, Radarr, Seerr, gluetun-watchdog.

## Overview

Docker Compose media automation stack on [TrueNAS SCALE (Big Boi)](<TrueNAS SCALE (Big Boi).md>), managed in [Dockhand](<Dockhand.md>) as stack `servarr`. It takes a request in Seerr, finds it on Usenet through Prowlarr/NZBGeek, downloads it through a VPN, and files it where Plex picks it up. Deployed 2026-02-19 from the TechHutTV homelab template; Dockge replaced by Dockhand 2026-03-04; Overseerr replaced by Seerr 2026-03-05.
Pipeline: Seerr → Sonarr/Radarr → Prowlarr → NZBGeek → NZBGet (via Gluetun VPN) → Newshosting → `/data/downloads/usenet/completed` → Sonarr/Radarr rename + hardlink into `/data/Movies` or `/data/TV Shows` → Plex (read-only NFS).
**Verified 2026-09-29:** all five web UIs answer on Big Boi; Dockhand app running (v1.0.49, catalog 1.1.34, no update); container list and config taken from the repo copy of the compose file (commit 2dd54a6), which only Aaron can refresh (see Related).

## Access

| Service | URL | Login |
| --- | --- | --- |
| Seerr | [http://192.168.1.248:5055](http://192.168.1.248:5055/) | Plex account |
| Sonarr | [http://192.168.1.248:8989](http://192.168.1.248:8989/) | Forms login, 1Password |
| Radarr | [http://192.168.1.248:7878](http://192.168.1.248:7878/) | Forms login, 1Password |
| Prowlarr | [http://192.168.1.248:9696](http://192.168.1.248:9696/) (published by Gluetun) | Forms login, 1Password |
| NZBGet | [http://192.168.1.248:6789](http://192.168.1.248:6789/) (published by Gluetun) | 1Password (default nzbget/tegbzn6789 was changed) |

Shell: `ssh aspriggs@192.168.1.248`, then `sudo docker …`. Claude has no shell on Big Boi, only the read-only TrueNAS API, so it can't see containers or files directly; Uptime Kuma monitors every UI above.

## Config

**Containers (7)** on bridge `servarrnetwork` 172.39.0.0/24 (`enable_ipv6: false`, needed or Dockhand's network recreate fails with `ParseAddr`):
- `gluetun` (qmcgaw/gluetun) 172.39.0.2: ProtonVPN WireGuard, US exits. Publishes 6789 and 9696 for the two containers inside it. Healthcheck hits Gluetun's own health server `http://127.0.0.1:9999`, never an external site ([ipinfo.io](http://ipinfo.io/) rate-limited the shared exit IP on 2026-07-11 and caused a restart loop).
- `nzbget`, `prowlarr` (linuxserver): `network_mode: service:gluetun`, so all their traffic goes through the VPN. Other containers reach NZBGet at **172.39.0.2:6789**.
- `sonarr` 172.39.0.5, `radarr` 172.39.0.6, `seerr` 172.39.0.7 (.3 is the watchdog, .4 unused) ([ghcr.io/seerr-team/seerr](http://ghcr.io/seerr-team/seerr)): direct, no VPN.
- `gluetun-watchdog` (alpine, docker socket): every 30 s, if Gluetun isn't `healthy`, restarts `nzbget` and `prowlarr` (they lose their network namespace when Gluetun restarts). Pinned to **172.39.0.3** since 2026-09-29 (commit c3c791d), so it can no longer take Gluetun's .2 during a recreate.
**Files on Big Boi:**
- Stack dir (Dockhand): `"/mnt/.ix-apps/app_mounts/dockhand/data/stacks/Big Boi/servarr/"` holds `compose.yaml`, `.env` (WireGuard private key; never leaves TrueNAS) and the per-app config dirs `gluetun/ nzbget/ prowlarr/ sonarr/ radarr/`. Backed up nightly into `vmstore` (see Dockhand).
- Seerr config: `"/mnt/Big Boi/BIGBOI/servarr/overseerr"` (absolute path, kept from the Overseerr days).
- `"/mnt/Big Boi/BIGBOI/servarr/"` otherwise holds only leftovers (old compose.yaml, Dockge data). Never run CLI compose against that directory.
- Media: `"/mnt/Big Boi/BIGBOI/plex_content"` mounted as `/data` in NZBGet, Sonarr and Radarr: `Movies/`, `TV Shows/`, `downloads/usenet/{intermediate,completed/{movies,tv}}`, plus older `Plex Media/`.
**Permissions:** containers run as PUID 3000 / PGID 0 (`aspriggs:root`); `plex_content` must be owned 3000:0, mode `rwxrwx---`, and `Big Boi/BIGBOI` needs `aclmode=passthrough`. If ownership reverts to root, imports fail silently ("Root folder not found") and NZBGet can purge completed downloads.
**App settings:** NZBGet MainDir `/data/downloads/usenet`, categories `movies`/`tv` (lowercase, must match the arrs), Newshosting `news.newshosting.com:563` SSL, 30 of 100 connections. Prowlarr holds NZBGeek and Full Syncs to Sonarr (172.39.0.5:8989) and Radarr (172.39.0.6:7878). Sonarr/Radarr use NZBGet at 172.39.0.2:6789 and root folders `/data/TV Shows` and `/data/Movies`. Seerr points at Plex 192.168.1.116:32400 and both arrs by internal IP (API keys had to be re-entered after the Overseerr migration). Seerr's `TZ` is hardcoded `America/Denver`; the others read `TZ` from `.env`.
**Services and cost (~$9/mo):** ProtonVPN Plus $71.76 per 2 years; Newshosting Unlimited $89.99/yr (renews at $9.99/mo after year 1); NZBGeek $12 lifetime.

## Dependencies

Runs on [Dockhand](<Dockhand.md>) on [TrueNAS SCALE (Big Boi)](<TrueNAS SCALE (Big Boi).md>); goes down with Big Boi. [Plex Media Server](<Plex Media Server.md>) reads the results over NFS. Watched by [Uptime Kuma](<Uptime Kuma.md>) (Sonarr, Radarr, Prowlarr, NZBGet, Seerr monitors), alerts via Home Assistant.

## Decisions

- **2026-02-19:** one `plex_content` dataset with no children, mounted once as `/data`, so Sonarr/Radarr can hardlink instead of copy (ZFS hardlinks can't cross datasets).
- **2026-02-19:** only the downloader and indexer go through the VPN; management UIs stay direct.
- **2026-03-04:** Dockge replaced by Dockhand because Dockge didn't substitute `${VAR}` in bind-mount paths with spaces. Mount paths stay hardcoded in compose; `.env` only carries PUID/PGID/TZ and the VPN settings.
- **2026-07-11:** Gluetun healthcheck moved to its internal health server (see Config).
- **2026-09-29:** every container on `servarrnetwork` gets a fixed IP, so nothing unpinned can take Gluetun's .2. Dockhand's deploy force-recreates the whole stack, which is exactly when that race used to hit.

## Related

Runbooks: [Managing the Servarr Docker Stack](<../runbooks/Managing the Servarr Docker Stack.md>), [Recovering Gluetun](<../runbooks/Recovering Gluetun - stuck exited - address already in use on restart.md>). Compose: [repo stacks/servarr](https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks/servarr) (refresh procedure in the stacks README).

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
