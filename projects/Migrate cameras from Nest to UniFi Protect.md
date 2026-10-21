---
type: idea
status: backlog
priority: low
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3e57ae76-22ba-8116-bd2b-c9886cacd1dd
---

Deferred for cost; target before the Nest subscription lapses (~2027-09, renewed ~2026-10). Driver: leaving Google/Nest (HA integration unreliable). Blocks the Nest GCP teardown task. Until then, don't spend effort fixing Nest camera issues in HA.

## Why

Aaron plans to replace the Nest cameras with UniFi Protect. The reason is that Nest's Home Assistant integration is unreliable. This isn't about moving further into the UniFi ecosystem. Decided around 2026-09-03. Deferred for cost (Aaron, 2026-10-06). The Nest subscription was renewed around 2026-10 and runs about 11 months, so the target is to finish before it lapses (~2027-09). This migration also unblocks Decommission Nest integration and its Google Cloud / Device Access project.

## Standing rule until then

Don't diagnose or fix Nest camera problems in HA (missing or unavailable camera entities, or HomeKit bridges that depend on them) unless Aaron asks directly. They're known and temporary.

## Known Nest-dependent breakage (deliberately left as-is)

- `camera.kitchen` is broken or missing. Because of that, the HomeKit "Kitchen" bridge fails on every HA startup. Flagged in the 2026-09-03 health check and deliberately not fixed.

## When this happens

- Repoint the HomeKit Kitchen bridge, and any other config that depends on Nest cameras, at the new UniFi Protect camera entities.
- Related: "Scrypted — UniFi Camera HomeKit Bridge" (Projects) covers bridging UniFi Protect cameras into HomeKit.
*Moved into Notion 2026-09-24. Before this it only existed in the ClaudeCode VM's local Claude Code memory.*

## Note 2026-09-26

HA auto-discovered **UniFi Protect** on the Dream Machine Pro (Settings → Integrations → Discovered). ~~Leave it un-added until this migration.~~ **Superseded 2026-10-17 (Aaron):** UniFi Protect is being added to HA now (API key only mode) as part of the Scrypted project, for the existing G6 Instant. This migration is still Deferred; only the HA integration moved earlier.
