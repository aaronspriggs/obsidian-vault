---
date: 2026-10-06
type: doc
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/ca22240
notion_id: 3f17ae76-22ba-8129-ba21-d2dca701c241
---

# Adopted three-tier change authority for Claude (KB Standards + CLAUDE.md)

What: new section 'Change authority' in KB Standards. Tier 1 = do and log. Tier 2 = say it and then do it; unattended, act then push, but push and wait first if it would interrupt someone using the service. Tier 3 = explicit yes every time. Also added a guardrails paragraph, and the Secrets policy now names the read-only vault 'Homelab - Claude'. [CLAUDE.md](http://claude.md/) now points to the tiers instead of requiring per-change Dockhand approval. Why: Aaron (2026-10-03/06) wants Claude to fix things itself, consulting on destructive changes. His edit: changes to existing HA automations, scripts and scenes are a judgment call by how critical they are, low-impact ones Tier 1 and household-critical ones Tier 2, with the config saved first. Roll back: revert commit ca22240 and remove the KB Standards section.
