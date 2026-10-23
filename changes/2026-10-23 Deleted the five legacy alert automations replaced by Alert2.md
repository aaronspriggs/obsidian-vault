---
date: 2026-10-23
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
---

# Deleted the five legacy alert automations replaced by Alert2

**What changed:** deleted five UI automations (none were in the repo): `automation.homelab_service_device_alerts` (id 1790363256092), `automation.homelab_container_alerts_dockhand` (1791331466068), `automation.homelab_container_restart_on_tap` (1791331478600), `automation.battery_low_notify` (1788547624700) and `automation.battery_watch_stale_unavailable_digest` (1788547635853). The description of `automation.homelab_container_restart_on_approval` now says the tap automation was deleted 2026-10-23 instead of "retiring". Approved by Aaron (Tier 3) in session.

**Why:** the last step of the alerting redesign. All five had been disabled since 2026-10-17 and were replaced by Alert2: service/device and container alerts by [ha/alert2.yaml](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml), the restart tap by `automation.homelab_container_restart_on_approval` (CONTAINER_RESTART), battery-low by `alert2.home_health_*_battery_low`. Last triggers before removal: 10-09, 10-14, never, 09-29, 10-14. A config search found no automation, script, scene or helper calling any of them.

**How:** ha-mcp `ha_manage_backup` (scope edits) saved each config first, then `ha_config_remove_automation`.

**Verify / roll back:** `ha_search(domain_filter='automation')` no longer lists them (30 automations before, 25 after). To restore one: `ha_manage_backup` scope edits, action restore, backup_name `automation.automation.<entity>.20261023_163157.yaml` (`…_163156.yaml` for homelab_service_device_alerts). The full HA backup "Automatic backup 2026.10.2" of 2026-10-23 05:19 (id 910ec00f) also holds them.
