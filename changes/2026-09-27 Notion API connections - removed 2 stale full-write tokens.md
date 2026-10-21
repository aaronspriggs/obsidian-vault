---
date: 2026-09-27
type: config
system:
- '[[ClaudeCode (VM)]]'
notion_id: 3e87ae76-22ba-81d3-a486-d70149528987
---

# Notion API connections: removed 2 stale full-write tokens, added read-only kb-export

Deleted the "HomeLab MCP" and "ChatGPT Connector" internal connections (both created Feb 2026, full read/update/insert, unused). Created "kb-export": Read content only, no user info. Its token is on the ClaudeCode VM and in 1Password.

Part of [KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)](<../projects/KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager).md>), phase 0.
**Removed:** "HomeLab MCP" and "ChatGPT Connector". Both were internal Notion connections created 2026-02-05/06 with full read, update and insert access to the whole KB. Neither was still in use: nothing on the ClaudeCode VM referenced their tokens, and Aaron no longer uses ChatGPT. Claude's Notion access is the account-level [claude.ai](http://claude.ai/) connector, which is unrelated to these tokens.
**Added:** internal connection "kb-export" for the weekly KB export and health-check script. Capabilities: Read content only (no update, insert, comments, user info or agents). Content access: "HomeLab KB — Home" plus three orphan top-level pages (Local DNS records explored, Servarr Media Automation Stack, WireGuard VPN configured on UDM Pro), which are being folded into the KB during the audit.
**Token:** `~/.config/kb-export/notion-token` on the ClaudeCode VM (file 600, dir 700), plus a 1Password item.
**Verified 2026-09-27:** authenticates as bot "kb-export"; sees 161 pages and 4 databases; a test PATCH is rejected with 403.
