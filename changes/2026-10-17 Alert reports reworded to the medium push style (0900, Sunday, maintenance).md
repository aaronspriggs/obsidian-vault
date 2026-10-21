---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
notion_id: 3fc7ae76-22ba-81e4-b194-d0f994819e45
---

# Alert reports reworded to the medium push style (09:00, Sunday, maintenance)

Applied the 2026-10-17 'medium' wording rule (runbook 'Homelab alerting') to the report automations (UI, not in repo): homelab_alerts_09_00_report title '🌙 Overnight: N alert(s) is/are still open' or '🌙 Overnight alerts have all cleared', 'Fired and cleared:' list, and its per-update Install push now matches the Alert2 update alert ('⬆️ <name> update available' / '<from> → <to>', no 'Tap, then Install' hint); homelab_alerts_weekly_report_sunday_09_00 title '📋 This week: N thing(s) need(s) attention' / 'all clear'; homelab_maintenance_mode on/over titles and messages. Container update / update-all handlers already matched and were left as is. Title templates render-tested with sample data for 0, 1 and several items.
