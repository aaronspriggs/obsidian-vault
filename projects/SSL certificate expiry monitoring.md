---
type: idea
status: deprecated
priority: low
system:
- '[[Home Assistant (integrations and automations)]]'
- '[[Uptime Kuma]]'
notion_id: 3e97ae76-22ba-8174-ac2d-e86d590bdc2e
---

**Dropped 2026-11-15** at the quarterly triage (Aaron's yes; [change](<../changes/2026-11-15 Allowed deprecated on project notes and dropped seven backlog notes.md>)). Only two Uptime Kuma monitors are HTTPS: Scrypted already has expiry notification on and the TrueNAS certificate runs to 2035-03-15. When a service gets a real certificate (Dockhand over HTTPS, a reverse proxy), turn expiry notification on for its monitor.

From HA Future Plans (2026-09-28). Likely fits Uptime Kuma's certificate-expiry notification on existing HTTPS monitors rather than anything new.

## Goal

Get warned before any homelab TLS certificate expires (TrueNAS UI cert runs to 2035-03-15; others unknown).
