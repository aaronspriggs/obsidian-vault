---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Uptime Kuma]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/60d1c84
notion_id: 3fc7ae76-22ba-8101-b09b-f6312a3074bc
---

# Alert pushes: medium wording and a reminder_message default

Follow-up to 7ac2d66: Aaron found the fragment wording too short and picked 'medium' from examples. ha/alert2.yaml titles are '<subject> is <state>', messages one plain sentence, recoveries '✅ <subject> is <state> again.'. Added defaults reminder_message 'Still on after {{ on_time_str }}: {{ get_message() }}' after a Radarr reminder arrived as Alert2's built-in 'Radarr health error: on for 19 min'; that reminder was re-armed by the 00:24Z alert2.reload while the alert was open (now a runbook gotcha). Handler confirmations (ack/snooze, Claude fix tap, container restart) reworded to one sentence each. Applied with ha_config_set_yaml + alert2.reload (no open alerts with reminders, no alert2_error); Snooze template render-tested.
