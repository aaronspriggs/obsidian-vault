---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
notion_id: 3f97ae76-22ba-81fe-b3f7-ec2be9c985d1
---

# Removed standalone Alert2 UI (merged into Alert2 v1.23)

What (Tier 2, Aaron said yes): HACS remove of Alert2 UI v1.22.1 (redstone99/hass-alert2-ui). Alert2 v1.23 merged the UI into the integration, which now serves /alert2/frontend/alert2.js itself; upstream release notes say to remove Alert2 UI so it doesn't conflict ([https://github.com/redstone99/hass-alert2/releases](https://github.com/redstone99/hass-alert2/releases)). Before this, both /hacsfiles/hass-alert2-ui/alert2.js and /alert2/frontend/alert2.js?v=1.23.2 were registered as dashboard resources, so the custom elements were defined twice. HACS removal also dropped the hacsfiles resource; only the Alert2 v1.23.2 resource remains. No repo change (ha/alert2.yaml never referenced the UI repo). Verify: hard-refresh browser/wall panel, custom:alert2-overview card in the Home Health #homelab-all popup renders. Roll back: reinstall redstone99/hass-alert2-ui from HACS (not recommended).
