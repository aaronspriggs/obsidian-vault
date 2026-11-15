---
type: idea
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
- '[[Claude Code (Remote Control service)]]'
parent: '[[Build a Tier 3 guard mod for Claude Code]]'
---

Extracted 2026-10-22 from the done tier3-guard project. Tier 3 covers deleting what Claude *didn't* create in the same session, but the guard holds every delete. It could record the ids Claude creates (`ha_config_set_*` and the like) and let deletes of those through. Worth doing only if approving cleanup of test items gets tedious.

**2026-11-15 (quarterly triage, kept):** do this together with [Narrow tier3-guard's ssh-keygen and authorized_keys rules](<Narrow tier3-guard's ssh-keygen and authorized_keys rules to commands that run or write them.md>) as one guard change, since every guard change is a Tier 3 deploy through Aaron's hands.
