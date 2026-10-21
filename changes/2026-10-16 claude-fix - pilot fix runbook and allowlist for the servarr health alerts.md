---
date: 2026-10-16
type: config
system:
- '[[ClaudeCode (VM)]]'
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/3d7323c
notion_id: 3fb7ae76-22ba-810d-b7b4-ed2bf86b7aa9
---

# claude-fix: pilot fix runbook and allowlist for the servarr health alerts

Plan 5 step 2. New runbook 'Fix run: servarr health alerts (Sonarr, Radarr, Prowlarr, Gluetun)' ([Fix run - servarr health alerts (Sonarr, Radarr, Prowlarr, Gluetun)](<../runbooks/Fix run - servarr health alerts (Sonarr, Radarr, Prowlarr, Gluetun).md>)) for alerts sonarr_health, radarr_health, prowlarr_health, gluetun_unhealthy. Its commands are the run's allowlist: reads via arr-api/dockhand-api /api/* prefixes and the Gluetun log; writes as exact commands only (restart sonarr/radarr/prowlarr/nzbget, restart or recreate-without-pull the servarr stack, CheckHealth), all Tier 1; never indexer tests or searches. claude-fix allowlist format changed to a **`fixes`** list so one entry covers several alert IDs (3d7323c, README 1a968d4); listener restarted to load it. Two Haiku permission tests ($0.050 and $0.052): exact rules and the `/api/*` wildcard match; the legacy `/api/:*` form never matched (word-boundary rule), fixed; unlisted writes denied. All three arrs healthy at the time, so no real fix run yet (that's step 4).
