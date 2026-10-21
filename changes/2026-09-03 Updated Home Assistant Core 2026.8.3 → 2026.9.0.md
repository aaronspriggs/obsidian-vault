---
date: 2026-09-03
type: upgrade
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d07ae76-22ba-81cc-a521-caa2f9ded48f
---

# Updated Home Assistant Core 2026.8.3 → 2026.9.0

Updated via Settings → System → Updates (standard path, automatic pre-update backup taken). Prompted while troubleshooting ha-mcp OAuth failures on a lead suggesting a minimum-version requirement for OAuth cross-origin metadata - that lead turned out to be a red herring (the actual cause was a Claude Code client-side bug, not an HA version gap, see the ha-mcp install Change entry). Update itself was uneventful; HA is now on a current, supported release regardless.
