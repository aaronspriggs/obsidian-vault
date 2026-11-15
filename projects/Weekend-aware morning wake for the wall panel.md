---
type: idea
status: done
system:
- '[[Raspberry Pi Wall Panel]]'
- '[[Home Assistant (integrations and automations)]]'
completed: 2026-11-15
notion_id: 3e97ae76-22ba-818a-a6f9-eb5d3609c87c
---

## Outcome

Done 2026-11-15 at the quarterly triage (Tier 2, Aaron's yes; [change](<../changes/2026-11-15 Ran the first quarterly KB triage.md>)). `automation.wall_panel_morning_wake` still triggers at 07:00 and now has a native time condition for Monday to Friday, so the panel stays dark on weekend mornings until someone touches it.

## Decisions

- **2026-11-15: a time condition with weekdays, not the Workday sensor this idea first named.** Aaron's ask was "weekdays only", which a native condition does with no new integration. Cost accepted: a public holiday that falls on a weekday still wakes the panel. If that matters later, the Workday integration replaces the condition.

## Links

![[Changes.base#For this project]]
