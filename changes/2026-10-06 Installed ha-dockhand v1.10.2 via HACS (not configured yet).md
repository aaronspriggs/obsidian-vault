---
date: 2026-10-06
type: install
system:
- '[[Home Assistant OS (VM)]]'
- '[[Dockhand]]'
project:
- '[[Monitoring - Dockhand container alerts to HA via ha-dockhand]]'
notion_id: 3f17ae76-22ba-816e-a6e0-f56da8aa8a91
---

# Installed ha-dockhand v1.10.2 via HACS (not configured yet)

What: raetha/ha-dockhand v1.10.2 (HACS default store, id 1176213494), pinned to the reviewed version, then HA restarted (Tier 2; the ha-mcp restart gate was approved by Aaron from a phone push). The integration loaded with only the usual 'custom integration not tested' warning. No config entry yet. Why: the project decision 2026-10-06 to use ha-dockhand for container alerts and one-tap restart. Verify: HACS lists Dockhand as installed, and HA's error log shows only the custom-integration warning for it. Roll back: HACS → Dockhand → Remove, then restart HA.
