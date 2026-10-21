---
type: project
status: done
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
completed: 2026-09-03
notion_id: 3ca7ae76-22ba-8183-8a27-e0c1daf0236b
---

# Set up ha-mcp for AI-driven automation/dashboard authoring

Done 2026-09-03: ha-mcp (HACS) gives Claude Code full HA read/write; auth via secret-path URL until the Claude Code OAuth bug is fixed (Blocked follow-up task). Page collapsed 2026-09-29.

## Outcome

Done 2026-09-03. Claude Code on the ClaudeCode VM has full read/write access to Home Assistant through **ha-mcp** ([homeassistant-ai/ha-mcp](https://github.com/homeassistant-ai/ha-mcp), installed via HACS on the HA VM), so it authors automations and dashboards directly instead of Aaron pasting YAML. First live call returned real data (HA 2026.9.0, 830 entities). Setup and troubleshooting: runbook "Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code". It replaced the old task "Point ClaudeCode VM at Home Assistant REST API" (closed).

## Decisions (2026-09-02 to 2026-09-03)

- **ha-mcp, not the official "Model Context Protocol Server" integration:** the official one only exposes the Assist API (control and state), not automation or dashboard writes.
- **In-process on HA via HACS,** not the Docker/PyPI server on the ClaudeCode VM. The ClaudeCode VM is the MCP client (not Claude Desktop on the Mac).
- **Broad scope from day one:** device control, automations/scripts, dashboards, history, backups/updates; Read Only Mode off. Mitigated by HA's daily Google Drive backups and by reviewing generated config before trusting it with Zigbee or MQTT.
- **Auth is the secret-path webhook URL for now,** not OAuth tied to a dedicated `claude` HA user as intended, because Claude Code bug anthropics/claude-code#89671 breaks OAuth for HTTP MCP servers. The integration's auth mode must match the URL type (a mismatch gave an empty tool list), and `claude-remote-control.service` needs a restart to rediscover tools. Switching back is the Blocked task "Switch ha-mcp auth to Home Assistant sign-in (OAuth)".
- An unrelated project (ganhammar/hass-mcp-server) was installed first by mistake and removed; see Changes.

## Links

Pre-collapse plan and risk notes: KB export commit 4ac914e.
