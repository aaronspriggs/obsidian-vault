---
type: project
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[UniFi (UDM Pro)]]'
next_step: '2026-11-14: Aaron picks up 2× G5 Turret Ultra + 1× G5 Bullet + ~800 ft Cat6 today; Claude helps plan the cable runs and adopts the cameras into Protect once they are powered.'
notion_id: 3e57ae76-22ba-8116-bd2b-c9886cacd1dd
---

**Activated 2026-11-14:** Aaron bought 2× G5 Turret Ultra, 1× G5 Bullet and ~800 ft of Cat6 from a neighbor for $325 (new: ~$453 before shipping/tax), which removes the cost blocker. Previously deferred for cost; target before the Nest subscription lapses (~2027-09, renewed ~2026-10). Driver: leaving Google/Nest (HA integration unreliable). Blocks the Nest GCP teardown task. Until then, don't spend effort fixing Nest camera issues in HA.

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

## Current Nest hardware (Aaron, 2026-11-14)

Driveway and Backyard are **Nest Cam Outdoor (1st gen, NC2400ES)**, bought as a 2-pack in 2022: 1080p, 130° diagonal FOV, powered by a wall adapter (no Ethernet at either mount, so UniFi replacements need new cable runs). Downstairs is a Nest camera, model not recorded; Front Door is a Nest Doorbell. HA's Nest integration only reports "Camera"/"Doorbell", not the model.

## Hardware bought 2026-11-14

Two **G5 Turret Ultra** (2K 2688×1512, 102.4° H / 54.9° V / 120.6° D, 10/100, ~4 W 802.3af) are the planned replacements for the Driveway and Backyard Nests; they frame slightly tighter than the Nest's 130° D. One **G5 Bullet** (2K, ~84° H, narrower) is for a long, narrow view; placement TBD. The cable is an ATS Cables EZ-Pull box (SKU on label CMP/2286-W…, white, 23AWG UTP "plenum"); ATS lists ATS2286 as copper-clad aluminum, so treat it as CCA until a scrape test says otherwise. CCA is fine for these ~4 W, 100 Mbps cameras up to ~150–250 ft with solid-wire-rated plugs and sealed outdoor ends; don't reuse it for APs, uplinks or high-power PoE.
