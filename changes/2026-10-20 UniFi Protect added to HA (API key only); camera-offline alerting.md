---
date: 2026-10-20
type: install
system:
- '[[Home Assistant OS (VM)]]'
- '[[UniFi (UDM Pro)]]'
project:
- '[[Scrypted — UniFi Camera HomeKit Bridge]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/ad7a6c6
notion_id: 3ff7ae76-22ba-818f-9afd-eee57e89425e
---

# UniFi Protect added to HA (API key only); camera-offline alerting

Aaron added the UniFi Protect integration from HA's discovery card (API-key-only, host 192.168.1.1, key from 1Password `Unifi Protect - HA API Key`) after Claude's own config flow aborted already_in_progress against that discovery flow; Aaron ignored the discovered Scrypted FE0A HomeKit bridge card. The G6 Instant has 38 entities incl. motion/person/vehicle binary sensors and detection events, so a local user isn't needed. Alert2 generator homelab_camera_offline (ha/alert2.yaml): fires after a Protect camera's high-resolution channel is unavailable 5+ min, not while the UDM Pro is down; picked by integration rather than the homelab_watch label so sensor.homelab_issue_count isn't affected. Applied with ha_config_set_yaml (config check ok) + alert2.reload; alert2.homelab_g6_instant_offline is off.
