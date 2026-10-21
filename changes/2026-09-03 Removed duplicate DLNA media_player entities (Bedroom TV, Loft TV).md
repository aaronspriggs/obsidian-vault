---
date: 2026-09-03
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d07ae76-22ba-8174-b45b-d4393cde1bd2
---

# Removed duplicate DLNA media_player entities (Bedroom TV, Loft TV)

media_player.bedroom_tv_2 and media_player.loft_tv_2 (flagged in the 2026-09-03 health check as apparent duplicates) turned out not to be a bad re-pair — they were the same two physical TVs discovered independently by two different integrations: Cast (bedroom_tv/loft_tv, no suffix) and DLNA (the _2 entities, each its own separate ssdp-discovered config entry scoped to just one TV). Both DLNA config entries were in a healthy 'loaded' state, not broken — all four entities happened to read 'unavailable' simultaneously at check time, most likely because both TVs were simply powered off, not because DLNA was faulty.

Aaron confirmed he's never built or planned automations against these entities, so kept it simple: removed both DLNA config entries (9e5c6205fcc68b16d90bae5cb1a5f07b 'Bedroom TV', 857f419c2accd80202c9db93716166d3 'Loft TV') via ha_remove_helpers_integrations, standardizing on the Cast integration for both TVs. Both removals were Aaron-approved through the Tool Security Policies gate before executing.
