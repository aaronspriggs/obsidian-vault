---
date: 2026-10-01
type: upgrade
system:
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
notion_id: 3ec7ae76-22ba-8158-81d2-c5dbfe286d7c
---

# Updated all servarr images through the Dockhand API

Approved by Aaron. POST /api/stacks/servarr/deploy {pull, forceRecreate}: all 7 containers on new images in ~40 s. Checked through the Dockhand API that NZBGet and Prowlarr are attached to the new Gluetun, gluetun .2 / watchdog .3, all UIs up, Seerr 3.5.0. Sonarr Health pending ~5 min, then up; no alerts.

**Before → after image IDs:** nzbget 498d0e95→d8997558, prowlarr e085b7e0→899607d0, gluetun 5694e332→7f376a7d, sonarr ac5a542a→1a11b875, radarr 91756157→17292112, seerr 83dd8709→c1673c6c, gluetun-watchdog (alpine) d529dd0c→320994c3.
**Timeline (UTC):** deploy job 18:40:5x; all containers recreated at +20 s; Gluetun healthy at +41 s. NZBGet/Prowlarr started before Gluetun reported healthy (Dockhand's deploy didn't wait on `depends_on: service_healthy` here); the watchdog covers that.
**Checks (API, no SSH):** nzbget and prowlarr `NetworkMode` = `container:a5b572e34099…` = Gluetun; servarrnetwork gluetun 172.39.0.2, watchdog .3, sonarr .5, radarr .6, seerr .7; :8989/:7878/:9696 ping 200, NZBGet 401 (login), Seerr status 200 v3.5.0.
**Kuma:** Radarr briefly `pending`, Sonarr Health `pending` 18:41:47–18:46:47 (likely a transient health error while Prowlarr/NZBGet came back), then all eight up. No HA alert fired (last trigger 2026-09-29).
Old images are left on disk (see the "Prune old Docker images on TrueNAS" task). Runbook "Managing the Servarr Docker Stack" now has an API update section.
