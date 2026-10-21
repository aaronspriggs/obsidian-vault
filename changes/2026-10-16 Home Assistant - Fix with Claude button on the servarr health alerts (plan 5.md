---
date: 2026-10-16
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/d794d85
notion_id: 3fb7ae76-22ba-815b-a77d-e099e4d5e185
---

# Home Assistant: Fix with Claude button on the servarr health alerts (plan 5 step 3)

Plan 5 step 3. Aaron added secret claude_fix_authorization ("Bearer <token>", 1Password 'Claude Fix Listener') to HA secrets.yaml from the web terminal (HA's SSH app exposes no port). With Aaron's yes (Tier 3), added rest_command to ha-mcp's extra YAML keys (integration 'HA-MCP File & YAML Tools', extra_yaml_keys now alert2 + rest_command). Added rest_command.claude_fix (repo ha/rest-command.yaml): config check ok, HA Core restarted (Tier 1, back in ~35 s); test call with an unlisted ID returned 404 from the listener, so token and source IP are accepted. New automations: automation.homelab_claude_fix_run_on_tap (CLAUDE_FIX tap -> rest_command while the alert is still firing; passive 'Claude is looking' push or a time-sensitive 'couldn't start' push) and automation.homelab_claude_fix_run_result (local-only webhook, ID from 1Password 'Claude Fix Listener'/webhook_id written by script so it never entered the chat; Tier 3 yes from Aaron; direct push, fixed = passive, rest time-sensitive; tested with a selftest post). Alert2 (Tier 2, said in session): arr health generator now pushes Fix with Claude / Ack / Snooze; gluetun_unhealthy pushes Restart servarr stack / Fix with Claude / Ack / Snooze; recovery pushes unchanged. Applied via ha_config_set_yaml (diff limited to those two alerts), alert2.reload, no alert2_error. Previous config = repo commit before d794d85.
