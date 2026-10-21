---
date: 2026-09-29
type: doc
system:
- '[[Uptime Kuma]]'
- '[[spriggs-homelab repo]]'
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
notion_id: 3ea7ae76-22ba-81be-9115-ee60b85a730f
---

# KB governance phase 4 (part 2b): homepage rewrite, Uptime Kuma + repo Systems pages, SSH access corrected

Homepage text rewritten (3 VMs, Kuma, UPS, access table, KB model) with all DB blocks kept; new Systems pages Uptime Kuma and spriggs-homelab repo; corrected docs claiming Claude can SSH to TrueNAS/HA (it can't).

## What

- **Homepage:** targeted text edits only (every database embed and the KB Standards link kept, verified by re-fetch). Current infrastructure overview (3 VMs, Dockhand stacks, Kuma, Home Health, UPS status), DHCP reservations, a "how each system is reached" table for Aaron and Claude, and the KB operating model with a link to KB Standards.
- **New Systems pages:** [Uptime Kuma](<../systems/Uptime Kuma.md>) (17 monitors, all up, read via HA's Kuma integration) and [spriggs-homelab repo](<../systems/spriggs-homelab repo.md>), each with an Open work view. The monitoring projects now link to Kuma.
- **Correction:** the ClaudeCode and HA pages said Claude can SSH to TrueNAS and HA. Checked 2026-09-29: TrueNAS's host key isn't in `known_hosts` (never connected), and the HA Terminal & SSH add-on exposes no port and has no keys (web terminal only). Claude's access is the read-only TrueNAS API and ha-mcp. Pages fixed; nothing was changed on any host.

## Roll back

Homepage pre-change copy: export 0709181, `pages/homelab-kb-home-3087ae76.md`.
