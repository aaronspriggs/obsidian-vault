---
type: project
status: done
priority: medium
system:
- '[[Servarr Stack (Docker Compose)]]'
completed: 2026-02-20
notion_id: 30b7ae76-22ba-8149-8ef9-df1c63adca75
---

Deployed 2026-02-19. Stack: Gluetun, NZBGet, Prowlarr, Sonarr, Radarr, Overseerr + Dockge. Usenet-only via Newshosting/NZBGeek, VPN via ProtonVPN. End-to-end tested successfully.

## Outcome

Deployed 2026-02-19 on TrueNAS (then 24.10) from the [TechHutTV media stack](https://github.com/TechHutTV/homelab/tree/main/media): Gluetun, NZBGet, Prowlarr, Sonarr, Radarr, Overseerr, managed in Dockge. End-to-end tested the same day (Overseerr request → Radarr → NZBGeek → NZBGet → Newshosting → `Movies/` → Plex picked it up) and VPN egress confirmed. Since then Dockge was replaced by Dockhand (2026-03-04), Overseerr by Seerr (2026-03-05), and `gluetun-watchdog` was added. Current state: [Servarr Stack](<../systems/Servarr Stack (Docker Compose).md>).

## Decisions

- **Usenet only, no torrents:** no qBittorrent, port forwarding or seeding; faster and simpler to automate.
- **ProtonVPN Plus** ($2.99/mo, 2-year): already in the Proton ecosystem, native Gluetun support, WireGuard, no port forwarding needed for Usenet.
- **Newshosting Unlimited** (annual): Tier-1 Omicron backbone, 6,390+ days retention. **NZBGeek** lifetime ($12) as the indexer.
- **Dropped from the template:** qBittorrent, Lidarr (no music), Bazarr (no subtitles), Deunhealth (Gluetun's healthcheck was judged enough; later superseded by `gluetun-watchdog`).
- Problems hit during the build and their fixes (`aclmode=passthrough`, lowercase NZBGet categories, reaching NZBGet via 172.39.0.2) are now on the System page and the servarr runbook.

## Links

Original write-up (merged here 2026-09-29, now deprecated): "Servarr Media Automation Stack", a subpage of this page.
[DEPRECATED] Servarr Media Automation Stack
