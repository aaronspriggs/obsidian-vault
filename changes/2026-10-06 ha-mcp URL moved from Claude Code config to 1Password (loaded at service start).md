---
date: 2026-10-06
type: config
system:
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/b4b398d
notion_id: 3f17ae76-22ba-8104-b7c7-e41f497fd93c
---

# ha-mcp URL moved from Claude Code config to 1Password (loaded at service start)

The ha-mcp direct-access URL (the secret path that gives HA admin) was stored in ~/.claude.json at local scope. Aaron added the 1Password item 'HA-MCP URL' (field password); the handshake test returned ha-mcp 8.6.0. The server is now defined in ~/homelab-agent/.mcp.json as url {HA_MCP_URL}, and `claude mcp remove homeassistant -s local` removed the stored URL (0 matches in ~/.claude.json afterwards). An unattended service can't approve a project MCP server, so .claude/settings.local.json now has enabledMcpjsonServers [homeassistant]; before that, the test showed 'Pending approval'. The new ExecStart launcher ~/.local/bin/claude-remote-control-start exports HA_MCP_URL via homelab-secret and starts Remote Control without the HA tools if 1Password is down. `make check` is clean (19 files). Verified: the service restarted 2026-10-06 00:21 UTC with Aaron's go, and in a fresh session ha_get_state(sun.sun) succeeded, so the URL is now coming only from 1Password. Old copies may remain in VM zvol snapshots and any Claude Code config backups. Rollback over SSH: cd ~/homelab-agent && ~/.local/bin/claude mcp add --transport http homeassistant "(~/.local/bin/homelab-secret 'HA-MCP URL/password')", then restart the service.
