---
date: 2026-10-07
type: config
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Stop false-positive arr health alerts (Sonarr-Radarr-Prowlarr flapping)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/ccef956
notion_id: 3f27ae76-22ba-81ce-9d7a-c77069444799
---

# Added arr-api for Claude; Sonarr RSS sync 15 → 30 min

What: Aaron added 'Sonarr API Key', 'Radarr API Key' and 'Prowlarr API Key' to the vault Homelab - Claude. Claude added `arr-api` (~/.local/bin): read-only unless --write, DELETE also needs --allow-delete, writes logged, secrets redacted. Then Claude set Sonarr's rssSyncInterval from 15 to 30 min (matching Radarr) via PUT /api/v3/config/indexer/1. Why: NZBgeek (the only indexer, no query/grab limit set in Prowlarr) returned 429 when its API limit was reached, which made the arr health checks flap. Prowlarr stats: 4,317 RSS queries vs 18 grabs. This cuts polling from 6 to 4 requests/hour. Verify: arr-api sonarr /api/v3/config/indexer shows 30. Roll back: PUT the same object with rssSyncInterval 15 (the prior config was saved in the session scratchpad: minimumAge 0, retention 0, maximumSize 0, rssSyncInterval 15).
