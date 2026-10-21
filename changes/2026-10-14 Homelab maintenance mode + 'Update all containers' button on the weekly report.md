---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[One-tap approval notifications (updates and similar)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/4524247
notion_id: 3f97ae76-22ba-8167-bced-e4ee707d888d
---

# Homelab maintenance mode + 'Update all containers' button on the weekly report

Maintenance mode mutes homelab Alert2 pushes, 2 h auto-off, summary when it ends, dashboard toggle. Weekly report gets 'Update all containers (N)'. Both tested.

Aaron approved both on 2026-10-14 (and skipped restart-proof snoozes; the post-rules review is a low-priority task).
**Maintenance mode:** new `input_boolean.homelab_maintenance_mode`, `timer.homelab_maintenance_mode` (2 h, restore on), `automation.homelab_maintenance_mode` (on → start timer + passive push; timer finished → off; off → cancel timer + summary of homelab alerts that started during maintenance and are still open, daytime only). Alert2 defaults `notifier` returns `[]` for domain `homelab` while it's on ([4524247](https://github.com/aaronspriggs/spriggs-homelab/commit/4524247)). Home Health dashboard: wrench toggle badge on the Homelab heading + amber banner while on. Tested: on/off, a `homelab.vm_updated` report during maintenance was muted, and a 10 s timer switched it off on its own.
**Update all:** new `automation.homelab_container_update_all_on_approval` (CONTAINER_UPDATE_ALL): installs every pending installable container update in turn (Gluetun excluded), waits up to 5 min, pushes ✅ or ⚠️ with what's still pending. `automation.homelab_alerts_weekly_report_sunday_09_00` shows the button (with the count) plus Open dashboard only when container updates are pending. Tested with nothing pending: tap reached the handler, stopped at its condition.
