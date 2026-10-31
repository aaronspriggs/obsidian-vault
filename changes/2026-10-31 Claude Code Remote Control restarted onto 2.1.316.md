---
date: 2026-10-31
type: upgrade
system:
- '[[ClaudeCode (VM)]]'
---

# Claude Code Remote Control restarted onto 2.1.316

The native installer had already auto-updated `~/.local/bin/claude` to 2.1.316, but `claude-remote-control.service` had been running since 2026-10-18 on 2.1.286, because a running process keeps its old binary. At Aaron's request, Claude ran `sudo systemctl restart claude-remote-control`. The service came back active, and its main PID's binary resolves to `versions/2.1.316`. The restart dropped the open Remote Control sessions.

## Why

Claude Code updates on disk by itself, but the long-running Remote Control server only picks up a new version when it restarts.
