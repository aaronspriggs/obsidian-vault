---
date: 2026-10-30
type: upgrade
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
---

# Upgraded ha-mcp to 9.0.0

Aaron updated the HA-MCP Custom Component through HACS from v2.2.2 (server 8.7.0) to v9.0.0 and restarted HA; both entries came back loaded with their settings unchanged.

## What changed

The HACS mirror `homeassistant-ai/ha-mcp-integration` now reports v9.0.0 installed. From 9.0.0 the component pins the exact server build, so the two share one version and update together through HACS ([#2740](https://github.com/homeassistant-ai/ha-mcp/pull/2740)). `update.ha_mcp_server_update` is gone; only `update.ha_mcp_custom_component_update` remains. Verified after the restart: the HA-MCP Server entry (`01M1KYZAYA6B52JCMR9308KXR4`) and the File & YAML Tools entry are both `loaded`, with `webhook_auth: none`, `bind_host: 0.0.0.0` and `server_port: 9584` unchanged, and Claude Code's tools work over the same direct-access URL. The [Setting Up ha-mcp](<../runbooks/Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>) runbook now covers the 9.0 install defaults and update path.

## Why

9.0.0 was released 2026-10-28 ([release notes](https://github.com/homeassistant-ai/ha-mcp/releases/tag/v9.0.0)). Its breaking changes ([#2740](https://github.com/homeassistant-ai/ha-mcp/pull/2740), [#2741](https://github.com/homeassistant-ai/ha-mcp/pull/2741), [#2742](https://github.com/homeassistant-ai/ha-mcp/pull/2742)) affect new entries and OAuth callbacks, not our existing secret-URL entry. It also brings a fastmcp-slim security bump and new features (an Access switch, a `ha_get_history` summary mode, `ha_restart` safe_mode).

## Notes

Before the update, nothing in automations, scripts, scenes or helpers referenced the removed server update entity. The old `auto_update`/`channel` options remain in the entry's stored options but nothing reads them any more. The new Access switch ([#2821](https://github.com/homeassistant-ai/ha-mcp/pull/2821)) ships disabled, per the PR, and hasn.t been enabled here (no active switch entity for it after the upgrade).
