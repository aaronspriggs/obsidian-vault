---
date: 2026-10-09
type: doc
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3f47ae76-22ba-8136-b70c-d3b39ad20960
---

# Moved Home Assistant Core restarts to Tier 1 in KB Standards

What: KB Standards → Change authority. HA Core restarts moved from Tier 2 to Tier 1 (do it and log it): run HA's config check first and log the restart with the change that needed it. Rebooting the HAOS VM or its host stays Tier 2. Why: Aaron, 2026-10-09: a restart isn't destructive and he doesn't want to be asked each time; he is also removing the ha-mcp approval requirement on restarts. Roll back: move the line back to Tier 2 on the KB Standards page.
