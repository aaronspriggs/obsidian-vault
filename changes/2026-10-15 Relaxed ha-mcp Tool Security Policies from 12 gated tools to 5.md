---
date: 2026-10-15
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
notion_id: 3fa7ae76-22ba-814d-9656-d44dbd33f577
---

# Relaxed ha-mcp Tool Security Policies from 12 gated tools to 5

Aaron removed the panel gates on restart, device/entity/automation/script/helper-integration removal and updates; still gated: area/floor, zone, scene, dashboard delete, radio.

## What changed

Aaron edited the ha-mcp Tool Security Policies in the HA UI. Still gated (always, single-shot): `ha_remove_area_or_floor`, `ha_remove_zone`, `ha_config_remove_scene`, `ha_config_delete_dashboard`, `ha_manage_radio`. No longer gated: `ha_restart`, `ha_remove_device`, `ha_remove_entity`, `ha_config_remove_automation`, `ha_config_remove_script`, `ha_remove_helpers_integrations`, `ha_manage_updates`. The current list now lives in the [Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code](<../runbooks/Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>), section Tool Security Policies.

## Why

Aaron, 2026-10-15: approving in the HA app for every call was tedious, and the approval push may not be reaching him since the Alert2 migration.

## Notes

The KB Standards tiers are unchanged: deleting HA entities, devices or integrations Claude didn't create stays Tier 3 (explicit yes in chat). The approval push is a direct `notify.mobile_app_aarons_iphone_17_pro` call, not Alert2. A test push sent the same way on 2026-10-15 reached Aaron's phone, so the approval-push path works and isn't affected by the Alert2 migration. Supersedes the gate list in the 2026-09-03 entry "Configured ha-mcp Tool Security Policies".
