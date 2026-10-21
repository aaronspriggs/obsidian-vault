---
date: 2026-09-29
type: doc
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[UniFi (UDM Pro)]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
notion_id: 3ea7ae76-22ba-81fb-8230-cc6b3db7c2fa
---

# KB governance phase 4 (part 3a): Servarr page and runbooks rewritten, orphan pages merged

Servarr System page rewritten to the skeleton (1,583 -> ~900 words) with corrected paths; servarr and Gluetun runbooks rewritten for Dockhand; 3 orphan top-level pages merged into Projects, deprecated and moved under them.

## What

- **Servarr Stack (Docker Compose):** rewritten to the Systems skeleton (1,583 → ~900 words). Fixed: TrueNAS 24.10 → 25.04, Dockhand v1.1.4 → v1.0.49 (catalog 1.1.34), per-app config dirs and `.env` are in the Dockhand stack dir (the page said `/mnt/Big Boi/BIGBOI/servarr/…`), Seerr config is `…/servarr/overseerr` (page said `…/seerr`), 7 containers not 6, kill switch doesn't "pause" dependents (the watchdog restarts them). The 16 gotchas were folded into Config/Decisions or moved to the runbooks. Added Open work view; set `Repo`, `Runs On` Dockhand, `Last Verified` 2026-09-29 (all five UIs answer; Dockhand app state via TrueNAS API; container config from repo commit 2dd54a6).
- **Runbook "Managing the Servarr Docker Stack":** rewritten for Dockhand (was Dockge/Overseerr): start/stop, update with the Gluetun-recreate and .2-IP checks, request tracing, common failures, verify, rollback.
- **Runbook "Recovering Gluetun":** first half was one mangled block with literal `nn` for line breaks; rewritten to the runbook skeleton. Corrected: the watchdog uses the Docker socket, not Gluetun's control API; only Sonarr/Radarr (not Prowlarr) reach NZBGet by IP.
- **Orphans:** "Servarr Media Automation Stack" merged into the empty Done project "Deploy Servarr Media Automation Stack" (Outcome/Decisions); "Local DNS records explored" merged into Idea "Set up Nginx Proxy Manager"; "WireGuard VPN configured on UDM Pro" merged into Done project "Set up WireGuard VPN". All three retitled `[DEPRECATED]` with a pointer line and moved under those project pages.
- "Add health checks and autoheal to servarr stack": Notes and Next Step updated (remaining work is pinning the watchdog IP).

## Roll back

Pre-change copies: export 4ac914e (branch `kb-export`), also in the session scratchpad. To undo a move, move the page back to the workspace top level.
