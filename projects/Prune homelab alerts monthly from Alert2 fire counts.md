---
type: task
status: active
priority: low
system:
- '[[Home Health (HA dashboard + alerts)]]'
parent: '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
next_step: '2026-10-23: first prune around 2026-11-15. Read each alert2.homelab_* fire count since 2026-10-14; for anything that fired repeatedly without needing action, lengthen delay_on_secs, lower priority or delete it in ha/alert2.yaml.'
---

Extracted 2026-10-23 from the done alerting redesign. Goal: keep homelab pushes to a handful of non-info alerts per week by pruning noisy ones monthly from Alert2's own fire counts. Alert config lives in [ha/alert2.yaml](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml); the Sunday 09:00 weekly report already shows what fired.
