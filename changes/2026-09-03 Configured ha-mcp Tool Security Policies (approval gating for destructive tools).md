---
date: 2026-09-03
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
notion_id: 3d07ae76-22ba-8185-9df3-f60ae7ec6699
---

# Configured ha-mcp Tool Security Policies (approval gating for destructive tools)

Went through the HA-MCP sidebar settings panel (Settings app in HA sidebar → HA-MCP, at /ha-mcp) end to end with Aaron to review tool scope. Tools tab was already broad (78/86 enabled) from initial setup; confirmed the 8 remaining disabled tools should stay off: Read/Set YAML Config (raw config file editing — dedicated tools cover automation/script/scene/dashboard authoring instead), Custom Tool (beta sandboxed code execution, no use case yet), and Manage Security Policy (`ha_manage_security_policy`) — deliberately left disabled so the AI can't rewrite its own approval-gating rules; that stays a human-only control.

Enabled Tool Security Policies (previously off entirely — no approval gating existed on any tool). Configuration:
- Master switch: On
- "Let AI agents edit these policies": Off (unchanged — matches the Manage Security Policy tool staying disabled)
- Wait seconds: 599 (near max of 600) — chosen because Aaron typically reaches Claude Code remotely via [claude.ai/mobile](http://claude.ai/mobile) rather than watching the HA-MCP panel live; a short default (60s) would let gated calls time out before he ever saw them
- Approval TTL: 10 minutes

Security-gated the following 12 tools (require approval via the Pending Approvals queue on the Tool Security Policies tab before executing), while leaving all create/edit/read tools (automations, scripts, scenes, dashboards, entities, helpers, backups, history, etc.) ungated for frictionless day-to-day authoring:
ha_restart, ha_remove_device, ha_remove_entity, ha_remove_area_or_floor, ha_remove_zone, ha_config_remove_automation, ha_config_remove_scene, ha_config_remove_script, ha_config_delete_dashboard, ha_remove_helpers_integrations, ha_manage_radio, ha_manage_updates

Restarted HA-MCP (via the integration's Reload) to activate the gating middleware. Verified post-restart that ha_get_overview still returns live data normally. Did not test an actual gated tool call (e.g. ha_restart) to confirm gating fires, since a false negative would mean actually executing the destructive action — verification instead relies on the Tool Security Policies tab's "Gated tools" list showing all 12 entries.

Rationale: this is a belt-and-suspenders layer, not a replacement for asking Aaron directly before destructive actions — Claude already holds itself to that in normal interactive sessions. It matters most as a server-side backstop against a future scenario where a tool call happens without a human actively watching the conversation (e.g. a scheduled/autonomous task).
