---
date: 2026-09-29
type: doc
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Raspberry Pi Wall Panel]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
notion_id: 3ea7ae76-22ba-8144-a57b-def84c04b3b1
---

# KB governance phase 4 (part 2a): HA OS rewrite, Home Health split, dashboard runbook

HA OS page rewritten as current state from live ha-mcp data (3,500 -> ~1,100 words). New Systems page Home Health; new reference runbook for dashboard conventions; wall-panel HA config moved to the Wall Panel page. Systems Category gained 'Software'.

## What

- [Home Assistant OS (VM)](<../systems/Home Assistant OS (VM).md>)**:** rewritten to the Systems skeleton from live ha-mcp data (Core 2026.9.4, HAOS 18.3, 5 add-ons, 71 integrations incl. 3 retrying, 18 automations). Dropped the six dated Home Health layers, Future Plans and Known Gaps (all tracked as Projects). `Last Verified` 2026-09-29. Open work view added.
- **New Systems page **[Home Health (HA dashboard + alerts)](<../systems/Home Health (HA dashboard + alerts).md>) (Category Software, Runs On HA): current status-board layout, labels, template helpers, automations, Battery Notes, decisions. The 5 related Projects now also link to it.
- **New runbook **[HA dashboard conventions and gotchas (reference)](<../runbooks/HA dashboard conventions and gotchas (reference).md>)**.**
- [Raspberry Pi Wall Panel](<../systems/Raspberry Pi Wall Panel.md>)**:** gained the HA-side config (dashboard, kiosk user, timers, 5 automations verified live) and PoE/port detail; Known Gaps replaced by an Open work view. `Last Verified` left empty because the Pi itself couldn't be checked (no SSH from the ClaudeCode VM).
- **Schema:** Systems `Category` gained the option `Software` (existing options kept).

## Roll back

Pre-change HA page: export 0709181 (branch `kb-export`), also saved in the session scratchpad.
