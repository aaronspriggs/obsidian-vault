---
date: 2026-09-24
type: doc
system:
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
notion_id: 3e57ae76-22ba-8171-abdd-facbf819b2cc
---

# Made Notion the sole source of truth for the ClaudeCode VM; migrated local-only state into the KB

Aaron asked for Notion to be the only source of truth, so that Cowork/[claude.ai](http://claude.ai/) and the Claude Code VM stay in sync (they don't share memory). I audited every local file Claude Code reads from on the VM.
**Found local-only (never in Notion), now migrated:**
- The 2026-09-05 Home Health dashboard redesign (hero banner, distribution cards, new helpers) → HA System page.
- Dashboard conventions and gotchas: auto-entities + card-mod, mushroom-chip card_mod selectors, and the declined Puppet screenshot sidecar → HA System page.
- The Nest → UniFi Protect camera plan → new Projects entry "Migrate cameras from Nest to UniFi Protect" (Idea, Deferred).
- Notion and the other [claude.ai](http://claude.ai/) connectors being account-level, and no SSH from the VM to the wall panel Pi → ClaudeCode (VM) System page.
**Found stale, now fixed:**
- ClaudeCode (VM) page: Claude Code version updated from 2.1.258 to 2.1.282; removed the stale "add Notion MCP" and "HA MFA disabled" TODOs.
- "Confirm SSH add-on in Home Assistant" was still Active. Verified live that it's Terminal & SSH (`core_ssh` 10.5.0) and marked it Done. Also documented all 5 installed add-ons on the HA System page and removed the "document add-ons" gap.
**Local changes on the VM:**
- Rewrote `CLAUDE.md`. It now makes Notion the only source of truth for reading and writing, limits local memory to Claude Code behavior only, and says to stop rather than guess if Notion is unreachable. Removed the stale "Right now" task pointer and the "Notion MCP known gap" note.
- Moved `current-task.md` and `homelab-cheatsheet.md` to `/home/aspriggs/homelab-agent/.archive/`. Their content is already in Notion or superseded.
- Pruned Claude Code memory from 10 entries down to 2 behavior-only rules (Notion-first, and ha-mcp approval-notification handling).
Noticed but not acted on: the Spotify Connect add-on is still running even though the Spotify integration was removed on 2026-09-03.
**Follow-up (same day):** the HA System page gave two different Core versions (2025.8.2 in the body, 2026.9.0 in Notes), and both were wrong. Live system health shows HAOS 18.3, Core 2026.9.3, kernel 6.18.52-haos, Supervisor 2026.09.2, HACS 2.0.5 and ha-mcp 8.5.0. Corrected the Software section and the Notes property.
