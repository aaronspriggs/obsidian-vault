---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[One-tap approval notifications (updates and similar)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/28da594
notion_id: 3f97ae76-22ba-8109-8ad3-c8fda1fa7dbf
---

# One-tap Install button on container image update alerts (Alert2 + 09:00 report + handler)

Container image update alerts now carry an Install button (CONTAINER_UPDATE). Handler automation.homelab_container_update_on_approval runs update.install on the ha-dockhand entity. 09:00 report sends one actionable push per pending update. Gluetun excluded (whole-stack deploy only).

**What changed (Aaron approved scope and safety net):**
- `ha/alert2.yaml` ([28da594](https://github.com/aaronspriggs/spriggs-homelab/commit/28da594)), applied with ha-mcp + `alert2.reload`: the `homelab_container_update` generator adds `action_data.entity_id` and an **Install** action (`CONTAINER_UPDATE`); Gluetun moved to its own button-less `gluetun_update` alert (same entity `alert2.homelab_gluetun_update`) because `dockhand.update=false` means it can only be updated with a whole-stack deploy.
- New `automation.homelab_container_update_on_approval`: triggers on `mobile_app_notification_action` / `CONTAINER_UPDATE`; condition: entity is `update.big_boi_containers_*`, still `on`, and supports Install (supported_features odd). Then pushes "⏳ Updating", logs, `update.install` (continue_on_error), waits up to 5 min for the entity to clear, pushes ✅ or ⚠️ (time-sensitive). Notifications reuse the alert's tag `alert2.homelab_<name>_update`, so they replace each other. Mode queued.
- `automation.homelab_alerts_09_00_report`: appended a repeat that sends one passive push per pending installable container update with the Install button, because Dockhand's 04:00 check fires inside quiet hours (Alert2's own push is suppressed then).
**Safety net:** nightly snapshots, not a pre-update snapshot (Aaron chose this). Servarr config dirs reach `vmstore` via the 23:30 rsync cron and `Big Boi/vmstore` is snapshotted daily (keep 30 d); Kuma/AutoKuma data in `Big Boi/BIGBOI`, also daily (verified via `pool.snapshottask.query`).
**Verified:** template lists 8 installable containers (nzbget, prowlarr, sonarr, radarr, seerr, gluetun-watchdog, uptime-kuma, autokuma; gluetun excluded). Safe tap test pointing at Sonarr (no update pending) ran the handler, which stopped at its condition. A real install is not yet tested; it waits for Dockhand to flag an update.
