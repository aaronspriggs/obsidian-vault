---
date: 2026-10-16
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/ce41c50
notion_id: 3fb7ae76-22ba-81ed-910a-ff4912133940
---

# claude-fix listener enabled on the ClaudeCode VM; Kuma monitor added

Aaron created 1Password item 'Claude Fix Listener' (ID mntpocp457ja6j7rbrtu4q3nae; password 40 chars = bearer token, webhook_id 32 chars = HA webhook ID). Set ITEM in claude-fix (ce41c50), deployed, enabled claude-fix-listener.service: active, real token passes auth, test post to the HA webhook returned OK (no automation consumes it yet; that's step 3). Added AutoKuma monitor 'Claude fix listener' (HTTP GET [http://192.168.1.156:8765/health](http://192.168.1.156:8765/health), 60 s; stacks/uptime-kuma/monitors/claude-fix-listener.toml, f303bfe), deployed through Dockhand with forceRecreate false (only AutoKuma recreated); Kuma monitor ID 21, up. make check ok.
