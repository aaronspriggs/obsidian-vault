---
type: task
status: active
priority: low
system:
- '[[Home Assistant (integrations and automations)]]'
next_step: '2026-11-15: (1) done: real Install (10-16) and real Update all incl. NZBGet/Prowlarr NetworkMode check (10-23) both passed. (2) real Snooze re-push, (3) leak buttons and (4) a real Fix with Claude run since the 2026-10-22 switch of the fix runs'' tools from Notion to the vault are still waiting on first real use.'
notion_id: 3f97ae76-22ba-818f-b59b-e4211a9a30dd
---

Follow-up from 'One-tap approval notifications' (Done 2026-10-14). Everything was tested with safe test pushes; these paths still need one real run: (1) a real container image update via Install or Update all: check new image, container healthy, and for NZBGet/Prowlarr that NetworkMode still matches Gluetun's ID (same checks as 'Trial HA Install (Dockhand update entities)', which this also completes); (2) a real Snooze (2hr) re-push after 2 h; (3) the leak alert's buttons on a real critical push, covered by the task 'Run a real end-to-end water leak test'.

(4) Added 2026-11-15 from the [setup review](<Review and tune the Claude Code setup on the ClaudeCode VM.md>): the fix runs (Fix with Claude on the arr health and Gluetun alerts) last ran on 2026-10-17. Their tools were switched from Notion to the vault at the 2026-10-22 cutover and have only been through a dry run since, so the first real tap is the test: check that the run reads its runbook from the vault, stays inside its cap, and writes its change note and commit.
