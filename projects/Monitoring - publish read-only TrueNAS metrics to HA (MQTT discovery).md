---
type: idea
status: backlog
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Home Assistant OS (VM)]]'
notion_id: 3e77ae76-22ba-8145-9b17-cb5875e9d87d
---

# Monitoring: publish read-only TrueNAS metrics to HA (MQTT discovery)

Aaron wants TrueNAS monitoring info in HA but declined the full-admin HACS integration (HA runs on TrueNAS; don't make HA an entry point). The read-only alternative: extend truenas-alert-relay to publish metrics as HA entities via MQTT discovery.

Candidate metrics, all readable with the read-only key: pool usage %, health and last scrub; disk temperatures; per-app update available; newest snapshot age per task; uptime. Publish via MQTT discovery using an MQTT-only credential, then add a TrueNAS card to Home Health. See the runbook "TrueNAS read-only API access and alert relay" and the 2026-09-26 integration comparison on the monitoring project page.
