---
date: 2026-11-23
type: upgrade
system:
- '[[Home Assistant (integrations and automations)]]'
- '[[ClaudeCode (VM)]]'
---

# Upgraded ha-mcp to 9.2.0

Aaron updated the HA-MCP Custom Component from v9.1.2 to v9.2.0 through the Marketplace and restarted HA, during the 30U cutover's maintenance window.

## What changed

`update.ha_mcp_custom_component_update` reports v9.2.0 installed. Checked by Claude after the restart: the HA-MCP Server entry (`01M1KYZAYA6B52JCMR9308KXR4`) and the File & YAML Tools entry are both `loaded`; the server entry still has `webhook_auth: none`, `bind_host: 0.0.0.0` and `server_port: 9584`; Claude Code's tools work over the same direct-access URL with no restart of `claude-remote-control.service`. The startup log shows only the known items (HomeKit "Kitchen" / `camera.kitchen`, the rivian, dyson_local and chargepoint deprecations) plus a one-off linkplay discovery warning for 192.168.1.244.

The first Update attempt failed with "Open the Marketplace and read the warning first": since Core 2026.11 the built-in Marketplace (formerly HACS) needs its custom-code warning accepted before it installs or updates anything, and keeps the acceptance per HA user. Aaron accepted it for his login; ha-mcp's `claude` user still needs its own, which showed when Claude's installs were refused the same way later that day. Recorded in the HA System note and the [ha-mcp runbook](<../runbooks/Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>).

## Why

9.2.0 ([release notes](https://github.com/homeassistant-ai/ha-mcp/releases/tag/v9.2.0), 2026-11-11) is a minor release with no breaking changes. Relevant here: every `ha_mcp_tools` service is now admin-only ([#2997](https://github.com/homeassistant-ai/ha-mcp/pull/2997)), and no automation, script or helper calls one (checked with `ha_search`); `ha_get_history` reads times without an offset as HA local time, America/Denver ([#3059](https://github.com/homeassistant-ai/ha-mcp/pull/3059)); helper flows go through Core's own flow ([#3050](https://github.com/homeassistant-ai/ha-mcp/pull/3050)); search and the overview use the names HA shows ([#3049](https://github.com/homeassistant-ai/ha-mcp/pull/3049)).

## Notes

No backup was taken before this update (STANDARDS Tier 2 asks for one); rollback is Marketplace → HA-MCP Custom Component → Redownload → v9.1.2, then restart HA. Still pending in the Marketplace: ha-dockhand 1.11.3 → 2.1.0 and kiosk-mode 15 → 16 (major versions, to review first), Power Flow Card Plus 0.4.1 → 0.6.1, Mushroom 5.3.0, Meross LAN 6.0.2, Wall Clock Card 3.18.2.
