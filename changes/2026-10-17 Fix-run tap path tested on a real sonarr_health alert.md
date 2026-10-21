---
date: 2026-10-17
type: doc
system:
- '[[ClaudeCode (VM)]]'
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
notion_id: 3fc7ae76-22ba-81b3-beeb-dd38ede55ebf
---

# Fix-run tap path tested on a real sonarr_health alert; runbook covers download-client backoff

Plan 5 step 4, tap path. Aaron stopped NZBGet (2026-10-16 23:30Z) to cause a real sonarr_health alert and tapped Fix with Claude at 00:05Z. Listener got HA's POST (202), the run restarted NZBGet and reported FIXED (18 turns, $0.47, 95 s, no denials); its own Changes entry is 'Fix run: restarted NZBGet (exited) after sonarr_health alert'. Afterwards Sonarr and Radarr kept 'All download clients are unavailable due to failures' (retry backoff, next retry ~00:28Z), and the run hadn't re-checked Radarr. Runbook 'Fix run: servarr health alerts' step 6 now says to CheckHealth both apps after an NZBGet restart and to treat the backoff message as FIXED that clears on the next retry.
