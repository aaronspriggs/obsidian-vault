---
date: 2026-10-16
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/cad96d1
notion_id: 3fb7ae76-22ba-8115-a1ac-cef41f50d117
---

# First claude-fix test run (Sonnet, sonarr_health): $0.16, 6 turns; budget cap kept at $1.00

Plan 5 step 4. Ran `claude-fix run sonarr_health` on the VM with all three arrs healthy. Result: FIXED: nothing needed, 18 s wall clock, 6 turns, total_cost_usd 0.159, no permission denials; it set the servarr fix-run runbook's Last Tested to 2026-10-16 and the result webhook push went out (automation.homelab_claude_fix_run_result trace 23:05:08Z). Base context is ~30k tokens (first-turn cache write 29.6k), most of the no-op run's cost. Projected 30-turn run ~$0.75, so MAX_BUDGET_USD stays 1.00 as a backstop behind max-turns; the measured basis is now in the code comment (cad96d1). Runs used toward the 3/24h cap: 1.
