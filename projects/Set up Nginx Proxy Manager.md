---
type: idea
status: backlog
priority: low
system:
- '[[UniFi (UDM Pro)]]'
notion_id: 3087ae76-22ba-819d-9c33-db08b4600abd
---

Previously installed on TrueNAS and removed. Needed for vanity HTTPS URLs without port numbers and reverse proxy for HA/other services.

## Goal

Clean HTTPS URLs for homelab services without port numbers (e.g. `plex.home`), via a reverse proxy plus local DNS.

## Status

Deferred. NPM was installed on TrueNAS once and removed after port conflicts. Everything is reached through bookmarks and native apps, which is good enough for now.

## Decisions

- **Local DNS on its own isn't worth it (explored 2026-02, UDM Pro → Settings → Policy Engine → DNS Records):** a record maps a name to an IP but can't drop the port (`:9443`, `:8123`), so it only pays off together with a reverse proxy (NPM or Caddy). The test record `plex.thespriggs.com → 192.168.1.116` was deleted; no local DNS records exist. The same session removed the stale DHCP DNS server 192.168.1.248 from the LAN, leaving 1.1.1.1.
- **If this is picked up:** use a `.home` suffix for local records (no public domain needed), behind NPM or Caddy.

## Links

Original note (merged here 2026-09-29, now deprecated): "Local DNS records explored — deferred, using bookmarks instead", a subpage of this page.
[DEPRECATED] Local DNS records explored — deferred, using bookmarks instead
