---
date: 2026-10-05
type: install
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/5cdd365
notion_id: 3f07ae76-22ba-817f-af1e-ceda5b0589a2
---

# 1Password CLI + read-only service account on ClaudeCode VM; Dockhand and UniFi creds moved to it

2026-10-05: Aaron created the vault 'Homelab - Claude' and the service account `claudecode-vm` (read on that vault only), and placed the token at ~/.config/homelab/op-service-account-token (600) over SSH; it was never in chat. Claude installed 1password-cli 2.40.0 from 1Password's apt repo. Verified: SERVICE_ACCOUNT identity, only that vault visible, and a test `op item create` was refused (read-only). 2026-10-06: Aaron added the items 'Dockhand API token' (field password) and 'Unifi read-only' (username/password). The new `homelab-secret` helper (~/.local/bin) reads one field; dockhand-api and unifi-api now call it at each run. Both were tested live (Dockhand environments, UniFi health) and `make check` is clean. Each dockhand-api run costs 1 read, each unifi-api run 2 (Families limits: 1,000 reads/hr per token, 1,000/day per account). With Aaron's OK, the old files ~/.config/homelab/dockhand-api-token and unifi-readonly were deleted on 2026-10-06 and both wrappers re-tested OK. Older VM zvol snapshots on Big Boi still contain them until they age out. The TrueNAS key, kb-export Notion token and homelab-update conf stay local because of the rate limits.
