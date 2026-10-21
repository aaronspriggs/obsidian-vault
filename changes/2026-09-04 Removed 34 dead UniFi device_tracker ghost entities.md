---
date: 2026-09-04
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d17ae76-22ba-8134-abe3-ffaf69c7d95a
---

# Removed 34 dead UniFi device_tracker ghost entities

Root cause of the 34/73 unavailable device_tracker entities flagged in the 2026-09-03 health check: Apple's Private Wi-Fi Address feature (MAC randomization) causes iPhones/Watches/iPads to periodically rotate their MAC on a given network. UniFi's client discovery creates a new device_tracker.unifi_default_<mac> entity for each new MAC it sees; the old MAC's entity goes permanently unavailable once the device rotates away from it. Confirmed via full device_tracker listing: the 34 unavailable entities were overwhelmingly generic-named (16x "Watch", 8x "iPhone", 2x "iPad", a few with no resolved name at all, plus several already auto-renamed to iphone_6/iphone_7/mac_3/watch_4/watch_5) — classic MAC-rotation ghosts, not a real network problem.

Verified no automation/script/scene/dashboard referenced any of them before removing. Bulk-removed all 34 via ha_remove_entity (which supports up to 100 entity_ids per call). This tool isn't one of the 12 HA-MCP Tool Security Policies-gated tools, but it IS blocked by Claude Code's own separate local auto-mode safety classifier for destructive actions — required an explicit in-chat 'go ahead' from Aaron rather than an HA panel approval. (Sent a phone notification referencing the HA-MCP panel for this one by mistake since it's a different gate than the one that pushes there — corrected going forward, see agent memory.)

Recommended (not yet done, per-device, Aaron's call): disable "Private Wi-Fi Address" for the home SSID specifically on each Apple device he wants reliably tracked (Settings → Wi-Fi → (i) → Private Wi-Fi Address → off; for Watches, via the paired iPhone's Watch app). Per-network only — does not affect MAC randomization on any other network, no security downside. No MDM/central push option exists for personal (non-managed) Apple devices. This closes out the last item from the 2026-09-03 general HA health check punch list.
