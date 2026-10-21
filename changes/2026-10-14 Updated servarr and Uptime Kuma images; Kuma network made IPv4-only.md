---
date: 2026-10-14
type: upgrade
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[Uptime Kuma]]'
project:
- '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/9b6ef2c
notion_id: 3f97ae76-22ba-8114-972c-eaf2cf27e8ee
---

# Updated servarr and Uptime Kuma images; Kuma network made IPv4-only

Requested by Aaron. POST /api/stacks/{servarr,uptime-kuma}/deploy {pull, forceRecreate}. Servarr clean. Kuma recreate failed on a compose IPv6 parse bug; fixed by pinning its default network IPv4-only (commit 9b6ef2c), ~1 min Kuma downtime. All UIs up, pending-updates now empty.

**Before → after image IDs:** nzbget d8997558→b2eb402b, prowlarr 899607d0→cc10ec06, sonarr 1a11b875→50297d3f, radarr 17292112→d13ecd01, uptime-kuma 836213ab→7eb1ae12. Gluetun, Seerr and the watchdog had no new image (recreated only).
**Servarr (14:45 UTC):** deploy done in ~45 s. This time NZBGet and Prowlarr started *after* Gluetun reported healthy. Both have `NetworkMode` = `container:21749d66c1c1` (the new Gluetun). Sonarr/Radarr/Prowlarr return 302, NZBGet 401 (login), Seerr 307.
**Kuma failure and fix:** the deploy pulled the image, then failed with `ParseAddr("fdd0:0:0:2::1/64"): unexpected character`, so the old container kept running. The cause is the compose-created `uptime-kuma_default` network: it got an IPv6 subnet from the TrueNAS Docker address pool with its gateway stored as `fdd0:0:0:2::1/64`, which compose can't parse when it inspects an existing network. `ix-dockhand_default` has the same shape. Servarr wasn't affected because `servarrnetwork` is explicit and `enable_ipv6: false`. The fix was to add `networks: default: enable_ipv6: false` to the Kuma compose (repo commit 9b6ef2c, pushed to Dockhand via PUT /api/stacks/uptime-kuma/compose). Then `down`, which removed the container but hit the same error on the network, so the network was deleted via DELETE /api/networks/<id>, then the stack was deployed again. The new network is IPv4-only, 172.16.1.0/24. A follow-up forceRecreate succeeded, so future updates won't hit this. Kuma was down ~14:48–14:49 UTC.
**Gotcha for future stacks:** any new Dockhand stack that uses the implicit default network on Big Boi will hit this on its first recreate. Declare the network IPv4-only up front.
Old images are left on disk (see [Prune old Docker images on TrueNAS](<../projects/Prune old Docker images on TrueNAS.md>)). `make check` is clean before and after.
