---
date: 2026-09-03
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d07ae76-22ba-81e2-8ecf-daeb4d4ebc83
---

# Removed Spotify integration (needed reauth, unused)

Spotify integration (entry_id cea05d27b7196579db0af8e9b0d56a05, title "aaronspriggs") had been stuck in setup_retry needing OAuth reauth since 2026-07-20 (config_entry_reauth repair, error severity). Reauth requires an interactive browser login to Spotify — not completable via ha-mcp/API. Aaron confirmed he isn't really using this connection, so rather than reauth, removed the integration entirely via ha_remove_helpers_integrations(target=entry_id, confirm=true). This clears the standing repair issue. Gated tool — Aaron approved via the HA-MCP Tool Security Policies panel before it executed.
