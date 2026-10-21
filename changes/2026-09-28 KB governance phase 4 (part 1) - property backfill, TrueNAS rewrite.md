---
date: 2026-09-28
type: doc
system:
- '[[ClaudeCode (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
- '[[UniFi (UDM Pro)]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/65bc103
notion_id: 3e97ae76-22ba-81e7-91e4-ccd0591bac73
---

# KB governance phase 4 (part 1): property backfill, TrueNAS rewrite, Known Gaps to Projects

Backfilled every property gap [HEALTH.md](http://health.md/) listed; rewrote TrueNAS as current state from the API; moved Known Gaps on 11 System pages into 10 new Projects + live Open work views; deprecated 3 runbooks; kb-export skips deprecated items (65bc103).

## What

Part 1 of phase 4 of [KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)](<../projects/KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager).md>).
- **Properties:** `System` on 30 Changes, 25 Projects and 11 Runbooks; `Date Completed` on 3 Done projects (from their Change dates); `Status` on all 17 Systems (Dockge Deprecated + Category Docker, USW Flex Spare, rest Active). `Runs On` = TrueNAS for Plex, ClaudeCode and Dockhand. Change title fixed to "Proton Authenticator".
- **TrueNAS SCALE (Big Boi):** rewritten to the Systems skeleton from a live read-only API pull (pool/disks, datasets with sizes, shares, snapshot tasks, cron, VMs, certs). Closed "Document TrueNAS drive configuration". `Last Verified` 2026-09-28.
- **Known Gaps / Future Plans:** removed from TrueNAS, Plex, Dockhand, ClaudeCode, UDM Pro, both switches, 3 APs, HDHomeRun and Workstation; each now ends in a live linked "Open work" view (Projects filtered by System, not Done). 10 new Projects entries: wall-panel SSH, HDHomeRun antenna docs, UniFi network docs, UDM hardening, Cloudflare Tunnel/WAF, SSL expiry monitoring, weekend-aware wake, second Google connected app, workstation specs + Apple TV model, GPU/AV1. Duplicates folded into existing entries instead.
- **Stale content fixed:** Dockhand stacks (Seerr, uptime-kuma), ClaudeCode updates (0 pending, kernel 7.0.0-34), Plex (library layout, EAE path, WAN IP removed), UDM (garbled duplicate WAN lines, subnet, WireGuard section, USW Flex spare).
- **Runbooks deprecated** (decisions 3 and 4): Home Assistant Recovery, Plex VM Restart / Recovery, Claude AI Workflow Setup.
- **kb-export** ([65bc103](https://github.com/aaronspriggs/spriggs-homelab/commit/65bc103)): staleness lints skip `[DEPRECATED]` runbooks and Deprecated systems, matching the KB Standards formulas. Deployed, `make check` clean.

## Verify

Export fab8047: [HEALTH.md](http://health.md/) has no property-gap sections left; untested runbooks 18 → 15, unverified systems 17 → 12.

## Roll back

Pre-change page content is in export 9fdc959 (branch `kb-export`).
