---
date: 2026-09-03
type: install
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
notion_id: 3d07ae76-22ba-81aa-ac8e-c9b5170fecae
---

# Installed ha-mcp (homeassistant-ai/ha-mcp) for AI-driven HA automation/dashboard authoring

Created dedicated 'claude' HA admin user (local-only login) to authenticate the integration as, per the planning session's decision to tie access to a real account rather than a bare secret.

First install attempt picked up the wrong project: added ganhammar/hass-mcp-server as a HACS custom repo (a real, functional, actively-maintained project, 67 GitHub stars) instead of the community-standard homeassistant-ai/ha-mcp (4,604 stars, discussed on the HA Community Forum, supports Claude Desktop/Code/ChatGPT/Cursor/etc.). Caught this before finishing setup by comparing GitHub star counts and forum activity across all similarly-named projects. Also re-confirmed HA's own built-in 'Model Context Protocol Server' integration is still Assist-API-only as of the current release (no automation/dashboard write support), so a community integration is still required.

Removed the ganhammar integration and its HACS custom repo entry. Installed the correct one: added homeassistant-ai/ha-mcp-integration (the HACS-installable mirror of the main 4.6k-star homeassistant-ai/ha-mcp project) as a custom repository, restarted HA, then added the HA-MCP Server integration entry. Skipped the optional HA-MCP File & YAML Tools entry (beta, off by default) since automation/script/scene/dashboard authoring goes through dedicated tools (ha_config_set_automation, ha_config_set_dashboard, etc.) rather than raw YAML file access.

Enabled camera image access and image file access (Aaron's call, not part of the original scope decision but wanted for camera visibility). Attempted 'Home Assistant sign-in (OAuth)' auth mode tied to the claude account, but hit a confirmed open upstream bug in Claude Code itself (anthropics/claude-code#89671 - OAuth status-check corrupts freshly-issued tokens immediately after a successful browser authorization) that currently blocks any OAuth-based HTTP MCP server from authenticating in Claude Code. Worked around by connecting via the integration's direct-access URL ([http://192.168.1.218:9584/private_](http://192.168.1.218:9584/private_)..., secret-path-as-credential, Network access left at 'Local network (default)') instead of the OAuth webhook URL. Added as a local-scoped remote MCP server on the ClaudeCode VM via 'claude mcp add --transport http homeassistant <url>' (must be run from /home/aspriggs/homelab-agent - local scope is tied to cwd). Verified working via a raw MCP initialize handshake (ha-mcp 8.4.1 responded correctly with full capabilities) - confirmed functioning at the protocol level, though live tool calls (create/test an automation) still need to happen in a fresh Claude Code session since tools are discovered at session start, not mid-session.

Along the way: updated Home Assistant Core 2026.8.3 to 2026.9.0 on a lead (HA version gap) that turned out not to be the actual cause of the OAuth failure - see separate Upgrade entry. Full step-by-step captured in the 'Setting Up ha-mcp' runbook, including the repo-selection pitfall, the auth-mode tradeoff, and a UI gotcha where lowercase l and uppercase I render identically in HA's secret-URL font (caused two failed-connection dead-ends from screenshot transcription - always use Copy Link Address instead).

Follow-up: switch from the direct-access secret URL to the OAuth webhook URL once anthropics/claude-code#89671 is fixed; test an actual automation write in a fresh session before trusting it with Zigbee/MQTT-touching automations.
