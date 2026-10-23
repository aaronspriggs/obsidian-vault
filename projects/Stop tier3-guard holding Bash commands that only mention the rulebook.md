---
type: idea
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
parent: '[[Build a Tier 3 guard mod for Claude Code]]'
---

Extracted 2026-10-23. A Bash heredoc that wrote vault notes was held as a rulebook edit because its text mentioned the rulebook's filename and the command had a `>` redirect: the guard's Bash path check matches the filename anywhere in a command that writes anywhere. Matching only the redirect, `tee`, `cp`/`mv` or `sed -i` target would fix it. Claude worked around it with the Write tool, so it only costs a retry.
