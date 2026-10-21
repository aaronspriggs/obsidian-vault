---
type: task
status: backlog
priority: medium
system:
- '[[Dockhand]]'
parent: '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
notion_id: 3fa7ae76-22ba-814f-8d25-c3d47bba33b0
---

Extracted 2026-10-15 from the Done Dockhand project (plan step 6). Dockhand is plain HTTP on 192.168.1.248:3001, so logins and the full-admin dh_ tokens (claude, homeassistant) cross the LAN unencrypted. Overlaps the access model project's HTTPS follow-up (Dockhand and ha-mcp). TLS changes are Tier 3.

## Goal

No Dockhand credential crosses the LAN in plaintext, and Dockhand's settings are reviewed and deliberately chosen.

## Plan

1. **HTTPS.** Check whether the TrueNAS catalog app can serve TLS itself (app certificate option) or needs a reverse proxy in front. Then repoint `dockhand-api`, ha-dockhand and the Uptime Kuma monitor. Tier 3 (TLS), so Aaron approves the approach first. Do it alongside the ha-mcp HTTPS follow-up in the [Claude access model - more admin access, secrets management, account hardening](<Claude access model - more admin access, secrets management, account hardening.md>) project.
2. **Settings review.** Check the global "Newer version tags" setting (matters for pinned tags like `uptime-kuma:2`), image vulnerability scans, image prune (off on Big Boi as of 2026-10-15), and Dockhand's own backup options. Keep `FEAT_API_DOCS` off, because it serves `/api/docs` unauthenticated.
3. Record the results on the Dockhand system page.
