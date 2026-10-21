---
type: task
status: blocked
priority: low
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
notion_id: 3d07ae76-22ba-8167-b38c-d6a751156cda
---

Currently running on ha-mcp's direct-access secret-path URL (Authentication mode = "Secret webhook URL (default)") instead of the originally intended "Home Assistant sign-in (OAuth)" tied to the dedicated `claude` HA user (admin, local-only, already created and otherwise unused). Blocked entirely by an upstream Claude Code bug, anthropics/claude-code#89671, which corrupts OAuth tokens for any HTTP MCP server immediately after a successful browser authorization. Re-checked 2026-09-24 (Claude Code now v2.1.282): still open, unassigned, no linked PR or fix release, no workaround in comments. Once that bug is fixed: switch the ha-mcp integration's Configure screen back to "Home Assistant sign-in (OAuth)", sign in as `claude`, reconnect Claude Code via the webhook URL ([http://192.168.1.218:8123/api/webhook/<id>](http://192.168.1.218:8123/api/webhook/%3Cid%3E)) instead of the direct-access URL, and restart claude-remote-control.service to force fresh tool discovery. See "Setting Up ha-mcp" runbook for full detail.
