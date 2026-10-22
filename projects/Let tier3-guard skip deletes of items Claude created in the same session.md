---
type: idea
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
parent: '[[Build a Tier 3 guard mod for Claude Code]]'
---

Extracted 2026-10-22 from the done tier3-guard project. Tier 3 covers deleting what Claude *didn't* create in the same session, but the guard holds every delete. It could record the ids Claude creates (`ha_config_set_*` and the like) and let deletes of those through. Worth doing only if approving cleanup of test items gets tedious.
