---
type: task
status: deprecated
priority: low
system:
- '[[Home Assistant (integrations and automations)]]'
notion_id: 3f97ae76-22ba-817e-a15d-d50f2910f1bc
superseded_by: '[[Prune homelab alerts monthly from Alert2 fire counts]]'
---

**Dropped 2026-11-15** at the quarterly triage (Aaron's yes; [change](<../changes/2026-11-15 Allowed deprecated on project notes and dropped seven backlog notes.md>)). Same data and same purpose as the monthly alert prune, which now also looks at the ack and snooze taps.

Push rules went live 2026-10-14 (runbook 'Homelab alerting', section Push rules). Around 2026-10-28, look at Alert2 fire counts and ack/snooze taps (logbook 'Homelab Alerts') and demote alerts Aaron always acks or ignores to FYI, lengthen delays, or delete them. Lower priority (Aaron, 2026-10-14). Overlaps with the alerting redesign's planned monthly prune.
