---
date: 2026-10-14
type: fix
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Give Claude a scoped TrueNAS maintenance key (apps, VMs, system updates)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/cd0a113
notion_id: 3f97ae76-22ba-81e6-b2f2-e24ac9017690
---

# Renamed TrueNAS read-only API user to claude-readonlyapi; TrueNAS tools no longer print raw errors

Aaron renamed TrueNAS user claude → claude-readonlyapi (clarity next to the planned claude-maint). truenas-api and truenas-alert-relay updated (548b601). A failed login during the switch printed the read-only API key into the session log; both tools now show only the error reason (cd0a113). Same key still works.

**What:** Aaron renamed the TrueNAS read-only API user `claude` → `claude-readonlyapi` (full name "Claude (Read-Only API)") so it reads clearly next to the planned `claude-maint` maintenance user. Updated the hard-coded username in `truenas-api` and `truenas-alert-relay` ([548b601](https://github.com/aaronspriggs/spriggs-homelab/commit/548b601)), deployed, `make check` clean.
**What went wrong:** right after the rename both tools failed to log in (relay runs at ~22:39 and 22:44 UTC). A test login as the new name minutes later also failed ("unexpected authenticator run state"), and TrueNAS's error traceback echoed the read-only API key, which `truenas-api` printed in full into the Claude Code session output. A retry a few minutes later succeeded with the same key, so the key survives a rename; the failures were transient.
**Fix:** both tools now print/log only the error reason, never the raw reply ([cd0a113](https://github.com/aaronspriggs/spriggs-homelab/commit/cd0a113)). Verified: `system.info` OK, relay `--dry-run` OK (1 active TrueNAS alert, nothing new to post), error path shows only "Method does not exist".
**Open:** rotating the read-only key is recommended since it appeared in a session log (read-only, LAN-only, low risk). Aaron's call.
