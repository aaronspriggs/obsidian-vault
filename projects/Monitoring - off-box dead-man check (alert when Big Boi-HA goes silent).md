---
type: idea
status: backlog
priority: low
system:
- '[[Home Assistant OS (VM)]]'
parent: '[[Homelab health monitoring with Home Assistant alerts (silent when nominal)]]'
next_step: 'Not scheduled. When picked up: compare a free external heartbeat (e.g. Healthchecks.io pinged by HA every few minutes) with the alternatives, and decide how it reaches Aaron when HA is down.'
notion_id: 3f47ae76-22ba-81ff-b6cf-fc6c3cb04f87
---

# Monitoring: off-box dead-man check (alert when Big Boi/HA goes silent)

Kuma, HA and the push path all run on Big Boi, so if it goes down nothing alerts. Declined 2026-09-24; raised again in the alerting redesign and deferred by Aaron 2026-10-09 as a later project.
