---
date: 2026-03-05
type: config
system:
- '[[Servarr Stack (Docker Compose)]]'
notion_id: 31a7ae76-22ba-8178-ab92-fcb845d77587
---

# Added gluetun-watchdog container to servarr stack

Added gluetun-watchdog service to servarr compose stack in Dockhand. Alpine-based container with docker-cli installed. Polls Gluetun health status every 30 seconds via 'docker inspect'. If status is not 'healthy', automatically restarts nzbget and prowlarr containers to reattach them to Gluetun's network namespace. Resolves the issue where Gluetun restarts orphaned NZBGet and Prowlarr from its network stack. Also added enable_ipv6: false to servarrnetwork definition to resolve ParseAddr IPv6 error during stack redeployment. Stack torn down and redeployed cleanly to apply changes. All 7 containers confirmed running and healthy.
